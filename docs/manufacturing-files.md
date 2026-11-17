# Manufacturing files

2026-11-15. `tools/export_fab.sh` writes everything the fab needs for a six-layer assembled order into `mfg/MujinaControl-S19/` at the workspace root (outside this repository). The folder is generated: re-run the script instead of editing files in it.

## What the script does

1. **ERC and DRC with schematic parity.** Any warning or error stops the export.
2. **Gerbers** for the six copper layers, paste, silkscreen, solder mask and outline: Protel file extensions, no X2 attributes, 4.6 mm format, solder mask subtracted from silkscreen.
3. **Drill files**: Excellon, millimetres, plated and non-plated holes in separate files.
4. **Parts list** `assembly/MujinaControl-S19-bom.csv`: Comment, Designator, Footprint, fab part number, MPN, quantity, one line per fab part number. Parts marked not fitted and board features (test points, mounting pads, fiducials) are left out. The part-number column is headed `JLCPCB Part #`, the name in the fab's own template: with the earlier heading `LCSC Part #` the fab's matching sheet of 2026-11-16 showed that column as not read (it still matched all 70 lines to the intended parts by itself). The export stops if a part has no fab part number or no MPN.
5. **Placement file** `assembly/MujinaControl-S19-cpl.csv`: Designator, Mid X, Mid Y, Layer, Rotation. Every part in the parts list must have a placement and the other way round.
6. A zip of the Gerbers and drill files, and a `README.md` with what the order has to say.

The project has no saved parts-list preset for the fab; the script names the columns itself.

## Placement angles and origins

KiCad's placement export gives each footprint's own anchor and angle. The fab places parts from its own library footprints, which often have another zero angle (SOT-23 is turned 180°, for example) or another origin (a through-hole connector's centre instead of pin 1).

`tools/fab_placement.csv` holds the correction per fab part number: the angle between our footprint and the fab's, and where the fab footprint's origin lies in ours. `tools/fab_placement_fit.py` computes it by overlaying pad positions; the fab footprint pads in that script were read from the fab's catalog on 2026-11-15. The export applies the table.

- 28 part numbers were compared: every part that is polarised or has more than two pads. Two-pad resistors, ceramic capacitors, inductors, ferrite beads, the bidirectional ESD diodes and the 32.768 kHz crystal are symmetric and are exported as KiCad has them.
- 37 placements changed. Turned 180°: the SOT-23 parts (D2, D230–D233, Q2–Q5), the regulators U110–U115, the supervisors U120–U124, the load switches U150–U152, the electrolytic capacitors C289 / C290 and the Ethernet jack. Turned 270°: J16 and the antenna connector J19. Origin moved to the fab footprint's centre: J100, J16, J19 (with their turn) and J2, J101, Q1, SW1 / SW2 (no turn); J3–J5 and U160 moved by 0.01 mm or less.
- Electrolytic capacitors: the fab footprint's pad 1 is the negative pad, ours is the positive one; the 180° comes from that.
- J10: the fab footprint numbers its pads in another order than ours (same hole grid, same pin-1 corner), so its entry is set by hand.
- Since 2026-11-15 all eight fan connectors (J6–J9, J11–J14) are not fitted by the fab and so are in neither file; their two rows stay in the corrections table unused. If J11 / J12 are ever fitted by the fab again, check their latch side in the preview: the pad comparison cannot tell it.
- Two fab footprints double as an independent check of footprints drawn here from datasheets: the fab's AP6212 and HR915340A footprints agree with ours pad for pad.

Re-run `tools/fab_placement_fit.py --write` after changing a footprint or a part number; add the fab footprint's reference pads to its table for a new polarised part.

## Paste openings on through-hole pads

The connector footprints taken over from bitcrane (J1, J6–J9, J11–J14) had solder-paste openings on their through-hole pads, on both sides: 38 pads. Paste printed over those holes would have been reflowed into them, including the holes of the connectors that are not fitted. The paste layers were removed from those pads on the board and in `lib/bitcrane.pretty`. Copper, mask and drills are unchanged; the bottom paste layer is now empty.

## Checks made on the output

- ERC 0, DRC 0 violations / 0 unconnected / 0 parity issues at export time (reports in `mfg/.../reports/`).
- All 15 Gerber and drill files parse without warnings in KiCad's Gerber reader in strict mode, and all 13 Gerbers render in an independent viewer (pygerber). The renders were looked at layer by layer: planes, power islands, the keep-out under the Ethernet jack, the exposed edge strips in copper and mask, outline with both notches.
- Drill count: 989 plated holes = 852 vias + 137 pad holes (4 of them slots); 10 non-plated holes. Matches the board.
- Parts list: 68 lines, 295 parts, all on the top side (70 lines and 299 parts before the fan connectors were taken out).

## What the files do not carry

The order form has to say these; they are also in the generated `README.md`: controlled-impedance build-up JLC06161H-3313, epoxy-filled and copper-capped vias in pads, ENIG, 1.6 mm, standard assembly on the top side, 5 pieces.
