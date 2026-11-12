# Routing from reviewed placement — 2026-11-10

Canonical board: `MujinaControl-S19.kicad_pcb`. Current saved Git blob: `a125af57035951a064f8b93d4ad1fcbce73c4419`. This is an unfinished routing milestone, not a manufacturing release.

## Current schematic and placement

The old routed checkpoint was not restored. The reviewed `fable` placement is retained: all 281 existing footprints have identical positions, rotations, layers and lock states. The current schematic, project, rules and library files were preserved byte-for-byte during this pass.

Native netlist import reconciled 20 SoC pad-net assignments and added J15, C303–C305 and R286–R287. J15 is vertical at the west edge, pin 1 at (69, 60.5) mm just right of mounting hole H3 (moved there on 2026-11-10 with its bypass capacitors, I²C pull-ups and local tracks as one group). No existing footprint was moved to make room. The board now has 287 unique footprints, and every exported schematic pad-net assignment matches the PCB. Parity has only the existing Q1 `ki_fp_filters` warning.

## Saved routing

- Completed SPI NAND CLK, CS and D0–D3, all three pull-up branches, both bypass capacitors and NAND ground connections. The dedicated 0.50 mm bottom-layer supply branch joins the 3.3 V converter output; it is not the shared rail trunk. D0/D3 are on top, D1/D2/CS on bottom, and the clock crossing is on In3.Cu with a stitched local In2.Cu ground reference.
- Routed all six TPS62933 local circuits from their current pad coordinates: short top-layer switch and bootstrap loops, 0.28 mm pin escapes and quiet control connections, 0.65 mm switch links, 0.8–1.0 mm output links, separate feedback sensing from the first output capacitor, and stitched solid top ground returns. The U115 enable divider is connected. The 125 native regulator checks pass; the converter inputs and outputs still require shared distribution.
- Connected 26 SoC supply/reference pins to their local bypass groups, including RTC_3V3 and CODEC_VCM. Adjacent same-rail pins 49/50 and 54/55 share their nearby connected bypass. The extra C244/C233 bypass capacitors still await rail distribution. Added ground-paddle stitching and connected both peripheral ground pins. These are short local supply connections, not substitutes for current-capable rail trunks.
- Connected the new accessory header's local 5 V/3.3 V pairs, bypass capacitors and I²C pull-ups. The accessory GPIOs and rail feeds remain unrouted.
- Retained the six-layer stackup and board outline. Set ground-zone clearance to 0.20 mm and minimum fill thickness to 0.125 mm so the reference planes retain copper between close signal-via antipads. Local regulator ground connections are solid.

## Flash checks

| Signal | PCB path, mm | Relative to clock, mm |
|---|---:|---:|
| D0 | 14.500 | -6.942 |
| D3 | 17.401 | -4.041 |
| D1 | 18.509 | -2.933 |
| D2 | 16.949 | -4.493 |
| CS_N | 20.338 | -1.104 |
| CLK_SOC | 21.442 | +0.000 |

Lengths include actual layer-to-layer barrel depths (1.5034 mm F.Cu–B.Cu; 0.8137 mm F.Cu–In3.Cu) and the 1.02 mm R225 pad span. Pull-up branches are excluded. Maximum data-to-clock mismatch is **6.942 mm**, below the local RV1106 guide's 7.62 mm PCB guideline. D0 has one broad length-compensation bend; there are no dense tuning meanders. Package delay is unknown, so this is not package-plus-board timing closure.

The fab's coated-microstrip calculator returned **51.08 Ω** for the 0.15 mm outer traces with the recorded six-layer dielectric and finished-copper assumptions. The existing validated calculation for 0.14 mm In3.Cu against local In2.Cu ground is 50.08 Ω. These are nominal transmission-line calculations, not pad/via/package simulations.

All 19 flash native connectivity checks pass. Saved filled-plane geometry covers every flash signal centerline outside its own immediate signal-via transition regions. Top, bottom, clock and reference-layer views were visually inspected. Future routing must preserve these reference paths.

## Verification and remaining work

- **351 tracks, 147 vias**, all vias 0.45 mm diameter / 0.30 mm drill. Dimensions 110 × 100 mm; smallest plated drill 0.30 mm. Fab metadata remains `order: false`.
- Filled-board DRC: **438 unconnected items, 67 other findings**, with zero new other findings by type and affected item IDs. All 178 regulator/SoC checks plus 19 flash checks pass.
- Independent native connectivity grouping also reports **438** missing connections. Earlier CLI reports plateaued at 499 while native grouping still showed 509, so the initial reported 499 is capped; do not interpret 499 → 438 as the total number of connections completed.
- Remaining non-connectivity findings are the existing silk, library-footprint, J2 hole-clearance and J1 courtyard issues. The Q1 metadata parity warning remains.

| Remaining rail | Missing connections |
|---|---:|
| `+0V9_CORE` | 12 |
| `+0V9_CPU` | 4 |
| `+12V_FAN` | 17 |
| `+12V_IN` | 3 |
| `+1V35_DDR` | 5 |
| `+1V8` | 10 |
| `+3V3` | 48 |
| `+5V_SYS` | 20 |
| `GND` | 97 |

Other unfinished work includes USB, Ethernet, SD, both crystal circuits, fan and hashboard circuits, accessory GPIOs, reset/sequencing and miscellaneous controls. The input protection and fan power copper must support 3 A per fan and all four fans plus board load; the 5 V budget is 2 A. No old routes were resurrected.

## Saved-file and history status

Native SaveDocument and read-back verified the canonical file, and `viewer_show` explicitly displayed that same path. **Backplane history is not synchronized:** this thread's history tree has no canonical `boards/...` entry, and the originating thread's board entry is stale. This was checked again after explicit MCP SaveDocument and viewer refresh. Existing history was preserved; no Git commit or push was made. The saved canonical board and rendered evidence contain the work; the history viewer must not be treated as its current snapshot.

## Evidence

`build/MujinaControl-S19/routing-current/`: `verification.json`, `bus-verification.json`, `final-connectivity.json`, `final-drc.json`, `history-verification.json`, `outer-impedance.json`, fresh route plans, created-item manifests and canonical SVG/PNG renders. `backup.txt` records the pre-edit CAD backup. The user's separate handoff backup was untouched.

![Current top-layer routing](../../../build/MujinaControl-S19/routing-current/top-whole.png)

## Power copper — 2026-11-10

High-current nets first, as zones. No signal routing in this pass. DRC is unchanged at 67 standing findings; unconnected items 456 → 450 after the earlier header move.

| Net | Copper | Notes |
|---|---|---|
| +12V_IN | Zones on F.Cu, In2.Cu and B.Cu from J1 pins 1–3 to the Q1 drain, extending under the J1 body for heat spreading | 6 filled vias in the drain pad plus 6 beside it |
| +12V_FAN | F.Cu zone at the Q1 source → 14 vias → bus zone on B.Cu (12.9 mm wide) and In2.Cu (12.4 mm) along the fan connectors, with a tongue to each small-header pin 2 | B.Cu lobe south to C284/C283, D2, D220 and the U115 input capacitor; bulk capacitors C289/C290 on 6 vias per pad |
| GND return | Solid zones on F.Cu and B.Cu around J1 pins 4–6 with 15 stitching vias; F.Cu zone over the fan connector strip with 4 vias per channel | Inner ground planes keep their thermal-relief setting, so the outer zones carry the solid pin connections |
| +5V_SYS | In2.Cu zone: U115 output capacitors → U112/U113/U114 inputs → 3.1–3.6 mm corridor north of the SoC → U110/U111 inputs → accessory header J15 pins 1/2 | 2 in-pad vias per regulator input capacitor, 4 at the U115 output |
| Q1 gate | 0.25 mm F.Cu track to D2 and R270 | |

All new zones use solid pad connections. The supervisors' 5 V pins, their bypass capacitors and the SEQ pull-ups are still open; they are small loads for the signal pass.

Two tool behaviours to keep in mind when adding vias through the KiCad interface: a via that touches only zone copper has its net re-derived from that copper on commit (the ground planes win), so non-ground stitching vias must sit in a same-net pad or be tied to one with a track; and a new zone's pad-connection style has to be set in its copper settings or it inherits thermal relief.

Sizing check (IPC-2221, outer 35 µm): the 12.9 mm B.Cu fan bus alone carries 12 A at under 10 °C rise; the 14 source vias see 1 A each.

## SoC rails — 2026-11-10

Regulator outputs to the SoC. DRC stays at the 67 standing findings; unconnected items 450 → 414. Each rail's only remaining open item is its supervisor sense resistor (R210, R212, R214, R216), left for the signal pass.

| Rail | How it is routed |
|---|---|
| +3V3 | General plane on In2.Cu, lowest priority, with in-pad vias at U114's output capacitors and at every SoC 3.3 V bypass capacitor. Through-hole 3.3 V pins connect directly. |
| +0V9_CORE | In2.Cu island: a plate under the SoC inside the bypass-capacitor ring, fed from U110 across the unused north-west corner, with a finger out to each core capacitor's in-pad via (9 pins, 2 bulk capacitors). |
| +1V35_DDR | In2.Cu strip south of the SoC from U112. The first-row DDR capacitors sit directly above their own ground vias, so two 0.28 mm In2 links pass through the ground-via lanes to reach them. |
| +0V9_CPU | Outer layers only: 0.6 mm F.Cu from U111's output round the 10 µF ground pad, then two B.Cu links (0.28 mm through the ground-via lane and a 0.5 mm loop west of C239) to the 100 nF at pin 115. C261 was turned 180° so its rail pad faces the 10 µF. |
| +1V8 | In3.Cu tracks (0.2–0.3 mm): U113 → FB201 and C258/pin 70 → under the SoC between the ground-pad vias and the pin-row vias → pin 53 (under-chip via) → pin 31 → west trunk to pin 1, R223, R238 and accessory header pin 26. |

Things the next pass must respect:

- The In2 core plate, In3 1.8 V lane (y ≈ 92.3–92.7 under the SoC) and the two B.Cu CPU links occupy space that signal escapes would otherwise use.
- Pin 43's 3.3 V via sits at the north end of C249's pad; FSPI_D1 and FSPI_D2 on B.Cu were given 0.17 mm jogs around it (about 0.14 mm longer each).
- C257 (pin 53) and the other first-row south capacitors have no room for more vias: the flash CS track and the ground vias fill the lanes.
- The 3.3 V plane, like the ground planes, runs under the RJ45 jack with only normal clearance to the shield pins. If chassis isolation distance matters, all three planes need a keep-out there.

## USB, Ethernet, SD card and flash — 2026-11-10

Routed and length-checked against the RV1106 hardware guide (`build/MujinaControl-S19/reference/guide.txt`). DRC is unchanged at the 67 standing findings; unconnected items 414 → 322. Lengths below are measured from the saved board, pad centre to pad centre, including via barrels (1.5034 mm F.Cu–B.Cu, 0.8137 mm F.Cu–In3.Cu); they are board copper only, not package delay.

| Interface | Guide limit | Result |
|---|---|---|
| USB 2.0 pair (90 Ω, 0.16/0.2032 mm) | pair skew < 0.762 mm, < 4 vias | DM 41.47 mm, DP 41.44 mm, skew 0.03 mm, no vias (F.Cu only) |
| Ethernet TX pair (100 Ω, 0.127/0.2032 mm) | pair skew < 0.762 mm, < 4 vias | 51.99 mm each, skew 0.004 mm, 2 vias per line |
| Ethernet RX pair | same | 47.59 mm each, skew 0.003 mm, 2 vias per line |
| SD card (50 Ω, 0.16 mm) | CMD/D0–D3 within 3.05 mm of CLK | CLK 61.76 mm; CMD +0.76, D0 −0.82, D1 −0.68, D2 +0.35, D3 +0.55 mm |
| Flash (50 Ω) | CS/D0–D3 within 7.62 mm of CLK | CLK 21.44 mm; CS −1.10, D0 −3.95, D1 −2.79, D2 −4.34, D3 −4.04 mm |

This table replaces the flash lengths under "Flash checks" above: D0 measured 11.01 mm on the board (10.4 mm short of the clock, outside the limit) and now has one folded return loop on F.Cu between the D3 and D0 diagonals.

How each is routed:

- **USB.** Pins 26/27 leave west between C262 and C248, turn coupled to R253/R252, then run as a pair on F.Cu to J2. DM lands on B7 and loops under the connector to A7; DP lands on A6 and reaches B6 through U140's pad. U141 sits on the DM line 3.7 mm from the connector. CC resistors, VBUS (F.Cu to the detect divider, B.Cu link between the two VBUS pads), VBUS detect (under-chip via, B.Cu) and the USB 1.8 V pin filter are routed.
- **Ethernet.** All four lines drop to B.Cu on vias under the SoC's north-east corner, run south under the SoC east of the ground-pad vias, leave through the south-east corner between the C250 and C235 vias, continue south at x ≈ 118.3–119.6 and turn west to in-pad vias at R242–R245. From there F.Cu through D201/D202 to the jack pins. The pin-field offset between the two rows of the jack is absorbed in where each line turns, so no meanders were needed. Centre taps go to C278/C279 on B.Cu. ETH_BIAS (under-chip via, B.Cu to R246), the 3.3 V and 1.8 V PHY filters and the jack shield (both tabs and pin 8 to C280/R247) are routed.
- **SD card.** The clock stays on F.Cu with no vias: pin 15 → between C247 and C267 → R235 → west along y = 87.0, clear of the 32 kHz crystal → down to socket pad 5 between C270's pads. CMD and D0–D3 use under-chip vias and run as one B.Cu group (0.16 mm, 0.27–0.32 mm gaps) south under the SoC, out under its south-west corner, then to vias beside the socket pads. Leaving southward is what puts them in the socket's pad order without crossings. Card detect leaves west on B.Cu and crosses the group on F.Cu to R234 and the switch pad.
- **Flash.** Unchanged except the D0 loop.

Changes to earlier copper and placement made for these routes:

- Removed the 0.5 mm B.Cu 3.3 V link from C223 to R226 (it crossed the Ethernet corridor). The flash and R226 take 3.3 V from the In2 plane through their existing vias; 3.3 V connectivity is unchanged in DRC.
- SoC ground pins 37 and 57 now tie to the centre pad on F.Cu instead of their own vias, which opens B.Cu under the SoC for the SD and Ethernet groups.
- C267 turned 180° (RTC supply pad now west, next to R224), which frees the gap between C247 and C267 for the SD clock. The VBUS-detect via moved 0.33 mm toward the pins.
- Small parts re-seated at the connectors: U140, U141, R250, R251 (USB); R242–R245, D201, D202, C278, C279 (Ethernet); R229–R234, C270, C271 (SD socket, pull-ups now in line with their pads). No connector, the SoC or any regulator moved. Reference labels for U140, D201, D202 and J100 were moved clear of pads.

Still open on these interfaces: the two Ethernet LED lines (pins 85/86 to R248/R249 and the jack), left for the general signal pass. The SD supply relies on the In2 3.3 V plane.

Evidence: `build/MujinaControl-S19/routing-hs/` (`usb.py`, `eth0.py`, `eth1.py`, `sd0.py`, `sd1.py`, `sd2.py`, `chassis.py`, `fl.py`, `measure.py`), DRC report `build/MujinaControl-S19/routing-power/drc-h11.json`, pre-change copy listed in `routing-hs/backup.txt`.

## Plane drops and local nets — 2026-11-11

DRC unchanged at the 67 standing findings; unconnected items 322 → 71. 1156 tracks, 488 vias.

- **Plane drops.** Every open ground, 3.3 V and 5 V pad that takes a 0.45 mm via has one in the pad; the rest have a via beside them on a short stub (105 vias). Ground and 3.3 V vias for the fan front-end parts pass through the 12 V fan bus on In2/B.Cu.
- **Local nets** (everything that does not start at a processor pin): hashboard connector pull-ups, plug-detect, UART series resistors and the three switched 3.3 V outputs (0.4 mm); fan tach/PWM front ends and gate drives; PSU connector parts; supervisor sense dividers and most of the sequencing chain; accessory header local parts; debug header; status LED; buttons; both crystals' load capacitors. 0.15 mm tracks, 0.2 mm clearance, 35 vias.
- These were laid with a rule-aware grid search (`build/MujinaControl-S19/routing-rest/rt.py`, `run.py`, `power.py`) against the saved board's pads, tracks, vias and zones, then checked with DRC.

Still open (71 connections):

- 57 processor signal pins to their connectors: hashboard UART/reset/plug/enable, fan PWM/tach, PSU I²C/enable, accessory GPIO, debug UART, Ethernet LEDs, status LED, reset, boot strap and both crystals.
- 4 sequencing links at the TPS62933 pins (U112/U113/U114 to U122/U123/U121), the reset button, the boot button, R211 ground, and seven 3.3 V items (three are islands of the In2 plane).

What the processor fan-out needs (found while trialling it; nothing from the trial is on the board, a copy is in `routing-rest/trial-with-escapes.kicad_pcb`):

- East, north and west sides: 31 of 39 pins escape with at most one via. The fan pins 89–95 need the gap between C263 and C252 widened by about 0.3 mm each side so all seven leave on F.Cu.
- South side: accessory pins 38, 40 and 58–63 have no legal escape. The bypass capacitors close the outboard side (0.53 mm gaps), and under the chip the SD group (x 107.7–109.4) and the Ethernet pairs' diagonal occupy B.Cu where their vias would go. HB_SCL/HB_SDA (pins 45/46) fit between C249 and C243 only if C249's ground tie is moved.
- The pad model used for the search treats the TPS62933 pads as unrotated, which is why the four sequencing links at those pins were not attempted.

## Ethernet re-lay — 2026-11-11

Done to free the under-chip lanes at the processor's south-east corner for the accessory and east-side pins. DRC unchanged at 67 standing findings; unconnected items unchanged at 71. 1178 tracks, 486 vias.

- Both pairs now drop on four vias in the north-east corner, leave **east** on B.Cu between C263 and C252 (y 83.9–85.25), run south outside the bypass ring at x 121.25–122.55, and rejoin the previous path at y ≈ 99.5 (x 118.3–119.6). The section under the processor's east strip and the diagonal across its south-east corner are gone.
- Measured from the saved board: TX 56.68 mm each, skew 0.003 mm; RX 52.22 mm, skew 0.009 mm; 2 vias per line. RX_N carries two 0.45 mm outward bumps at y 89–93 and the TX_N jack-side track was re-laid 0.26 mm lower to hold the match.
- ETH_BIAS via moved 0.4 mm west. The ground vias in C273.2 and C230.2 sat in the new path; those pads now tie on F.Cu to C235's ground pad and via.

Unused processor pins checked for the accessory header: only 117–128 and 22 are free, and they are input-only (GPI3_B0–C3, GPI4_C1), so none replaces the blocked accessory GPIO.

Fan-out status after this change (trial only, nothing written): 38 of 48 processor pins on the four sides reach a breakout line with at most one via. Still without a legal escape: pins 38 and 40 (ACC_GPIO4_A7/A5, under the SD group), and in the trial order 46, 58, 60, 72, 73, 75, 89, 90, 114 and 9, which need hand placement rather than more lanes. The recurring obstacle on the west side is the In3 1.8 V trunk at x = 103.3 (y 84.6–95.8): it closes In3 to everything leaving west, which pushes SD, VBUS detect, boot strap and the accessory lines onto the same few B.Cu lanes.

## Board fully routed — 2026-11-11

**0 unconnected items.** DRC (all severities, with schematic parity) shows exactly the 67 findings that existed before routing started (2 J2 locating-hole clearances and J1's open courtyard inside library footprints, 43 silkscreen overlaps, 16 silk-to-edge, 2 silk-over-copper, 3 library mismatches) and the one Q1 metadata parity note. 2406 tracks, 644 vias (all 0.45 mm / 0.30 mm), 36 zones. Minimum track 0.127 mm (processor pin escapes and the Ethernet pairs only).

This section supersedes the "still open" lists in the sections above.

### Matched interfaces (measured from the saved board, pad centre to pad centre, via barrels included)

| Interface | Guide limit | Result |
|---|---|---|
| USB 2.0 pair | skew < 0.762 mm | DM 41.47 / DP 41.44 mm, skew 0.03 mm, no vias |
| Ethernet TX | skew < 0.762 mm | 56.68 mm each, skew 0.003 mm, 2 vias per line |
| Ethernet RX | skew < 0.762 mm | 52.22 mm, skew 0.009 mm, 2 vias per line |
| SD card | CMD/D0–D3 within 3.05 mm of CLK | CLK 60.85 mm; CMD +0.66, D0 −0.66, D1 −0.34, D2 −0.11, D3 +0.49 mm |
| Flash | CS/D0–D3 within 7.62 mm of CLK | CLK 21.44 mm; CS −1.10, D0 −3.95, D1 −2.79, D2 −4.34, D3 −4.04 mm |

### What changed to make the processor fan-out possible

- **In3.Cu now carries signals** (547 segments), as agreed. Both 1.8 V trunks that were on In3 are now narrow strips on In2 (`1V8 west In2.Cu`, `1V8 east In2.Cu a/b/c`, 0.5–0.6 mm, priority 8) cut into the 3.3 V plane. The 3.3 V plane piece that the east strip cuts off around pin 81's capacitor is tied back with a 0.25 mm B.Cu link (C251 via to C252 via).
- **SD data group** leaves the processor westward under the pins (B.Cu), then south-west to the socket; the clock is still top-layer only. Matching re-measured above.
- **Ethernet pairs** leave east on B.Cu (see "Ethernet re-lay").
- **Processor escapes.** West and south-east corner pins were placed by hand; east and north pins by a rule-aware search pin by pin. Under-chip vias pass through the In2 core plate. HB_SCL/HB_SDA (pins 45/46) go inward to vias under the south strip and north on B.Cu between the centre-pad via columns; the flash CS via moved 0.14 mm east to let them through (flash lengths unchanged).
- **Parts nudged** (pad nets unchanged): C305 +0.9 mm x; C263 −0.3 mm y; C245 and C250 swapped positions; C232 −0.13 mm x; R237 +0.1 mm x; C267 turned 180° (earlier). Ground vias for SoC pins 37 and 57, C234.2, C273.2 and C230.2 were replaced by short top-layer ties to a neighbouring ground pad or the centre pad.
- **Fan front-end 3.3 V.** The 3.3 V pads of R263/R265/R267/R269 and D230–D233 sit over the 12 V fan bus, where In2 has no 3.3 V plane. They are chained with 0.3 mm tracks (F.Cu/In3.Cu) to the plane vias at (110.4, 52.85) and (149.25, 52.2). Load is pull-ups and clamp diodes only.

### How the long runs were laid, and what that means

Everything from the processor escapes to the connectors was laid with a grid search (`build/MujinaControl-S19/routing-fan/run2.py`, 0.05 mm grid, 45° moves, 0.2 mm clearance, DRC as the judge), committed in small groups with hand-chosen order and corridors, and re-checked after each group. Unused stub ends were trimmed afterwards. The result is rule-clean and connected, but it is not tidy hand routing:

- **Via counts on slow nets are higher than a hand layout would use:** HB0_PWR_EN and HB1_PWR_EN 9 each, HB2_RX 8, SEQ_MID 7, HB0_TX/HB1_RX/HB2_TX/ACC_GPIO0_A1 6, STATUS_LED/HB2_PWR_EN/FAN4_PWM/boot-button net/HB0_PLUG 5. These are 115200-baud UART, I²C, GPIO and LED lines, so this is a neatness issue, not a timing one.
- **Long runs:** the hashboard-0 and hashboard-1 lines start on the processor's east side and go round the north to the west connectors: HB0_RX 117 mm, HB0_TX 112 mm, HB0/HB1_PWR_EN about 102 mm.
- **Sequencing nets cross a regulator pour.** SEQ_MID and SEQ_IO run diagonally on F.Cu across U113's local ground pour (about x 132–140, y 81–88) to reach the EN pins. Ground stays connected, but those two tracks split the pour and would be better on In3 with a short top-layer stub at each pin. No other signal crosses a regulator pour on the top layer.
- No impedance or crosstalk analysis was done on the long parallel sections.

Evidence: `build/MujinaControl-S19/routing-fan/` (step scripts, per-group DRC reports `routing-power/drc-g*.json`, `drc-h*.json`, `drc-p*.json`, `drc-q3.json` final; milestone board copies `milestone-*.kicad_pcb`), pre-change backups listed in `routing-rest/backup.txt` and `routing-rest/backup-fanout.txt`.

## Track clean-up and review — 2026-11-11

Every track was reviewed and tidied after routing. 0 unconnected items; DRC shows exactly the 67 pre-routing findings. 1927 tracks (was 2406), 617 vias (was 644), all 0.45/0.30 mm. Via counts and lengths in the previous section are superseded by the figures here.

What was done (signal nets other than the length-matched buses, unless noted):

- **Jogs straightened.** Each run between fixed points (pads, vias, junctions, width changes) was re-fitted with the fewest 45° segments that keep full clearance. Segments under 0.15 mm: 145 → about 25 (the rest are inside the processor outline or the matched buses).
- **Duplicate copper merged.** 51 segments laid on top of themselves and 29 unmerged straight joins were merged, without changing the copper outline. Vertices at pad and via centres were kept.
- **Corners.** Right-angle corners chamfered where there was room, power links included: 31 → 15 left (the rest have no room for a chamfer or sit at junctions). 18 pad-to-via power stubs that were at arbitrary angles re-laid at 45°; five pad entries straightened by hand.
- **Vias.** 6 avoidable layer hops removed, one via that connected nothing removed, 14 track pieces hidden inside via pads removed.
- **Net-by-net optimisation.** The 60 nets with the most wasted length or vias were re-routed one at a time on the settled board; a new route was kept only when length + 4 mm per via improved, otherwise the original was restored exactly. 21 nets improved (for example HB1_PWR_EN 100.9 mm/8 vias → 63.6 mm/4; HB0_3V3, HB1_3V3, USB_VBUS and FAN3_TACH now have no vias; FAN3_PWM_PIN 29.3 → 8.6 mm). Signal copper is now 1.16× the shortest possible tree (was 1.19×) with 167 signal vias (was 189).
- **Dead copper removed:** a redundant HB2_3V3 spur lying on its own trunk, a dead HB1_PWR_EN branch, several leftover escape stubs.

SD clock re-matched: the board had been edited outside this work between the "fully routed" save and this clean-up (SD_CLK, the five ACC1V8 top-layer lanes, HB1_RST_N, ACC_I2C4_SCL, ACC_GPIO0_A2/A3 and HB1_TX were re-laid as longer diagonals). That shortened SD_CLK by 7.14 mm and put the data lines 6.5–7.8 mm longer than the clock (limit 3.05 mm). The clock's old path is now occupied by the re-laid ACC1V8 lanes, so the clock got one chamfered compensation loop beside its diagonal (around x 80–85, y 102–107, 0.32 mm or more from other copper). Measured now: CLK 60.85 mm; CMD +0.66, D0 −0.66, D1 −0.34, D2 −0.11, D3 +0.49 mm. USB, Ethernet and flash figures are unchanged from the table above.

What remains, and why:

- About 30 short side-steps (0.05–0.28 mm) outside the processor. Those checked are where a track holds 0.2 mm from a pad or joins one of the tightly packed processor lanes; removing them needs the neighbouring pad or lane to move.
- 12 right-angle corners with no room for a chamfer.
- The long east-side hashboard lines are unchanged: HB0_RX 117 mm/4 vias, HB0_TX 111 mm/6, HB1_RX 91 mm/6, HB2_RX 83 mm/8, HB2_TX 73 mm/6, HB0_PWR_EN 90 mm/9, HB2_PWR_EN 84 mm/5. Re-routing them individually did not help; their length comes from the pins sitting on the processor's east side while the connectors are to the north-west. Shortening them needs a pin reassignment in the schematic, not routing.
- SEQ_MID and SEQ_IO still cross U113's ground pour on the top layer (see previous section).

Tools and evidence: `build/MujinaControl-S19/cleanup/` (`review.py` read-only review, `clean.py`, `dedupe.py`, `viahop.py`, `offangle.py`, `optnet.py`, `score.py`; milestone boards `milestone-*.kicad_pcb`; `opt1.log`), final DRC `routing-power/drc-s8.json`, pre-clean-up copy listed in `cleanup/backup.txt`.

## Regulator ground pours and ground stitching — 2026-11-12

0 unconnected items; DRC shows exactly the 67 pre-routing findings. 1925 tracks, 774 vias (414 on ground), all 0.45/0.30 mm. Matched buses re-measured and unchanged.

### What was wrong

- **Signals split four of the six regulator pours.** SEQ_MID ran 10.6 mm diagonally across U113's pour and 4.6 mm across U112's; SEQ_IO crossed U114 (4.8 mm), U115 (6.6 mm) and clipped U113 and U112; the core-rail sense line to supervisor resistor R210 ran 6 mm across U110's pour. U110's pour was in 2 pieces, U112's in 3, U113's in 4, U115's in 2.
- **No stitching in the pours.** Each pour had exactly one via per ground pad (8, or 10 for U115) and none in the open copper.
- **Sparse ground vias on the rest of the board.** 261 ground vias plus 56 through-hole ground pins, but only 43 % of the board was within 3 mm of one and 66 % within 5 mm; the worst spot was 21 mm away.

### What changed

- **Sequencing nets re-laid.** SEQ_MID and SEQ_IO now reach each enable pin (U112.2, U113.2, U114.2) by a 2.5–2.7 mm top-layer stub to a via beside the IC and run on In3.Cu/B.Cu outside the pours. SEQ_MID 84 mm/7 vias → 94 mm/9 vias; SEQ_IO 59 mm/4 vias → 57 mm/5 vias. These are slow enable signals.
- **Core sense line.** R210.1 now has an in-pad via and reaches the +0V9_CORE output via on In3.Cu (7.3 mm), off the pour.
- **Pours.** U110, U111, U114 and U115 are now one piece each. U112 (2 pieces) and U113 (3 pieces, two of them under 6 mm²) are divided only by their own input, output and feedback copper. What still runs on the top layer inside each pour is the regulator's own circuit, the rail it produces, its 5 V (or 12 V) input and the enable stub.
- **Pour stitching: +86 ground vias** (13–16 per regulator, now 21–26 each), placed in the open pour copper nearest the ground pads first, at least 1.5 mm apart, never under an inductor or IC, 0.45 mm or more from any pad edge and clear of copper on every layer.
- **Board stitching: +67 ground vias**, placed one at a time at the free spot farthest from any ground via until no free spot was more than 6 mm from one. Coverage is now 61 % of the board within 3 mm and 94 % within 5 mm; the farthest point is 9.5 mm (inside areas where no via may go).

Stitching vias avoid: other-net copper on all layers, all pads and footprint outlines, the processor outline, the RJ45 keep-out, the 12 V and narrow power-layer zones (5 V corridor, core, DDR and 1.8 V strips), the board edge and its cut-outs, and anything within 0.6 mm of the length-matched tracks. They do pass through the 3.3 V plane and the wide east block of the 5 V zone, where each makes a 0.95 mm clearance hole.

### Why stitching matters here

In1.Cu and In4.Cu are both ground. Signals on F.Cu return on In1; signals on In3.Cu and B.Cu return on In4. Wherever a signal changes layer its return current has to move between the two planes through the nearest ground via, and after the fan-out about 160 signal vias do this. The 6 mm target is roughly a twentieth of a wavelength at 1 GHz in FR-4. In the regulator pours the vias give the switching return current a short path into the planes and carry heat out of the top copper.

### Left as is

- HB0_RST_N runs along the east boundary of U111's pour (x = 116.0, between the pour and U121's pads). It does not cross the pour; there is 0.5 mm between the pour edge and the pads, so it cannot move without moving U121.
- U115's enable divider net (R284/R285 to pin 2, 8.8 mm) is the regulator's own circuit and does not split the pour.
- No outer-layer ground fill was added outside the regulator and connector zones; the stitching ties the two inner ground planes only.

Evidence: `build/MujinaControl-S19/regs/` (`survey.py`, `seq1.py`, `routenet.py`, `stitch.py`, `stitch-plan.json`, `orig-nets.json`, `milestone-stitched.kicad_pcb`), final DRC `routing-power/drc-g5.json`, pre-change copy listed in `regs/backup.txt`.
