# SD-card routing

Canonical board: `boards/MujinaControl-S19/MujinaControl-S19.kicad_pcb`.

CLK through the existing 22-ohm R235, CMD, D0–D3, card detect, pull-ups, socket supply, decouplers and socket grounds/shields are routed. Native connectivity confirms all intended SD connections, including supply continuity to the regulator-output via at (122.5, 75.3).

## Length-tuning cleanup

The four F.Cu tuning crossovers in the open SD corridor were replaced with nested B.Cu length-compensation sections. Entries, exits and outer corners use 45-degree bends. The four sections stay on the original bottom layer, with no tuning vias or top-layer crossovers.

Removed eight signal vias and seven ground stitches installed specifically for those transitions. Existing stitching at the remaining transitions is retained. There are now 281 vias, all 0.45 mm diameter / 0.30 mm drill. The new tuning copper has at least 0.44 mm edge spacing from other SD signals, exceeding the 0.32 mm (2W) requirement for 0.16 mm tracks.

All 255 footprint instances, every schematic sheet, the project and rules files, and all 1,661 retained track/via objects are unchanged from the start of this cleanup. The earlier SD-routing milestone had moved R235 to (107.00, 99.40), 0 degrees; this cleanup did not move it or any other part.

## Routing and length

Main signals use 0.16 mm F.Cu/B.Cu tracks referenced to In1.Cu/In4.Cu ground. The existing coated-microstrip calculation gives 49.524 ohms for the saved stackup and nominal process assumptions. Short SoC pad necks are 0.127 mm. D0/D1 retain their necessary top-layer crossings near the flash/USB escape. Short pull-up branches and the D1 pull-up via stub are unchanged.

Lengths follow the shortest connected path between native pad centers. Totals add 1.6 mm per F/B transition and, for CLK, 1.02 mm across R235's pad centers. The pre-resistor clock route is included. These are geometric estimates, not extracted electrical delays; package-internal paths and propagation differences are not included.

| Signal | Planar copper, mm | F/B transitions | Estimated total, mm |
|---|---:|---:|---:|
| D0 | 67.581 | 4 | 73.981 |
| D1 | 70.105 | 4 | 76.505 |
| D2 | 71.800 | 2 | 75.000 |
| D3 | 71.800 | 2 | 75.000 |
| CMD | 71.800 | 2 | 75.000 |
| CLK | 67.580 | 4 | 75.000 |

Maximum data/command mismatch to CLK is **1.505 mm**, below the 120 mil (3.048 mm) limit in the local `research/rv1106/reference-designs/Raven1106/docs/rv1106/RV1106 Design Guide.pdf`, pages 46–47. Overall bus spread is 2.525 mm. The longest board path leaves approximately 25 mm for package routing under the guide's 4-inch package-plus-board limit. Package allowance and actual timing remain final-system validation items.

The card supply retains 0.6 mm internal-layer trunks, its short In3.Cu crossing of existing control routing, and local 0.3–0.5 mm branches.

## Reference planes and rules

The existing `SD reference planes` zone on In1.Cu/In4.Cu, priority 10, uses 0.20 mm clearance and 0.127 mm minimum copper thickness under the SD corridor. Both planes are filled. Native ground connectivity passes. Geometric projection finds no signal-centerline reference gaps outside 0.65 mm disks around remaining vias; this is not an electromagnetic simulation.

The existing `SD_50ohm` netclass and all design rules are unchanged. The local F.Cu RV1106 via-hole-to-track clearance remains 0.20 mm within U100's courtyard; the general rule is 0.25 mm elsewhere.

## Verification of the cleanup

- Native connectivity: all SD signals, pull-ups, supply, decouplers and six socket ground/shield pads connected. No SD airwires.
- Native DRC: **84 findings before and after; zero new findings** by type and item IDs. The two switch-library comparison warnings introduced by the earlier button change remain part of this baseline; see `right-angle-buttons.md`.
- Overall unconnected count unchanged at 256. Other routing and existing DRC findings remain unfinished.
- No footprint moved or changed; all schematic/project/rule files match the pre-cleanup backup byte for byte.
- Board dimensions remain 110 × 100 mm; minimum plated drill remains 0.30 mm.
- Full board and enlarged corridor inspected from a fresh native copper export. The corrected corridor has regular spacing and no layer-change holes.
- Canonical viewer shows the saved board. Saved board blob and current Backplane history match: `97b1c5d521bd292032bf413878f26cca114eac54`.

Cleanup evidence: `build/MujinaControl-S19/sd-cleanup/` contains before/final DRC, native length measurements, scope/connectivity/plane audits, plan/applied item IDs, renders and history verification. Its `backup.txt` identifies the preserved pre-cleanup backup. Original SD milestone evidence remains in `build/MujinaControl-S19/routing-sd/`.

This remains a routing milestone, not a fabrication release.
