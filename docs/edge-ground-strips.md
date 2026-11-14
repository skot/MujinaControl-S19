# Exposed ground strips at the left and right edges

2026-11-14. The board slides into metal slots in the miner's case. Both side edges now carry a bare, gold-finished ground strip on the top and the bottom, like the stock control board, so the slots make contact with ground.

## What was added

- **Copper:** four ground zones (`Edge ground strip west/east F.Cu/B.Cu`), solid, priority 12, from the outermost board edge (x = 58.26 and 168.26) to 3.7 mm inside it (x = 61.96 and 164.56), over the full height of the board. The fill stops 0.3 mm short of the board edge, as everywhere else on the board, so the bare copper is 3.4 mm wide.
- **Solder mask:** openings on `F.Mask` and `B.Mask` over the same 3.7 mm, following the outline. With the ENIG finish the strips come out gold.
- **Notches and the bottom step:** where the outline steps in by 3 mm (the notch at y 50.5–55.7 and the lower 5 mm of each side) only 0.7 mm of the band is left, 0.4 mm of it copper.
- **Stitching:** 20 new ground vias (11 west at x = 60.1, 9 east at x = 166.4) between the existing ones, so each strip ties into the two ground planes at most 6.5 mm apart outside the notch.
- The mounting-hole pads H1–H4 overlap the strips and merge with them.

## What it touched

Nothing had to move: the two bands held only ground vias and the mounting pads. The 12 V input copper beside J1 on the top and bottom layers is cut back by the strip and now ends 0.5 mm from it. No part, track or other zone outline changed.

## Not done

- **The edge walls are not plated.** Copper reaching and wrapping the board edge needs the fab's edge-plating option and a rule exception for copper at the edge; it was left out because the slots grip the faces of the board. Say so if wrap-around plating is wanted.
- Fit against the real case has not been checked: the strip width comes from the request (3.7 mm), not from a measurement of the slots here. The J1 body ends 0.2 mm inside the east strip's inner edge.

## Checks

DRC with schematic parity: 0 violations, 0 unconnected, 0 parity issues. 329 footprints, 2199 tracks, 856 vias, 40 zones. Evidence: `build/MujinaControl-S19/edge/` (`survey.py`, `apply.py`, `mask.py`, `drc1.json`, renders).
