# USB-A host port, USB switch, JTAG header and J15 not fitted — 2026-11-12

## What was added

- **USB-A host port J17** for a WiFi dongle, on the front edge between the Ethernet jack and the RESET button. Its front face is flush with the Ethernet jack's (4.2 mm past the board edge).
- **USB 2.0 switch U142** (FSUSB42MUX). The RV1106G2 has one USB port; U142 connects it to USB-C (J2) or USB-A (J17), never both.
  - Select = `USB_VBUS_DET`: a host plugged into USB-C puts about 3 V on the select pin and the switch goes to USB-C, so device mode and Maskrom recovery work with no firmware. With nothing on USB-C the port goes to USB-A.
  - Firmware still has to set the controller role: host for USB-A, device while `USB_VBUS_DET` is high.
- **Port power U143** (TPS2051CDBVR): 5 V to J17, rated 0.5 A, current limit 0.67 to 1.01 A. `USBA_PWR_EN` (GPIO0_A3) has a 4.7 k pull-up, so the port is on by default; firmware can drive it low to power-cycle a dongle. A dongle can take up to 0.5 A of the 5 V / 2 A system budget.
- **JTAG header J18** (1x5, 2.54 mm, not fitted), between the microSD socket and USB-C: 1 = 3.3 V reference, 2 = TMS (`SD_D3`), 3 = TCK (`SD_D2`), 4 = `RESET_N`, 5 = GND. The RV1106G2's two-wire CPU JTAG is an alternate function of the SD_D2 / SD_D3 pins (JTAG_CPU_TCK_M0 / TMS_M0), so it is used with no card in the socket. The same function also exists on the J16 console pins (M1), where it would take the console away.
- **J15 accessory header** is marked not fitted (no placement, not in the BOM); users solder it in if they need it. Pin 17 is no longer connected: GPIO0_A3 became `USBA_PWR_EN`.
- RESET and BOOT buttons moved east to make room: SW1 x 134.0 -> 144.75, SW2 x 145.0 -> 153.95 (pitch 11.0 -> 9.2 mm). The front panel openings change accordingly.

## Parts

| Ref | Part | Fab part | Category | Stock 2026-11-12 |
|---|---|---|---|---|
| U142 | FSUSB42MUX, MSOP-10 | C11355 | extended | 30,460 |
| U143 | TPS2051CDBVR, SOT-23-5 | C129581 | extended | 15,235 |
| J17 | USB-A socket, right angle, through hole (AF 90 WJDG) | C456018 | extended | 82,413 |
| U144, U145 | TPD1E05U06DYA ESD on the USB-A data lines | C3702980 | extended, already used | 11,727 |
| C313 | 10 uF 0805 at the switch input | C15850 | basic | |
| C314, C315 | 22 uF 0805 on the port's 5 V | C45783 | basic | |
| C312, C316 | 100 nF 0402 | C1525 | basic | |
| R302 | 4.7 k enable pull-up | C25900 | basic | |
| J18 | 1x5 header 61300511121, not fitted | C6461551 | extended | 1,116 |

Three new extended lines (U142, U143, J17); J15's header line leaves the fitted BOM. The BOM now has 67 part numbers: 24 basic, 9 preferred, 34 extended. Of 297 fitted placements 212 are basic, 20 preferred, 65 extended.

The J17 footprint is the standard through-hole USB-A pattern (four 0.92 mm pins over 7.0 mm, two 2.3 mm shell holes 13.14 mm apart, 2.71 mm in front of the pins), checked against the part's drawing.

## Schematic

- New sheet `10_usb_host.kicad_sch` (page 11): switch, port power, socket, ESD. The 2.2 ohm series resistors R252 / R253 moved here from the Ethernet / USB sheet and stay at the processor.
- `06_network_usb.kicad_sch`: the USB-C data lines now end at `USBC_DP` / `USBC_DM`.
- `05_boot.kicad_sch`: J18. `09_power_service.kicad_sch`: J15 not fitted, pin 17 not connected. `01_soc.kicad_sch`: GPIO0_A3 is `USBA_PWR_EN`.
- Project libraries gained the symbols and footprints used (`lib/Interface_USB.kicad_sym`, `lib/Package_SO.pretty`, `lib/Connector_USB.pretty` and additions to four existing libraries), with 3D models under `3d/kicad/`.
- ERC 0. Readability checker 0 errors.

## Board

- U142 sits in line on the old USB lane at (95.7, 112.5). The SoC-side pair and the USB-C pair re-use the previous lane; the USB-A pair drops to B.Cu at the switch, runs east north of the Ethernet jack (clear of the jack's plane cut-out), and comes down to J17's pins. Same geometry as before on both outer layers: 0.16 mm tracks, 0.204 mm gap.
- Measured lengths, processor pin to connector: USB-C 38.79 / 38.87 mm (skew 0.08 mm, no vias); USB-A 80.94 / 80.96 mm (skew 0.02 mm, one via per line plus the socket pin). D+ on the USB-A pair has three small bumps near the switch to make up 0.89 mm.
- Ethernet, SD and flash lengths are unchanged (SD_D2 / SD_D3 each gained a branch to J18: 12.5 mm and 19 mm).
- 5 V for the port comes from the existing 5 V via beside U124 on a 0.3 mm bottom-layer track into C313; the port's 5 V runs 0.5 mm wide on top to the bulk capacitors and J17 pin 1.
- The Ethernet speed LED resistor R249 moved north of the new USB pair to (126.2, 109.6); its bottom-layer run now stops there and the jack side continues on top between the jack and J17.
- A design rule was added for U142's 0.5 mm pad pitch (0.127 mm clearance inside its courtyard, top layer only), like the processor's.
- The new parts' reference designators are hidden on silkscreen like the rest; J17's outline is trimmed at the board edge (board and library copy).
- 323 footprints, 2021 tracks, 794 vias. DRC with schematic parity: 0 violations, 0 unconnected, 0 parity issues.

## Still to do or decide

- Front panel: new opening for USB-A and the shifted buttons.
- Firmware: USB role switching from `USB_VBUS_DET`, the WiFi driver, `USBA_PWR_EN`, and the pin mux for JTAG.
- A dongle inside a metal enclosure needs its antenna outside to be useful.
- U142's select pin is fed through 12.4 k when USB-C is plugged into an unpowered board (under 0.3 mA into its input clamp).

Evidence: `build/MujinaControl-S19/usba/` (`prep.py`, `sch_build.py`, `sch_j18.py`, `sch_fix1.py`, `sch_clean.py`, `sync.py`, `rip.py`, `route_usb.py`, `route_pwr.py`, `route_en.py`, `route_d3.py`, datasheets in `ds/`, `backup.txt`), DRC `build/MujinaControl-S19/routing-power/drc-u12.json`, lengths from `routing-hs/measure.py`.
