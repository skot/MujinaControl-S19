# Controller fuse removal

Removed F100 at the user's request on 2026-11-01. The former +12V_CTRL rail is now connected directly to +12V_FAN, downstream of Q1. Removed the redundant controller power flag and rail label; replaced the fuse and adjacent wire fragments with one straight wire. Updated the root architecture and power-sheet notes. The catalog mapping now excludes F100.

## Protection retained and changed

The native netlist confirms J1 positive connects to Q1 drain pins 5–8, and Q1 source pins 1–3 feed the fan/controller rail. Q1 is the P-channel DMP3013SFV-7. R270 connects its gate to ground, and D2 has its cathode on the source rail and anode on the gate. This is the existing reverse-input-polarity blocking arrangement; it is independent of F100 and remains unchanged. See the [MOSFET manufacturer datasheet](https://www.diodes.com/_files/datasheets/DMP3013SFV.pdf) for terminal assignments and device characteristics.

D220 (SMBJ15A) still provides transient suppression on the protected rail. Removing F100 removes the controller branch's local fault-current disconnection. An input-rail short or failed-short TVS now relies on upstream protection. Q1 is not an electronic current limiter. The upstream supply and wiring's fault response has not been qualified by this schematic edit; the drawing states this dependency explicitly.

## Verification

- Staged native netlist proved that F100 is the only physical component removed; every other component attribute and pin assignment is preserved except the requested merge of +12V_CTRL into +12V_FAN.
- Canonical native netlist: 260 physical components, 192 nets. ERC: zero violations.
- Readability: zero errors, 74 existing cross-group-wire advisories retained. No new errors or advisories.
- Visually reviewed all ten sheets as a contact sheet; inspected the two changed pages, root and power/service, at readable zoom. Eight other page renders are pixel-identical to the previous verified renders. Direct wiring is continuous; no spurious fuse-end junction dots remain.
- PCB, project and companion metadata unchanged. No placement or routing performed.
- IPC was unavailable with an explicit documented direct-file fallback. Changes were staged, parsed and netlist-validated, then promoted to the exact canonical files after a full project backup. Saved canonical files were read back and displayed in Backplane.
- Backplane history has no commits, so history synchronization cannot be verified. Existing history is preserved; the explicit backup is recorded below.

[Verification](../../../build/MujinaControl-S19/remove-fuse/verification.json) · [Backup path](../../../build/MujinaControl-S19/remove-fuse/backup.txt) · [Power circuit render](../../../build/MujinaControl-S19/remove-fuse/power-detail.png)

Earlier generator scripts and reports are historical drafting artifacts and still contain the former fuse design. Do not run them to regenerate the canonical schematic; the saved canonical hierarchy is authoritative.
