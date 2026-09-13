# V3 master progress tracker

Updated: 2026-09-13. This is the **only implementation progress tracker** for
V3. Requirements and decisions live in [REQUIREMENTS.md](REQUIREMENTS.md);
architecture and process are described in [DEVELOPMENT_SUMMARY.md](DEVELOPMENT_SUMMARY.md).
Research reports hold evidence, not competing task-status lists.

Assistant scope: complete schematic, PCB layout and the first preliminary BOM
for exactly one ESP32-S3R8, with pin-capability and design-review evidence (DEC-022). **Stop at that design/BOM handoff.** The owner manages production;
Mellow manufactures and performs initial functional testing (DEC-019).
Physical bring-up, production management and application/OTA/test-firmware
implementation are downstream responsibilities, not assistant deliverables.
No separate thermal-design exercise or continuous 1.5 A RMS rating is required;
use the Fly TMC2209 StepStick/passive-heatsink reference for room-temperature use.

Current stage: **owner authorized the V2-based restart (DEC-021).** The rejected
draft, library copies and generators were moved to local rollback: 83 files,
all hashes checked; see [cleanup evidence](research/rejected-draft-cleanup.json).
The V2 archive and necessary references remain unchanged. G-01 is complete. The corrected five-sheet native schematic is captured.
KiCad ERC reports 0 errors / 0 warnings; 116 intended nets and 551 connected endpoints
reconcile, with 37 explicit NC endpoints. Independent schematic review and its
bounded drawing recheck are complete. **G-02 is waiting for owner approval of B1.**
Open the [review package](review/README.md); all remaining qualifications are recorded below.
No V3 PCB exists. Review evidence from the earlier rejected draft is superseded.

[V2 circuit and OWMC style study](research/V2_DESIGN_STUDY.md) records the direct
reading of all four V2 sheets, native PCB/footprints and both OWMC schematic pages.
DEC-020 limits changes to the Pico replacement, integrated drivers and external
display connection, subject to the existing agreed compatibility requirements.
Use the owner's hierarchical-sheet style, no more than five sheets total,
installed KiCad libraries first and V2's practical hand-solder footprint intent.
No CAD edits were made during the study. The subsequent reset is now authorized.
G-02 still requires independent review
of the completed schematic and explicit owner approval before PCB implementation.

## Status rules

- **Done**: the stated deliverable and exit evidence exist; record the link.
- **In progress**: active work with an identified next action.
- **Waiting**: a named decision, dependency, hardware item or external result is needed.
- **Planned**: authorized work has not started.
- **Paused**: the owner stopped implementation; do not resume dependent work.
- **Reopened**: earlier completion no longer satisfies corrected requirements;
  redo the affected definition/review before the gate can pass.
- **External**: recorded downstream work owned by the user/Mellow; not an
  assistant deliverable or a prerequisite to calling the preliminary handoff done.
- Track discovered corrective actions here using stable IDs; do not mark a
  phase complete because an analyzer ran or a draft file exists.
- Update the affected row and the short change log after meaningful work.
  Requirements agreement and verification are different from task completion.
- **G-01 is mandatory before any V3 schematic implementation. G-02 is mandatory
  before PCB implementation.** Do not substitute ERC for independent review or
  the agent's own judgment for explicit owner approval.
- Approval attaches to the exact reviewed schematic revision. Material changes
  reopen the affected review and approval; generated artifacts must follow it.

## Work register

| ID | Work | Status | Exit evidence / next action |
| --- | --- | --- | --- |
| R-01 | Audit and refresh workspace electronics skills | Done | Pinned upstream release, provenance/backups and tool validation in [skills record](../.agents/SKILLS.md) |
| R-02 | Extract V2.1 baseline and reference inventories | Done | Native geometry, nets and source hashes in [design inventory](research/design-inventory.json); application sources in [application inventory](research/application-inventory.json) |
| R-03 | Maintain requirements and scope | In progress | DEC-020/021 constrain and resume the V2-based design; DEC-022 excludes firmware rework and application-port analysis. Keep requirements and active design evidence synchronized. |
| R-04 | Initial mechanical incompatibility research | Done | mechanical_compatibility agent: MECH-01..07 in [research report](COMPATIBILITY_RESEARCH.md); corrective actions below remain open |
| R-05 | Initial electrical incompatibility research | Done | electrical_compatibility agent: ELEC-01..13 in [research report](COMPATIBILITY_RESEARCH.md), with source/manufacturer evidence and limits |
| R-06 | Initial static firmware compatibility research | Done | firmware_feasibility agent: FW-01..12 and candidate peripheral allocation in [research report](COMPATIBILITY_RESEARCH.md); pin-capability scope now recorded under V-00 |
| R-07 | Mellow/Fly catalog and QSPI fallback research | Done | mellow_display_research agent: verified Mellow candidates do not meet strict QSPI; TDO TS040WVS02CP-B1617A is a sourced QSPI lead requiring qualification, DISP-05 |
| R-08 | Fly TMC2209 reference investigation | Done | Official revision 1.0 schematic, UART/heatsink illustrations and adaptation limits recorded in [research report](COMPATIBILITY_RESEARCH.md#fly-tmc2209-reference-implementation); no separate thermal-design project |
| R-09 | TDO selected-candidate desk qualification | Done | [TDO evidence](COMPATIBILITY_RESEARCH.md#tdo-desk-qualification): numbered pins, 8/12/9-signal options and actual ESP32 transport code reviewed; example targets another panel/touch. Supplier and sample closure remains A-05 |
| R-10 | Resolve servo baseline from the sourcing guide | Done | [Pinned guide](https://github.com/eamars/OpenTrickler/blob/6a0b9711194d59aa796af89c6224d7331031c4ff/Manual/sourcing_guide.md#servo-motors) names MG90S, recommends full metal/180 degrees and links item 1005004550692203. Model/source question closed; current evidence remains A-03 |
| R-11 | Study V2 circuits/assembly intent and OWMC schematic style | Done | [Direct study](research/V2_DESIGN_STUDY.md): four V2 sheets, power/serial/output/motor nets, placed footprints, hand-solder intent and two OWMC pages with explicit parent/child ports. Establishes scope/style, not electrical release |
| C-01 | Audit and clean copied reference assets | Done | Initial copied-reference cleanup, [83-file rejected-draft cleanup](research/rejected-draft-cleanup.json) and [18 unused datasheets](research/unused-datasheets-cleanup.json) complete with hash-checked rollback copies. V2 archive untouched. |
| C-02 | Establish self-contained project libraries/resources | Done | [Resource audit](design/library-audit.json): all 166 instances use installed KiCad assets; zero custom symbols/footprints. The [datasheet cache](datasheets/README.md) records retained evidence and download gaps. Exact pad/source qualifications remain B-02. |
| C-03 | Maintain documentation and artifact references | Done | Current READMEs, requirements, pin check, design/power descriptions, source cache and [B1 review index](review/README.md) match the corrected design. Local links, source hashes and untouched V2 baseline checked at this gate. |
| A-01 | Architecture and interface contract | Done | [Intended circuit](design/net-intent.json): V2-based controller, two onboard drivers and external display connection. Main PD required for USB service; no controller power mux or display-selection circuitry. |
| A-02 | Exact GPIO/peripheral/memory allocation | Done | [Independent pin-capability check](research/PIN_CAPABILITY_CHECK.md): physical pin36=GPIO48/pin37=GPIO47, R8 reserved pads, nativeUSB19/20 and all required functions. Motor EN uses GPIO42/48. |
| A-03 | Electrical power and transient budget | Done | [Power design](POWER_ARCHITECTURE.md) records the two-servo/four-LED plus controller/display planning allocation and its limits. Retain V2's TPS5450 capacity; actual servo/display peaks and aggregate PD demand remain external P-04 measurements, not a guaranteed simultaneous-load rating. |
| A-04 | Connector and mechanical contract | Done | [V2 mechanical inventory](research/design-inventory.json) and [direct study](research/V2_DESIGN_STUDY.md) define outline/holes/retained datums. Applying and locking them in a fresh PCB remains L-01 after owner approval. |
| A-05 | Qualify the external QSPI display connection | In progress | TDO numbered connector, QSPI/direct-touch pin capability and voltage interfaces are captured. Supplied FFC contact orientation, maximum module load and Mellow sourcing remain B-02/DISP-05 qualifications. One display is physically connected at a time. |
| A-06 | Specify intended netlist, net classes and clearances | Done | [116 named nets/endpoints](design/net-endpoints.json) and [numeric classes/clearances](design/net-classes.json) recorded before capture. Stackup-dependent impedance geometry is an explicit routing-stage assumption. |
| A-07 | Specify schematic hierarchy and drawing conventions | Done | [Five-sheet hierarchy](design/hierarchy.json): populated parent, four coherent children; both motors on one sheet, matching sheet pins/hierarchical labels, no global labels. |
| G-01 | Pre-schematic readiness gate | Done | [Initial pre-capture gate](design/pre-capture-gate-initial.json) predates corrected CAD. The [current contract](design/pre-capture-gate.json) includes subsequent L4/Q2 part amendments; 166 instances, all pin/pad resources resolve. Later source/package checks are explicit. |
| S-01 | MCU core schematic | Done | B1 populated parent captures the ESP32 core, flash/clock/RF/reset/EEPROM and available spare GPIO. Independent review remains V-03. |
| S-02 | Power and programming/service schematic | Done | B1 power child retains V2 PD/TPS5450, adds AP63203 and separate USB data service/pads. SERVICE_VBUS has no board-supply connection. |
| S-03 | Two onboard TMC2209 schematic blocks | Done | B1 motors child contains both complete TMC2209 channels, external 0.11 ohm / 1 W sensing, shared UART and V2 phase-connector order. |
| S-04 | Retained display headers and external QSPI connector | Done | B1 display child retains EXP1/2 and adds an external TDO 20-contact FFC plus necessary touch/interface parts. |
| S-05 | Retained serial/output/storage and additional I/O schematic | Done | B1 interfaces child retains serial/output ports; a receiver-selection shunt avoids output contention and AHCT buffers accept 3.3 V high at 5 V. EEPROM/spare GPIO are on the parent. |
| B-01 | First preliminary BOM and component candidates | In progress | Export from the corrected design with per-board references/quantities, exact MPN/package and LCSC/Mellow source evidence. Rejected draft candidate counts are not a preliminary BOM handoff |
| B-02 | Symbol/footprint and population-variant audit | In progress | All stock symbol/pad sets resolve; J8, TPS5450 and Sunlord land patterns are identified. Finish actual FFC/cable, switch/model, bulk-capacitor and supplier/package qualifications; preserve DNP service socket and RF tuning options in the preliminary BOM. |
| V-00 | ESP32 pin-capability check | Done | Owner clarified: only establish that pins can serve their purpose; firmware needs rework separately. Independent pin-capability review passed; capture/export reconciliation remains V-01. |
| V-01 | Schematic electrical review and ERC | Done | [Native ERC](review/erc.json): 0 errors / 0 warnings. [Reconciliation](review/connectivity-check.json): 116 nets, 551 connected and 37 NC endpoints match. Final five-page render inspected; [independent findings](review/INDEPENDENT_SCHEMATIC_REVIEW.md) are dispositioned below. |
| V-03 | Mandatory independent schematic review against requirements | Done | [Independent B1 review](review/INDEPENDENT_SCHEMATIC_REVIEW.md) and drawing-only renewal complete. Verdict: suitable for owner schematic review; no remaining definitive connection blocker. Exact native/export/image hashes recorded; ISR-02..06 remain bounded qualifications. |
| G-02 | Owner approval of reviewed schematic | Waiting | Owner approval of the exact [B1 review package](review/README.md), identified by [artifact hashes](review/package-manifest.json), is required before PCB implementation under REQ-PROC-007. No approval has been inferred. Schematic review is ready; no V3 PCB exists. |
| L-01 | Create and lock V2.1-compatible PCB geometry | Planned | After G-02, create a fresh V3 PCB using full archived V2.1 outline/corners, mounting and connector-fixing datums. OWMC PCB is reference-only and is not a starting layout |
| L-02 | Placement, RF and heatsink layout | Planned | Fit power/core/interface blocks and heatsinks against A-04; use a real Mellow stack-up, sound return paths and ordinary manufacturer exposed-pad/copper/via practices |
| L-03 | Routing and copper zones | Planned | Route required nets, USB/RF and power paths, fill zones and inspect return paths; depends on accepted placement and schematic |
| L-04 | PCB DRC and schematic-to-PCB reconciliation | Planned | Disposition all DRC/connectivity findings, then recheck critical connector/pin mapping and physical clearances |
| V-02 | EMC, reference-layout and manufacturing review | Planned | Source-backed layout assessment, applicable electrical calculations and explicit prototype validation gaps; no fabrication-readiness claim from DRC alone and no separate thermal-design exercise |
| P-01 | Design and first preliminary-BOM handoff; assistant endpoint | Planned | Deliver self-contained schematic/PCB, review and owner-approval records, static/ERC/DRC evidence, preliminary BOM and relevant export/interface/assembly/test notes. Clearly list downstream validation gaps; no claim of a physically tested production release |
| P-02 | Initial hardware bring-up | External | Mellow: assembled-hardware rail, PD/service, recovery and interface checks; owner coordinates production. Test-image/fixture provision is arranged downstream |
| P-03 | First-prototype QSPI and retained Mini12864 demonstration | External | Mellow/owner: demonstrate actual selected QSPI panel and Mini12864 separately. REQ-DISP-004 remains a product acceptance requirement; no assistant runtime result is claimed |
| P-04 | Load, fault and normal-operation prototype checks | External | Mellow/owner: measure agreed loads/transients, power loss/reset/hot-plug and source isolation; observe operation with passive heatsinks. Formal continuous 1.5 A RMS qualification remains excluded |
| P-05 | Production and tested-revision release | External | Owner manages production, purchasing and release; Mellow manufactures and performs initial functional testing. Final production BOM, actual test records and as-built changes are downstream of the assistant's P-01 handoff |

## Dependencies requiring decisions or evidence

| Item | Current position | Work affected |
| --- | --- | --- |
| QSPI panel | TDO TS040WVS02CP-B1617A is the selected 3.95-inch QSPI target. Board pin suitability is checked. Supplied connector/cable geometry, maximum current and Mellow sourcing remain qualifications; firmware driver work is excluded by DEC-022 | A-05, B-02, external P-03 |
| Driver reference implementation | Fly reference identified under R-08. Adapt its support circuitry and heatsink construction using manufacturer guidance; exact supplied IC identity and full V3 component ratings remain engineering/BOM work. Thermal scope is settled by DEC-016 | S-03, B-01/B-02, L-02 |
| Servo load evidence | Use two MG90S servos from the guide's full-metal 180-degree recommendation and item 1005004550692203. Identity question is closed; current/transient evidence is engineering work, with physical measurement by Mellow if needed | A-03, S-02, external P-04 |
| Extra I/O | Scope settled by DEC-017: remaining usable native 3.3 V GPIOs on a 2/2.54 mm control header, lower priority and no minimum count. Finish required display/service/power resources before assigning spares | A-02, S-05 |
| Manufacturing inputs | Owner handles production; Mellow manufactures and performs initial tests. Document design-critical stack-up/assembly assumptions and per-board BOM quantities. Batch size, purchasing, production budget and scheduling are not assistant prerequisites | B-01/B-02, L-02, P-01; external P-02/P-05 |

## Compatibility actions

The following register retains initial research evidence. Its suggested circuitry,
operating modes and mitigation methods must be reassessed under DEC-020 before
implementation; a previous Planned/In-progress entry does not authorize keeping
that feature. The reopened work register above controls current execution.

| Finding | Action | Status | Completion evidence needed |
| --- | --- | --- | --- |
| MECH-01 | Create and lock the complete V2.1 PCB mechanical baseline | Planned | DEC-018 corrects the initial WIP assumption: no V3 PCB exists. Compare fresh L-01 geometry with archived V2.1, including outline/corners, holes and connector fixings |
| MECH-02 | Preserve DB9 fixing drills, shell overhang and mating geometry | Planned | Selected connector drawing matched to the archived placed footprint |
| MECH-03 | Establish J8 power connector identity and preserve actual mating geometry | Done | GCT USB4125 stock footprint preserves the studied mating body/anchor; source pin mapping uses SH instead of old S1. Stock land differences are documented for PCB application. |
| MECH-04 | Preserve connector side, rotation, key/latch direction and pad-to-function mapping | Planned | Connector compatibility matrix and cable/plug fit check |
| MECH-05 | Design actual driver/heatsink assemblies and relocate conflicting internal components | Planned | Placement/collision review including capacitors and access to motor/EXP plugs |
| MECH-06 | Replace unrealistic archived stack-up metadata with a real fabrication stack-up | Planned | Mellow stack-up, thickness and connector-Z assumptions documented before routing |
| MECH-07 | Define actual new display and programming-fixture interfaces | Waiting | Selected display pinout and factory fixture/contact geometry |
| ELEC-01 | Correct the four 5 V buffer input-threshold/enable implementations | Done | U5-U8 use SN74AHCT1G125DBVR with the V2 pin-compatible SOT23-5 function and a guaranteed 3.3 V input high at 5 V. |
| ELEC-02 | Isolate/select J3 versus MAX3232 receive sources | Done | J17 selects TTL or RS232 RX with a 3-pin shunt. Both V2 external connector pin maps remain; native export shows no tied receiver outputs. |
| ELEC-03 | Separate raw PD and service/controller/accessory net names and protection references | Done | Separate VMOTOR/V5V/V3V3/SERVICE_VBUS names and physical endpoints reconcile. Service 5 V never joins board rails. |
| ELEC-04 | Extract the complete MCU support circuit across reference sheet boundaries | Done | One ESP32-S3R8 core is captured with power, clock, flash, RF and reset support. OWMC PMIC was not adopted. |
| ELEC-05 | Close memory/strapping/peripheral pin constraints | Done | Independent pin check and native net reconciliation close numbered memory/strap/USB/peripheral allocation. |
| ELEC-06 | Record operating limits and apply the requested Fly/heatsink reference | In progress | B1 captures the Fly/manufacturer driver support approach and excludes a continuous 1.5 A RMS claim. Apply ordinary exposed-pad/copper/heatsink practices during L-02; physical observations remain external P-04. |
| ELEC-07 | Implement complete bare-IC TMC2209 channels and sensing contract | Done | Independent B1 review checks both numbered TMC2209 circuits, external 0.11 ohm / 1 W sensing and the range calculation. Exact shunt MPN and supplied OTP variant remain B-02; runtime configuration is external. |
| ELEC-08 | Handle motor-driver reset while controller service power remains present | Done | Main PD powers service operation; driver EN defaults inactive. PC-only controller operation is not implemented. Physical attach/reset testing remains external. |
| ELEC-09 | Account for local motor capacitance and regenerative/fault energy | In progress | Local motor bulk capacitors are captured. Retained raw-PD topology has no new reverse blocker or clamp; ISR-05 records the unmeasured regenerative/transient limitation. Review copper/layout in L-02 and leave rail-excursion tests to P-04. |
| ELEC-10 | Define inactive-display isolation and verify signal levels | In progress | One physically connected display at a time; power-off cable changes. Pin/voltage mapping is captured; exact Mini KILL-link and supplied FFC/module checks remain ISR-03/04. |
| ELEC-11 | Complete Type-C service and factory recovery interface | Done | Independent CC pulldowns, USB data isolation and factory VBUS/DP/DN/GND/BOOT/EN/sense pads are captured; native ERC and net checks pass. Main PD is required. |
| ELEC-12 | Revalidate antenna placement/matching in V3 | Planned | Exact antenna identity, clearance/stack-up and tuning provisions; measured RF evidence |
| ELEC-13 | Close the 5 V load/transient budget before reducing converter rating | External | No converter reduction is made. The retained capacity and planning allocation are documented in A-03; representative servo/display demand and rail droop are Mellow/owner P-04 measurements. |
| FW-01 | Specify the ESP32 platform and initialization contract | External | DEC-022 excludes firmware rework/application-port analysis. Hardware pin capability is covered by A-02; firmware implementation and runtime acceptance belong to the owner/Mellow. |
| FW-02 | Complete both display modes' pin/resource/reset ownership | Done | DEC-022 limits work to pin purpose. Mini controls and external QSPI/direct touch fit the completed allocation. |
| FW-03 | Document ESP32 GPIO/interrupt migration requirements | External | DEC-022 excludes firmware rework/application-port analysis. Hardware pin capability is covered by A-02; firmware implementation and runtime acceptance belong to the owner/Mellow. |
| FW-04 | Establish waveform peripheral/clock/timing contract | Done | Pins support the required PWM/step/pixel functions through ESP32 peripherals. Exact firmware scheduling and runtime timing are outside scope by DEC-022. |
| FW-05 | Specify driver UART and current-unit contract | Done | UART addresses 0/1, separate STEP/DIR/EN, external 0.11 ohm sensing and RMS units are recorded. Actual current/communication tests remain external. |
| FW-06 | Qualify display-driver feasibility and exclusive initialization contract | External | DEC-022 excludes firmware rework/application-port analysis. Hardware pin capability is covered by A-02; firmware implementation and runtime acceptance belong to the owner/Mellow. |
| FW-07 | Define QSPI input and future UI/mirroring contract | External | DEC-022 excludes firmware rework/application-port analysis. Hardware pin capability is covered by A-02; firmware implementation and runtime acceptance belong to the owner/Mellow. |
| FW-08 | Budget fitted flash/PSRAM/internal memory | External | DEC-022 excludes firmware rework/application-port analysis. Hardware pin capability is covered by A-02; firmware implementation and runtime acceptance belong to the owner/Mellow. |
| FW-09 | Define controller-only service and restart output behavior | Done | Main PD is required; USB VBUS is sensing only. Boot pin behavior is checked without depending on application firmware. |
| FW-10 | Specify native USB loading and ROM recovery | Done | GPIO19/20 native USB and BOOT/RESET contacts are allocated. Physical blank-board loading/recovery is Mellow testing. |
| FW-11 | Document EEPROM schema/CRC/identity handoff | External | DEC-022 excludes firmware rework/application-port analysis. Hardware pin capability is covered by A-02; firmware implementation and runtime acceptance belong to the owner/Mellow. |
| FW-12 | Document radio/serial hardware and application expectations | External | DEC-022 excludes firmware rework/application-port analysis. Hardware pin capability is covered by A-02; firmware implementation and runtime acceptance belong to the owner/Mellow. |
| DISP-01..04 | Disposition documented Mellow products against the strict QSPI requirement | Done | [Sourced candidate comparison](COMPATIBILITY_RESEARCH.md): ordinary SPI, UART smart screen, host computer and HDMI/DSI alternatives do not meet the present requirement |
| DISP-05 | Qualify selected TDO QSPI candidate for Mellow sourcing | Waiting | TDO numbered host interface and pin capability are captured. Exact WAIT/touch output levels, load, cable and supplier confirmation remain ISR-03 before final connector/BOM commitment. No supplier contact or order was made. |

## Independent B1 review dispositions

The [independent report](review/INDEPENDENT_SCHEMATIC_REVIEW.md) holds the review
basis and findings. Their live work status is recorded only here.

| Finding | Status | Disposition and responsible stage |
| --- | --- | --- |
| ISR-01 | Done | Q2 changed to BSS138LT1G with the same 1=gate, 2=source, 3=drain mapping; independent amended-part check passed. GPIO44 may assert touch reset at boot; driving it low releases reset. |
| ISR-02 | Planned | B-02 / before final component and PCB commitment: establish C8 switching-frequency ESR/filter suitability or qualify an equivalent capacitor. Nominal ripple/package evidence alone does not close TPS5450 loop stability. |
| ISR-03 | Waiting | B-02 / A-05: supplied TDO assembly must establish FFC contact face/pin-1 mapping, maximum/inrush load and WAIT/touch-interrupt electrical outputs. Board pin capability is checked; physical demonstration remains external P-03. |
| ISR-04 | Waiting | B-02 / P-03: verify the supplied Mini12864 revision and cable have no KILL link that shorts retained EXP2.10 +5 V when pressed. The dedicated button buffer addresses input voltage, not a panel-internal short. |
| ISR-05 | External | Mellow/owner P-02/P-04: power cycling, USB attach/detach, servo/display transients and motor deceleration. Retained raw PD topology has no added voltage qualification or specified regenerative-energy absorption. No such test result is claimed. |
| ISR-06 | In progress | B-01/B-02: choose exact commodity passives, effective ceramic capacitance, low-inductance shunts and mechanical variants. D4 is nominated as MDD SS54/C22452 in SMA and still needs source/package qualification. No positive lifecycle/stock result exists. |

## Current decisions that should not be reopened without cause

- Motor Expansion Board V3: V2.1 plus Pico replacement, onboard TMC2209s and an
  external display connector. OWMC is the schematic-style/selective MCU reference.
  At most five sheets total; explicit hierarchical ports, standard KiCad assets
  first and V2's larger hand-solder footprint intent (DEC-020).
- Exactly one directly fitted ESP32-S3R8 MCU.
- OWMC assets are reference-only; there is no pre-existing V3 CAD. Cleanup,
  self-contained libraries and net/clearance/hierarchy specification precede
  schematics. Independent schematic review precedes explicit owner approval,
  which gates PCB implementation (DEC-018).
- Archived V2.1 board dimensions, mounting pattern and existing connector
  placement preserved. No mandatory existing enclosure or component-height fit.
- Required compatible 12 V PD PSU retained; main power and service access separate.
- Two onboard TMC2209s, 800 mA RMS default and adjustment up to 1.2-1.5 A RMS;
  passive heatsinks and Fly StepStick reference for room-temperature use.
  No separate thermal design or continuous 1.5 A RMS board rating is required;
  the upper setting is not the recommended normal operating point (DEC-016).
- Two sourcing-guide MG90S servos plus four board-powered external LEDs; display load additional.
- Mini12864 retained; one display mode at a time; selected 3.5-4 inch QSPI
  display required on prototype one, without encoder or physical buttons in that mode.
- Keep QSPI and qualify TDO TS040WVS02CP-B1617A for Mellow sourcing (DEC-015).
- Remaining usable native GPIOs go to a 2/2.54 mm 3.3 V control header, lower
  priority with no minimum count; 2.54 mm is the starting choice (DEC-017).
- Complete schematic, PCB layout and first preliminary BOM, then hand off.
  Check pin-purpose suitability only; firmware rework and application-port
  analysis are excluded (DEC-022). Owner/Mellow handle production and physical
  testing (DEC-019).
- Servo baseline is MG90S as specified in the OpenTrickler sourcing guide;
  model/source selection is settled and should not be asked again (DEC-019).

## Change log

- 2026-09-13: DEC-021 authorizes the reset. Reversibly moved and hash-verified
  83 rejected draft/tool/library files; kept V2.1, necessary references and
  datasheets. Corrected specification underway; no new CAD captured yet.
- 2026-09-13: Owner rejected the expanded 15-sheet draft, library duplication,
  small-footprint defaults and product/display scope drift; stopped CAD work.
  Completed direct V2 circuit/footprint and OWMC hierarchy/style study (R-11).
  Reopened architecture, pin allocation, netlist, hierarchy/library work and G-01;
  marked schematic/BOM implementation paused. Earlier clean ERC/native-netlist
  results apply only to the rejected draft. No PCB exists and no CAD was modified
  during this study. Independent final schematic review/owner approval remain open.
- 2026-09-12: Created the single master tracker at the user's request. Launched
  separate read-only mechanical, electrical and firmware research agents plus
  Mellow/Fly display research. Linked the tracker from root guidance and README.
  Existing research and tooling evidence are recorded as completed; schematic
  implementation, PCB placement/routing and hardware validation remain open.
- 2026-09-12: Integrated all four completed investigations and the bounded QSPI
  fallback search into [COMPATIBILITY_RESEARCH.md](COMPATIBILITY_RESEARCH.md).
  Added individual compatibility actions and a distinct final firmware-feasibility
  gate. Updated confirmed one-MCU, display-size/control, mechanical-freedom and
  hardware-only development scope. No CAD or firmware source was changed.
- 2026-09-12: Captured DEC-015/016/017 and removed superseded thermal-envelope
  and extra-I/O-purpose questions. Completed official Fly TMC2209 reference
  research and selected TDO desk qualification. The upper current setting
  does not establish a continuous board rating. Source isolation, electrical
  load budgeting and normal manufacturer layout practices remain in scope.
- 2026-09-12: Added the user's seven process requirements under DEC-018 and
  REQ-PROC-001..007. Corrected the copied-reference-versus-V3 distinction;
  introduced cleanup/resource tasks and mandatory pre-schematic and owner-approval
  gates. Independent dependency/cleanup audit launched before moving assets.
- 2026-09-12: Completed C-01 after the independent audit. Preserved and hash-checked
  203 files / 50,481,575 bytes in local rollback, retained only five justified
  reference files, and established clean CAD/library documentation. Replaced
  local-workspace source links with reference snapshots or pinned repository
  citations, including the Trinamic submodule's own revision. No V3 CAD was created.
- 2026-09-12: Documentation/cleanup validation passed: 32 requirement IDs,
  including all seven process requirements; 41 work-register entries; 121 local
  links and 267 file-hash checks. No active CAD exists. Git whitespace checks
  passed; external application checkouts remain clean and OWMC retains only its
  pre-existing power-sheet modification. These checks do not establish electrical
  correctness or pass either design gate.
- 2026-09-12: DEC-019 confirms complete schematic/PCB plus the first preliminary
  BOM as the assistant endpoint. Assigned production to the owner and manufacturing/
  initial testing to Mellow; kept downstream acceptance in this same tracker as
  External work. Resolved MG90S identity/source from the guide and removed batch,
  budget/schedule and physical-test ownership questions from assistant prerequisites.

- 2026-09-13: Captured the corrected five-sheet B1 schematic after G-01. All
  assets are shipped KiCad libraries. Native ERC0/0 and116nets/551connected/37NC
  reconciliation pass. Independent review started. DEC-022 narrows firmware
  work to pin-purpose suitability. L4 resolved to stock Sunlord4.7uH within
  the AP63203 permitted range; original pre-capture gate retained as evidence.

- 2026-09-13: Completed independent B1 schematic review and bounded drawing
  renewal. Corrected Q2 low-voltage MOSFET choice, readable revision fields and
  shared motor ground graphics. Native ERC remains 0/0; 116 nets, 551 connected
  and 37 NC endpoints reconcile. Qualified pin purpose only under DEC-022.
  Added all six independent findings to this tracker, retained explicit source/
  prototype gaps, cleaned 18 unused datasheets with hash-checked rollback and
  prepared the exact review package. G-02 waits for owner approval; no PCB work
  or production has started.
