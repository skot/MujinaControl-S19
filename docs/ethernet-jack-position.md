# Ethernet jack: position and type

2026-11-14. The face of the Ethernet jack J100 (HR911105A at the time, now HR915340A, see the end of this page) is now **2.25 mm** past the bottom board edge. It was 4.195 mm, the position taken over from bitcrane.

## Check

- Bottom board edge: y = 134.245.
- The jack's face is 10.90 mm in front of its two locating posts (datasheet, side view; body length 21.30 mm). In the footprint that is y = +17.26 from pin 1, which the footprint's body outline also shows.
- Before: pin 1 at y = 121.18, face at 138.44, 4.195 mm past the edge.
- Now: pin 1 at (109.775, 119.235), face at 136.495, 2.25 mm past the edge. The jack moved 1.945 mm north; it is still locked.

## What moved with it

| Part | From | To | Why |
|---|---|---|---|
| J100 | (109.775, 121.18) | (109.775, 119.235) | the request |
| C278, C279 (centre-tap capacitors) | (113.6 / 114.855, 114.82) | (114.0 / 115.255, 113.62) | they sat inside the jack's new courtyard; shifted 0.4 mm east to stay clear of R245 |
| C280 (chassis capacitor), R247 | y = 113.8, 111.8 | y = 113.2, 111.2 | C280's courtyard overlapped the jack's new courtyard |

The ESD diodes D201 / D202, the series resistors R242–R245 and both pairs upstream of them did not move.

## Copper

- Both Ethernet pairs keep their shape between the ESD diodes and the jack; each of the four lines is exactly 1.945 mm shorter, so the mismatch inside each pair is unchanged (0.50 mm on the transmit pair, 0.02 mm on the receive pair, on these last segments).
- Centre taps: vias in the capacitor pads, bottom-layer lines to pins 4 and 5 as before.
- Chassis: the lines from C280 to pin 8 and to the shield pins, and the bottom-layer link between the two shield pins, follow the jack.
- LEDs: pins 9 and 12 reconnected to R248 and R249.
- The copper-pour keep-out under the jack on In2 was extended north by the same 1.945 mm (top edge now y = 113.955).

## Checks

DRC with schematic parity: 0 violations, 0 unconnected, 0 parity issues. 329 footprints, 2211 tracks, 852 vias. Evidence: `build/MujinaControl-S19/ethpos/` (`rip.py`, `route.py`, `drc1.json`, datasheet, before / after plots).

Not checked here: the jack against the real case opening. The 2.25 mm figure is the requested value.

## Tab-up jack (HR915340A)

2026-11-14, after the move above. The planned enclosure makes a latch tab on the underside hard to reach, so J100 was changed from HanRun HR911105A (tab down) to **HanRun HR915340A** (tab up, fab part C2760325). Both are 10/100 jacks with built-in magnetics, 75 Ω terminations, the 1 nF / 2 kV chassis capacitor and two LEDs.

| | HR911105A | HR915340A |
|---|---|---|
| Signal pins 1–8 and their functions | – | identical positions and functions |
| Locating posts | 11.43 mm apart | same position, hole 3.2 mm |
| Shield pins | 15.49 mm apart, 1.63 mm holes | 15.75 mm apart, 1.70 mm holes |
| LED pins | four in a row, 4.90 mm in front of the posts | two 2-pin clusters 13.45 mm apart, 2.54 and 4.57 mm in front of the posts |
| LEDs | green on 9 (A) / 10 (K), yellow on 12 (A) / 11 (K) | green on 11 (A) / 12 (K), yellow on 9 (A) / 10 (K) |
| Face in front of the posts | 10.90 mm | 10.85–10.90 mm |

- **Position:** unchanged, pin 1 at (109.775, 119.235); the face stays 2.25 mm past the board edge (within the 0.05 mm the two datasheet views differ by).
- **Schematic:** new symbol `Connector:RJ45_Hanrun_HR915340A_Horizontal`, the old drawing with the four LED pins renumbered, so the sheet's wiring is as drawn before. The link signal still lights the green LED (left, seen from the front) through R248, the speed signal the yellow one (right) through R249.
- **Footprint:** new `Connector_RJ:RJ45_Hanrun_HR915340A_Horizontal`, from the datasheet's PCB layout (REV. 01, page 3).
- **Copper:** only the two LED lines and the shield-pin connections were redrawn. The Ethernet pairs, centre taps and the pin-8 chassis line are untouched.
- **3D model:** `3d/generated/HanRun_HR915340A.step`, a generated envelope with the tab-up opening; not a vendor model.

ERC 0. DRC with schematic parity: 0 violations, 0 unconnected, 0 parity issues. Readability checker clear. 329 footprints, 2211 tracks, 852 vias. Evidence: `build/MujinaControl-S19/ethtab/` (datasheets, `libs.py`, `rip.py`, `route.py`, `drc2.json`, renders).

Not verified: the footprint on a real part (first build), and the fit in the real enclosure.
