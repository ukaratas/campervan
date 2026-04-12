#!/usr/bin/env bash
# Montserrat (OFL) + lv_font_conv: Türkçe için Latin-1 + Latin Extended-A
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FONT_URL="https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
FONT="${ROOT}/fonts/Montserrat-Variable.ttf"
mkdir -p "${ROOT}/fonts" "${ROOT}/src/ui/fonts"
curl -fsSL -o "$FONT" "$FONT_URL"
RANGE="0x20-0x7F,0x00A0-0x017F,0x2022"
OPTS=(--font "$FONT" --bpp 4 --format lvgl --no-compress --force-fast-kern-format -r "$RANGE")
npx --yes lv_font_conv "${OPTS[@]}" --size 12 -o "${ROOT}/src/ui/fonts/lv_font_tr_12.c" --lv-font-name lv_font_tr_12
npx --yes lv_font_conv "${OPTS[@]}" --size 14 -o "${ROOT}/src/ui/fonts/lv_font_tr_14.c" --lv-font-name lv_font_tr_14
echo "OK: lv_font_tr_12.c / lv_font_tr_14.c"
