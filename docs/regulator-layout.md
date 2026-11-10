# TPS62933 regulator layout review

U110–U115 were repositioned and locally rerouted to follow section 12 of the [TI TPS62933 datasheet, SLUSEA4D](https://www.ti.com/lit/ds/symlink/tps62933.pdf#page=40), particularly the top and bottom layout examples on printed page 41. This supersedes the PCB layout described in `regulator-reuse.md`; the schematic, BOM, rail settings and current budgets from that conversion are unchanged.

## Layout applied to all six stages

| TI recommendation | Implementation |
|---|---|
| Minimize the high-frequency input loop | The 100 nF capacitor sits immediately beside VIN and GND, with the bulk input capacitor behind it. Both are on the IC's top layer. The ground return joins a solid local pour. |
| Keep switching copper short and wide | All SW-to-inductor paths are now 1.669 mm measured along track centerlines. A 0.28 mm pin escape expands to 0.65 mm. Inductors and both output capacitors remain on the top layer, with 0.8–1.0 mm output connections. |
| Put the bootstrap capacitor close to BST/SW | Each bootstrap capacitor is beside the right-hand pins. Its return joins the SW pin escape directly, rather than detouring around the inductor. Both connections use 0.28 mm copper. |
| Place FB, RT and SS parts close to their pins | Dividers are above the IC, timing resistors on the quiet input side, and SS capacitors beside the SS pin. These signal paths use 0.28 mm copper, exceeding TI's 10 mil recommendation. |
| Sense output away from SW copper | Each divider has a separate sense connection from an output capacitor, on a buried or bottom layer around the switching area. The FB pin connection stays local on top. The existing inner ground planes provide shielding. |
| Spread heat and stitch ground generously | Six solid top ground pours connect the local returns to the two existing inner ground planes through nearby vias. Ground stitching surrounds the input return and output capacitors; power transitions use paired vias where connected on both receiving layers. |

The six-layer stackup is retained: nominal 1.6 mm, 1 oz outer and 0.5 oz inner copper. TI's illustration uses a two-layer, 2 oz board; the routing topology was adapted to our reference planes, not copied as an assertion of equal thermal performance. All 432 vias remain 0.45 mm diameter / 0.30 mm drill, including the agreed filled/capped via-in-pad placements. SW and bootstrap loops do not change layers.

## Measured local paths

Lengths below are in millimetres along routed track centerlines between pad centers, not copper-edge gaps. Bootstrap entries give BST-pin-to-capacitor / capacitor-to-SW-pin lengths. The CPU output capacitor has a small offset to clear an existing supply via.

| Converter | SW → L, before → after | VIN → 100 nF | Bootstrap paths | FB → divider | L → first Cout |
|---|---:|---:|---:|---:|---:|
| U110 | 6.08 → 1.669 | 1.255 | 1.855 / 1.963 | 2.1 | 1.97 |
| U111 | 6.08 → 1.669 | 1.255 | 1.855 / 1.963 | 2.1 | 2.301 |
| U112 | 5.013 → 1.669 | 1.255 | 1.855 / 1.963 | 2.1 | 1.97 |
| U113 | 2.131 → 1.669 | 1.255 | 1.855 / 1.963 | 2.1 | 1.97 |
| U114 | 2.131 → 1.669 | 1.255 | 1.855 / 1.963 | 2.1 | 1.97 |
| U115 | 2.131 → 1.669 | 1.255 | 1.855 / 1.963 | 2.1 | 1.97 |

The total bootstrap path is now 3.818 mm in each stage. RT paths are 1.649 mm (1.737 mm for U115); SS paths are 2.585 mm. The individual BST or SS leg is not shorter than every previous leg: the improvement is the compact complete arrangement, direct SW return, wide local copper and quiet feedback placement. Both output capacitors are now part of each local stage, including C288, which previously sat remotely.

## Preserved connections and checks

- 69 footprints moved within the 72-part regulator scope. All 209 other footprints, including every connector, retain their position and orientation.
- All 281 footprints remain unique. Every pad net, component value, DNP state and model reference was preserved. All schematic sheets and the project configuration are byte-for-byte unchanged.
- 122 native KiCad connectivity checks pass across the input, output, bootstrap, feedback, timing and ground connections. Every local private regulator net is fully connected.
- HB2_PLUG, FAN4_PWM, PSU_SCL, FAN1_TACH, FAN1_PWM and PSU_EN were moved locally to other copper layers where needed. Their pad connectivity partitions match the original copper. The pre-existing unfinished FAN1_TACH connection to R13 remains unfinished; this layout pass did not claim to finish that net.
- Zone fill and board DRC: **83 findings before, 83 after; zero new findings**. Existing findings remain: 43 silk overlap, 16 silk edge clearance, 12 dangling vias, 4 dangling tracks, 3 footprint-library mismatches, 2 hole-clearance findings, 2 silk-over-copper findings and 1 malformed courtyard.
- Unconnected items: **239 → 238**, due to one completed ground connection. No net gained an unconnected component. The board is still partially routed.
- Schematic parity retains the existing Q1 `ki_fp_filters` metadata warning. No new parity issue appeared.
- All six groups were visually inspected on top, bottom, both signal/power inner layers and both ground-reference layers. The power loops remain on top; the ground references are continuous around them apart from normal via antipads. No new courtyard overlap was introduced.
- Measured outline remains 110 × 100 mm; the minimum drilled hole remains 0.30 mm. The fab metadata was refreshed and remains marked not for ordering.

The canonical PCB was saved after each placement/routing milestone and shown in Backplane. Its disk hash matches the Backplane history checkpoint. The canonical root schematic and two regulator sheets also match their existing history hashes. Existing history and companion metadata were preserved.

This is a layout correction, not prototype qualification. Thermal rise, startup, load-step response and overload behavior still require the assembled-board checks identified in `regulator-reuse.md`.

## Evidence

- `build/MujinaControl-S19/regulator-layout-review/verification.json`: native checks, preservation audit and before/after path lengths.
- `final-drc.json`: saved-board DRC with schematic parity.
- `top-six.png`, `bottom-six.png`, `in1-six.png` through `in4-six.png`: six-stage review montages; individual `U110-top.png` etc. provide larger crops.
- `history-verification.json`: canonical disk/history hashes.
- `measured-features.json`: board dimensions and minimum drill.
- `backup.txt`: location of the complete pre-edit CAD backup.

![All six final top-layer regulator layouts](../../../build/MujinaControl-S19/regulator-layout-review/top-six.png)
