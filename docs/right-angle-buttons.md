# RESET and MASKROM edge buttons

SW1 (RESET) and SW2 (MASKROM) use HCTL TC-S3601-3.5-260G-F0.6, catalog code C49101620, matching SW3/SW4 in `~/Bitcoin/bitaxe/bitaxeBonanza-1004x`.

The project-local footprint is `bitaxe:SW-SMD_TC-S3601-3.5-260G-F0.6`. Its original embedded STEP model and transform are retained. The pads and locating holes match Bonanza. Local artwork changes shorten silkscreen to clear solder pads, move the actuator outline onto F.Fab, expand the courtyard around the actuator, and identify the part as SMT for assembly.

| Reference | Function | Footprint origin, mm | Rotation | Placement |
|---|---|---|---|---|
| SW1 | RESET | 134.0, 130.6 | 180 degrees | First button to the right of Ethernet |
| SW2 | MASKROM | 145.0, 130.6 | 180 degrees | Right of SW1 |

Both actuators face outward toward increasing Y. The bottom board edge is Y = 134.245 mm. The actuator outline reaches Y = 134.45 mm. The footprint origin is not the body center. No other component was moved. Button PCB connections remain unrouted, as before this placement change.

## Physical pin map

Source: HCTL drawing revision A, page 1, exact part TC-S3601-3.5-260G-F0.6; [manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/70e001fc3cbf586ec6d03ccb392f692f.pdf?productCode=C49101620). The manufacturer land pattern and Bonanza footprint agree. Coordinates below are footprint-local, with the actuator toward negative Y. The two switch contacts are electrically interchangeable; preserve this project's original signal-on-1, ground-on-2 mapping.

| Physical feature | Function | Symbol | Footprint pad | Local X, Y mm | Evidence |
|---|---|---|---|---|---|
| Contact 1 | Normally open contact | Pin 1, passive; RESET_N / Net-(R239-Pad2) | 1 | -2.1, -0.6 | Manufacturer circuit and PCB land pattern, p.1 |
| Contact 2 | Normally open contact | Pin 2, passive; GND | 2 | 2.1, -0.6 | Manufacturer circuit and PCB land pattern, p.1 |
| Right anchor | Mechanical solder attachment | Intentionally absent | 3, no net | 3.742, -2.842 | Outer land in manufacturer PCB pattern; Bonanza pad 3 |
| Left anchor | Mechanical solder attachment | Intentionally absent | 4, no net | -3.742, -2.842 | Outer land in manufacturer PCB pattern; Bonanza pad 4 |
| Left locating peg | Mechanical positioning | Intentionally absent | Unnumbered NPTH | -1.15, -1.9; diameter 0.9 | Manufacturer PCB land pattern, p.1 |
| Right locating peg | Mechanical positioning | Intentionally absent | Unnumbered NPTH | 1.15, -1.9; diameter 0.9 | Manufacturer PCB land pattern, p.1 |

There are two electrical leads, two mechanical solder anchors, and two locating holes. The retained two-pin normally-open schematic glyph is appropriate; the exact hardware is specified by MPN, manufacturer, footprint, catalog and datasheet fields. Mechanical pads 3/4 remain floating, like the reference project.

## Verification

Artifacts: `build/MujinaControl-S19/right-angle-buttons/` from the project root.

- Native KiCad 10.99.0-bp.6 exported netlists: all 192 pin-connectivity partitions unchanged.
- SW1/SW2 retain original footprint UUIDs and schematic paths. Their MPN/catalog fields agree between schematic and PCB.
- 255 total footprints; every other footprint's complete IPC snapshot is unchanged. Existing tracks and vias are identical to the pre-edit snapshot.
- No new clearance, courtyard overlap, hole clearance, copper-to-edge, silkscreen or other geometric DRC findings. Both buttons face the edge in the native 3D render.
- DRC: 82 pre-existing findings plus two footprint-library comparison warnings; 256 unconnected items before and after. These warnings have not been excluded or suppressed.
- The library comparison warnings concern the switch footprints. Native IPC normalizes their custom anchor polygons from nine stored vertices (including a repeated closing vertex) to eight. Comparing the point lists proves the same closed polygon; the library comparator checks vertex count. The pad geometry, spacing, holes and connection map were checked independently. The repeated closing vertex remains in the source library, so the parity warnings remain visible.
- ERC: unchanged two `isolated_pin_label` warnings. No new electrical findings.
- Shared readability checker: zero errors, 71 retained cross-group-wire advisories. All ten saved sheets were visually inspected, with full-page and enlarged review of RESET and MASKROM. No symbol positions or wire geometry were changed.
- Canonical board/root schematic/edited sheets were shown in Backplane. Their saved hashes match the current Backplane history checkpoint. Board hash: `cc62c91c78306b7eb48e3c6ea74f33fd4a432dbc`.

This is a placement milestone, not completed board routing or manufacturing sign-off.
