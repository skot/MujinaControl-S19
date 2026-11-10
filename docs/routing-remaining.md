# Remaining-net routing milestone — 2026-11-10

Saved through native KiCad IPC to the canonical `MujinaControl-S19.kicad_pcb`. This pass reduced unrouted connections from **238 to 116** (122 completed). Filled-zone DRC went from **83 to 81 other findings**, with no new findings by type and affected item IDs. The existing Q1 `ki_fp_filters` metadata parity warning remains. Routing is still incomplete.

Completed work includes the local fan PWM/tach protection and gate circuits, all nine hashboard address-divider networks, all five supervisor sense-divider networks, local auxiliary/testpoint and boot-divider connections, both crystal signal circuits, and 33 ground groups. Additional routes complete the reset/button connections, HB2_TX, HB1_RST_N, FAN2_PWM and FAN3_PWM, plus portions of sequencing and tachometer networks. Some fan and hashboard connections to the SoC remain open; local completion does not mean every interface is complete.

The 24 MHz feedback resistor R237 was moved close to the SoC clock pins. C236/C258 moved by 0.84 mm and C235 by 0.30 mm to open the output escape; R224 moved by 0.20 mm to clear the RTC input route. Exactly these five footprints moved. All 276 other footprints, including the connectors, SoC, crystals and six regulator groups, stayed at their original positions and rotations. Values, library identities, pad nets, attributes and 3D models were preserved. The schematic sheets, project settings and routing rules are byte-for-byte unchanged.

All 488 vias use 0.45 mm copper diameter and 0.30 mm drill. No pre-existing copper was changed except six obsolete clock/nearby-ground segments that were replaced for the local clock layout. All 470 existing USB, Ethernet and SD copper objects are unchanged. A projection comparison of the filled ground planes found no new reference-plane gaps beneath those routes; new tracks outside the SoC courtyard maintain at least 0.50 mm edge separation from USB data and 0.32 mm from Ethernet/SD data. These checks preserve the earlier routing milestone, not a complete signal-integrity qualification.

The six converters and clock connections passed 126 native connectivity checks. Top, bottom, In2 and In3 whole-board views and local SoC, clock, fan, hashboard and supervisor views were inspected. Existing silkscreen and library/clearance findings remain for a later cleanup pass.

## Remaining connections

| Circuit | Unrouted connections |
|---|---:|
| 3.3 V | 43 |
| 0.9 V core | 15 |
| 5 V system | 14 |
| 1.8 V | 7 |
| 1.35 V DDR | 7 |
| 0.9 V CPU | 4 |
| RTC supply and ground | 3 |
| Sequencing | 4 |
| Flash bus | 5 |
| Other controls and analog support | 14 |
| **Total** | **116** |

The flash CS and D2 pull-up branches are connected. Preliminary longer flash routes were discarded; five main bus connections remain open. Finish this bus as a coordinated group with a continuous reference plane, appropriate impedance and the Rockchip clock-relative skew limit of 7.62 mm. The existing D0/D3 routes are preserved. Power distribution still needs wide trunks/pours and suitable via arrays; the small signal widths used in this pass are not a substitute for current-capable power routing.

Evidence is under `build/MujinaControl-S19/routing-remaining/` at the workspace root: `before-drc.json`, `final-drc.json`, `verification.json`, `fast-bus-proximity.json`, `reference-changes.json`, native route logs and rendered PNG/SVG views. The pre-edit backup is recorded in that directory's `backup.txt`. Board dimensions remain 110 × 100 mm and minimum plated drill 0.30 mm. This milestone is not a manufacturing release.
