#!/usr/bin/env bash
# Compile the vendor HC32F4A0 low-level clock driver as a Cortex-M4 object.
# No linking, flashing, or modification of vendor source.
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 /path/to/hc32-f4-series/hc32f4a0" >&2
    exit 2
fi

VENDOR="$(realpath "$1")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$SCRIPT_DIR/../build/hc32-clock"
mkdir -p "$OUT"

for f in "$VENDOR/inc/hc32_ll_clk.h" "$VENDOR/src/hc32_ll_clk.c"; do
    if [[ ! -f "$f" ]]; then echo "Missing $f" >&2; exit 1; fi
done

# Find the vendor's own device and configuration headers; don't assume their location.
echo "Vendor headers potentially needed:"
find "$VENDOR" -type f \( -name hc32f4xx.h -o -name hc32f4xx_conf.h -o -name hc32f4a0.h \) -print

echo "Compiling hc32_ll_clk.c (no link)..."
arm-none-eabi-gcc -c -std=gnu11 -mcpu=cortex-m4 -mthumb -Os \
    -ffunction-sections -fdata-sections \
    -I"$VENDOR/inc" \
    -o "$OUT/hc32_ll_clk.o" \
    "$VENDOR/src/hc32_ll_clk.c"

echo "SUCCESS: $OUT/hc32_ll_clk.o"
