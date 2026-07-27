# T06 移动端高保真资源包验证

- 时间：`2026-07-27T18:31:52+08:00`
- 状态：`passed_ready_for_rereview`
- 失败 / 错误 / 跳过：`0 / 0 / 0`

## 生成与派生

- 内置 imagegen 母图：7。
- 最终资源：9（JPEG 8、WebP 1）。
- `tools/build_assets.sh`：`asset_build=passed files=9`。
- 重建检查：`reproducible_build=passed assets=9 sources=7 tmp_refs=0`。
- `tmp/`：路径不存在。

## Manifest

```text
manifest_check=passed assets=9 tmp_refs=0 hashes=9 approved_sources=passed
```

每项包含路径、用途、尺寸、格式、sRGB 色彩空间、状态、SHA-256、`approved_source`、
Prompt ID、source path/hash 和确定性派生操作。

```text
color_profile_check=passed assets=9 profile=sRGB_IEC61966-2.1
```

Iteration 1 评审后，导出脚本为 8 项 JPEG 和 1 项 WebP 嵌入同一 sRGB
profile，更新全部资源哈希，并删除 `tmp/` 路径。修正后重复构建与复核：

```text
rereview_check=passed assets=9 profile=sRGB_IEC61966-2.1 tmp_path=absent ledger_rows=16 diff_check=passed
```

首次复核 shell 使用了 zsh 特殊变量名 `path`，导致命令查找失败；变量改为
`asset_path` 后同一检查通过。这是验证命令问题，不是资源构建失败。

## 纹理

```text
texture_seam_check=passed left_right_mean=1.006 top_bottom_mean=1.155
```

## 本地预览

- TEST-UI-T06-ASSET-PREVIEW-DESKTOP
  - 静态文件：`preview/preview.html`
  - 启动命令 / 端口 / 关闭：N/A；静态 `file://` 页面。
  - viewport：1440×900。
  - 结果：9 cards、8 img + 1 repeated texture、overflow=false、errors=0。
  - 截图：`evidence/T06-asset-preview-desktop.png`。
- TEST-UI-T06-ASSET-PREVIEW-MOBILE
  - viewport：390×844。
  - 结果：9 cards、8 img + 1 repeated texture、overflow=false、errors=0。
  - 截图：`evidence/T06-asset-preview-mobile.png`。

首次沙盒 Chromium 因 macOS Mach port 权限失败；按规则在授权的沙盒外重跑通过。

## 视觉抽查

- 肩颈、保洁、家电、环境、卫生、头像和纹理均已通过 imagegen 输出检查。
- 桌面和移动整包截图已用 `view_image` 检查。
- 人物、制服、暖光和空间连续；无内嵌文字、商标、品牌或水印。

## 未完成

- 独立资源包复审。
- Penpot 移动端高保真同步。
