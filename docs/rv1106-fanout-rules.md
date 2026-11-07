# RV1106G2 local fanout rules

Originally saved 2026-11-06; via sizes updated 2026-11-07 for U100 on the canonical MujinaControl-S19 board. The native project rule file is `../MujinaControl-S19.kicad_dru`. The original change defined routing constraints. See [via sizing update](via-sizing.md) for the subsequent board-wide resize and verification.

## Dimensions and scope

| Item | Local setting |
| --- | --- |
| Front-layer escape trace | 0.15 mm preferred, 0.127 mm minimum |
| Front-layer copper clearance | 0.127 mm minimum when both objects intersect U100's courtyard |
| Through-via diameter / drill | 0.45 / 0.30 mm preferred and minimum |
| Differential pair launch gap | 0.20 mm preferred, 0.127 mm minimum |

U100 has 0.35 mm peripheral pin pitch, 0.15 mm-wide by 0.875 mm-long pads and a central ground pad. A 0.15 mm trace matches the pin width; parallel launches at pin pitch have 0.20 mm edge spacing. The former 0.20 mm trace/0.20 mm clearance defaults do not fit adjacent launches at that pitch.

Default routing uses 0.20 mm trace/clearance and 0.45/0.30 mm through-vias. The board-wide minimum via diameter is 0.45 mm, drill 0.30 mm, and annular ring 0.075 mm. All existing through-vias now use this geometry, including power and ground vias. Trace and clearance constraints are unchanged. No microvias or reduced drill sizes are introduced.

KiCad applies an `intersectsCourtyard` condition to the entire matching object. Keep each escape segment short, with a segment boundary at the transition out of the local region. Do not create long segments that intersect U100 and then carry the relaxed local rule across the board. The clearance exception requires **both** objects to intersect the courtyard; clearance to surrounding parts remains 0.20 mm unless another existing rule applies. The width and pair-gap exceptions apply only on F.Cu. The via rule applies to vias intersecting U100's courtyard; vias outside it retain their normal net-class sizes.

## Routing use

- Launch perpendicular to the peripheral pads. Use early bends as needed around nearby decouplers. Stagger through-vias; 0.45 mm via pads cannot occupy one row at 0.35 mm pitch. Observe drill-to-drill clearance as well as copper clearance when arranging staggered rows.
- Use these widths for short individual power-pin neckdowns only. Widen immediately into suitable supply copper or a plane; this is not a bulk-current trace sizing rule.
- The pair launch gap follows the pad geometry, not a controlled-impedance calculation. Keep the launch short and symmetrical. The longer USB and Ethernet routes still require stackup-specific 90-ohm and 100-ohm differential geometry respectively; this change does not qualify their impedance or timing.
- The exposed ground pad's thermal/ground-via pattern and complete signal escapes still need to be designed during routing. A passing initial-escape geometry check does not prove full-board routability.

## Original rule verification (2026-11-06)

For current via-size verification, see [via sizing update](via-sizing.md).

Native KiCad 10.99.0-bp.6 accepted all four custom rules (`CRS_VALID`), returned their saved constraints through the API, and ran DRC successfully with the rule file present.

A read-only geometric test used the native front-layer pad polygons and courtyard, and tested simultaneous straight escape traces from all 128 peripheral pins, conservatively including unused pins. It checked each proposed trace against other-net pads and the other proposed traces with the actual local/global clearance scope:

| Geometry | Result |
| --- | --- |
| Old 0.20 mm traces, 0.24 mm extension beyond pad | 128 pins fail |
| New 0.15 mm traces, 0.24 mm extension beyond pad | All 128 pass; smallest extra clearance margin 0.0075 mm |
| New 0.15 mm traces, 0.30 mm extension beyond pad | 15 pins fail against nearby parts requiring the normal 0.20 mm clearance |

These are short initial escapes, not finished routes or a via-placement test. No traces from this test were written to CAD.

Before/after native DRC findings are identical after normalizing item order: 59 existing violations (40 silk overlaps, 16 silk-to-edge clearances, two J2 hole clearances, one J16 library-footprint mismatch), plus 499 unconnected items on the unrouted board. There are no new DRC findings. The canonical PCB, project settings and all schematic sheets are byte-identical to the pre-change backup; the new rule file is the CAD configuration change.

Evidence: `../../../build/MujinaControl-S19/fanout-rules/` contains `native-readback.json`, `geometric-fanout.json`, `geometric_fanout_check.py`, `before-drc.json`, `after-drc.json`, `verification.json` and the pre-change backup location in `backup.txt`.

## Sources

- [The fab's published PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/), checked 2026-11-06: multilayer 1 oz minimum track/space 0.09/0.09 mm and pad-to-track clearance 0.10 mm. The selected 0.127 mm minimum is above these limits. The selected via diameter/drill also exceeds the published minimum diameter-to-drill difference.
- [KiCad PCB Editor documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html), custom-rule conditions, `intersectsCourtyard`, track-width, clearance, via and pair-gap constraints. Native acceptance was verified on this project's selected KiCad version.
- Existing project [six-layer stackup](pcb-stackup.md) and local Rockchip hardware guide, extracted in `../../../build/MujinaControl-S19/reference/guide.txt`.

## Viewer and history

Backplane confirmed that the displayed board is the canonical saved PCB. Its file hash matches the existing thread history checkpoint. The new `.kicad_dru` file is saved on disk and read back successfully by KiCad, but it was not present in the inspected Backplane checkpoint refs; automatic history capture of the new rules could not be verified. Existing history was not modified. See `history-verification.json` in the evidence directory.
