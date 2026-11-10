# Flash bus and SoC support routing — 2026-11-10

Saved to the canonical `MujinaControl-S19.kicad_pcb`. The board viewer shows that exact file; its saved content and Backplane history checkpoint both resolve to Git blob `6fe229a8ad1bdbc95adef099a94c3ddd8d62f3ab`. This is an unfinished routing milestone, not a manufacturing release.

## Changes

- Completed SPI NAND CLK, CS and D0–D3, the R225 clock termination, the three pull-up branches, the 3.3 V regulator feed, bypass capacitors, and ground connections.
- Rotated U130 within the flash area and placed C268/C269 beside its supply pin; moved R226/R227/R228 beside their signal pins. These six footprints are the only placement changes in this pass. The other 275 footprints, including fixed connectors, SoC, clocks and all six regulators, kept their positions.
- Used 0.14 mm In3.Cu (L4) flash trunks with a local stitched In2.Cu (L3) ground reference. D0 stays on F.Cu; short F.Cu escapes use 0.15/0.16 mm widths. All vias remain 0.45 mm diameter / 0.30 mm drill.
- Added nearby return vias and connected the flash's exposed ground pad and bypass grounds. The 0.30 mm supply branch feeds the flash circuit; it is not a trunk sized for the entire 3.3 V rail.
- Reconnected Ethernet link-LED and MASKROM button control paths around the bus.
- Also completed BOOT_ADC, CODEC_VCM and DRAM_ZQ. The DDR calibration route uses the existing SoC escape and one destination via, without the trial router's redundant transitions.
- Preserved schematic files, project/routing rules, all pad net identities, values, footprint library IDs, attributes and 3D models.

## Flash geometry

The local RV1106 Design Guide FSPI section specifies 50 ohm ±10%, data-to-clock matching below 300 mil (7.62 mm), and short traces. The new 0.14 mm inner trunk calculates to 50.08 ohms with the saved six-layer geometry using the [fab's impedance calculator](https://jlcpcb.com/pcb-impedance-calculator). This is a nominal transmission-line calculation, not a simulation of pads, vias or package parasitics. Inputs/results are in the build evidence.

| Signal | PCB path, mm | Difference from clock, mm |
|---|---:|---:|
| CLK | 19.622 | +0.000 |
| D0 | 20.119 | +0.497 |
| D1 | 16.816 | -2.807 |
| D2 | 20.688 | +1.066 |
| D3 | 15.948 | -3.674 |
| CS_N | 17.549 | -2.073 |

Lengths are source-to-sink pad-center paths, excluding pull-up branches. They include actual F.Cu–In3.Cu depth (0.8137 mm per transition) and the 1.02 mm pad span across R225. Maximum PCB mismatch is **3.674 mm**, with no added tuning meanders. Package routing and resistor/via parasitics are not known; these measurements do not establish complete package-plus-board timing closure.

The saved filled L3 ground covers every inner flash centerline outside the immediate signal-via antipads. The same check passes for top flash traces against L2 ground. Existing USB, Ethernet data and SD routes gained no reference-plane gaps. Pads/via discontinuities still require normal assembled-board signal-integrity validation.

## Verification

- Native KiCad DRC with schematic parity: **116 → 102 unconnected items**; other findings **81 → 75**, with **zero new findings** by type and item IDs.
- The existing Q1 `ki_fp_filters` parity warning remains unchanged.
- 21 flash/support connectivity checks and 126 regulator/clock checks passed.
- 281 unique footprints. 510 vias, all 0.45/0.30 mm. All 384 pre-existing USB, Ethernet data and SD copper objects checked are unchanged.
- Filled-plane checks and inspection of top, bottom, inner-signal and local-ground renders completed. No new mechanical outline or stackup changes.

## Remaining routing

- `+0V9_CORE`: 15
- `+0V9_CPU`: 4
- `+1V35_DDR`: 7
- `+1V8`: 7
- `+3V3`: 37
- `+5V_SYS`: 14
- `DEBUG_TX`: 1
- `FAN2_TACH`: 1
- `FAN3_TACH`: 1
- `FAN4_TACH`: 1
- `GND`: 2
- `HB0_PLUG`: 1
- `HB1_PLUG`: 1
- `HB1_RX`: 1
- `HB2_RST_N`: 1
- `HB2_RX`: 1
- `HB_SCL`: 1
- `RTC_3V3`: 1
- `SEQ_IO`: 2
- `SEQ_MID`: 2
- `STATUS_LED`: 1

The remaining RTC supply escape and control signals need deliberate fanout/corridor work; broad automatic attempts were not retained. Most unrouted items are rail distribution. Existing DRC findings and Q1 parity warning still need a later cleanup/review.

## Evidence

Build directory: `build/MujinaControl-S19/routing-flash/` from the project root. Key files: `verification.json`, `bus-verification.json`, `final-drc.json`, `reference-changes.json`, `flash-reference-gaps.json`, `flash-front-reference-gaps.json`, `impedance-014.json`, saved route/placement plans and before-state backups. Renders: `top-whole.png`, `top-flash.png`, `in3-soc.png`, `in2-soc.png`, `bottom-soc.png`.
