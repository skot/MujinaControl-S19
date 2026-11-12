# Parts against the fab's stock — 2026-11-12

The board is assembled by the fab, so every purchased part carries the fab part number (`LCSC` field) and an `MPN` field, and uses a basic-category part wherever one exists in the same footprint with the same value and an equal or better rating.

Live stock was read on 2026-11-12 for every part number. Stock is a reading, not a reservation.

## Result

- 310 symbols: 304 purchased parts, all with both fields; the six others are the four mounting holes and two test pads (`N/A`).
- 65 part numbers: **24 basic, 9 preferred (no fee), 32 extended.** Before this pass: 70 part numbers, 7 basic, 2 preferred, 61 extended.
- Of 287 fitted placements, 206 are basic, 20 preferred, 61 extended.
- The RV1106G2 is listed for standard assembly only, so the whole order goes through the fab's standard (not economic) assembly service.

## Changed in this pass

| Was | Now | Parts | Note |
|---|---|---|---|
| C71629 GRM155R71C104KA88D | C1525 CL05B104KO5NNNC | 39 × 100 nF 0402 | basic; same 16 V X7R |
| C76999 GRM155R61A105KE15D | C52923 CL05A105KA5NQNC | 13 × 1 µF 0402 | basic; 25 V X5R (was 10 V) |
| C77073 GRM21BR61A106KE19L | C15850 CL21A106KAYNNNE | 7 × 10 µF 0805 | basic; 25 V X5R (was 10 V) |
| C77177 GRM1555C1H101JA01D | C1546 0402CG101J500NT | 4 × 100 pF 0402 | basic; same 50 V C0G 5 % |
| C33149 GRM1555C1H180JA01D | C1549 0402CG180J500NT | 4 × 18 pF 0402 | basic; same 50 V C0G 5 % |
| C77019 GRM155R71H103KA88D | C15195 CL05B103KB5NNNC | 3 × 10 nF 0402 | basic; same 50 V X7R |
| C77018 GRM155R71H102KA01D | C1523 0402B102K500NT | 1 × 1 nF 0402 | basic; same 50 V X7R |
| C97973 GRM32ER7YA106KA12L | C138687 CL32B106KBJNNNE | C284, 10 µF 1210 | still extended; now the same part as C285 (50 V X7R, was 35 V), one extended line fewer |
| C105871 RC0402FR-074K7L | C25900 0402WGF4701TCE | 36 × 4.7 k | basic |
| C60490 RC0402FR-0710KL | C25744 0402WGF1002TCE | 23 × 10 k | basic |
| C60491 RC0402FR-07100KL | C25741 0402WGF1003TCE | 17 × 100 k | basic |
| C60485 RC0402JR-070RL | C17168 0402WGF0000TCE | 7 × 0 Ω | basic |
| C106235 RC0402FR-071KL | C11702 0402WGF1001TCE | 5 × 1 k | basic |
| C114765 RC0402FR-0722RL | C25092 0402WGF220JTCE | 3 × 22 Ω | basic |
| C106232 RC0402FR-07100RL | C25076 0402WGF1000TCE | 2 × 100 Ω | basic |
| C138033 RC0402FR-071ML | C26083 0402WGF1004TCE | 2 × 1 M (not fitted) | basic |
| C276273 RC0402FR-07510RL | C25123 0402WGF5100TCE | 2 × 510 Ω | basic |
| C105872 RC0402FR-075K1L | C25905 0402WGF5101TCE | 2 × 5.1 k | basic; merges with R283/R285 |
| C138044 RC0402FR-0718KL | C25762 0402WGF1802TCE | R255, 18 k | preferred (no fee) |
| C185446 RC0402FR-071RL | C25086 0402WGF100KTCE | R223, 1 Ω | preferred (no fee) |
| C138062 RC0402FR-07124KL | C36777 0402WGF1243TCE | R208, 124 k | still extended; old part had 15 in stock, new one 117 k |
| C185443 RC0402FR-07215KL (215 k) | C25764 0402WGF2003TCE (200 k) | R214 | basic; value changed, see the trip-point section |
| C138065 RC0402FR-07110KL (110 k) | C25741 0402WGF1003TCE (100 k) | R210, R212 | basic; value changed |
| C226987 316 k, C227183 665 k | C25774 0402WGF3003TCE (300 k) | R216, R218 | preferred (no fee); value changed |
| C25741 100 k | C25792 0402WGF4702TCE (47 k) | R219 | basic; value changed |
| C130253 ABS07-32.768KHZ-T | C32346 Q13FC13500004 | Y101, 32.768 kHz 3215 | basic; same 12.5 pF load, ±20 ppm, 70 kΩ ESR |
| C19653 TPS3808G01DBVR | C42394092 TPS3808G01DBVR-TP | U120–U124 | TI ordering code had **0** in stock; second-source part chosen for stock (6,283), see the supervisor section below |

All resistors are 0402, 1 %, 62.5 mW, as before. Footprints and nets are unchanged. Values are unchanged except the supervisor dividers (R210, R212, R214, R216, R218, R219, see below) and C284's value text (10u / 35V → 10u / 50V).

## Stock to watch

| Part | Use | Stock | Per board | Note |
|---|---|---|---|---|
| C894097 NTTFS008P03P8Z | Q1 input MOSFET | 7 | 1 | Enough for the five boards in the fab file only if nothing else takes them. Same-voltage candidates in a 3×3 mm power package exist in stock (for example C431196 AONR21357, 30 V, 12.3 mΩ at 4.5 V) but have roughly twice the on-resistance and need a footprint and thermal check; not changed. |
| C437089 X2026WV-2x09D-46SN | J3–J5 hashboard connectors | 29 | 3 | Nine boards. Same-series 2×9, 2 mm parts in stock: C2845620 HC-PHD-2*9A (2,413; same maker as J10), C495666 B18B-PHDSS (9,609). Not changed: the footprint should be checked against the chosen part first. |
| C492365 50362462 | J1 power input | 476 | 1 | |
| C5272606 RV1106G2 | U100 | 773 | 1 | Standard assembly only. |
| C2167485 1 nF 2 kV, C3010298 W25N02KVZEIR | C280, U130 | 1,948–1,992 | 1 | |

## Supervisors U120–U124 — second source, 2026-11-12

U120–U124 use C42394092 (TPS3808G01DBVR-TP, TECH PUBLIC), 6,283 in stock, about 0.18 USD each. Its datasheet was read against how the part is used here:

| Needed by the circuit | Datasheet |
|---|---|
| SOT-23-6, pins 1 RESET, 2 GND, 3 MR, 4 CT, 5 SENSE, 6 VDD | same pinout; 2.9 × 1.6 mm body, 0.95 mm pitch |
| Adjustable threshold 0.405 V at SENSE (dividers R210–R219) | adjustable version, 0.405 V; accuracy ±1 % typical, ±2 % limits; hysteresis 1.5 % |
| Runs from +5V_SYS | 1.7–6.5 V supply; 7 V absolute maximum on every pin |
| CT left open | 20 ms delay (12–28 ms) |
| MR tied to +5V_SYS or driven by the previous stage (SEQ_MID, SEQ_IO) | MR low below 0.3 VDD, high above 0.7 VDD, internal 90 kΩ pull-up; must not exceed VDD (it does not here) |
| Open-drain output on a 10 kΩ pull-up (R220–R222) | open drain, 0.4 V at 1 mA; pull-up of 10 kΩ or more |
| Divider impedance up to 75 kΩ | SENSE current ±25 nA (about 0.5 % threshold shift at most) |

These figures are the same as the TI part's, and the document is close to a copy of TI's, so the match is on paper only: the part has not been characterised here. Alternatives with the same pinout and threshold, if the first boards show a sequencing problem: C33144197 TPS3808EG01DBVR (TI's newer version, 1,023 in stock, about 1.58 USD, supply up to 6 V) and C702161 TPS3808G01DBVT (the original TI device, 200 in stock, about 1.38 USD). Either is a field-only change.

## Supervisor trip points lowered — 2026-11-12

Before, each supervisor tripped at about 94 % of its rail and released at about 96 %. With the 0.405 V threshold at its +2 % limit, hysteresis at 3 % and 1 % divider resistors, the release point reached the nominal rail voltage, so a rail sitting slightly low could have held the chain in reset. The dividers now put the trip point at about 90 %:

| Supervisor | Rail (nominal) | Divider, top / bottom | Trip, falling | Release, typical | Release, limits |
|---|---|---|---|---|---|
| U120 | +0V9_CORE (0.899 V) | R210 100 k / R211 100 k (was 110 k / 100 k) | 0.810 V, 90.1 % (was 0.851 V) | 0.822 V, 91.4 % | 0.860 V, 95.6 % |
| U121 | +0V9_CPU (0.899 V) | R212 100 k / R213 100 k (was 110 k / 100 k) | 0.810 V, 90.1 % (was 0.851 V) | 0.822 V, 91.4 % | 0.860 V, 95.6 % |
| U122 | +1V35_DDR (1.345 V) | R214 200 k / R215 100 k (was 215 k / 100 k) | 1.215 V, 90.3 % (was 1.276 V) | 1.233 V, 91.7 % | 1.294 V, 96.2 % |
| U123 | +1V8 (1.792 V) | R216 300 k / R217 100 k (was 316 k / 100 k) | 1.620 V, 90.4 % (was 1.685 V) | 1.644 V, 91.8 % | 1.727 V, 96.4 % |
| U124 | +3V3 (3.307 V) | R218 300 k / R219 47 k (was 665 k / 100 k) | 2.990 V, 90.4 % (was 3.098 V) | 3.035 V, 91.8 % | 3.196 V, 96.6 % |

"Limits" stacks threshold +2 %, hysteresis 3 % and both divider resistors 1 % the wrong way. The release point now stays 3.4 % or more below nominal even then, and about 8 % below in the typical case. The lowest trip with everything the other way is 0.786 V, 1.18 V, 1.57 V and 2.88 V.

The 3.3 V supervisor needed both resistors changed: no stocked no-fee value gives 90 % against a 100 k bottom resistor. 300 k / 47 k also brings its divider impedance down from 87 kΩ to 41 kΩ. The sheet note on `03_sequencing.kicad_sch` lists the new thresholds.

All six resistors are now basic or preferred parts, which removes four extended lines (110 k, 215 k, 316 k, 665 k). Evidence: `build/MujinaControl-S19/bom/trip.py`; the sequencing sheet was rendered and inspected (`build/MujinaControl-S19/bom/render/seq.png`).

## Small diodes and FETs moved to preferred parts — 2026-11-12

Thirteen parts changed maker to the fab's preferred (no-fee) parts of the same type number and package, all from Zhuhai Hongjiacheng. Each datasheet was read against the circuit:

| Parts | Was | Now | Stock | Pinout | Figures that matter here |
|---|---|---|---|---|---|
| D230–D233, tach clamps to 3.3 V and ground | C47546 BAT54S,215 | C7420333 BAT54S | 495,986 | 1 anode, 2 cathode, 3 common: same | 30 V, 200 mA, 0.40 V max at 10 mA, 2 µA at 25 V, 10 pF: same as before. They sit behind a 10 kΩ series resistor, so they carry under 1 mA. |
| Q2–Q5, fan PWM open-drain drivers | C52895 BSS138 | C7420339 BSS138 | 680,383 | 1 gate, 2 source, 3 drain: same | 50 V, ±20 V gate, 340 mA (was 220 mA). Threshold 0.8–1.6 V (was 0.8–1.5 V); the gates are driven from 3.3 V pins through 1 kΩ. On-resistance 3 Ω max at 4.5 V. Input capacitance 60 pF (was 27 pF): about 60 ns with the 1 kΩ gate resistor. |
| D3–D6, 3.3 V clamps at the fan tach pins | C2112 BZT52C3V3 | C19077396 BZT52C3V3 | 678,357 | SOD-123, band is cathode: same | 3.14–3.47 V at 5 mA (was 3.1–3.5 V), 5 µA at 1 V: same. Rated 350 mW where the old listing said 500 mW; with a fan pulling its tach line to 12 V through 1 kΩ the diode dissipates about 30 mW. |
| D2, 12 V gate clamp on Q1 | C12773 LBZX84C12LT1G | C19077471 BZX84C12 | 206,127 | 1 anode, 2 not connected, 3 cathode: same | 11.4–12.7 V at 5 mA, 300 mW, 0.1 µA at 8 V: same. Current is set by R270 (10 kΩ): about 1.2 mA with the input at the TVS clamp voltage. D2's value text now reads BZX84C12. |

These are datasheet comparisons; none of the parts was measured. Evidence: `build/MujinaControl-S19/bom/pref.py`, datasheets in `build/MujinaControl-S19/bom/ds-pref/`.

## Why the remaining extended parts stay

- **No basic or preferred part in that footprint and value:** 12.4 k, 68.1 k, 124 k (regulator feedback and USB detect), 240 Ω (DDR ZQ), 6.04 k (Ethernet bias), 2.2 Ω (USB series), 10 µF 1210 X7R, 0402 ferrite bead, 24 MHz crystal, green 0603 LED, 1.5 µH 2016 inductor, 100 µF hybrid capacitor, 1 nF 2 kV. Moving any of these to basic means a different value or footprint, which is a circuit or layout change.
- **ICs, protection and connectors:** none of these exist as basic parts.

## Full list

| Category | Fab part | MPN | Value | Refs | Not fitted | Stock |
|---|---|---|---|---|---|---|
| basic | C15195 | CL05B103KB5NNNC | 10n | C230, C278, C279 |  | 5,549,465 |
| basic | C1523 | 0402B102K500NT | 1n | C276 |  | 3,687,852 |
| basic | C1525 | CL05B104KO5NNNC | 100n | C225 … C305 (39) |  | 33,118,181 |
| basic | C1546 | 0402CG101J500NT | 100p | C205, C210, C215, C220 |  | 3,379,419 |
| basic | C1549 | 0402CG180J500NT | 18p | C272, C273, C274, C275 |  | 1,013,214 |
| basic | C15850 | CL21A106KAYNNNE | 10u | C240 … C270 (7) |  | 8,592,703 |
| basic | C21117 | CL10B333KB8NNNC | 33n / 50V | C291, C293, C295, C297, C299, C301 |  | 927,437 |
| basic | C307331 | CL05B104KB54PNC | 100n / 50V | C202 … C302 (12) |  | 19,936,254 |
| basic | C45783 | CL21A226MAQNNNE | 22u / 25V | C201 … C288 (17) |  | 4,346,730 |
| basic | C52923 | CL05A105KA5NQNC | 1u / 1u / 10V | C261 … C311 (13) |  | 10,627,305 |
| basic | C11702 | 0402WGF1001TCE | 1k | R9, R10, R11, R12, R201 |  | 31,963,426 |
| basic | C17168 | 0402WGF0000TCE | 0 | R242 … R301 (7) |  | 15,934,871 |
| basic | C25076 | 0402WGF1000TCE | 100 | R224, R239 |  | 11,066,123 |
| basic | C25092 | 0402WGF220JTCE | 22 | R225, R235, R236 |  | 4,916,814 |
| basic | C25123 | 0402WGF5100TCE | 510 | R248, R249 |  | 2,571,586 |
| basic | C25741 | 0402WGF1003TCE | 100k | R203 … R271 (18) |  | 8,780,305 |
| basic | C25744 | 0402WGF1002TCE | 10k | R13 … R279 (24) |  | 22,050,581 |
| basic | C25756 | 0402WGF1502TCE | 15k | R274, R275, R276, R277, R278, R281 |  | 2,103,940 |
| basic | C25764 | 0402WGF2003TCE | 200k | R214 |  | 3,530,390 |
| basic | C25792 | 0402WGF4702TCE | 47k | R219, R280 |  | 5,792,162 |
| basic | C25900 | 0402WGF4701TCE | 4.7k | R17 … R300 (36) | R17, R19, R22, R23, R26, R27, R29, R30, R31, R272, R273 | 14,691,629 |
| basic | C25905 | 0402WGF5101TCE | 5.1k | R250, R251, R283, R285 |  | 4,060,435 |
| basic | C26083 | 0402WGF1004TCE | 1M | R237, R247 | R237, R247 | 2,412,824 |
| basic | C32346 | Q13FC13500004 | 32.768kHz / CL12.5pF | Y101 |  | 322,110 |
| preferred | C19077396 | BZT52C3V3 | 3.3V Zener | D3, D4, D5, D6 |  | 678,357 |
| preferred | C19077471 | BZX84C12 | BZX84C12 | D2 |  | 206,127 |
| preferred | C19077569 | SMBJ15A | SMBJ15A | D220 |  | 72,408 |
| preferred | C7420333 | BAT54S | BAT54S | D230, D231, D232, D233 |  | 495,986 |
| preferred | C7420339 | BSS138 | BSS138 | Q2, Q3, Q4, Q5 |  | 680,383 |
| preferred | C25086 | 0402WGF100KTCE | 1 | R223 |  | 287,371 |
| preferred | C25762 | 0402WGF1802TCE | 18k | R255 |  | 465,784 |
| preferred | C25771 | 0402WGF2702TCE | 27k | R282, R284 |  | 605,943 |
| preferred | C25774 | 0402WGF3003TCE | 300k | R216, R218 |  | 1,980,506 |
| extended | C138687 | CL32B106KBJNNNE | 10u / 50V | C284, C285 |  | 70,607 |
| extended | C178640 | EEHZC1E101XP | 100u / 25V | C289, C290 |  | 3,278 |
| extended | C2167485 | C1808C102KGRACTU | 1n / 2kV | C280 |  | 1,948 |
| extended | C125094 | LTST-C190KGKT | STATUS GREEN | D100 |  | 467,400 |
| extended | C552535 | PESD3V3Y1BSFYL | PESD3V3Y1BSF | D201, D202 |  | 135,010 |
| extended | C85812 | BLM15AG121SN1D | 120R @ 100MHz | FB201, FB202 |  | 451,026 |
| extended | C12074 | HR911105A | RJ45_Hanrun_HR911105A_Horizontal | J100 |  | 52,638 |
| extended | C2845614 | HC-PHD-2\*3A | PSU Comm | J10 |  | 40,283 |
| extended | C2915006 | 61300311121 | UART2 DEBUG | J16 |  | 12,542 |
| extended | C2982043 | HC-2510-4AW | 61900411021 | J6, J7, J8, J9 | J6, J7 | 18,212 |
| extended | C3020560 | USB4105-GF-A | USB_C_Receptacle_USB2.0 | J2 |  | 17,359 |
| extended | C437089 | X2026WV-2x09D-46SN | 2x9P 2mm | J3, J4, J5 |  | 29 |
| extended | C492365 | 50362462 | 0455580003 | J1 |  | 476 |
| extended | C5224014 | PZ2.54-2\*20 | ACC 2x20 / 0.1 in | J15 |  | 13,325 |
| extended | C54909 | 4.2-2\*2AW | 0353180420 | J11, J12, J13, J14 | J13, J14 | 31,420 |
| extended | C719027 | DM3D-SF | Micro_SD_Card_Det2 | J101 |  | 8,372 |
| extended | C5832350 | FTC201612S1R5MBCA | 1.5u | L201, L202, L203, L204, L205, L210 |  | 4,318 |
| extended | C894097 | NTTFS008P03P8Z | NTTFS008P03P8Z | Q1 |  | 7 |
| extended | C114755 | RC0402FR-07240RL | 240 | R241 |  | 1,098,560 |
| extended | C138060 | RC0402FR-0712K4L | 12.4k | R202, R204, R254 |  | 334,273 |
| extended | C276276 | RC0402FR-0768K1L | 68.1k | R206 |  | 60,002 |
| extended | C327251 | RC0402FR-072R2L | 2.2 | R252, R253 |  | 1,306,664 |
| extended | C36777 | 0402WGF1243TCE | 124k | R208 |  | 117,031 |
| extended | C97819 | RC0402FR-076K04L | 6.04k | R246 |  | 135,328 |
| extended | C49101620 | TC-S3601-3.5-260G-F0.6 | RESET / BOOT | SW1, SW2 |  | 125,528 |
| extended | C2149796 | TPS22919DCKR | TPS22919DCKR | U150, U151, U152 |  | 19,257 |
| extended | C3010298 | W25N02KVZEIR | W25N02KVZEIR | U130 |  | 1,992 |
| extended | C3200405 | TPS62933DRLR | TPS62933DRLR | U110, U111, U112, U113, U114, U115 |  | 13,466 |
| extended | C3702980 | TPD1E05U06DYA | TPD1E05U06DYA | U140, U141 |  | 11,727 |
| extended | C42394092 | TPS3808G01DBVR-TP | TPS3808DBV | U120, U121, U122, U123, U124 |  | 6,283 |
| extended | C70590 | X322524MOB4SI | 24MHz / CL12pF | Y100 |  | 331,470 |
| extended, standard assembly only | C5272606 | RV1106G2 | RV1106G2 | U100 |  | 773 |

## Verification

- Changes are 181 symbols and 181 footprints, two fields each (`LCSC`, `MPN`), plus C284's value text; made as text edits with the documents closed and checked by diff (363 changed lines in the schematic sheets, 363 in the board, nothing else).
- Netlist before and after is identical (219 nets). ERC 0. Board DRC with schematic parity: 0 violations, 0 unconnected, 0 parity issues. Readability checker: 0 errors.
- Evidence: `build/MujinaControl-S19/bom/` (`apply.py`, `stock.json`, `bom-flat.csv`, `bom-status.csv`, `erc.json`, `drc.json`, `net.xml`, `net-after.xml`, `backup.txt`).

This supersedes the part numbers in [lcsc-mapping.md](lcsc-mapping.md) and [stock-replacements.md](stock-replacements.md) for the lines listed above.
- Later the same day: the supervisor part and the six divider resistors were changed as described above; netlist connectivity unchanged, ERC 0, DRC 0 / 0 / 0 with parity, readability checker 0 errors.
- Preferred diodes and FETs: 13 symbols and 13 footprints, fields only; netlist connectivity unchanged, ERC 0, DRC 0 / 0 / 0 with parity, readability checker 0 errors.
