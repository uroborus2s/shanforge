#!/bin/sh
set -eu

pack=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
sources="$pack/sources"
assets="$pack/assets"
srgb_profile=${SRGB_PROFILE:-/System/Library/ColorSync/Profiles/sRGB Profile.icc}
mkdir -p "$assets"

[ -f "$srgb_profile" ] || {
  echo "sRGB profile not found: $srgb_profile" >&2
  exit 1
}
command -v sips >/dev/null
command -v webpmux >/dev/null

photo() {
  source=$1
  output=$2
  width=$3
  height=$4
  ffmpeg -y -v error -i "$sources/$source" \
    -vf "scale=${width}:${height}:force_original_aspect_ratio=increase,crop=${width}:${height}" \
    -frames:v 1 -q:v 2 -pix_fmt yuvj420p "$assets/$output"
  sips -e "$srgb_profile" "$assets/$output" >/dev/null
}

photo neck-service-master.png home-hero-master.jpg 2400 1600
photo neck-service-master.png service-card-neck.jpg 1200 800
photo service-cleaning-master.png service-card-cleaning.jpg 1200 800
photo service-appliance-master.png service-card-appliance.jpg 1200 800
photo neck-service-master.png service-detail-01.jpg 1800 1350
photo service-environment-master.png service-detail-02.jpg 1800 1350
photo service-hygiene-master.png service-detail-03.jpg 1800 1350
photo provider-li-master.png provider-li.jpg 800 800

ffmpeg -y -v error -i "$sources/surface-mineral-master.png" -filter_complex \
  "[0:v]split=4[a][b][c][d];[b]hflip[bh];[c]vflip[cv];[d]hflip,vflip[dhv];[a][bh]hstack[top];[cv][dhv]hstack[bottom];[top][bottom]vstack,scale=1024:1024[out]" \
  -map "[out]" -frames:v 1 -c:v libwebp -quality 90 -compression_level 6 \
  "$assets/surface-mineral.webp"
profiled_webp=$(mktemp "${TMPDIR:-/tmp}/shanforge-surface.XXXXXX")
trap 'rm -f "$profiled_webp"' EXIT
webpmux -set icc "$srgb_profile" "$assets/surface-mineral.webp" \
  -o "$profiled_webp" >/dev/null
mv "$profiled_webp" "$assets/surface-mineral.webp"
trap - EXIT

expected='
home-hero-master.jpg 2400 1600
service-card-neck.jpg 1200 800
service-card-cleaning.jpg 1200 800
service-card-appliance.jpg 1200 800
service-detail-01.jpg 1800 1350
service-detail-02.jpg 1800 1350
service-detail-03.jpg 1800 1350
provider-li.jpg 800 800
surface-mineral.webp 1024 1024
'

printf '%s\n' "$expected" | while read -r file width height; do
  [ -z "$file" ] && continue
  actual=$(ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height -of csv=s=x:p=0 "$assets/$file")
  [ "$actual" = "${width}x${height}" ] || {
    echo "$file: expected ${width}x${height}, got $actual" >&2
    exit 1
  }
done

echo "asset_build=passed files=9"
