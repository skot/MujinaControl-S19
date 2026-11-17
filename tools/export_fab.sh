#!/usr/bin/env bash
# Fabrication and assembly outputs for MujinaControl-S19 (six layers, assembled by the fab).
#
#   tools/export_fab.sh [output-dir]      (default: ../../mfg/MujinaControl-S19 from the board folder)
#
# Order of work: ERC and DRC (any finding stops the export), Gerbers, drill files,
# parts list (BOM), placement file (CPL), then cross-checks and a zip of the Gerbers.
# The placement file is corrected with tools/fab_placement.csv: per fab part number, the
# angle between our footprint and the fab library's, and where the fab footprint's origin
# lies in ours (found by comparing pad positions; see docs/manufacturing-files.md).
# Needs KiCad 10.99+ and python3. Set KICAD_CLI to choose a kicad-cli.
# The output folder is generated: do not edit files in it by hand, re-run this script.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
name="MujinaControl-S19"
board="$here/$name.kicad_pcb"
sch="$here/$name.kicad_sch"
out="${1:-$here/../../mfg/$name}"

if [[ -z "${KICAD_CLI:-}" ]]; then
  for c in "$HOME/.backplane-bend/kicad/10.99.0-bp.6/bin/kicad-cli" \
           "$HOME"/.backplane-bend/kicad/*/bin/kicad-cli \
           "$(command -v kicad-cli || true)"; do
    if [[ -x "$c" ]]; then KICAD_CLI="$c"; break; fi
  done
fi
[[ -n "${KICAD_CLI:-}" ]] || { echo "kicad-cli not found; set KICAD_CLI" >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 not found" >&2; exit 1; }
echo "Using $KICAD_CLI ($("$KICAD_CLI" version))"

mkdir -p "$out"
out="$(cd "$out" && pwd)"
# start from an empty output folder so no stale file survives a re-run
find "$out" -mindepth 1 -maxdepth 1 \( -name reports -o -name gerbers -o -name assembly -o -name '*.zip' -o -name 'README.md' \) -exec rm -rf {} +
mkdir -p "$out/reports" "$out/gerbers" "$out/assembly"

# --- 1. checks: any ERC or DRC finding stops here -----------------------------
"$KICAD_CLI" sch erc --output "$out/reports/erc.rpt" --format report --units mm \
  --severity-warning --severity-error --exit-code-violations "$sch"
"$KICAD_CLI" pcb drc --output "$out/reports/drc.rpt" --format report --units mm \
  --severity-warning --severity-error --schematic-parity --exit-code-violations "$board"

# --- 2. Gerbers (Protel extensions, no X2, 4.6 mm) ---------------------------
layers="F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts"
"$KICAD_CLI" pcb export gerbers --output "$out/gerbers/" --layers "$layers" \
  --no-x2 --no-netlist --subtract-soldermask --precision 6 "$board"

# --- 3. drill files (Excellon, mm, plated and non-plated separate) ------------
"$KICAD_CLI" pcb export drill --output "$out/gerbers/" --format excellon \
  --drill-origin absolute --excellon-units mm --excellon-zeros-format decimal \
  --excellon-oval-format alternate --excellon-separate-th "$board"
rm -f "$out/gerbers/"*.gbrjob
# KiCad puts the layers' user names in the file names; no spaces in what goes to the fab
for f in "$out/gerbers/"*; do n="${f##*/}"; [[ "$n" == *" "* ]] && mv "$f" "$out/gerbers/${n// /_}"; done

# --- 4. parts list: Comment, Designator, Footprint, fab part number, MPN ------
# (the project has no saved BOM preset for the fab, so the columns are given here)
# one row per fitted part here; grouped into one line per fab part number in step 6
"$KICAD_CLI" sch export bom --output "$out/assembly/bom_raw.csv" \
  --fields 'Reference,Value,Footprint,LCSC,MPN' \
  --labels 'Reference,Value,Footprint,LCSC,MPN' \
  --sort-field 'Reference' --ref-range-delimiter '' --exclude-dnp "$sch"

# --- 5. placement file: Designator, Mid X, Mid Y, Layer, Rotation -------------
"$KICAD_CLI" pcb export pos --output "$out/assembly/positions_raw.csv" \
  --format csv --units mm --side both --exclude-dnp "$board"

# --- 6. convert, cross-check, summarise ---------------------------------------
python3 - "$out" "$name" "$here/tools/fab_placement.csv" <<'EOF'
import csv, sys, pathlib, re, math
out, name = pathlib.Path(sys.argv[1]), sys.argv[2]
corr = {r["LCSC"]: (float(r["RotationOffset"]), float(r["dX"]), float(r["dY"])) for r in csv.DictReader(open(sys.argv[3], newline="", encoding="utf-8"))}
asm = out / "assembly"
flat = list(csv.DictReader((asm / "bom_raw.csv").open(newline="", encoding="utf-8")))
bad = [r["Reference"] for r in flat if not re.fullmatch(r"C\d+", r["LCSC"].strip()) or not r["MPN"].strip()]
if bad:
    sys.exit(f"error: parts without a fab part number or MPN: {bad}")
bom_refs = [r["Reference"].strip() for r in flat]
assert all("," not in x for x in bom_refs) and len(bom_refs) == len(set(bom_refs)), "unexpected designators in the raw parts list"
def key(ref):
    m = re.fullmatch(r"([A-Za-z]+)(\d+)", ref); return (m.group(1), int(m.group(2))) if m else (ref, 0)
groups = {}
for r in sorted(flat, key=lambda r: key(r["Reference"])):
    groups.setdefault(r["LCSC"].strip(), []).append(r)
bom = []
for lcsc, rs in groups.items():
    for field in ("Footprint", "MPN"):
        assert len({r[field] for r in rs}) == 1, f"{lcsc}: parts with different {field}: {[r['Reference'] for r in rs]}"
    values = list(dict.fromkeys(r["Value"] for r in rs))          # distinct value texts, in order
    bom.append([" / ".join(values), ",".join(r["Reference"] for r in rs), rs[0]["Footprint"].split(":")[-1], lcsc, rs[0]["MPN"], len(rs)])
with (asm / f"{name}-bom.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["Comment", "Designator", "Footprint", "JLCPCB Part #", "MPN", "Qty"]); w.writerows(bom)
(asm / "bom_raw.csv").unlink()
raw = list(csv.DictReader((asm / "positions_raw.csv").open(newline="", encoding="utf-8")))
need = {"Ref", "PosX", "PosY", "Rot", "Side"}
assert raw and need <= set(raw[0]), f"unexpected position header: {list(raw[0]) if raw else None}"
lcsc_of = {r["Reference"].strip(): r["LCSC"].strip() for r in flat}
rows, dropped, corrected = [], [], 0
for r in raw:
    if r["Ref"] not in bom_refs:          # board features without a parts-list line (fiducials)
        dropped.append(r["Ref"]); continue
    side = (r["Side"] or "").strip().lower()
    assert side in ("top", "front"), f'{r["Ref"]}: the corrections assume parts on the top side'
    x, y, a = float(r["PosX"]), float(r["PosY"]), float(r["Rot"])          # y up, angle counter-clockwise
    th, dx, dy = corr.get(lcsc_of[r["Ref"]], (0.0, 0.0, 0.0))
    if (th, dx, dy) != (0.0, 0.0, 0.0):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        x += dx * c + dy * s                # offset given in the footprint's frame (y down), turned with the part
        y -= -dx * s + dy * c
        corrected += 1
    rows.append([r["Ref"], f"{x:.4f}", f"{y:.4f}", "T", f"{(a + th) % 360:.1f}"])
missing = sorted(set(bom_refs) - {r[0] for r in rows})
if missing:
    sys.exit(f"error: parts in the parts list without a placement: {missing}")
with (asm / f"{name}-cpl.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"]); w.writerows(rows)
(asm / "positions_raw.csv").unlink()
sides = {r[3] for r in rows}
print(f"parts list: {len(bom)} lines, {len(bom_refs)} parts; placement: {len(rows)} parts on side(s) {sorted(sides)}, {corrected} with an angle or origin correction; left out of the placement file: {sorted(dropped)}")
EOF

# --- 7. zip the Gerbers and drill files ---------------------------------------
( cd "$out/gerbers" && rm -f "../$name-gerbers.zip" && zip -q -X "../$name-gerbers.zip" ./* )

# --- 8. order notes -----------------------------------------------------------
cat > "$out/README.md" <<EOF
# $name: manufacturing files

Generated by \`tools/export_fab.sh\` on $(date -u +%Y-%m-%d) from the board at git commit $(git -C "$here" rev-parse --short HEAD 2>/dev/null || echo unknown)$(git -C "$here" diff --quiet 2>/dev/null || echo " (with uncommitted changes)"). Do not edit by hand; re-run the script.

| File | What it is |
|---|---|
| \`$name-gerbers.zip\` | Gerbers for 6 copper layers, paste, silkscreen, mask, outline, plus plated and non-plated drill files |
| \`assembly/$name-bom.csv\` | Parts list: Comment, Designator, Footprint, fab part number, MPN, quantity |
| \`assembly/$name-cpl.csv\` | Placement file: Designator, Mid X, Mid Y, Layer, Rotation (mm, degrees) |
| \`reports/erc.rpt\`, \`reports/drc.rpt\` | Check reports the export ran on (both must be clean or the export stops) |

## What the order has to say

- 6 layers, 110 x 100 mm, 1.6 mm, ENIG, 1 oz outer / 0.5 oz inner copper, 5 pieces.
- **Controlled-impedance build-up JLC06161H-3313** (0.0994 mm prepreg between each outer layer and its ground plane).
- **Vias in pads: epoxy filled and copper capped.** About 380 vias sit inside pads. All vias are 0.30 mm hole / 0.45 mm pad.
- **Standard assembly, top side only** (RV1106G2 is not available in economic assembly). Parts not fitted are already left out of both assembly files.
- Exposed, ENIG-finished ground strips run along the left and right edges on both sides; the copper stops 0.3 mm from the edge, so no edge plating is needed.
- The Ethernet jack J100 and USB / power connectors overhang the board outline.

## Check in the fab's placement preview

The placement file is already corrected for the fab's part library: for the 26 polarised or multi-pin part numbers the angle and origin were found by comparing the fab library footprint's pads with ours (\`tools/fab_placement.csv\`). The preview is still the final check. Look at pin 1 / polarity of U100, U160, U130, Q1, the regulators U110-U115, the SOT-23 parts, the diodes and LEDs, and the electrolytic capacitors C289 / C290. The eight fan connectors J6-J9 and J11-J14 are not fitted by the fab.
EOF
echo "Wrote $out"
