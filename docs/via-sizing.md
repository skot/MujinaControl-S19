# Through-via sizing update — 2026-11-07

Changed all 166 existing through-vias to 0.45 mm copper diameter and 0.30 mm drill, including power and ground vias, as requested. Positions, nets, layer spans, tenting and identifiers are preserved. Default netclass, via preset, board-wide minimum diameter, and local RV1106 diameter rule now use this size; minimum via annulus is 0.075 mm. Track width, clearance and drill minima are unchanged.

The fab’s [published capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/), checked 2026-11-07, prefer a 0.15 mm difference between via diameter and drill. This size does not fall under its listed small-via surcharge conditions for multilayer boards.

Two existing F.Cu ground segments at y=97.18 mm were extended 0.55 mm each to adjoining via centers (x=113.60 and 114.80 mm), restoring ground continuity that had depended on the larger lands. No footprints moved. Native readback after reopening confirms all via sizes, all 255 footprint definitions and placements, and only these two track endpoint changes. Session-generated parent-board identifiers are excluded from comparisons.

Fresh CLI DRC reports the exact same 161 findings and the same 454 unconnected item pairs as before the edit: 102 dangling vias from unfinished routing, 40 silk overlaps, 16 silk-edge clearances, two existing J2 hole clearances and one J16 library mismatch. There are no new findings. Routing remains unfinished.

Board and custom rules were saved to their canonical paths. The headless runtime kept project settings read-only on ordinary save; a native SaveCopyOfDocument with include_project produced a validated project file in the build directory. That native output was promoted to the backed-up canonical project, then reopened and read back successfully. No CAD text edits were used.

Evidence and backup location: `../../../build/MujinaControl-S19/via-resize/`. All schematic sheets are byte-identical to the backup. Backplane displays the canonical board. The current board and project match automatic history checkpoint blobs; the custom-rule file is saved and validated, but no matching automatic history blob was found for it. Existing history was preserved.
