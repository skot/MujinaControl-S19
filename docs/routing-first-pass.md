# Routing work in progress

Canonical board: `../MujinaControl-S19.kicad_pcb`. Routing began with RV1106 local connections and escapes, followed by regulator blocks and 5 V distribution. Work continues; this is not a finished layout.

## Saved routing milestone

767 track segments and 167 through-vias. Power distribution is on the front/back layers; low-speed control routes also use the designated In3.Cu signal layer. All 255 footprint instances, all schematic sheets, project settings and the existing custom rules are unchanged. The smallest actual plated drill is now 0.30 mm and the fabrication record has been updated. C285 was inspected but not moved: C283/C284 are the local U115 input bypass capacitors.

- Initial RV1106 escapes, decoupler, clock and flash connections. The control-routing passes added 45 connections across 28 nets; 21 control nets with external destinations are now fully copper-connected. Twelve control-net connections and several critical local links remain incomplete.
- Removed 17 superseded fanout vias and 11 dangling track segments, checking native pad connectivity after every removal. No dangling-track warnings remain.
- All six buck switch-node paths are connected. The four adjustable feedback dividers and two fixed-output feedback inputs have verified copper paths to their output capacitors.
- The 5 V output is copper-connected to all five downstream regulator inputs. Distribution uses 1.5 mm back-layer tracks and paired through-vias.
- Local power traces use 0.8 mm where possible, with short 0.6 mm package-constrained sections. Feedback routes use 0.2 mm and avoid the projected switch copper/inductor regions where routed on the back layer.
- Ground-return vias were placed at local passives and regulators. Four exposed-pad vias sit between U100's existing paste windows. Reference planes are not yet filled, so these returns are unfinished.

Native connectivity verification passed all 21 regulator/distribution checks. Final native DRC reports 162 violations: the 59 pre-existing silk, J2 hole-clearance and J16 library findings, plus 103 dangling vias belonging to unfinished signal/plane connections. No new copper-clearance, short-circuit, track-width or drill-clearance violations were introduced. There are no dangling-track warnings. **454 missing pad-group connections remain**, confirmed independently through native copper-connectivity queries. This is an initial routing milestone, not a completed board.

The saved PCB was visually inspected in top, bottom, inner-signal and SoC close-up renders. All 255 footprint instances are unchanged, including their attributes and 3D models. Schematics, project settings and fanout rules remain byte-identical to the pre-routing backup.

## Sizing basis

The supplied Rockchip guide specifies peak currents of 1.6 A for the core and 0.4 A each for CPU and DDR. The buck circuitry has a 2 A output rating. Local power routing was conservatively checked at 2 A with 35 µm outer copper using the IPC-2221 external-trace estimate, a 20 °C rise budget and resistance at 60 °C (40 °C ambient assumption). Estimated rises are 9.6 °C for 0.8 mm and 15.5 °C for 0.6 mm traces. A 4 mm, 0.6 mm section drops about 7.6 mV at 2 A; a 15 mm, 0.8 mm section drops about 21 mV. The 1.5 mm 5 V distribution has a 100 mV drop budget; the longest branch is about 84 mm, approximately 64 mV at a conservative 2 A before the short terminal links and parallel-via losses. These are routing estimates, not board thermal qualification.

The [regulator datasheet](https://www.diodes.com/assets/Datasheets/AP63200-AP63201-AP63203-AP63205.pdf) calls for compact input loops, close feedback parts and ground vias, and recommends 2 oz copper for thermal performance. This project retains its chosen 1 oz outer copper; completed ground copper and thermal validation remain necessary. No copper-weight setting was changed.

The [local fanout rules](rv1106-fanout-rules.md) remain active. Fine-pitch neckdowns are not bulk-current paths. USB/Ethernet impedance geometry and SD/flash width, spacing and timing still require a dedicated pass using the selected [stackup](pcb-stackup.md). Initial flash routes are provisional, not impedance-qualified.

## Remaining work

Complete the remaining low-speed RV1106 control nets, complete the remaining decouplers and both oscillator circuits (in particular RTC_XIN and OSC_XOUT), finish flash/SD and USB/Ethernet with impedance and timing checks, distribute the regulated rails, and complete reference/return planes and stitching. U130's central ground return remains to be addressed. Keep every originally fixed footprint unmoved.

The 12 V input/fan trunk has not been sized or routed: the maximum fan current per connector was requested and remains pending. The logic-regulator routing can proceed independently.

Evidence is in `../../../build/MujinaControl-S19/routing/`, including native connectivity and preservation checks, saved DRC reports, routing decisions, sizing assumptions, and top/bottom/SoC renders. `backup.txt` identifies the pre-routing backup. All edits use native KiCad IPC with canonical saves; existing history is preserved.

## Control-routing follow-up

Unfinished control connections: DEBUG_TX, FAN3_TACH, HB0_PLUG, HB1_PLUG, HB1_RST_N, HB1_RX, HB2_RST_N, HB2_RX, HB2_TX, HB_SCL, RESET_N and STATUS_LED. These remain open after the bounded routing passes; they are not declared unroutable. The current schematic/netlist has only one pad each for DISPLAY_SCL and DISPLAY_SDA, so no external endpoint exists to route on those two nets.

Both monitored shell jobs had unreliable watcher status. The actual routing process completed with exit code 0, and saved geometry, per-net DRC checks and native connectivity were inspected afterward. No duplicate CAD writer was started.

Backplane displayed the exact canonical saved PCB, and its blob matches the thread history checkpoint. Existing history and companion metadata were preserved.
