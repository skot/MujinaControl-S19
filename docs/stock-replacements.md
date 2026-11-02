# Stock replacements — 2026-11-01

Historical selection record: F100 was subsequently removed at the user’s request. Its entry below is no longer part of the current BOM. See [fuse removal](fuse-removal.md).

Updated the hidden MPN, Manufacturer, LCSC and Datasheet fields for five schematic components. Values, US resistor symbols, connections and drawing geometry are unchanged. Stock below is the fab's catalog snapshot, not reserved inventory; all five are extended parts.

| Reference | Previous MPN / code | Selected MPN / code | Stock |
|---|---|---|---:|
| R216 | RC0402FR-07316KL / C185427 | Yageo AC0402FR-07316KL / C226987 | 2,174 |
| R218 | RC0402FR-07665KL / C274355 | Yageo AC0402FR-07665KL / C227183 | 7,300 |
| F100 | 0466002.NR / C187595 | Littelfuse 0466002.NRHF / C3105 | 63,780 |
| L204 | SRN6028C-3R3M / C19947651 | APV ANR6028T3R3M / C7427149 | 4,005 |
| L210 | SRN6028C-4R7M / C19947654 | APV ANR6028T4R7M / C7427151 | 2,258 |

## Electrical and package checks

R216/R218 retain 316 kΩ / 665 kΩ, ±1%, 0402, 62.5 mW, 50 V and ±100 ppm/°C. These automotive-grade AC parts preserve the monitor divider ratios. See the [Yageo AC series datasheet](https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_YAGEO-AC0402FR-07316KL_C226987.pdf), including ordering codes, dimensions and electrical specifications.

F100 stays in the same 466 fast-acting, thin-film 1206 family. HF denotes halogen-free construction. The 2 A part is rated 63 V AC/DC, 50 A interrupting capacity, nominal cold resistance 0.031 Ω and nominal melting I²t 0.2326 A²s. The existing drawing's 32 V requirement remains conservative; the substitution does not raise the circuit's voltage rating. See the [Littelfuse 466 datasheet](https://www.lcsc.com/datasheet/lcsc_datasheet_1810111920_Littelfuse-0466002-NRHF_C3105.pdf), pages 1 and 3.

Both APV inductors preserve nominal inductance and ±20% tolerance, resin shielding, nominal 6 × 6 mm body and 2.8 mm maximum height. Operating range is −45 to +125 °C including self-heating (the former Bourns family specifies −55 °C minimum). This selection is for the existing indoor controller application, not an extension of its environmental qualification.

| Reference | Inductance | DCR maximum | Irms typical | Isat typical |
|---|---:|---:|---:|---:|
| L204 | 3.3 µH ±20% | 33 mΩ | 3.8 A | 4.5 A |
| L210 | 4.7 µH ±20% | 39 mΩ | 3.4 A | 3.3 A |

APV defines Isat at approximately 30% inductance loss and Irms at 40 °C temperature rise. The datasheet additionally lists lower current-column values of 3.53/4.21 A for L204 and 3.13/3.05 A for L210; these also exceed the estimated continuous-load RMS/peak currents. The current column headings are oddly labelled “Max.” and “Typ.”; they should not be treated as a guaranteed hot-temperature minimum saturation current.

At 2 A load and nominal switching frequency, using minimum inductance, estimated peak current is about 2.35 A for the 5 V → 1.792 V L204 rail, and 2.35 A for the 12 V → 5 V L210 rail. Maximum-DCR copper dissipation is approximately 0.133 W and 0.158 W respectively. The DCR maxima are slightly above the former Bourns 28.8/36 mΩ maxima; these are not identical-loss substitutions. Normal thermal and transient validation is still required on hardware.

Sources: [APV ANR series datasheet](https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2309201138_APV-ANR6028T3R3M_C7427149.pdf), pages 2, 14, 15 and 19; [Bourns SRN6028C datasheet](https://bourns.com/docs/Product-Datasheets/SRN6028C.pdf). Downloaded manufacturer PDFs and catalog evidence are retained in `build/MujinaControl-S19/stock-replacements/`.

## Footprint limitation before layout

The assigned local `Inductor_SMD:L_Bourns-SRN6028` has 1.6 × 5.7 mm copper pads at x = ±2.35 mm. APV recommends 1.7 × 5.7 mm pads with a 2.8 mm gap (centres ±2.25 mm). Existing pads overlap the APV nominal 1.7 × 4.9 mm terminal lands by 1.45 × 4.9 mm, so the terminals fit the copper. This is not an exact match to APV's recommended land pattern.

**Before PCB placement, qualify a dedicated APV footprint with its recommended pads and an enlarged courtyard.** APV's maximum body is 6.3 × 6.3 mm; the inherited courtyard is only 6.6 × 6.2 mm. A 6.8 × 6.8 mm courtyard would provide 0.25 mm clearance around the maximum body. Do not interpret the present Bourns footprint name/model as an exact APV mechanical qualification. This requirement is also saved in each inductor's hidden Assembly Note field. No PCB or footprint-library file was changed in this sourcing task.

## Saved-file verification

- Canonical fields read back from native KiCad XML; only the approved hidden metadata changed in the five symbols.
- All 193 named net partitions, values, footprints and US resistor symbols preserved.
- ERC: zero violations. Readability: zero errors, 74 retained cross-group wire advisories.
- All ten rendered pages pixel-identical to the previously reviewed drawing. Full-page contact sheet reviewed; changed regulator, qualification and input-power circuits inspected at readable zoom. No new drawing issues.
- PCB and project files byte-identical to the immediate backup; companion metadata preserved.
- Canonical root shown successfully in Backplane. History still has no commits, so history synchronization cannot be verified; an explicit complete project backup was made.

[Verification](../../../build/MujinaControl-S19/stock-replacements/verification.json) · [Catalog evidence](../../../build/MujinaControl-S19/stock-replacements/selected-parts.json) · [Backup path](../../../build/MujinaControl-S19/stock-replacements/backup.txt)
