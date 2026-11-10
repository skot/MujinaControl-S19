# USB and Ethernet routing — 2026-11-07

Saved to the canonical `MujinaControl-S19.kicad_pcb` through native KiCad IPC. USB data is connected from U100 through R252/R253 and U140/U141 to both Type-C orientations. Ethernet TX/RX is connected through R242–R245 and D201/D202 to J100. USB CC, VBUS sensing, USB PHY supply, Ethernet PHY supply beads and decoupling, bias, transformer center taps, LED resistor outputs and chassis connections are routed. Ground escapes and nine transition-stitching vias are placed; their reference-plane connections remain unfinished.

The original 22 fixed components remain unchanged. R242–R245, which were placed later, were adjusted to centers (122,84.9), (122,86), (125,84.9), (125,86) mm; R242/R244 face 180°, R243/R245 face 0°. All other 251 footprints are unchanged. Values, pad nets, footprint identities and the ten schematic sheets are preserved. A few existing fan-control tracks, a 3.3 V segment, FSPI_D0 and USB-detect/VCM escapes were rerouted to make room. The 168 existing 12 V and wide ground copper objects, board outline and stackup are unchanged.

The long data-pair trunks run on B.Cu, with short F.Cu fanouts. USB uses 0.160 mm width and Ethernet uses 0.127 mm; both use a 0.2032 mm edge gap. USB has short 0.127 mm connector/SoC necks. All 271 vias retain 0.45/0.30 mm diameter/drill. The `USB_90ohm` and `Ethernet_100ohm` netclasses and assignments were saved through native project serialization and verified after reopening; all twelve data-net sections resolve to the intended class.

Sizing uses the saved six-layer stackup: 0.0994 mm outer-to-reference dielectric, Er 4.1, and the fab calculator's finished 0.04064 mm outer copper, 0.0127 mm etch taper, mask C1/C3 0.0254 mm, C2 0.01524 mm and mask Er 3.8. The [fab's coated differential-microstrip calculator](https://jlcpcb.com/pcb-impedance-calculator), queried on 2026-11-07, returned 89.63 Ω for USB and 99.15 Ω for Ethernet. Requests and responses are recorded in `build/MujinaControl-S19/routing-interfaces/impedance-results.json` at the workspace root. These are nominal trunk calculations, not a field-solver signoff of pads, vias, uncoupled fanouts or tuning sections.

Lengths below are shortest copper-centerline paths through the series-resistor sections, excluding equal resistor-body spans and via-barrel lengths. Each active leg has four layer transitions. The USB ESD branch and duplicate connector contact mean summing every segment on a net would overcount the active path. Ethernet tuning compensates the connector and resistor fanout differences. USB tuning balances the two connector orientations.

| Path | P length (mm) | N length (mm) | Absolute skew (mm) |
|---|---:|---:|---:|
| USB A6/A7 | 43.451 | 42.733 | 0.717 |
| USB B6/B7 | 43.016 | 43.733 | 0.717 |
| Ethernet TX | 57.615 | 57.610 | 0.0054 |
| Ethernet RX | 57.982 | 57.976 | 0.0054 |

The local Rockchip RV1103G/RV1106G Hardware Design Guide V1.1 specifies 90 Ω USB and 100 Ω Ethernet differential targets, ±10%, intrapair mismatch below 30 mil (0.762 mm), and maximum trace length 6 inches. Four transitions are below its six-via maximum, though the guide recommends fewer than four. See `research/rv1106/reference-designs/Raven1106/docs/rv1106/RV1106 Design Guide.pdf` and the extracted guide in the build evidence directory.

Native KiCad 10.99.0-bp.6 DRC reports no unconnected interface data or non-ground support nets, no new copper/clearance violations, and no new footprint-placement violations. The board as a whole remains unfinished: 385 unconnected items and 179 other findings, comprising 120 dangling vias awaiting routing/planes, 40 silkscreen overlaps, 16 silk-to-edge clearances, the two pre-existing J2 pad-to-locating-hole clearances and the existing J16 library mismatch. Top/bottom whole-board renders and SoC, connector and pair zooms were inspected. Evidence is under `build/MujinaControl-S19/routing-interfaces/` at the workspace root.

Continuous In1.Cu/In4.Cu ground reference planes are still required. They must cover the complete data paths and join the return vias before impedance/return-path acceptance. Keep future routing and pours clear of the Ethernet isolated/chassis region as appropriate to the magnetics. Recheck pair spacing, skew, reference continuity and filled-zone DRC after the remaining routing and pours. This is a routing milestone, not a fabrication release; the earlier power-stage thermal/current concern remains recorded in `routing-12v.md`.
