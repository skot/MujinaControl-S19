# Six-layer PCB setup

The canonical PCB is configured for six copper layers, nominal 1.6 mm FR-4, green mask, ENIG, 1 oz outer and nominal 0.5 oz inner copper. The manufacturing record agrees. The previous board had four copper layers while its manufacturing record still said two; both are now six.

Use the fab's specified **JLC06161H-3313** construction. ENIG replaces the previous lead-free HASL selection because the fab's current six-layer process does not support HASL. References: [published stackups](https://jlcpcb.com/impedance), [current capabilities](https://jlcpcb.com/capabilities/pcb-capabilities), checked 2026-11-01 local time.

## Layer plan

| Layer | KiCad layer | Intended use |
|---|---|---|
| 1 | F.Cu | Components and signals; critical interfaces referenced to L2 |
| 2 | In1.Cu | Continuous ground reference |
| 3 | In2.Cu | Power distribution |
| 4 | In3.Cu | Slow auxiliary signals |
| 5 | In4.Cu | Continuous ground reference |
| 6 | B.Cu | Signals referenced to L5 |

These are saved layer names and intended functions, not completed copper planes. No zones, tracks, vias or placements were added. Keep USB and Ethernet pairs on an outer layer over uninterrupted ground. L4 is closer to the power layer than to L5 in this construction; do not route fast signals across power splits there. Calculate differential geometry using the selected construction before routing; existing generic differential-pair defaults are not impedance-qualified.

## Saved construction

| Element, top to bottom | Thickness mm | Relative permittivity |
|---|---:|---:|
| F.Cu | 0.035 | — |
| 3313 ×1 prepreg | 0.0994 | 4.1 |
| In1.Cu | 0.0152 | — |
| Core | 0.55 | 4.6 |
| In2.Cu | 0.0152 | — |
| 2116 ×1 prepreg | 0.1088 | 4.16 |
| In3.Cu | 0.0152 | — |
| Core | 0.55 | 4.6 |
| In4.Cu | 0.0152 | — |
| 3313 ×1 prepreg | 0.0994 | 4.1 |
| B.Cu | 0.035 | — |

Published copper/dielectric entries sum to 1.5384 mm; with the existing 0.01 mm mask model per side, KiCad's construction sums to 1.5584 mm. The nominal board/order thickness remains 1.6 mm. No dielectric value was artificially adjusted to force an exact sum. Confirm the pressed construction and impedance geometry with the fab before fabrication. Loss tangent 0.02 remains a generic modeling assumption, not a qualified laminate loss specification.

## Rules and presets

- Minimum track width and clearance: 0.127 mm; normal netclass remains 0.2 mm width/clearance.
- Copper to routed outline: 0.3 mm.
- Standard through-via drill minimum: existing 0.3 mm; via diameter minimum: existing 0.5 mm; annular ring minimum: existing 0.1 mm. Default via remains 0.6/0.3 mm.
- Added via presets: 0.5/0.3, 0.6/0.3, 0.8/0.4 and 1.0/0.5 mm; track presets from 0.127 to 2.0 mm. Power widths must still be sized to actual current and copper geometry.
- Silkscreen clearance 0.15 mm, text height 1.0 mm and stroke 0.15 mm; new silkscreen graphic/text defaults use 0.15 mm strokes.

These are working design rules, not a complete certification of every fabrication capability. PTH annular rings, drills, soldermask, assembly clearances and impedance still require the final manufacturing review.

## Verification and outstanding layout work

Native KiCad DRC parsed the saved canonical board. A separate native read/resave verified all six copper layers and stackup entries. Geometry, the 20 existing footprints, schematic sheets and companion metadata were preserved. Measured outline remains 110 × 100 mm; smallest existing plated drill is 0.6 mm. No routing vias exist yet, so manufacturing features correctly retain that measured drill rather than the future routing default.

DRC: 36 findings before setup; 44 after. The eight additional findings are silkscreen overlaps exposed by the new 0.15 mm clearance. Current totals: 40 silkscreen overlaps, two hole-clearance violations, one copper-to-edge violation, and one library-footprint mismatch. This scaffold is not ready for fabrication, and its zero unrouted-item count does not mean the full schematic has been imported or routed. Existing footprint placement issues remain for the layout task.

IPC was unavailable; Backplane explicitly authorized its file fallback. A full project backup preceded staged edits and native validation. The validated board/project were promoted to their exact canonical paths, read back, and the canonical PCB was displayed in Backplane. History has no commits, so history synchronization could not be verified; existing history is untouched. `pcb structure` exited 2 without a report, so no structural-validator pass is claimed; native read/resave and DRC are the validation evidence.

[Verification](../../../build/MujinaControl-S19/six-layer/verification.json) · [DRC](../../../build/MujinaControl-S19/six-layer/after-drc.json) · [Backup location](../../../build/MujinaControl-S19/six-layer/backup.txt)
