# Schematic validation - revision 0.1

Validated with Backplane KiCad 10.99.0 on 2026-11-01.

- 10 sheets, 261 physical components, 193 nets.
- ERC: **0 errors, 0 warnings**, with all severities requested and no added exclusions.
- 438 semantic checks passed, including all 129 SoC package contacts, the miner connector mappings, original strap/header DNP states and sequencing connections.
- Exact bitcrane Edge.Cuts and J1-J16 / H1-H4 footprint placement/orientation retained: 110 x 100 mm.
- PCB parsed/exported successfully; no inherited tracks, vias or copper zones remain. It is an unrouted scaffold.
- Project-local symbols and footprints resolve under the selected CLI.

Machine-readable evidence: `../../../build/MujinaControl-S19/validation.json`, `erc.json`, and `design.xml`. Page renders are in the adjacent `render/` folder.

This verifies the saved design structure and selected connectivity invariants. It does not validate electrical operation, operating-point choices, sequencing margins, component package/rating suitability, sourcing, signal integrity, miner compatibility or firmware. See the project README for the remaining engineering checks.

Backplane viewer confirmed the canonical files under `boards/MujinaControl-S19/`. Its history repository had no commits when checked; explicit milestone backups were retained under `backups/MujinaControl-S19/`.
