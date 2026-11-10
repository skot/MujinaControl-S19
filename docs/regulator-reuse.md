# TPS62933 regulator conversion

> Subsequent layout update: see [regulator-layout.md](regulator-layout.md) for the datasheet-based placement and routing now on the PCB. Placement and PCB check counts below record the earlier conversion milestone; the current board has 238 unconnected items and 83 retained DRC findings.

All six buck converters, U110–U115, now use TPS62933DRLR. The protected 12 V → 5 V → sequenced SoC rails architecture and TPS3808 supervisors are retained. Fan current bypasses the 5 V converter. This is a saved design milestone, not a production release: the board still has 239 unrouted connections.

## Reuse from bitaxeBonanza-1004x

60 component instances use 11 exact manufacturer part numbers present in the reference design. The converter and inductor footprints preserve Bonanza's pad geometry; their local outlines were cleaned up, and their STEP models were attached. The existing precision dividers for the four low-voltage rails and their 100 pF feedforward capacitors were retained. All 111 resistor symbols remain US zigzag.

| Manufacturer part number | Catalog ID | Count | References |
|---|---|---:|---|
| CL21A226MAQNNNE | C45783 | 17 | C201, C203, C204, C206, C208, C209, C211, C213, C214, C216, C218, C219, C221, C223, C224, C287, C288 |
| CL05B104KB54PNC | C307331 | 12 | C202, C207, C212, C217, C222, C292, C294, C296, C298, C300, C286, C302 |
| CL10B333KB8NNNC | C21117 | 6 | C291, C293, C295, C297, C299, C301 |
| FTC201612S1R5MBCA | C5832350 | 6 | L201, L202, L203, L204, L205, L210 |
| 0402WGF1502TCE | C25756 | 6 | R274, R275, R276, R277, R278, R281 |
| 0402WGF4702TCE | C25792 | 1 | R280 |
| TPS62933DRLR | C3200405 | 6 | U110, U111, U112, U113, U114, U115 |
| CL32B106KBJNNNE | C138687 | 1 | C285 |
| 0402WGF1002TCE | C25744 | 1 | R279 |
| 0402WGF2702TCE | C25771 | 2 | R282, R284 |
| 0402WGF5101TCE | C25905 | 2 | R283, R285 |

The converter and inductor are extended parts in the fab's stock; the 22 µF capacitor is basic. Observed stock was 19,531 converters and 7,338 inductors on 2026-11-10 UTC. These are inventory observations, not reservations. Raw part observations are in `build/MujinaControl-S19/regulator-conversion/catalog-observations.json`.

## Rail settings

| Converter | Input | Nominal output | Feedback top / bottom | RT / nominal frequency |
|---|---|---|---|---|
| U110 | 5 V | 0.8992 V core | 12.4 kΩ / 100 kΩ | 15 kΩ / 1.35 MHz |
| U111 | 5 V | 0.8992 V CPU | 12.4 kΩ / 100 kΩ | 15 kΩ / 1.35 MHz |
| U112 | 5 V | 1.3448 V DDR | 68.1 kΩ / 100 kΩ | 15 kΩ / 1.35 MHz |
| U113 | 5 V | 1.792 V analog | 124 kΩ / 100 kΩ | 15 kΩ / 1.35 MHz |
| U114 | 5 V | 3.3067 V I/O | 47 kΩ / 15 kΩ | 15 kΩ / 1.35 MHz |
| U115 | protected 12 V | 5.0353 V | 27 kΩ / 5.1 kΩ | 10 kΩ / 1.98 MHz |

Computed using Vout = 0.8 × (1 + Rtop/Rbottom) and the RT equation in the [TI datasheet](https://www.ti.com/lit/ds/symlink/tps62933.pdf). Each SS pin has 33 nF, giving approximately 4.8 ms nominal soft start. Each converter has a local 100 nF input bypass and bootstrap capacitor. U115 uses a 27 kΩ / 5.1 kΩ EN divider; its nominal start threshold is about 7.6 V. EN is no longer connected directly to 12 V. The other enable nets retain their original sequencing.

## Current and capacitance checks

The shared 5 V rail retains its **2 A system budget**. IC current rating alone does not establish a 3 A rating for every assembled converter. Existing core/CPU/DDR peak budgets remain 1.6 A / 0.4 A / 0.4 A.

Using the selected 1.5 µH inductance and nominal frequencies, calculated inductor ripple is about 0.36 A peak-to-peak at 0.9 V from 5 V and 0.98 A at 5.035 V from 12 V. Thus nominal peaks are approximately 1.78 A for the 1.6 A core load and 2.49 A for the 2 A 5 V load. These are ideal steady-state calculations, not measurements or a fault analysis.

The [inductor manufacturer's table](https://pcbparts.dev/mcp/datasheet/C5832350), FTC201612 section on PDF page 16, lists 40/50 mΩ typical/maximum DCR and 4.0/3.5 A in its two current columns. The second current column is confusingly headed “Max”; this design uses the lower 3.5 A figure for screening, not the catalog's simplified 4 A figure. It does **not** establish nonsaturation at the converter's maximum 5.8 A high-side current limit. Overload, hard-short recovery, and temperature behavior need prototype qualification; a higher-saturation-current inductor may be necessary if these tests fail. Reusing this compact part is not a guarantee of fault robustness.

The [Samsung part-specific capacitance curves](https://datasheet.octopart.com/CL21A226MAQNNNE-Samsung-Electro-Mechanics-datasheet-182022794.pdf) show roughly 55–60% capacitance loss at 5 V. Two nominal 22 µF output capacitors therefore provide roughly 18–20 µF typical at 5 V, before tolerance, temperature, and aging; they must not be treated as 44 µF effective. The five 5 V input capacitors each have the same derating. U115 also sees their distributed capacitance. Verify startup, ripple, load steps and control-loop margin on the assembled board, including the retained 100 pF feedforward capacitors. Manufacturer curves are typical, not guaranteed minimum capacitance.

## PCB integration

Only the six converter groups were repositioned. All 215 original footprints outside these groups, including every connector, retained position and orientation. U115 moved into the open area to the right to fit its 1210 input capacitor and keep the switching circuit local. New pads, vias, and traces match the saved schematic. Obsolete converter copper and remote feedback tails were removed; the retained supply backbones were reconnected. Existing control-signal tracks were preserved.

Ground returns use the inner reference planes. Power transitions use 0.45/0.30 mm vias, including paired vias where appropriate. The full board has 355 vias, all at that size. The board remains six layers, 110 × 100 mm, nominal 1.6 mm. The minimum plated drill is 0.30 mm. Footprint model references resolve, including the existing embedded button models. The reused inductor STEP is a 1.1 mm nominal-height model; the selected part is specified as 1.2 mm tall, so allow the actual component envelope in mechanical clearance work.

## Verification

- 800 original pin-to-net assignments preserved directly; four FB pins deliberately remapped from pin 1 to pin 8. U114/U115 now have external feedback dividers, and U115 has the new EN divider.
- 24 new physical symbols; 281 unique footprints. Board pad nets match the exported schematic netlist. Existing DNP states are preserved; the new converter parts are fitted.
- 221 original components outside the changed BOM set retain values, footprints, and metadata.
- ERC: zero errors, two existing warnings on DISPLAY_SCL/DISPLAY_SDA pin-connected labels.
- Readability: zero errors, 72 retained cross-group-wire advisories. These are visible local circuit runs; shortening them into label-only stubs would obscure the functional groups. No checks were suppressed for this conversion.
- All ten saved sheets reviewed at overview scale; `02_regulators.kicad_sch` and `09_power_service.kicad_sch` also reviewed at readable zoom. The changed circuits are locally wired, with aligned fields and explicit notes.
- PCB DRC: **85 → 83 findings**, with **zero new findings**. The remaining findings are the existing silk, dangling copper, footprint-library, USB-hole and courtyard issues. One existing Q1 metadata parity warning remains.
- Unconnected count: **242 → 239**; the difference is three ground connections completed. No net gained an unconnected component. Previously unrouted sequencing and SoC supply connections remain part of the unfinished board routing.

Evidence and renders: `build/MujinaControl-S19/regulator-conversion/verification.json`, `final-erc.json`, `final-drc.json`, `readability-final/`, `after.pdf`, `final-sheet-*.png`, and `upper.png`, `ddr.png`, `1v8.png`. Backups are recorded in `backup.txt` in that directory. All CAD edits were saved to the canonical project paths through native or Konnect tools.

The canonical root schematic and PCB were shown in Backplane. Their saved hashes, and those of both changed sheets, match the current Backplane history checkpoint; see `history-verification.json`. Existing history and companion metadata were preserved.
