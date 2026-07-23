"""Immutable static-site builds with an atomic current symlink."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import posixpath
import re
import shutil
import sqlite3
import stat
import sys
from ctypes import CDLL, c_char_p, c_int, get_errno
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from application.project_knowledge.site_service import RenderedSite

_DARWIN_CLONEFILE = None
if sys.platform == "darwin":
    _darwin_libc = CDLL(None, use_errno=True)
    _DARWIN_CLONEFILE = _darwin_libc.clonefile
    _DARWIN_CLONEFILE.argtypes = (c_char_p, c_char_p, c_int)
    _DARWIN_CLONEFILE.restype = c_int


@dataclass(frozen=True, slots=True)
class SitePublicationReceipt:
    schema_id: str
    site_id: str
    site_fingerprint: str
    cache_hit: bool
    current_index: str
    rendered_pages: int
    reused_pages: int


class AtomicSitePublisher:
    def __init__(self, site_root: Path, *, database_path: Path | None = None) -> None:
        self._root = site_root
        self._builds = site_root / "builds"
        self._current = site_root / "current"
        self._database_path = database_path

    def publish(
        self,
        rendered: RenderedSite,
        *,
        profile: str,
        built_at: str,
        fail_at: str | None = None,
    ) -> SitePublicationReceipt:
        if profile not in {"local-owner", "shared-restricted"}:
            raise ValueError("unsupported site profile")
        directory_mode, file_mode = (0o700, 0o600) if profile == "local-owner" else (0o750, 0o640)
        self._root.mkdir(parents=True, exist_ok=True, mode=directory_mode)
        self._builds.mkdir(parents=True, exist_ok=True, mode=directory_mode)
        os.chmod(self._root, directory_mode)
        os.chmod(self._builds, directory_mode)
        previous_build, previous_manifest = self._previous()
        if (
            previous_manifest.get("site_fingerprint") == rendered.site_fingerprint
            and previous_manifest.get("input_token") == rendered.input_token
            and previous_manifest.get("profile") == profile
        ):
            if previous_build is None:
                raise RuntimeError("managed site cache manifest has no build")
            self._validate_cached_entry(previous_build, previous_manifest, profile)
            self._record_catalog(previous_build, previous_manifest)
            return SitePublicationReceipt(
                "SitePublicationReceipt/v1",
                str(previous_manifest["site_id"]),
                rendered.site_fingerprint,
                True,
                str(self._current / "index.html"),
                0,
                len(rendered.page_fingerprints),
            )
        if previous_build is not None:
            self._validate_cached_entry(previous_build, previous_manifest, profile)
        self._validate_routes_and_links(
            rendered.pages,
            expected_routes=set(rendered.page_fingerprints),
        )
        build_digest = hashlib.sha256(
            f"{rendered.site_fingerprint}:{rendered.input_token}".encode("utf-8")
        ).hexdigest()
        site_id = f"site-{build_digest[:24]}"
        temporary = self._builds / f"{site_id}.tmp"
        final = self._builds / site_id
        if temporary.exists():
            shutil.rmtree(temporary)
        cloned_tree = previous_build is not None and self._clone_tree(previous_build, temporary)
        if not cloned_tree:
            temporary.mkdir(mode=directory_mode)
        rendered_count = 0
        reused_count = 0
        previous_pages_value = previous_manifest.get("pages", {})
        previous_pages = previous_pages_value if isinstance(previous_pages_value, dict) else {}
        previous_metadata_value = previous_manifest.get("page_metadata", {})
        previous_metadata = (
            previous_metadata_value if isinstance(previous_metadata_value, dict) else {}
        )
        page_metadata: dict[str, list[int]] = {}
        try:
            for route in sorted(rendered.page_fingerprints):
                target = temporary / route
                target.parent.mkdir(parents=True, exist_ok=True, mode=directory_mode)
                fingerprint = rendered.page_fingerprints[route]
                previous = None if previous_build is None else previous_build / route
                if (
                    previous is not None
                    and previous_manifest.get("profile") == profile
                    and previous_pages.get(route) == fingerprint
                ):
                    if not cloned_tree:
                        cloned = self._clone_or_copy(previous, target)
                        if not cloned:
                            os.chmod(target, file_mode)
                    raw_metadata = previous_metadata.get(route)
                    if isinstance(raw_metadata, list) and len(raw_metadata) >= 2:
                        page_metadata[route] = [int(raw_metadata[0]), int(raw_metadata[1])]
                    reused_count += 1
                else:
                    content = rendered.pages.get(route)
                    if content is None:
                        raise RuntimeError(f"renderer omitted changed page content: {route}")
                    target.write_text(content, encoding="utf-8")
                    os.chmod(target, file_mode)
                    rendered_count += 1
            if cloned_tree:
                for removed_route in set(previous_pages) - set(rendered.page_fingerprints):
                    removed_path = temporary / removed_route
                    if removed_path.is_file():
                        removed_path.unlink()
            for route in sorted(rendered.page_fingerprints):
                if route in page_metadata:
                    continue
                metadata = (temporary / route).stat()
                page_metadata[route] = [
                    metadata.st_size,
                    metadata.st_mtime_ns,
                ]
            manifest: dict[str, object] = {
                "schema_id": "ProjectSiteManifest/v1",
                "site_id": site_id,
                "site_fingerprint": rendered.site_fingerprint,
                "profile": profile,
                "input_token": rendered.input_token,
                "generation_id": rendered.generation_id,
                "built_at": built_at,
                "pages": rendered.page_fingerprints,
                "page_inputs": rendered.page_input_fingerprints,
                "page_metadata": page_metadata,
            }
            manifest_path = temporary / "manifest.json"
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
                encoding="utf-8",
            )
            os.chmod(manifest_path, file_mode)
            for directory, _, _ in os.walk(temporary):
                os.chmod(directory, directory_mode)
            self._fsync_file(temporary / "index.html")
            self._fsync_file(manifest_path)
            self._fsync_tree_directories(temporary)
            if fail_at == "after_write":
                raise RuntimeError("injected failure after write")
            if final.exists():
                shutil.rmtree(temporary)
            else:
                temporary.rename(final)
                self._fsync_directory(self._builds)
            self._validate_cached_entry(
                final,
                manifest,
                profile,
                require_current=False,
                verify_all_pages=False,
            )
            if fail_at == "after_rename":
                raise RuntimeError("injected failure after immutable build rename")
            next_link = self._root / "current.next"
            next_link.unlink(missing_ok=True)
            os.symlink(f"builds/{site_id}", next_link)
            if not next_link.resolve().is_relative_to(self._builds.resolve()):
                next_link.unlink(missing_ok=True)
                raise RuntimeError("site pointer resolves outside managed builds")
            if fail_at == "before_pointer_replace":
                next_link.unlink(missing_ok=True)
                raise RuntimeError("injected failure before pointer replace")
            os.replace(next_link, self._current)
            self._fsync_directory(self._root)
            self._validate_cached_entry(final, manifest, profile, verify_all_pages=False)
            self._record_catalog(final, manifest)
        except BaseException:
            if temporary.exists():
                shutil.rmtree(temporary)
            raise
        return SitePublicationReceipt(
            "SitePublicationReceipt/v1",
            site_id,
            rendered.site_fingerprint,
            False,
            str(self._current / "index.html"),
            rendered_count,
            reused_count,
        )

    def render_cache(self, *, profile: str) -> dict[str, object] | None:
        build, manifest = self._previous()
        if build is None:
            return None
        if manifest.get("profile") != profile:
            return None
        raw_pages = manifest.get("pages")
        pages = raw_pages if isinstance(raw_pages, dict) else {}
        raw_page_inputs = manifest.get("page_inputs")
        page_inputs = raw_page_inputs if isinstance(raw_page_inputs, dict) else {}
        return {
            "pages": {str(route): str(value) for route, value in pages.items()},
            "page_inputs": {str(route): str(value) for route, value in page_inputs.items()},
        }

    def lookup(self, *, input_token: str, profile: str) -> SitePublicationReceipt | None:
        build, manifest = self._previous()
        if manifest.get("input_token") != input_token or manifest.get("profile") != profile:
            return None
        if build is None:
            raise RuntimeError("managed site cache manifest has no build")
        self._validate_cached_entry(build, manifest, profile)
        self._record_catalog(build, manifest)
        pages = manifest.get("pages")
        page_count = len(pages) if isinstance(pages, dict) else 0
        return SitePublicationReceipt(
            "SitePublicationReceipt/v1",
            str(manifest["site_id"]),
            str(manifest["site_fingerprint"]),
            True,
            str(self._current / "index.html"),
            0,
            page_count,
        )

    def _previous(self) -> tuple[Path | None, dict[str, object]]:
        if not self._current.exists() and not self._current.is_symlink():
            return None, {}
        if not self._current.is_symlink():
            raise RuntimeError("managed site current pointer is not a symlink")
        resolved = self._current.resolve()
        if not resolved.is_relative_to(self._builds.resolve()):
            raise RuntimeError("managed site current pointer escapes builds root")
        manifest_path = resolved / "manifest.json"
        if not manifest_path.is_file():
            raise RuntimeError("managed site current manifest is missing")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        return resolved, manifest

    def _validate_cached_entry(
        self,
        build: Path,
        manifest: dict[str, object],
        profile: str,
        *,
        require_current: bool = True,
        verify_all_pages: bool = True,
    ) -> None:
        directory_mode, file_mode = (0o700, 0o600) if profile == "local-owner" else (0o750, 0o640)
        if manifest.get("profile") != profile:
            raise RuntimeError("managed site cache profile mismatch")
        if manifest.get("site_id") != build.name:
            raise RuntimeError("managed site cache build identity mismatch")
        builds_root = self._builds.resolve()
        if (
            build.is_symlink()
            or not build.is_dir()
            or not build.resolve().is_relative_to(builds_root)
        ):
            raise RuntimeError("managed site cache build is not a safe directory")
        self._assert_owner_and_mode(build, directory_mode, "build directory")
        self._assert_owner_and_mode(self._root, directory_mode, "site root")
        self._assert_owner_and_mode(self._builds, directory_mode, "builds directory")
        if require_current:
            current_stat = self._current.lstat()
            if not stat.S_ISLNK(current_stat.st_mode) or current_stat.st_uid != os.getuid():
                raise RuntimeError("managed site current pointer has an unsafe owner or type")
            if self._current.resolve() != build.resolve():
                raise RuntimeError("managed site current pointer changed during validation")

        pages = manifest.get("pages")
        expected_sha256 = pages.get("index.html") if isinstance(pages, dict) else None
        if not isinstance(expected_sha256, str):
            raise RuntimeError("managed site cache index fingerprint is missing")
        manifest_path = build / "manifest.json"
        index_path = build / "index.html"
        self._assert_regular_managed_file(manifest_path, build, file_mode, "manifest")
        self._assert_regular_managed_file(index_path, build, file_mode, "index entry")
        actual_sha256 = hashlib.sha256(index_path.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise RuntimeError("managed site cache index content hash mismatch")
        if verify_all_pages:
            if not isinstance(pages, dict):
                raise RuntimeError("managed site cache page manifest is invalid")
            expected_routes = {str(route): str(fingerprint) for route, fingerprint in pages.items()}
            raw_metadata = manifest.get("page_metadata")
            page_metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
            actual_routes: set[str] = set()
            build_text = os.fspath(build)
            for directory, dirnames, filenames in os.walk(build_text):
                for dirname in dirnames:
                    directory_metadata = os.lstat(os.path.join(directory, dirname))
                    if not stat.S_ISDIR(directory_metadata.st_mode):
                        raise RuntimeError("managed site contains a non-directory path segment")
                    if (
                        directory_metadata.st_uid != os.getuid()
                        or stat.S_IMODE(directory_metadata.st_mode) != directory_mode
                    ):
                        raise RuntimeError("managed site directory owner or mode mismatch")
                relative_directory = os.path.relpath(directory, build_text)
                for filename in filenames:
                    if filename == "manifest.json":
                        continue
                    actual_routes.add(
                        filename
                        if relative_directory == "."
                        else f"{relative_directory}/{filename}"
                    )
            if actual_routes != set(expected_routes):
                raise RuntimeError("managed site cache page manifest does not match build files")
            for route, fingerprint in expected_routes.items():
                route_path = PurePosixPath(route)
                if route_path.is_absolute() or ".." in route_path.parts:
                    raise RuntimeError("managed site cache manifest contains an unsafe route")
                page_text = os.path.join(build_text, *route_path.parts)
                metadata = os.lstat(page_text)
                if not stat.S_ISREG(metadata.st_mode):
                    raise RuntimeError("managed site page is not a regular file")
                if metadata.st_uid != os.getuid() or stat.S_IMODE(metadata.st_mode) != file_mode:
                    raise RuntimeError("managed site page owner or mode mismatch")
                expected_metadata = page_metadata.get(route)
                actual_metadata = [metadata.st_size, metadata.st_mtime_ns]
                if isinstance(expected_metadata, list) and len(expected_metadata) == 3:
                    actual_metadata.append(metadata.st_ctime_ns)
                with open(page_text, "rb") as stream:
                    actual_hash = hashlib.file_digest(stream, "sha256").hexdigest()
                if actual_hash != fingerprint:
                    raise RuntimeError(f"managed site cache page content hash mismatch: {route}")
                if expected_metadata != actual_metadata:
                    raise RuntimeError(f"managed site cache page metadata drift: {route}")

    def _record_catalog(self, build: Path, manifest: dict[str, object]) -> None:
        if self._database_path is None:
            return
        pages = manifest.get("pages")
        generation_id = manifest.get("generation_id")
        if not isinstance(pages, dict) or not isinstance(generation_id, str) or not generation_id:
            raise RuntimeError("managed site manifest cannot be registered without generation")
        profile = str(manifest["profile"])
        site_id = str(manifest["site_id"])
        built_at = str(manifest["built_at"])
        raw_page_metadata = manifest.get("page_metadata")
        page_metadata = raw_page_metadata if isinstance(raw_page_metadata, dict) else {}
        authorization_digest = hashlib.sha256(profile.encode("utf-8")).hexdigest()
        manifest_sha256 = hashlib.sha256((build / "manifest.json").read_bytes()).hexdigest()
        connection = sqlite3.connect(self._database_path)
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            current = connection.execute(
                "SELECT generation_id FROM pk_generation WHERE status='current'"
            ).fetchone()
            if current is None or str(current[0]) != generation_id:
                raise RuntimeError("site generation does not match current knowledge generation")
            existing_views = connection.execute(
                "SELECT COUNT(*),MIN(manifest_sha256),MAX(manifest_sha256) "
                "FROM pk_render_view WHERE profile=? AND generation_id=?",
                (profile, generation_id),
            ).fetchone()
            existing_cache = connection.execute(
                "SELECT COUNT(*) FROM pk_cache_entry WHERE cache_kind='site-page' "
                "AND generation_id=?",
                (generation_id,),
            ).fetchone()
            if (
                existing_views is not None
                and int(existing_views[0]) == len(pages)
                and existing_views[1] == manifest_sha256
                and existing_views[2] == manifest_sha256
                and existing_cache is not None
                and int(existing_cache[0]) == len(pages)
            ):
                return
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("DELETE FROM pk_render_view WHERE profile=?", (profile,))
            connection.execute("DELETE FROM pk_cache_entry WHERE cache_kind='site-page'")
            render_rows = []
            cache_rows = []
            for route, raw_fingerprint in sorted(pages.items()):
                fingerprint = str(raw_fingerprint)
                view_kind = str(route).split("/", 1)[0].removesuffix(".html") or "overview"
                view_id = hashlib.sha256(
                    f"{view_kind}:{route}:{profile}:zh-CN:{authorization_digest}".encode("utf-8")
                ).hexdigest()
                render_rows.append(
                    (
                        view_id,
                        view_kind,
                        str(route),
                        profile,
                        "zh-CN",
                        authorization_digest,
                        generation_id,
                        fingerprint,
                        f"current/{route}",
                        fingerprint,
                        "current",
                        built_at,
                        manifest_sha256,
                    )
                )
                raw_metadata = page_metadata.get(route)
                if not isinstance(raw_metadata, list) or not raw_metadata:
                    raise RuntimeError(f"site page metadata is missing: {route}")
                cache_rows.append(
                    (
                        f"site:{site_id}:{route}",
                        "site-page",
                        f"builds/{site_id}/{route}",
                        int(raw_metadata[0]),
                        built_at,
                        generation_id,
                        authorization_digest,
                        fingerprint,
                    )
                )
            connection.executemany(
                """
                INSERT INTO pk_render_view(
                    view_id,view_kind,subject_id,profile,locale,authorization_digest,
                    generation_id,input_fingerprint,output_path,content_sha256,render_status,
                    as_of,manifest_sha256
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                render_rows,
            )
            connection.executemany(
                """
                INSERT INTO pk_cache_entry(
                    cache_key,cache_kind,relative_path,size_bytes,created_at,expires_at,
                    generation_id,authorization_digest,content_sha256,legal_hold
                ) VALUES (?,?,?,?,?,NULL,?,?,?,0)
                """,
                cache_rows,
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _assert_owner_and_mode(path: Path, expected_mode: int, label: str) -> None:
        metadata = path.stat()
        if metadata.st_uid != os.getuid():
            raise RuntimeError(f"managed site {label} owner mismatch")
        actual_mode = stat.S_IMODE(metadata.st_mode)
        if actual_mode != expected_mode:
            raise RuntimeError(
                f"managed site {label} mode mismatch: {oct(actual_mode)} != {oct(expected_mode)}"
            )

    @classmethod
    def _assert_regular_managed_file(
        cls,
        path: Path,
        build: Path,
        expected_mode: int,
        label: str,
    ) -> None:
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode):
            raise RuntimeError(f"managed site {label} is not a regular file")
        if not path.resolve().is_relative_to(build.resolve()):
            raise RuntimeError(f"managed site {label} resolves outside its build")
        cls._assert_owner_and_mode(path, expected_mode, label)

    @staticmethod
    def _clone_or_copy(source: Path, target: Path) -> bool:
        """Reuse bytes without coupling the old and new immutable build inodes."""

        if _DARWIN_CLONEFILE is not None:
            if _DARWIN_CLONEFILE(os.fsencode(source), os.fsencode(target), 0) == 0:
                return True
            clone_error = get_errno()
            if clone_error not in {errno.EXDEV, errno.EINVAL, errno.ENOTSUP}:
                raise OSError(clone_error, os.strerror(clone_error), target)
        shutil.copyfile(source, target)
        return False

    @staticmethod
    def _clone_tree(source: Path, target: Path) -> bool:
        """Clone an immutable build tree in one APFS copy-on-write operation."""

        if _DARWIN_CLONEFILE is None:
            return False
        if _DARWIN_CLONEFILE(os.fsencode(source), os.fsencode(target), 0) == 0:
            return True
        clone_error = get_errno()
        if clone_error not in {errno.EXDEV, errno.EINVAL, errno.ENOTSUP}:
            raise OSError(clone_error, os.strerror(clone_error), target)
        return False

    @staticmethod
    def _fsync_file(path: Path) -> None:
        with path.open("rb") as stream:
            os.fsync(stream.fileno())

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    @classmethod
    def _fsync_tree_directories(cls, root: Path) -> None:
        directories = [Path(directory) for directory, _, _ in os.walk(root)]
        for directory in reversed(directories):
            cls._fsync_directory(directory)

    @staticmethod
    def _validate_routes_and_links(
        pages: dict[str, str],
        *,
        expected_routes: set[str] | None = None,
    ) -> None:
        routes = set(pages) if expected_routes is None else expected_routes
        if not set(pages).issubset(routes):
            raise ValueError("rendered page content contains an undeclared route")
        for route in routes:
            path = PurePosixPath(route)
            if path.is_absolute() or ".." in path.parts or path.as_posix() != route:
                raise ValueError(f"unsafe site route: {route}")
        for route, content in pages.items():
            if not route.endswith(".html"):
                continue
            for href in re.findall(r'href="([^"]+)"', content):
                parsed = urlsplit(href)
                if parsed.scheme in {"http", "https", "mailto"}:
                    continue
                if parsed.scheme or parsed.netloc:
                    raise ValueError(f"unsafe external link from {route} to {href}")
                if not parsed.path:
                    continue
                target = posixpath.normpath(
                    posixpath.join(posixpath.dirname(route), parsed.path)
                )
                if target not in routes:
                    raise ValueError(f"broken internal link from {route} to {href}")
