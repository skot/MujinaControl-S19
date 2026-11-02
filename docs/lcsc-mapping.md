# Schematic catalog fields

Current schematic: hidden `LCSC` fields on all 254 purchased components (including DNP parts), representing 65 selected MPNs. F100 was removed at the user’s request; see [fuse removal](fuse-removal.md). The four mounting holes and two bare test pads are `N/A`; virtual power markers are not BOM items. All units of multi-unit components are annotated. The initial field-population pass preserved every MPN. Five MPNs were subsequently updated in the [stock replacement pass](stock-replacements.md); values, footprints, connections and drawing geometry remain unchanged.

Catalog lookup date: 2026-11-01. Stock is a catalog snapshot except entries marked live; it is not an order reservation. The selected manufacturer is recorded below to disambiguate generic part numbers.

## Stock replacements

The five previous stock shortages were addressed in the [replacement selection report](stock-replacements.md). The two APV inductors require dedicated footprint/courtyard qualification before PCB placement; this is recorded in their symbol Assembly Note fields.

## Identity decisions

- U140/U141: C3702980 is TI TPD1E05U06DYAR, the reel ordering number for the existing TPD1E05U06DYA device/package. The [TI datasheet](https://www.ti.com/lit/ds/symlink/tpd1e05u06.pdf) confirms DYA is SOD-523 and lists DYAR packaging. The original bitcrane catalog code agrees. The shorter existing MPN field was retained.
- D3–D6: retained the original bitcrane C2112 manufacturer/part identity.
- Q2–Q5: C52895 matches the existing onsemi BSS138 MPN and datasheet. The old bitcrane reference code C5248642 actually identifies BSS138K-13 from another manufacturer, so it was not copied.
- D220: selected preferred-stock SMBJ15A C19077569, same nominal part and SMB package; no manufacturer was previously fixed.
- U130: selected C3010298, explicitly listed as WSON-8-EP (6 × 8 mm).

## Initial catalog-field verification

This section records the earlier field-population pass. See the replacement report for the latest five-part metadata update.

Native exported fields verified for every component; all 193 named net partitions unchanged; ERC 0 errors/warnings; readability 0 errors and 74 advisories. All ten native rendered pages are pixel-identical to renders of the immediate pre-edit backup. Structural comparison proves that only hidden LCSC fields were added. PCB and project files remain byte-identical.

The older 438-check script could not complete its mechanical checks: 20 footprints already lack explicit placement records in the current PCB and its immediate backup. No PCB edits were made. This does not prevent field, netlist, ERC, drawing or metadata verification; no claim of a new 438-check pass is made.

Backplane IPC was unavailable; supported Konnect schematic field tools performed the changes. Saved canonical files were re-read and displayed. History still has no commits; explicit backups are preserved.

[Verification evidence](../../../build/MujinaControl-S19/catalog-fields/verification.json) · [Lookup evidence](../../../build/MujinaControl-S19/catalog-fields/catalog-lookups.json) · [Low-stock lookup evidence](../../../build/MujinaControl-S19/catalog-fields/low-stock-lookups.json) · [Backup location](../../../build/MujinaControl-S19/catalog-fields/backup.txt)

## Selected parts

| References | Selected MPN | LCSC field | Manufacturer | Package | Catalog class | Stock | Source |
|---|---|---|---|---|---|---:|---|
| J11, J12, J13, J14 | 4.2-2*2AW | C54909 | BOOMELE(Boom Precision Elec) | Push-Pull,P=4.2mm | extended | 17933 | catalog snapshot |
| J1 | 50362462 | C492365 | MOLEX | Push-Pull,P=4.2mm | extended | 515 | catalog snapshot |
| J16 | 61300311121 | C2915006 | Wurth Elektronik | Plugin,P=2.54mm | extended | 13343 | catalog snapshot |
| J15 | 61300411121 | C5184785 | Wurth Elektronik | Plugin,P=2.54mm | extended | 1746 | catalog snapshot |
| Y101 | ABS07-32.768KHZ-T | C130253 | Abracon LLC | SMD3215-2P | extended | 3500 | catalog snapshot |
| U110, U111, U112, U113 | AP63200WU-7 | C2071868 | Diodes Incorporated | TSOT-23-6 | extended | 5960 | catalog snapshot |
| U114 | AP63203WU-7 | C780769 | Diodes Incorporated | TSOT-23-6 | extended | 2531 | catalog snapshot |
| U115 | AP63205WU-7 | C2071056 | Diodes Incorporated | TSOT-23-6 | extended | 14850 | catalog snapshot |
| D230, D231, D232, D233 | BAT54S,215 | C47546 | Nexperia | SOT-23 | extended | 220830 | catalog snapshot |
| FB201, FB202 | BLM15AG121SN1D | C85812 | Murata Electronics | 0402 | extended | 523696 | catalog snapshot |
| Q2, Q3, Q4, Q5 | BSS138 | C52895 | onsemi | SOT-23 | extended | 79763 | catalog snapshot |
| D3, D4, D5, D6 | BZT52C3V3 | C2112 | Jiangsu Changjing Electronics Technology Co., Ltd. | SOD-123 | extended | 37064 | catalog snapshot |
| C280 | C1808C102KGRACTU | C2167485 | KEMET | 1808 | extended | 2058 | catalog snapshot |
| J101 | DM3D-SF | C719027 | HRS(Hirose) | SMD | extended | 1056 | catalog snapshot |
| Q1 | DMP3013SFV-7 | C264098 | Diodes Incorporated | PowerDI3333-8 | extended | 1496 | catalog snapshot |
| C205, C210, C215, C220 | GRM1555C1H101JA01D | C77177 | Murata Electronics | 0402 | extended | 1052225 | catalog snapshot |
| C272, C273, C274, C275 | GRM1555C1H180JA01D | C33149 | Murata Electronics | 0402 | extended | 294734 | catalog snapshot |
| C261, C264, C266, C267, C269, C277, C282 | GRM155R61A105KE15D | C76999 | Murata Electronics | 0402 | extended | 209883 | catalog snapshot |
| C202, C207, C212, C217, C222, C225, C226, C227, C228, C229, C231, C232, C233, C234, C235, C236, C237, C238, C239, C241, C243, C244, C245, C247, C248, C249, C250, C251, C252, C253, C255, C256, C257, C258, C262, C263, C265, C268, C271, C281, C283, C286 | GRM155R71C104KA88D | C71629 | Murata Electronics | 0402 | extended | 1065057 | catalog snapshot |
| C276 | GRM155R71H102KA01D | C77018 | Murata Electronics | 0402 | extended | 634335 | catalog snapshot |
| C230, C278, C279 | GRM155R71H103KA88D | C77019 | Murata Electronics | 0402 | extended | 381181 | catalog snapshot |
| C201, C206, C211, C216, C221, C240, C242, C246, C254, C259, C260, C270 | GRM21BR61A106KE19L | C77073 | Murata Electronics | 0805 | extended | 17464 | catalog snapshot |
| C203, C204, C208, C209, C213, C214, C218, C219, C223, C224, C287, C288 | GRM21BR61A226ME44L | C441864 | Murata Electronics | 0805 | extended | 6015 | catalog snapshot |
| C284, C285 | GRM32ER7YA106KA12L | C97973 | Murata Electronics | 1210 | extended | 6306 | catalog snapshot |
| J6, J7, J8, J9 | HC-2510-4AW | C2982043 | HCTL | Push-Pull,P=2.54mm | extended | 8618 | catalog snapshot |
| J10 | HC-PHD-2*3A | C2845614 | HCTL | Plugin,P=2mm | extended | 42289 | catalog snapshot |
| J100 | HR911105A | C12074 | HANRUN(Zhongshan HanRun Elec) | Plugin | extended | 59388 | catalog snapshot |
| D2 | LBZX84C12LT1G | C12773 | LRC | SOT-23 | extended | 5153 | catalog snapshot |
| D100 | LTST-C190KGKT | C125094 | Lite-On | 0603 | extended | 411211 | catalog snapshot |
| H1, H2, H3, H4 | PCB_MOUNTING_HOLE | N/A | N/A | PCB feature | N/A | — | Not purchased |
| TP29, TP30 | PCB_TESTPOINT | N/A | N/A | PCB feature | N/A | — | Not purchased |
| D201, D202 | PESD3V3Y1BSFYL | C552535 | Nexperia | DSN0603-2 | extended | 136773 | catalog snapshot |
| R203, R205, R207, R209, R211, R213, R215, R217, R219, R256, R258, R260, R262, R264, R266, R268, R271 | RC0402FR-07100KL | C60491 | YAGEO | 0402 | extended | 9296986 | catalog snapshot |
| R224, R239 | RC0402FR-07100RL | C106232 | YAGEO | 0402 | extended | 9091326 | catalog snapshot |
| R220, R221, R222, R226, R227, R228, R229, R230, R231, R232, R233, R234, R238, R240, R257, R259, R261, R13, R14, R15, R16, R263, R265, R267, R269, R270 | RC0402FR-0710KL | C60490 | YAGEO | 0402 | extended | 6811419 | catalog snapshot |
| R210, R212 | RC0402FR-07110KL | C138065 | YAGEO | 0402 | extended | 604300 | catalog snapshot |
| R208 | RC0402FR-07124KL | C138062 | YAGEO | 0402 | extended | 15 | catalog snapshot |
| R202, R204, R254 | RC0402FR-0712K4L | C138060 | YAGEO | 0402 | extended | 348860 | catalog snapshot |
| R255 | RC0402FR-0718KL | C138044 | YAGEO | 0402 | extended | 958457 | catalog snapshot |
| R201, R9, R10, R11, R12 | RC0402FR-071KL | C106235 | YAGEO | 0402 | extended | 2098774 | catalog snapshot |
| R237, R247 | RC0402FR-071ML | C138033 | YAGEO | 0402 | extended | 1947937 | catalog snapshot |
| R223 | RC0402FR-071RL | C185446 | YAGEO | 0402 | extended | 183298 | catalog snapshot |
| R214 | RC0402FR-07215KL | C185443 | YAGEO | 0402 | extended | 12042 | catalog snapshot |
| R225, R235, R236 | RC0402FR-0722RL | C114765 | YAGEO | 0402 | extended | 4987234 | catalog snapshot |
| R241 | RC0402FR-07240RL | C114755 | YAGEO | 0402 | extended | 1265412 | catalog snapshot |
| R252, R253 | RC0402FR-072R2L | C327251 | YAGEO | 0402 | extended | 1352811 | catalog snapshot |
| R216 | AC0402FR-07316KL | C226987 | YAGEO | 0402 | extended | 2174 | catalog snapshot |
| R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R272, R273, R274, R275, R276, R277 | RC0402FR-074K7L | C105871 | YAGEO | 0402 | extended | 8583663 | catalog snapshot |
| R248, R249 | RC0402FR-07510RL | C276273 | YAGEO | 0402 | extended | 2085940 | catalog snapshot |
| R250, R251 | RC0402FR-075K1L | C105872 | YAGEO | 0402 | extended | 2393046 | catalog snapshot |
| R218 | AC0402FR-07665KL | C227183 | YAGEO | 0402 | extended | 7300 | catalog snapshot |
| R206 | RC0402FR-0768K1L | C276276 | YAGEO | 0402 | extended | 22 | catalog snapshot |
| R246 | RC0402FR-076K04L | C97819 | YAGEO | 0402 | extended | 158134 | catalog snapshot |
| R242, R243, R244, R245 | RC0402JR-070RL | C60485 | YAGEO | 0402 | extended | 8742279 | catalog snapshot |
| U100 | RV1106G2 | C5272606 | Rockchip | QFN-128(12.3x12.3) | extended | 959 | catalog snapshot |
| D220 | SMBJ15A | C19077569 | hongjiacheng | DO-214AA(SMB) | preferred | 84365 | catalog snapshot |
| L201, L202, L203 | SRN4018-2R2M | C913207 | BOURNS | SMD,4x4mm | extended | 1840 | catalog snapshot |
| L204 | ANR6028T3R3M | C7427149 | APV | SMD,6x6mm | extended | 4005 | catalog snapshot |
| L205 | SRN6028C-3R9M | C19947652 | BOURNS | SMD,6x6mm | extended | 145 | catalog snapshot |
| L210 | ANR6028T4R7M | C7427151 | APV | SMD,6x6mm | extended | 2258 | catalog snapshot |
| U140, U141 | TPD1E05U06DYA | C3702980 | Texas Instruments | SOT-5X3 | extended | 5316 | live lookup |
| U120, U121, U122, U123, U124 | TPS3808G01DBVR | C19653 | Texas Instruments | SOT-23-6 | extended | 4627 | catalog snapshot |
| SW1, SW2 | TS-1088-AR02016 | C720477 | XUNPU | SMD,4x3mm | basic | 582888 | catalog snapshot |
| J2 | USB4105-GF-A | C3020560 | Global Connector Technology | SMD | extended | 2864 | catalog snapshot |
| U130 | W25N02KVZEIR | C3010298 | Winbond Elec | WSON-8-EP(6x8) | extended | 1737 | catalog snapshot |
| J3, J4, J5 | X2026WV-2x09D-46SN | C437089 | XKB Connection | Plugin,P=2mm | extended | 29 | catalog snapshot |
| Y100 | X322524MOB4SI | C70590 | YXC Crystal Oscillators | SMD3225-4P | extended | 173512 | catalog snapshot |
