# MujinaControl-S19

An open-hardware Antminer S19 controlboard built around the Rockchip RV1106G2, for [Mujina](https://mujina.org) mining firmware. It keeps the bitcrane v3.1 form factor, outline, mounting holes and miner connectors, and replaces bitcrane's RP2040 with a Linux-capable SoC, Ethernet and local storage.

**Status (2026-11-12):** schematic complete, PCB placed and fully routed on six layers. ERC 0; DRC 0 violations, 0 unconnected items, 0 schematic-parity issues. Every purchased part has a fab (LCSC) part number. **Not yet reviewed for manufacturing and not built or tested.** Do not order until the review below is done.

Open `MujinaControl-S19.kicad_pro` with **KiCad 10.99 or later**. The files use a newer format than KiCad 10.0 can read.

## Hardware

- **SoC:** RV1106G2 with 128 MB in-package DDR3L, 24 MHz crystal and RTC crystal.
- **Storage:** W25N02KVZEIR 2 Gbit (256 MB) SPI NAND on the quad-SPI bus, following the Luckfox Pico Pro/Max, plus a microSD socket. A bootable NAND takes precedence over microSD.
- **Network and USB:** 100BASE-TX through the SoC's internal PHY and an integrated MagJack. USB-C device port for recovery and console; VBUS is detection-only, so **12 V must be present for USB recovery**.
- **Power:** 12 V from J1's 6-pin input (pins 1–3 positive, 4–6 ground) through reverse-polarity P-MOSFET Q1 (NTTFS008P03P8Z) and an SMBJ15A TVS. There is no controller fuse. Six TPS62933 bucks: 12 V → 5 V system (2 A budget), then sequenced 0.9 V core, 0.9 V CPU, 1.35 V DDR, 1.8 V and 3.3 V. Five TPS3808 supervisors (trip at about 90 % of each rail) qualify the sequence and hold reset.
- **Hashboards:** three ports, each with its own hardware UART, sharing one hashboard I²C bus; BCB100-style I²C/UART pull-ups and plug-detect pull-downs, and a TPS22919 switched 3.3 V supply per port, enabled directly by SoC GPIOs.
- **Fans:** four independent channels, PWM and tach, each sized for 3 A; the input stage carries all four fans plus the board. Each channel has both a 1×4 2.54 mm and a 2×2 4.2 mm footprint; fit one. Two 100 µF bulk capacitors on the fan rail.
- **PSU and accessories:** PSU I²C and enable, accessory header J15 (display I²C, GPIO, 5 V / 3.3 V), console UART on J16 (pin 1 TX, 2 GND, 3 RX, 3.3 V), RESET and BOOT (maskrom) right-angle buttons beside the Ethernet jack.

J1–J14 keep bitcrane's pin assignments. The SoC pin allocation is in `docs/pin-allocation.md`.

## Schematic

Ten sheets: system overview, SoC interfaces, sequenced regulators, power qualification, SoC supply and bypass, boot storage and clocks, Ethernet and USB, hashboard interfaces, fan interfaces, input power and service. Cross-sheet signals use global labels; resistors use US-style symbols.

## PCB

- 110 × 100 mm, six layers, nominal 1.6 mm FR-4, ENIG, 1 oz outer / 0.5 oz inner, using the fab's JLC06161H-3313 stackup (`docs/pcb-stackup.md`).
- Layers: F.Cu signals and parts; In1 ground; In2 3.3 V plane with islands for core, DDR, 1.8 V, 5 V and 12 V; In3 slow signals; In4 ground; B.Cu signals.
- 310 footprints, 1925 tracks, 774 vias. All vias are 0.45 mm diameter / 0.30 mm drill; minimum track 0.127 mm (SoC escapes and Ethernet pairs).
- USB, Ethernet, SD card and SPI NAND are length-matched within the RV1106 hardware-guide limits.
- Each regulator follows the TPS62933 datasheet layout, with its own stitched ground pour. 414 ground vias in total; wherever a via is allowed, no point is more than 6 mm from one.
- Reference designators are hidden on the silkscreen; only the RESET and BOOT labels are printed.

Routing details, measurements and history are in `docs/routing-current.md`. The other routing documents describe the board before the 2026-11-10 rip-up.

## Assembly and parts

The board is meant to be assembled by the fab. Every purchased part carries `LCSC` and `MPN` fields: 65 part numbers, 24 basic, 5 preferred and 36 extended, checked against live stock on 2026-11-12. The RV1106G2 needs the fab's standard (not economic) assembly. Stock was low for Q1 and the hashboard connectors J3–J5. See `docs/bom-fab-stock.md`. Fab settings are in `MujinaControl-S19.fab.json` (`order: false`).

## Before ordering

1. **Manufacturing review.** The routing was largely laid by a grid search: it is rule-clean but not tidy. The east-side hashboard lines are long (up to 117 mm) with up to 9 vias. They are slow signals, but they should be reviewed and could be shortened.
2. **Hashboard and PSU compatibility.** Confirm the real S19 hashboard and PSU voltages, reset and plug-detect polarity, PSU-enable polarity and powered/unpowered behaviour. Matching bitcrane's connections is not a measured compatibility test.
3. **Power.** Check cold start, slow ramp, brownout and shutdown on all rails, the supervisor thresholds, and regulator transient response. Measure Q1 and the 12 V copper at the full four-fan load. Upstream wiring must protect against shorts, as there is no controller fuse.
4. **Footprints and parts.** Audit the footprints against datasheets, especially the SoC and NAND exposed pads, MagJack, crystals, inductors and microSD. Re-check stock before ordering.
5. **Firmware.** Bring up the UART, PWM and I²C pin groups, fan tach, hashboard power GPIOs, NAND boot and USB recovery in the BSP. Keep the CPU at its fixed 0.9 V operating point.
6. **On hardware.** Tune the crystals; check USB and Ethernet signal integrity, ESD, thermals and EMC.

## Files

- `MujinaControl-S19.kicad_pro` with ten `.kicad_sch` sheets, `.kicad_pcb` and `.kicad_dru` (custom rules).
- `lib/`, `models/`, `3d/`: project-local symbols, footprints and 3D models.
- `docs/`: design notes for each change (stackup, placement, regulators, routing, parts).
- `scripts/`: the original generator `build_schematic.py`. **Do not rerun it**; it would overwrite the hand-edited schematic. `validate_design.py` and `verify_readability.py` are read-only checks.
- Check reports, renders and working evidence are kept outside this repository, in `build/MujinaControl-S19/` at the workspace root.

## Sources and attribution

- [Braiins BCB100](https://github.com/braiins/BCB100): open-source S19 control board (CERN-OHL-S v2), used as the reference for hashboard interface biasing and logic-power control (I2C/UART pull-ups, plug-detect pull-downs and per-port switched 3.3 V). Thanks to Braiins for publishing it.
- [bitcrane](https://github.com/skot/bitcrane) v3.1 (CERN-OHL v2): form factor, outline, mounting holes, connector pinouts and placements, fan-header options, and the inherited `bitaxe` and `bitcrane` libraries.
- Raven1106 v1.1: starting RV1106 package-pin definition, QFN footprint and model, and storage reference. Its full SBC circuit was not copied. No top-level licence was found for Raven; clarify reuse terms for the derived library assets before publishing them more widely.
- Luckfox Pico Pro/Max: SPI NAND reference.
- Rockchip RV1106 datasheet Rev 2.2 and hardware design guide: pin functions, power and layout rules.
- [TI TPS62933](https://www.ti.com/lit/ds/symlink/tps62933.pdf), [TI TPS3808](https://www.ti.com/lit/ds/symlink/tps3808.pdf), [TI TPS22919](https://www.ti.com/lit/ds/symlink/tps22919.pdf), [onsemi NTTFS008P03P8Z](https://www.onsemi.com/download/data-sheet/pdf/nttfs008p03p8z-d.pdf) and [Nexperia PESD3V3Y1BSF](https://assets.nexperia.com/documents/data-sheet/PESD3V3Y1BSF.pdf) datasheets.

Standard KiCad symbols and footprints are copied into the project-local libraries. Their original licence and attribution markings still apply.

## License

CERN Open Hardware Licence v2, Strongly Reciprocal (`LICENSE`).
