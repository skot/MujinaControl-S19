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
