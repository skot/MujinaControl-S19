# Q1 input protection upgrade

Q1 is now **onsemi NTTFS008P03P8Z**, a 3.3 × 3.3 mm WDFN8 (CASE483AW, nominal height 0.75 mm). This is the smallest suitable package found among the reviewed P-channel candidates. The design target is four simultaneous 3 A fans plus a conservative 2 A controller allowance: **14 A continuous at 40 °C local ambient**. This is a design target, not a measured board rating.

The schematic's Value, MPN, Manufacturer, LCSC (`C894097`), Datasheet and Description identify the new device. The fab's live stock was seven pieces when checked; this is an extended part. Recheck availability before ordering. No parts were ordered.

## Electrical and thermal basis

The [manufacturer datasheet](https://www.onsemi.com/download/data-sheet/pdf/nttfs008p03p8z-d.pdf), NTTFS008P03P8Z/D Rev. 7 (March 2023), specifies −30 V drain-source, ±25 V gate-source, and 3.8 mΩ maximum on-resistance at −10 V gate drive and 25 °C. The old DMP3013SFV-7 specified 9.5 mΩ under the same gate-drive/temperature conditions. At 14 A, calculated conduction loss falls from **1.862 W to 0.7448 W**, a 60% reduction. At 12 A it is 0.5472 W.

For preliminary hot-loss budgeting, a 1.5 resistance multiplier gives 5.7 mΩ, **1.117 W and 79.8 mV at 14 A**. This is an engineering allowance informed by the normalized temperature curve, not a guaranteed temperature coefficient. A 125 °C junction target at 40 °C ambient requires effective junction-to-ambient thermal resistance no greater than approximately **76 °C/W** at that loss. The absolute junction limit is 150 °C.

The datasheet's steady-state ambient ratings are 22 A at 25 °C and 16 A at 85 °C, with 47 °C/W on its specified 1 square inch, 2 oz copper test board. Neither that thermal resistance nor the 96 A case-controlled headline rating is assigned to this PCB. This board has 1 oz outer and approximately 0.5 oz inner copper. Actual thermal resistance remains to be established by measurement or a validated coupled thermal model.

The reverse-polarity topology is unchanged: drain pins 5–8 and the exposed pad connect to raw +12V_IN; source pins 1–3 feed +12V_FAN and the controller branch; gate pin 4 retains D2's 12 V clamp and R270's 10 kΩ pull-down. At normal 12 V input the gate drive is close to −12 V. No fuse, current limiter or controlled-inrush circuit was added. The larger typical gate charge (134 nC at −10 V) is acceptable for this normally static protection switch, but startup, hot-plug and fan surge behavior still need bench verification with the actual fan models and input supply.

## Footprint and copper

Q1 remains at (148.4, 57.0) mm, angle 0°. The other 254 footprints, including all fixed connectors, are unchanged. The new project footprint is `Mujina:onsemi_WDFN-8_3.3x3.3mm_P0.65mm_CASE483AW`. It follows the mounting pattern on datasheet page 6: 0.65 mm pitch; source/gate lands 0.42 × 0.70 mm centered at y=1.40; drain fingers 0.42 × 0.45 mm centered at y=−1.525; main drain land 2.37 × 1.70 mm centered at y=−0.45. The resulting drain outline spans y=−1.75 to +0.40. The main land intentionally shares pad number 8. Courtyard is 3.8 × 4.0 mm with a 0.25 mm minimum margin beyond body/pad extents. No via-in-pad is used.

Dedicated raw-input heat spreaders were added in the already routed input region on F.Cu, B.Cu, In2.Cu and In3.Cu, with solid connections and 0.30 mm clearance. Their filled areas are about 194 mm² on top and 185 mm² on each other layer. Twelve additional through-vias stitch this area; the existing 15-via drain transition bank and three input plated pins also connect the copper. Every one of the board's 283 vias is 0.45/0.30 mm. These areas do not, by themselves, establish a thermal resistance. In1/In4 remain available for the later ground-plane pass, and whole-board reference planes are still unfinished.

The existing 3.3 mm package STEP is retained as a **compatible placement envelope**, not represented as an exact onsemi model. Its association and this limitation are recorded in the footprint description.

## Physical pin-map acceptance

Sources: datasheet p.1 electrical drawing and p.6 CASE483AW Issue C, document 98AON13672G (25 September 2026). The package **top view** shows pin 1 at bottom left, 1→4 left-to-right along the bottom, then 5→8 right-to-left along the top. The separate bottom-view drawing is mirrored and was not copied directly into the footprint.

The existing `bitcrane:DMP3013SFV` symbol is reused solely as its compatible eight-pin PMOS glyph; its instance value and procurement fields identify the new device. All symbol pin types are passive, as in the original symbol. The library's old default description is not the selected device specification.

| Physical lead | Function / symbol pin | Footprint pad | Local x, y mm | View / evidence |
|---|---|---|---|---|
| 1 | S / 1 | 1 | −0.975, +1.400 | Top; p.1, p.6 |
| 2 | S / 2 | 2 | −0.325, +1.400 | Top; p.1, p.6 |
| 3 | S / 3 | 3 | +0.325, +1.400 | Top; p.1, p.6 |
| 4 | G / 4 | 4 | +0.975, +1.400 | Top; p.1, p.6 |
| 5 | D / 5 | 5 | +0.975, −1.525 | Top; p.1, p.6 |
| 6 | D / 6 | 6 | +0.325, −1.525 | Top; p.1, p.6 |
| 7 | D / 7 | 7 | −0.325, −1.525 | Top; p.1, p.6 |
| 8 | D / 8 | 8 | −0.975, −1.525 | Top; p.1, p.6 |
| Exposed drain | D, common to 5–8 | 8 (duplicate) | 0, −0.450 | Top land pattern; p.6, drain thermal reference p.1 |

Reconciliation: eight numbered physical leads plus exposed drain; eight symbol pins; nine electrical copper pads, with one intentional duplicate number; no mechanical-only pads or holes. Queried library and native board readbacks, a disposable board export, the package drawings and the saved schematic were inspected. Pad numbers, physical orientation and pin-to-net assignments agree.

## Verification and remaining qualification

- All 192 exported schematic pin-to-net partitions are unchanged. Native board connectivity confirms all eight raw-input pads, 18 protected-rail pads and three gate-net pads remain connected.
- ERC: zero errors and the same two existing DISPLAY_SCL / DISPLAY_SDA isolated-label warnings.
- DRC: the same 179 pre-existing findings and 385 unfinished connections; no new findings from this change. Existing findings are 120 dangling vias, 40 silk overlaps, 16 silk-edge clearances, two J2 hole clearances and one J16 library mismatch.
- Readability: zero errors, no suppressed groups; 71 retained long-wire advisories. The continuous local wires remain useful and unambiguous. All ten sheets were visually reviewed; the changed power sheet was also reviewed at readable zoom.
- Nine other schematic files and the project/custom-rule files are byte-identical to the pre-change backup. Existing routing is retained, with Q1's 2.6 mm drain collector shifted 0.10 mm upward to maintain clearance to the manufacturer's source lands. Only Q1's footprint definition/metadata, that collector, local thermal copper and 12 new stitching vias changed on the PCB.

Before rating the assembled board for continuous 14 A, measure Q1 and the source/drain neck temperatures at thermal equilibrium in the intended enclosure, at 40 °C local ambient and the minimum credible airflow. Establish junction temperature using a defensible thermal/electrical method; a top-surface measurement alone is not junction temperature. Target Tj ≤125 °C, verify connector/contact and copper temperatures, and test simultaneous startup, stall/restart and hot-plug transients with actual fans. Increase spreading/airflow or derate if the target is missed. This PCB remains unfinished and is not released for fabrication.

Evidence: [Q1 checks and renders](../../../build/MujinaControl-S19/q1-upgrade/), including `preservation.json`, `power-connectivity.json`, `checks.json`, `final-drc.json`, `after-erc.json`, `before.xml`, `after.xml`, readability reports, footprint readback and the downloaded manufacturer PDF.

Canonical board, root schematic and changed sheet were shown in Backplane; board/project/root/changed-sheet blobs match the existing history checkpoint. [Visual review record](../../../build/MujinaControl-S19/q1-upgrade/review.md).
