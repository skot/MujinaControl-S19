# Q1 input protection

## 2026-11-14: Q1 is Vishay SiSS27DN-T1-GE3

Q1 was changed from onsemi NTTFS008P03P8Z (fab part C894097) to **Vishay SiSS27DN-T1-GE3** (fab part `C506609`, PowerPAK 1212-8S, 3.3 × 3.3 × 0.75 mm) because the fab had 7 pieces of the onsemi part for the 5 needed. The Vishay part had 7,565 in stock on 2026-11-14 and costs about a quarter as much. It is an extended part, like the one it replaces. It goes on the same lands: no copper, via or placement change.

It is the only 30 V P-channel part in this package size in the fab's stock that comes from a major maker with a guaranteed on-resistance below 6 mΩ. It has a higher on-resistance than the onsemi part, so **Q1 runs hotter than before**:

| | SiSS27DN (now) | NTTFS008P03P8Z (before) |
|---|---|---|
| Drain-source / gate-source rating | −30 V / ±20 V | −30 V / ±25 V |
| On-resistance at −10 V, 25 °C, maximum | 5.6 mΩ (4.6 typical) | 3.8 mΩ |
| On-resistance at −4.5 V, maximum | 9.0 mΩ | 6.5 mΩ |
| Loss at 14 A, 25 °C figure | 1.10 W | 0.74 W |
| Loss at 14 A, hot (× 1.5) | 1.65 W, 118 mV | 1.12 W, 80 mV |
| Loss at 12 A, hot | 1.21 W | 0.82 W |
| Junction-to-ambient needed for 125 °C at 40 °C ambient, 14 A | ≤ 52 °C/W | ≤ 76 °C/W |
| Same, at 13 A (four 3 A fans plus about 1 A for the board) | ≤ 60 °C/W | ≤ 88 °C/W |
| Total gate charge at −10 V, typical | 92 nC | 134 nC |

The × 1.5 allowance is kept from the earlier calculation; the Vishay curve (datasheet page 3, −10 V) reads about 1.45 at 125 °C and 1.57 at 150 °C. Vishay's own steady-state figure on a 1 inch square FR-4 test board is 63 °C/W maximum, which would not hold 125 °C at 14 A. This board's drain copper on four layers and its via bank should do better than that test board, but that has not been measured. **The temperature measurement described at the end of this page matters more now; at the full 14 A target the margin is thin.**

Gate drive is unchanged: D2 clamps gate-source at 11.4–12.7 V, inside the ±20 V rating; the threshold is −1 to −2.2 V, so the part is fully on at 12 V input. Reverse-polarity blocking is unchanged.

**Land pattern.** Vishay package drawing 6008 (datasheet page 7): leads 0.30 mm wide and 0.43 mm long at 0.65 mm pitch, drain pad 2.25 × 1.70 mm with 0.41 mm fingers to the package edge, 0.76 mm between source leads and drain pad. In the footprint's coordinates the source and gate leads span y 1.22 to 1.65 (lands 1.05 to 1.75, 0.42 wide), the drain pad spans y −1.24 to +0.46 and x ±1.125 (land −1.30 to +0.40, ±1.185) and the fingers reach −1.65 (lands to −1.75). The package's drain pad overhangs the land by 0.06 mm toward the source side, leaving 0.59 mm to the source lands. Pin numbers are the same: source 1–3, gate 4, drain 5–8 and the exposed pad. The footprint keeps its name (`Mujina:onsemi_WDFN-8_3.3x3.3mm_P0.65mm_CASE483AW`); its description now names both parts.

**Ways back.** NTTFS008P03P8Z fits the same lands and is the lower-loss choice whenever the fab has enough of it. If the measurement shows too little margin, the next step is a 5 × 6 mm package, for example onsemi NTMFS002P03P8Z (C2902170, 1.4 mΩ maximum, 1,306 in stock): about a quarter of the loss, but a new footprint and a re-layout of the input copper, and against the project note to use the smallest package.

Changed: Q1's Value, MPN, Manufacturer, fab part number, Datasheet, Description and Source fields in the schematic and on the board, the sheet note beside Q1, and the footprint description (library and board): 16 lines in `09_power_service.kicad_sch`, 16 in the board file. ERC 0; DRC with schematic parity 0 violations, 0 unconnected, 0 parity issues; readability checker clear. Evidence: `build/MujinaControl-S19/q1sub/` (both datasheets, `apply.py`, `erc.json`, `drc.json`, `bom.csv`). Source: [Vishay SiSS27DN datasheet](https://www.vishay.com/docs/62847/siss27dn.pdf), document 62847 Rev. A.

## Earlier: upgrade to NTTFS008P03P8Z

The rest of this page is the record of the earlier change from DMP3013SFV-7 to the onsemi part. The footprint, copper and pin map it describes are what the board still has.

Q1 became **onsemi NTTFS008P03P8Z**, a 3.3 × 3.3 mm WDFN8 (CASE483AW, nominal height 0.75 mm). This is the smallest suitable package found among the reviewed P-channel candidates. The design target is four simultaneous 3 A fans plus a conservative 2 A controller allowance: **14 A continuous at 40 °C local ambient**. This is a design target, not a measured board rating.

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
