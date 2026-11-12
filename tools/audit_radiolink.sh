#!/usr/bin/env bash
# Read-only inventory of a local RadioLink ArduPilot-RL checkout.
# Usage: bash tools/audit_radiolink.sh /path/to/ArduPilot-RL
set -euo pipefail
root="${1:?Pass the path to a RadioLink ArduPilot-RL checkout}"
test -d "$root/.git" || { echo "Not a git checkout: $root" >&2; exit 2; }
cd "$root"
echo '=== Repository and revision ==='
git remote -v
git status --short
git rev-parse HEAD
echo '=== Submodule revisions ==='
git submodule status || true
echo '=== CrossFlight definition ==='
test -f libraries/AP_HAL_ChibiOS/hwdef/Crossflight/hwdef.dat && grep -E '^(MCU |APJ_BOARD_ID |FLASH_|PWM|[A-Z][A-Z][0-9]+ +TIMA_)' libraries/AP_HAL_ChibiOS/hwdef/Crossflight/hwdef.dat || true
echo '=== Static archives ==='
find . -type f \( -name 'libch.a' -o -name 'libHAL_ChibiOS_libs.a' \) -print | while IFS= read -r f; do
  echo "-- $f"
  sha256sum "$f"
  file "$f"
  if command -v arm-none-eabi-nm >/dev/null; then
    echo 'Defined/undefined symbol counts:'
    arm-none-eabi-nm -g --defined-only "$f" 2>/dev/null | grep -Ec ' [A-Z] ' || true
    arm-none-eabi-nm -g --undefined-only "$f" 2>/dev/null | grep -Ec ' U ' || true
  fi
done
echo '=== Host toolchain ==='
for cmd in arm-none-eabi-gcc arm-none-eabi-ld arm-none-eabi-nm python3; do
  if command -v "$cmd" >/dev/null; then "$cmd" --version | head -1; else echo "$cmd: not installed"; fi
done
echo '=== No build or flashing performed ==='
