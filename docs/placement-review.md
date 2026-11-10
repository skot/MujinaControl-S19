# Placement review — 2026-11-10

Done on the unrouted board (branch `fable`), before re-routing. 70 of 281 footprints moved. The locked connectors (J1, J3–J9, J11–J14, J100), R259, the mounting holes and the SoC did not move. Pad nets, values and footprints are unchanged; no tracks or vias exist.

DRC after the moves matches the pre-move baseline: the two J2 pad-to-locating-hole findings and J1's open courtyard (all inside library footprints), 43 silkscreen overlaps, 16 silk-to-edge, 2 silk-over-copper, 3 library mismatches. No courtyard overlaps. 499 unconnected items, as expected with no routing.

## What was kept, and why

- **SoC position and rotation.** Scoring every rotation and a grid of positions by distance from each SoC pin to its fixed connector gave a spread of about 4 % between the current spot and the best one, and no rotation beat 0°. Rotating to face the Ethernet pins at the jack would put SD and USB on the far side.
- **SoC decoupling ring.** Every supply pin has a 100 nF within 1.3–1.8 mm, except pins 108, 115 and 116 on the north side at 3.0 mm, where the second row leaves an escape lane for four signals. Left as is apart from the two capacitors noted below.
- **Core and CPU regulators (U110, U111)** north of the SoC, next to pins 115/116, with their supervisors.
- **3.3 V and 5 V regulators (U114, U115), input protection (Q1, D2, D220)** near J1.
- **Hashboard strap and pull-up rows, fan front-ends, PSU connector parts, SD pull-ups, USB-C parts, status LED, both buttons, 24 MHz crystal.**

## What moved

| Change | Why | Before → after |
|---|---|---|
| 1.8 V regulator U113 and supervisor U123 from the far west into an east column under U115 | It sat alone 65 mm from the 5 V source, in the hashboard/SD routing field | 5 V input cap to 5 V output cap 65.3 → 8.6 mm; output cap to SoC pin 70 33.1 → 15.1 mm |
| DDR regulator U112 turned so its output faces the SoC, lined up with U113; supervisor U122 beside it | Output was on the far side | Output cap to pin 56 22.0 → 17.0 mm |
| 3.3 V supervisor U124 to the SoC's south-east | Its old spot is now the 1.8 V regulator; RESET_N pin is at that corner | — |
| Ethernet series resistors R242–R245 from east of the SoC to the jack, with D201/D202 and the centre-tap capacitors | The old spot forced a long loop round the SoC | Resistor to jack pin 38.1 → 8.9 mm |
| Flash U130 rotated 180° and centred under its pins; R225 at the flash clock pad; pull-ups and decoupling re-seated | At 0° three signals had to cross two; at 180° D3, D0 and CS line up | Clock resistor to flash pad 7.0 → 1.2 mm |
| SD clock resistor R235 to its pin | It was past the SoC corner | 11.2 → 3.2 mm |
| USB series resistors R252/R253 to the south-west exit; C248/C256 shifted 0.5 mm down the pin row | Opens a lane for the USB pair between C262 and C248 (courtyard gap 0.44 → 0.96 mm) | Pin-28 and pin-31 capacitors 1.27 → 1.38/1.40 mm |
| RTC crystal Y101 and load capacitors re-seated; R223, R224 moved out of the crystal's path | R223 and R224 left a 0.3 mm gap for both crystal lines | Crystal pad to pin 7.0 → 6.3 mm |
| 1.8 V bulk C259, VCM C277, boot-strap parts R238/R239/C276 | Make room for the USB exit | C259 to pin 31 5.4 → 3.1 mm |
| Debug header J16 and R240 from the west edge to south-east of the SoC | Its pins are on the SoC's east side | 56.3 → 23.0 mm |

Straight-line length of all signal connections fell from 2868 to 2710 mm. The sequencing and reset nets fell most: SEQ_MID 107 → 83 mm, SEQ_IO 83 → 54 mm, RESET_N 58 → 42 mm.

## Routing this placement expects

These are intentions the placement was made for. None has been routed or checked by a router yet.

- **Ethernet:** under-chip via at each SoC pin, bottom layer straight south beneath the SoC and flash, one via up at each series resistor, then top layer through the ESD diode to the jack pin. Two vias per line and roughly 40 mm (38 mm straight-line), against four layer changes and 57.6 mm before.
- **USB:** top layer out through the gap between C262 and C248, through R252/R253, then top layer to J2. The old route had four layer changes.
- **Flash:** D3, D0 and CS on the top layer. The clock must change layer once, which is why R225 is at the flash end. D1 and D2 arrive in swapped order, so one of them also changes layer.
- **SD, boot strap, VBUS detect:** still need under-chip vias; the decoupling capacitors stand in front of those pins.
- **Regulators:** U112/U113 are rigid rotations of the reviewed datasheet arrangement in `regulator-layout.md`; their local loops are the same shape as before.

## Left for a decision

- **SD socket J101** could slide about 7 mm toward J2, shortening each SD line by roughly 15 %. Not done: it changes where the card slot sits on the edge.
- **Debug header J16** moved off the board edge. If it has to be reachable at the west edge, it should go back; only the two UART lines get longer.
- **Fan channels** 1 and 4 are laid out differently from 2 and 3 because the bulk capacitors sit under the middle pair. Left alone; a common layout needs the bulk capacitors moved.
- **Silkscreen:** the 43 overlaps predate this pass and still need a label clean-up.

Evidence (before/after part tables, DRC reports, renders, move lists): `build/MujinaControl-S19/placement-review/`. Pre-move copy of the board: see `backup.txt` there.
