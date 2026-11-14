#!/usr/bin/env bash
# Ray-traced 3D render of the board with all parts, transparent background.
#
#   tools/render.sh [output.png]        (default: render.png next to the board)
#
# Needs KiCad 10.99+ (the board format is newer than KiCad 10.0). Set KICAD_CLI
# to choose a kicad-cli; otherwise Backplane's KiCad is used if present, then
# kicad-cli on PATH. If Python with Pillow is available, empty transparent
# margins are trimmed to a small border.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
board="$here/MujinaControl-S19.kicad_pcb"
out="${1:-$here/render.png}"

if [[ -z "${KICAD_CLI:-}" ]]; then
  for c in "$HOME/.backplane-bend/kicad/10.99.0-bp.6/bin/kicad-cli" \
           "$HOME"/.backplane-bend/kicad/*/bin/kicad-cli \
           "$(command -v kicad-cli || true)"; do
    if [[ -x "$c" ]]; then KICAD_CLI="$c"; break; fi
  done
fi
[[ -n "${KICAD_CLI:-}" ]] || { echo "kicad-cli not found; set KICAD_CLI" >&2; exit 1; }
echo "Using $KICAD_CLI ($("$KICAD_CLI" --version))"

# Render with a private, throwaway KiCad config so the result does not depend on
# the 3D viewer settings saved on this machine. It uses KiCad's default
# ray-tracing settings except post-processing, which is turned off: its
# screen-space shadow draws hard-edged grey boxes below parts that overhang the
# board edge (the Ethernet jack) and turns them into half-transparent black on a
# transparent background.
cfg="$(mktemp -d)"
trap 'rm -rf "$cfg"' EXIT
ver="$("$KICAD_CLI" --version | grep -Eo '^[0-9]+\.[0-9]+')"
mkdir -p "$cfg/$ver"
echo '{"render": {"raytrace_post_processing": false}}' > "$cfg/$ver/3d_viewer.json"

# Camera and lights are fixed here so every render looks the same.
KICAD_CONFIG_HOME="$cfg" "$KICAD_CLI" pcb render "$board" -o "$out" \
  --width 2300 --height 2116 \
  --quality user --background transparent \
  --perspective --rotate '-20,0,0' --zoom 0.8 \
  --light-top 0.25 --light-bottom 0.25 --light-side 0.17 \
  --light-camera 0.2 --light-side-elevation 67

# Trim transparent margins (keeps a 24 px border), if Pillow is available.
for py in "${PYTHON:-}" python3 "$here/../../build/MujinaControl-S19/venv/bin/python"; do
  [[ -n "$py" ]] && command -v "$py" >/dev/null 2>&1 || continue
  if "$py" -c 'import PIL' 2>/dev/null; then
    "$py" - "$out" <<'EOF'
import sys
from PIL import Image
p = sys.argv[1]
im = Image.open(p)
x0, y0, x1, y1 = im.getchannel("A").getbbox()
m = 24
box = (max(x0 - m, 0), max(y0 - m, 0), min(x1 + m, im.width), min(y1 + m, im.height))
im = im.crop(box)
im.save(p, optimize=True)
print(f"Trimmed to {im.width}x{im.height}")
EOF
    break
  fi
done
echo "Wrote $out"
