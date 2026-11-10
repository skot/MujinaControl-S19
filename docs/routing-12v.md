# 12 V routing — four 3 A fan channels

Saved to the canonical MujinaControl-S19 board on 2026-11-07. The user specified 3 A per fan channel: 12 A total fan load. The input copper calculation reserves another 2 A for the controller, giving a conservative 14 A input target. J6/J11, J7/J12, J8/J13 and J9/J14 are alternative connector footprints for four channels; this is not an eight-fan rating.

## Saved connections

All eight +12V_IN pads form one copper-connected group, including the three input pins and all Q1 drain lands. All 18 +12V_FAN pads form one copper-connected group: Q1 source pins, both connector options for every fan channel, D220, C285, D2, and the U115 input/enable and bypass parts. The gate/clamp/pull-down net is connected. Every fan-ground pin is connected to all three input-ground pins.

The latest pass added 102 track segments and 43 through-vias. The board now has 854 segments and 214 vias. Every via remains 0.45 mm diameter / 0.30 mm drill. All 255 footprints and all schematic sheets are unchanged.

- Fan branches and paired connector links: 1.5 mm on outer copper.
- Protected fan bus and source riser: 6.5 mm on B.Cu.
- Upper ground bus: 5.8 mm on F.Cu.
- Input pin bus: 3.0 mm on both outer layers, narrowing to 1.8 mm at the outermost pin to maintain clearance to the return corridor.
- Ground return around the connector: six parallel 1.8 mm tracks, one on every copper layer. They avoid the mounting hole and outline notch; a 16-via bank connects them to the upper ground bus and all three plated input-ground pins connect their far ends.
- Q1 transitions: 15 raw-input vias and 12 protected-output vias. Package-constrained source necks are short 0.45 mm fingers with wider collectors. Drain copper spreads to 2.6–3.0 mm. The existing MOSFET footprint and pin geometry are preserved.
- The earlier local regulator feed, TVS/capacitor connections, gate clamp and pull-down return remain connected.

Netclasses `12V_Input` and `12V_Fan` now provide 3.0 mm and 1.5 mm preferred routing widths respectively; both retain 0.20 mm clearance and 0.45/0.30 mm vias. Broader bus widths are explicit track widths and available in the routing presets. GND retains the ordinary netclass for logic routing; its heavy-current paths use the explicit geometry above. Absolute board constraints and RV1106 custom rules are unchanged.

## Copper sizing basis and limits

Sizing uses the IPC-2221 trace estimate, 35 um outer copper, the selected stackup's 15.2 um inner copper, 40 C ambient, and a 30 C rise budget for this high-current distribution pass. Calculated rises are approximately 8.6 C for a 3 A / 1.5 mm branch, 17.9 C for a 12 A / 6.5 mm fan bus, 25.4 C for the 14 A source riser, 21.6 C for the 12 A / 5.8 mm ground bus, and 18.8 C for each 7 A / 3.0 mm parallel input track. These are preliminary estimates, not a coupled multilayer thermal simulation.

The return corridor has a summed cross-section of 0.2354 mm². With proportional current sharing, each outer layer carries about 3.21 A and each inner layer about 1.39 A; separate-layer estimates are 7.4 C and 21.3 C rises. Actual coupling and current sharing need validation on the completed copper layout.

At a conservative 70 C copper temperature, estimates charging the full 12 A along the entire bus lengths give about 49 mV for a 45 mm supply bus, 63 mV for a 52 mm ground bus, 37 mV for a 35 mm return corridor, and 21 mV for an 18 mm combined 3 A branch path. The copper-loop budget is 250 mV excluding Q1 and connector contact resistance. Actual current in the shared bus segments decreases as fan branches split off.

Via-bank calculations assume a 1.6 mm barrel, 0.30 mm drill and the fab's published 18 um average hole plating. Estimated bank resistances at 70 C are 0.162 mOhm for 12 vias, 0.130 mOhm for 15 vias, and 0.122 mOhm for 16 vias. These values assume approximately even sharing. Terminal necks and the source collectors are short, package-constrained connections; their temperatures cannot be qualified by the long-trace calculation. No separate fan startup/stall profile has been provided.

## Q1 upgrade (supersedes the original limitation)

Q1 has since been replaced by onsemi NTTFS008P03P8Z in a 3.3 × 3.3 mm package, with a verified project footprint and local heat spreaders. See [Q1 upgrade and thermal qualification](q1-upgrade.md) for the 14 A design target, loss calculations and remaining physical validation. The following records the original routing-stage limitation.

### Original Q1 limitation

The original DMP3013SFV must not be considered qualified for four simultaneous 3 A fans plus controller load. Its [manufacturer datasheet](https://www.diodes.com/_files/datasheets/DMP3013SFV.pdf), checked 2026-11-07, specifies 12 A at 25 C ambient and 10 A at 70 C ambient under a 2 oz, one-square-inch thermal test layout. This board uses 1 oz outer copper and a different layout. The 35 A figure is case-temperature controlled and is not an ambient board rating.

At the specified maximum 9.5 mOhm at VGS=-10 V and 25 C, Q1 alone dissipates 1.37 W at 12 A or 1.86 W at the 14 A copper target; resistance increases when hot. The datasheet's 65 C/W test-board thermal resistance is not sufficient evidence for this layout. A lower-loss protection device and suitable footprint/copper, or a validated thermal solution and derating, is needed before release at the requested load. Q1 and the schematic were not changed during this routing task.

## Verification

After canonical saves and reopening, native connectivity checks confirm the two complete 12 V groups, the gate group and all 24 fan-ground-to-input-ground checks. All 255 footprint instances are unchanged after excluding only the transient parent-board UUID generated on reopen. Every via has the requested size. Schematics and custom rules are byte-identical to the pre-pass backup.

Fresh CLI DRC returns exactly the previous 161 findings, with no new violations: 102 dangling vias from unfinished other routing, 40 silk overlaps, 16 silk-edge clearances, two existing J2 hole clearances and one J16 library mismatch. Missing connections decrease from 447 to 422. Two preliminary new input-via drill-clearance findings were fixed by moving that bank to 0.60 mm column pitch. Top and bottom routing renders were visually inspected.

The board and project are saved at their canonical paths and the board is shown in Backplane. Project settings required a native SaveCopyOfDocument export followed by validation and promotion to the backed-up canonical project, because ordinary headless board save did not persist the project settings. Both files were reopened and checked. No CAD text edits were used.

Evidence: `../../../build/MujinaControl-S19/routing-12v-trunks/`, including `verification.json`, `sizing.json`, before/final DRC, native rule readback, renders and `backup.txt`. The board remains incomplete and is not ready for fabrication.
