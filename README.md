# MujinaControl-S19

Initial RV1106G2 Antminer controlboard schematic, revision 0.1. Open `MujinaControl-S19.kicad_pro` with the selected Backplane KiCad runtime. This is a schematic development milestone, not a fabrication release.

The ten-sheet design contains a 128 MB RV1106G2, 24 MHz and RTC clocks, SPI NAND, microSD, USB recovery, a 100BASE-TX MagJack, five sequenced SoC supplies, and the bitcrane miner interfaces. The PCB contains only the original outline, mounting holes and connector placements. New component placement, Ethernet placement, stackup design and routing remain to be done.

## Initial choices

- Confirmed power source: J1's existing 6-pin 12 V input (pins 1-3 positive, pins 4-6 ground). A fused branch generates 5 V for the SoC regulators. Fans retain the protected 12 V rail. USB-C VBUS is detection-only: **12 V must be present for USB recovery**.
- Confirmed storage choice: SPI NAND following Luckfox Pico Pro/Max. U130 is W25N02KVZEIR, a 2 Gbit (256 MB) raw SPI NAND connected to the SoC's quad-SPI interface. MicroSD remains in the draft as an additional storage/boot option. U100's 128 MB in-package DDR3L is separate RAM.
- CPU and logic use separate nominal 0.9 V regulators. DDR uses 1.3448 V, analog uses 1.792 V, and I/O uses 3.3 V. Five TPS3808 supervisors qualify the rail sequence and reset, using their CT-open delay. This first draft prioritizes explicit sequencing; the regulator/supervisor BOM can be cost-optimized after validation.
- Three separate hardware UARTs serve the hashboards. Hashboard, PSU and display I2C use separate hardware controllers. Four hardware PWM outputs and four GPIO tach inputs serve the fans.
- J1-J15 retain bitcrane connector pin assignments. J16 keeps its footprint but changes from RP2040 SWD to **pin 1 TX, pin 2 GND, pin 3 RX**, at 3.3 V. USB SBU pins formerly used for SWD are NC.
- All bitcrane address-strap and fan-header fitted/DNP choices are preserved. The original mixes 2x2 and 1x4 fitted fan headers; each channel's two footprints are alternative ways to connect one fan.
- All cross-sheet signals use global labels. Internal circuit nets use local labels. Every physical BOM entry has an MPN field; test pads and mounting holes use explicit PCB-feature identifiers.

## Verification

The selected CLI is `/Users/skot/.backplane-bend/kicad/10.99.0-bp.6/bin/kicad-cli`. Reports, netlists and page renders are under `../../build/MujinaControl-S19/`. The semantic checker verifies all 129 SoC package contacts, miner connector net assignments, original DNP choices, sequencing connections, and exact preservation of the bitcrane outline and connector positions.

The KiCad IPC startup timed out and its tool explicitly authorized file editing as fallback. The generator constructs and round-trips structured S-expressions, then the actual KiCad CLI reopens the saved design for ERC/netlist/render verification. No original bitcrane or research CAD was edited. A saved schematic milestone is in `../../backups/MujinaControl-S19/erc-clean-milestone/`.

`scripts/build_schematic.py` is the initial authoring source. **Do not rerun it after editing the schematic manually:** it replaces the generated sheets and scaffold. `scripts/validate_design.py` is read-only and validates the exported reports. Use the normal KiCad editing workflow for later revisions.

## Before layout signoff

1. Confirm actual S19 hashboard and PSU voltages, reset/plug polarity, PSU enable polarity, cable-side I2C pull-ups and powered/unpowered behavior. Connectivity parity with bitcrane is not a measured compatibility test.
2. Validate cold-start, slow-ramp, brownout, reset and shutdown behavior on all rails. Check supervisor thresholds including tolerance/hysteresis, regulator transient response and effective ceramic capacitance. Confirm the fixed 0.9 V CPU operating points; do not inherit Raven's overclock or enable unrestricted DVFS.
3. Bring up the selected UART/PWM/I2C pin groups in the BSP, using `docs/pin-allocation.md`. Check UART throughput and 128 MB application memory use. Implement PWM inversion, fan tach counting and watchdog/failure behavior. These firmware changes are not implemented here.
4. Verify NAND support in the exact boot ROM/loader/BSP and flash/recovery tools. A bootable NAND takes precedence over microSD. Test the recovery key and USB enumeration.
5. Complete a datasheet-to-footprint audit, especially the SoC exposed pad, NAND exposed pad, MagJack, reused connector variants, crystal, inductors and microSD. Core part lookups were performed; this is not a full sourcing review. The selected 3.3 uH / 4.7 uH inductors and DM3D-SF socket were not found in the fab's in-stock catalog snapshot and need sourcing or substitution.
6. Develop the PCB stackup and floorplan. The scaffold retains bitcrane's existing two-layer file structure; a four-layer implementation is recommended for the SoC and power/return routing, but has not been laid out. Check RJ45 height, front-panel space and mounting clearance. Validate the PMOS and connectors for the actual fan current.
7. Tune crystal loading/drive, USB signal integrity and Ethernet magnetics/ESD performance on hardware. Conduct thermal and EMC checks. ERC does not prove any of these properties.

## Sources and attribution

- `../../bitcrane-v3.1/`: connector pinout, populated options, outline, mounting holes and placement reference; original README states CERN OHL v2. Original files are preserved.
- `../../research/rv1106/`: supplied research, including Rockchip datasheet Rev 2.2, Table 2-1 and Table 3-2; hardware design guide sections 2.1-2.3; Luckfox Pico Pro/Max; and Raven1106 v1.1.
- Raven supplied the starting RV1106 package-pin definition, QFN footprint/model, and storage reference. Its complete SBC circuitry was not copied. Its documented USB-mux and optional-flash limitations were considered. The supplied research notes did not find a top-level Raven license; clarify reuse/redistribution terms before publishing these derived library assets.
- [Diodes AP63200/AP63203/AP63205 datasheet](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf): regulator pinouts, feedback equation, soft-start and passive selection.
- [TI TPS3808 datasheet](https://www.ti.com/lit/ds/symlink/tps3808.pdf): open-drain reset, monitor thresholds, manual reset and CT-open delay. The project-local symbol corrects RESET to open-drain for wired-AND operation.
- [Bourns SRN6028C datasheet](https://bourns.com/docs/Product-Datasheets/SRN6028C.pdf): selected larger inductors; complete footprint verification before layout.
- [Nexperia PESD3V3Y1BSF datasheet](https://assets.nexperia.com/documents/data-sheet/PESD3V3Y1BSF.pdf): bidirectional Ethernet-pair ESD devices and DSN0603 package.

Standard KiCad symbols and only the required standard footprints are snapshotted into project-local libraries, alongside the inherited custom libraries. Their original license and attribution markings remain applicable.
