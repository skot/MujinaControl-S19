# On-board WiFi (AP6212) — branch `onboard-wifi`

2026-11-12. An AMPAK AP6212 2.4 GHz 802.11 b/g/n module (BCM43438 inside, fab part C2798300) sits in the south-east corner where the badger logo was, wired to the RV1106G2 over 4-bit SDIO. This is the alternative to the USB-A dongle port on branch `usb-a-wifi`; the two branches both start from `main`.

## Circuit (sheet 11, `10_wifi.kicad_sch`)

| Function | Module pin | Net | SoC contact |
| --- | ---: | --- | ---: |
| SDIO clock | 17 | WIFI_SDIO_CLK_SOC → R310 22 Ω → module | 93 (SDMMC1_CLK_M1) |
| SDIO command | 16 | WIFI_SDIO_CMD | 92 |
| SDIO data 0–3 | 18, 19, 14, 15 | WIFI_SDIO_D0–D3 | 94, 95, 90, 91 |
| WiFi enable | 12 | WIFI_REG_ON, 4.7k pull-down R311 | 62 (GPIO0_A3) |
| Wake / interrupt | 13 | WIFI_HOST_WAKE | 40 (GPIO4_A5) |
| 32.768 kHz | 24 | WIFI_LPO_32K | 58 (GPIO0_A0 as RTC_CLK_OUT) |

- Supply: VBAT (pin 9) and VDDIO (pin 22) on +3V3, so SDIO runs at 3.3 V. C320 10 µF + C321 100 nF at VBAT, C322 100 nF at VDDIO.
- Internal buck: L211 4.7 µH between pins 21 and 23, C323 4.7 µF on pin 23. The AP6212 datasheet gives no values; 4.7 µH / 4.7 µF is what a published reference schematic for a sibling AMPAK module with the same pin names uses. **Confirm against AMPAK's AP6212 reference design or on the first board.**
- Clock: Y102 26 MHz, ±10 ppm, CL 16 pF, ESR 50 Ω max (the datasheet's crystal requirement), C324 / C325 22 pF.
- Antenna: 50 Ω line to J19, a U.FL receptacle for an external 2.4 GHz antenna. C327 10 pF in series; C326 / C328 are unpopulated matching positions.
- Bluetooth is not connected: BT_RST_N is tied low; the BT UART, PCM and wake pins are open.
- The module's pads 5, 8, 29, 30, 32, 35, 37, 38 and the three test pads are not connected.

## What moved to make room

SDIO only exists on the pins the fans were using, so:

- Fan 2 / 3 / 4 PWM moved to PWM2_M0 / PWM3_M0 / PWM1_M0 (pins 59, 60, 63). Same open-drain BSS138 stages.
- Fan 1 / 2 / 3 tach moved to the 1.8 V pins 2, 3, 4 (GPIO3_C4–C6). Their 10k pull-ups (R263, R265, R267) and the upper clamp diodes (D230–D232 pin 2) now go to +1V8. Fan 4 tach and fan 1 PWM did not move.
- Nine signals left the accessory header, so J15 was reduced from 2×20 to a 2×7 header (see below). It is marked not fitted, as the footprint on `main` already was.
- The badger logo moved to the open area west of the processor (same size, top side).

## Accessory header J15: 2×7

With only eight signals left, the 40-pin header became a 14-pin one (2×7, 2.54 mm), at the top of the old position on the west edge.

| Pin | Net | Pin | Net |
| ---: | --- | ---: | --- |
| 1 | +5V_SYS | 2 | +3V3 |
| 3 | I2C4 SCL (GPIO2_A1, 3.3 V, 4.7k pull-up) | 4 | I2C4 SDA (GPIO2_A0, 3.3 V, 4.7k pull-up) |
| 5 | GPIO4_A7 (3.3 V) | 6 | GND |
| 7 | +1V8 reference | 8 | GND |
| 9 | GPIO3_C7 (1.8 V) | 10 | GPIO3_D0 (1.8 V) |
| 11 | GPIO3_D1 (1.8 V) | 12 | GPIO3_D2 (1.8 V) |
| 13 | GPIO3_D3 (1.8 V) | 14 | GND |

Pins 9–13 are 1.8 V only; pin 7 is a level-shifter reference, not a supply. Pins 9 / 10 can be UART5 TX / RX or I2C4 (M2), pins 11 / 12 UART5 RTS / CTS or I2C3 (M2). No PWM output is left on the header. Part for those who fit it: PZ254V-12-14P (fab part C492424). C305 (the 1.8 V reference capacitor) moved beside pin 7.

## Parts added

| Ref | Part | Fab part | Class | Stock (2026-11-12) |
| --- | --- | --- | --- | ---: |
| U160 | AP6212 | C2798300 | extended | 326 |
| Y102 | XL2EL89CQI-111YLC-26M, 26 MHz 3225 | C19711727 | extended | 9,322 |
| L211 | FTC201610S4R7MBCA, 4.7 µH 2016 | C5832346 | extended | 307,429 |
| J19 | Hirose U.FL-R-SMT-1(80) | C88374 | extended | 319,721 |
| C323 | CL21A475KAQNNNE, 4.7 µF 0805 | C1779 | basic | 2,260,275 |
| C324, C325 | 0402CG220J500NT, 22 pF | C1555 | basic | 1,486,130 |
| C327 | CL05C100JB5NNNC, 10 pF | C32949 | basic | 2,098,509 |
| C320; C321, C322; R310; R311 | 10 µF 0805; 100 nF; 22 Ω; 4.7k | C15850; C1525; C25092; C25900 | basic | already on the board |
| C326, C328 | not fitted | – | – | – |

Four new extended part numbers; the module is the only one with low stock.

## Layout

- Module at (151.5, 112.0), rotated 180°: SDIO pads face north; the antenna pin is on the east side near the south-east corner. Footprint `Mujina:AMPAK_AP6212` is drawn from the datasheet's layout recommendation (0.5 × 1.125 mm lands at 0.9 mm pitch, three test lands); the 3D model is a generated envelope (`3d/generated/`).
- SDIO: top layer from the processor, south-east between existing vias, then east through the gap between the 1.8 V and DDR regulator blocks (R310 in line, 16 mm from the SoC pin), down to the bottom layer east of the regulators, parallel to a via staircase beside the module, and top-layer drops into the pads. Two layer changes per line, always over a ground plane. Lengths 49–60 mm (clock 55 mm).
- Antenna line 0.18 mm wide on the top layer (50 Ω over the 0.1 mm prepreg to In1). It leaves pin 2 on the east side, runs 8 mm down past the module's corner through the matching positions and ends at J19, which sits south of the module, 13 mm from the east edge and clear of the case slots. Ground vias at the matching parts and at both ends of both connector shell pads.
- Three things were moved slightly to clear the SDIO path: C264's ground via, the layer change of FAN1_PWM, and the 5 V via of C227. A short section of the +1V35 sense track was shifted 0.3 mm.
- The fan PWM / tach lines and the three WiFi control lines are slow and were routed with the grid router: they are long (40–77 mm) with up to 8 layer changes. Worth a tidy-up pass before ordering; electrically uncritical.
- A 0.15 mm +1V8 branch feeds the fan 1–3 tach pull-ups and clamps (under 1 mA).

## Checks

ERC 0. DRC with schematic parity: 0 violations, 0 unconnected, 0 parity issues. Schematic readability checker: 0 errors. USB, Ethernet, SD, SPI NAND and clock copper is unchanged (compared segment by segment against the board before this work). 329 footprints (three fiducials added on 2026-11-14), 2199 tracks, 836 vias.

## Open points

1. L211 / C323 values come from a sibling module's reference schematic, not from the AP6212 datasheet: confirm them.
2. Firmware: SDMMC1 in mux M1 at 3.3 V with internal pull-ups, `brcmfmac` with its firmware and NVRAM files, WIFI_REG_ON as the power-sequence GPIO, the RTC clock output (RTC_CLK_OUT) enabled on GPIO0_A0, fan PWM on pwm2m0 / pwm3m0 / pwm1m0, tach 1–3 on GPIO3_C4–C6.
3. An external antenna on J19 is required; there is no on-board antenna.
4. Module stock at the fab: 326 pieces on 2026-11-12, 1,784 on 2026-11-14.
