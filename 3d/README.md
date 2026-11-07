# MujinaControl-S19 3D models

Models are stored within this project and referenced through `${KIPRJMOD}/3d/` in both the local footprint libraries and the PCB. See `manifest.json` for sources, hashes, references and transforms. No placement or electrical geometry was changed.

Coverage: 249 physical components on the current PCB have a model. Four mounting holes and two bare test pads intentionally have none. The libraries also contain models for J15 and R274–R277, which are present in the schematic but not yet on the PCB.

## Model fidelity and limitations

- D201/D202 use `proxies/L_0201_0603Metric.step`: a generic black 0201 package with a measured 0.6 × 0.3 × 0.3 mm envelope. This matches the SOD962 body envelope but is NOT the exact diode CAD; terminal shape is approximate. The manufacturer's [SOD962 model](https://www.nexperia.com/packages/SOD962) download returned HTTP 403.
- U130 and L205 use downloaded SamacSys VRML preview models for W25N02KVZEIR TR and SRN6028C-3R9M. They work in KiCad 3D/VRML output, but are not STEP solids and will be omitted from STEP assembly exports. The STEP download requires a signed-in supplier session. U130 measures 8 × 6 × 0.75 mm after unit/orientation conversion; L205 sits at approximately 0.003–2.64 mm above the PCB.
- L204/L210 use the correct KiCad APV ANR6028 STEP model as PCB-instance overrides. They still share the existing Bourns copper footprint. Preserve their instance 3D models when updating footprints from libraries; the shared library's default model is Bourns. Copper land-pattern qualification is outside this model-only change.
- Standard passives and small packages use nominal KiCad package models, not individually certified manufacturer models. Do not treat nominal height as a maximum-tolerance enclosure clearance.
- J2 now uses the correct GCT USB4105 model. Q1 now uses PowerDI3333, rotated to the existing pin-1 corner. J100 uses the Raven HR911105A model/transform with identical footprint pad coordinates. The other bitcrane connector transforms are retained.
- FreeCAD is not installed. Backplane's STEP renderer reported that it could not mesh the models. Numerical mesh/bounds checks and a native KiCad VRML export passed; visual fit review remains outstanding. Install FreeCAD from https://www.freecad.org/downloads/ (Backplane finds `freecadcmd` on PATH, or use `BACKPLANE_FREECAD`).

## Provenance

KiCad model license and README are included. Bitcrane's project license is included for its copied assets. Vendor and third-party model files retain their own provenance; the KiCad license is not applied to those files. No STEP/VRML geometry was rewritten.

The model-only update was backed up under `backups/MujinaControl-S19/models-20261102T192514Z`. Verification and the coverage report are under `build/MujinaControl-S19/models/` in the repository root.

The canonical board was saved, read back, and opened with `viewer_show` in the 3D tab; the returned path matches the canonical file. Existing history was preserved, but its repository has no HEAD/commits, so history synchronization could not be verified.
