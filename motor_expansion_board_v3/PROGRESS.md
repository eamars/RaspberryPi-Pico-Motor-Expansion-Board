# V3 master progress tracker

Updated: 2026-09-12. This is the **only implementation progress tracker** for
V3. Requirements and decisions live in [REQUIREMENTS.md](REQUIREMENTS.md);
architecture and process are described in [DEVELOPMENT_SUMMARY.md](DEVELOPMENT_SUMMARY.md).
Research reports hold evidence, not competing task-status lists.

Assistant scope: complete schematic, PCB layout and the first preliminary BOM
for exactly one ESP32-S3R8, with static firmware-feasibility and design-review
evidence. **Stop at that design/BOM handoff.** The owner manages production;
Mellow manufactures and performs initial functional testing (DEC-019).
Physical bring-up, production management and application/OTA/test-firmware
implementation are downstream responsibilities, not assistant deliverables.
No separate thermal-design exercise or continuous 1.5 A RMS rating is required;
use the Fly TMC2209 StepStick/passive-heatsink reference for room-temperature use.

Current stage: requested compatibility and reference investigations complete;
pre-design cleanup and specification work are in progress. **No V3 schematic or
PCB exists yet.** Copied OWMC files are reference material only (DEC-018).
The consolidated
[research report](COMPATIBILITY_RESEARCH.md) records MECH-01..07, ELEC-01..13,
FW-01..12 and DISP-01..05.
Next deliverable: a clean, self-contained project resource structure and the
pre-schematic connectivity, clearance and hierarchy specification. Schematic
implementation cannot begin until gate G-01 passes.

## Status rules

- **Done**: the stated deliverable and exit evidence exist; record the link.
- **In progress**: active work with an identified next action.
- **Waiting**: a named decision, dependency, hardware item or external result is needed.
- **Planned**: authorized work has not started.
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
| R-03 | Maintain requirements and scope | In progress | DEC-001 through DEC-019 captured in [requirements](REQUIREMENTS.md); complete design and first preliminary BOM, then owner/Mellow handle production and initial testing |
| R-04 | Initial mechanical incompatibility research | Done | mechanical_compatibility agent: MECH-01..07 in [research report](COMPATIBILITY_RESEARCH.md); corrective actions below remain open |
| R-05 | Initial electrical incompatibility research | Done | electrical_compatibility agent: ELEC-01..13 in [research report](COMPATIBILITY_RESEARCH.md), with source/manufacturer evidence and limits |
| R-06 | Initial static firmware compatibility research | Done | firmware_feasibility agent: FW-01..12 and candidate peripheral allocation in [research report](COMPATIBILITY_RESEARCH.md); final production feasibility remains V-00 |
| R-07 | Mellow/Fly catalog and QSPI fallback research | Done | mellow_display_research agent: verified Mellow candidates do not meet strict QSPI; TDO TS040WVS02CP-B1617A is a sourced QSPI lead requiring qualification, DISP-05 |
| R-08 | Fly TMC2209 reference investigation | Done | Official revision 1.0 schematic, UART/heatsink illustrations and adaptation limits recorded in [research report](COMPATIBILITY_RESEARCH.md#fly-tmc2209-reference-implementation); no separate thermal-design project |
| R-09 | TDO selected-candidate desk qualification | Done | [TDO evidence](COMPATIBILITY_RESEARCH.md#tdo-desk-qualification): numbered pins, 8/12/9-signal options and actual ESP32 transport code reviewed; example targets another panel/touch. Supplier and sample closure remains A-05 |
| R-10 | Resolve servo baseline from the sourcing guide | Done | [Pinned guide](https://github.com/eamars/OpenTrickler/blob/6a0b9711194d59aa796af89c6224d7331031c4ff/Manual/sourcing_guide.md#servo-motors) names MG90S, recommends full metal/180 degrees and links item 1005004550692203. Model/source question closed; current evidence remains A-03 |
| C-01 | Audit and clean copied reference assets | Done | Independent dependency audit completed; all 203 imported files moved to verified rollback. [Cleanup inventory](research/asset-cleanup.json) and [five retained references](references/manifest.json) preserve evidence. Active CAD area has documentation only; archived V2.1 is untouched |
| C-02 | Establish self-contained project libraries/resources | In progress | [Library conventions](pcb/libraries/README.md) and [adoption manifest](pcb/libraries/manifest.json) created; no foreign production assets adopted yet. Qualify needed parts, create local tables as assets are adopted, and verify fresh-checkout resolution |
| C-03 | Maintain documentation and artifact references | In progress | Existing-V3 assumption and moved links corrected; portable citations recorded. [Current validation](research/documentation-validation.json) passes; keep READMEs/exports synchronized with every later revision under REQ-PROC-002 |
| A-01 | Architecture and interface contract | In progress | [Power architecture](POWER_ARCHITECTURE.md) and [overview](DEVELOPMENT_SUMMARY.md) drafted; reconcile compatibility findings and freeze settled blocks |
| A-02 | Exact GPIO/peripheral/memory allocation | In progress | Preliminary count exists; complete pin-level matrix after R-05/R-06/R-07, including straps, memory, USB, display, diagnostics and spare I/O |
| A-03 | Electrical power and transient budget | In progress | Complete source/rail/transient budgets for two servos, four LEDs, selected display, controller and drivers; upper motor software setting is not a continuous board-current rating |
| A-04 | Connector and mechanical contract | In progress | Include complete rounded outline, all connector fixing holes/body/key datums and placed J8 geometry from MECH-01 through MECH-04; select new service/display/heatsink geometry |
| A-05 | Qualify the selected TDO QSPI display interface for design | Waiting | Desk work R-09 done. Exact B1617A assembly/driver/touch/power/drawing/cable facts must support the schematic. Distinguish interface feasibility from downstream Mellow sourcing and sample demonstration; physical acceptance remains P-03 |
| A-06 | Specify intended netlist, net classes and clearances | Planned | REQ-PROC-005: complete named-net/endpoint and connector-pin contract plus numeric clearance matrix, width/via rules and basis before schematic work. Later exported netlist must match this specification |
| A-07 | Specify schematic hierarchy and drawing conventions | Planned | REQ-PROC-006: top-level functional blocks, child-sheet responsibilities/ports, signal flow, power/decoupling context, symbol/text grid and junction/label conventions |
| G-01 | Pre-schematic readiness gate | Waiting | C-01/C-02 preparation, A-01 through A-07 and initial critical-part/library checks must establish complete circuit-affecting contracts. No unresolved net/pin/clearance assumptions may silently pass into schematic implementation |
| S-01 | MCU core schematic | Planned | One ESP32-S3R8, flash/PSRAM configuration, clock, reset/boot, RF and decoupling checked against reference and manufacturer evidence |
| S-02 | PD, rail conversion, protection and service power schematic | Planned | Implement A-03 and power modes, reverse-current blocking, voltage qualification and unpowered-domain behaviour |
| S-03 | Two onboard TMC2209 schematic blocks | Planned | Correct support circuitry/current configuration and retained motor interfaces, with passive-heatsink implementation constraints |
| S-04 | Mini12864 and selected QSPI display schematic | Waiting | A-05 must establish the selected assembly's connector, control/input method, voltage and GPIO contract |
| S-05 | Retained serial/output/storage and additional I/O schematic | Planned | Preserve external cable compatibility, levels and functions; expose remaining usable native GPIOs on a 2/2.54 mm control header with GND, using 2.54 mm as the starting point; no minimum count |
| B-01 | First preliminary BOM and component candidates | In progress | Fill symbol properties and export per-board references/quantities, exact MPN/package, LCSC or Mellow source, population/alternate notes and dated evidence. Explicitly flag unconfirmed supply/validation; no order quantities, purchasing or final production allocation |
| B-02 | Symbol/footprint and population-variant audit | Planned | MECH-03/07: resolve J8 actual connector identity versus misleading library/model naming, and replace reference display/service placeholders with verified interfaces; audit all part/pad mappings and variants |
| V-00 | Final static firmware-feasibility gate | Waiting | REQ-VER-001: exact panel, completed GPIO/peripheral/memory/reset matrix and disposition of hardware-affecting FW findings. Initial research alone does not pass this gate |
| V-01 | Schematic electrical review and ERC | Planned | Critical pin/rail review, power and reset cases, applicable calculations/simulation and disposition of all findings; depends on S-01 through S-05 |
| V-03 | Mandatory independent schematic review against requirements | Planned | REQ-PROC-007: independent agent reviews the exact schematic revision, requirement matrix, intended/exported nets, ERC, BOM/footprints, hierarchy/readability and power/reset cases; findings and dispositions recorded before G-02 |
| G-02 | Owner approval of reviewed schematic | Planned | Prepare completed V-01/V-03 evidence and exact revision/hash for owner review. Explicit owner approval is required before PCB implementation. Not ready to request approval yet; no approval is inferred from earlier authorization to design |
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
| QSPI panel | TDO TS040WVS02CP-B1617A is the user-selected 3.95-inch QSPI qualification target. Exact driver/touch, connector/cable/drawing, maximum current and Mellow sourcing evidence remain necessary | A-05, A-02/A-03, S-04, P-03 |
| Driver reference implementation | Fly reference identified under R-08. Adapt its support circuitry and heatsink construction using manufacturer guidance; exact supplied IC identity and full V3 component ratings remain engineering/BOM work. Thermal scope is settled by DEC-016 | S-03, B-01/B-02, L-02 |
| Servo load evidence | Use two MG90S servos from the guide's full-metal 180-degree recommendation and item 1005004550692203. Identity question is closed; current/transient evidence is engineering work, with physical measurement by Mellow if needed | A-03, S-02, external P-04 |
| Extra I/O | Scope settled by DEC-017: remaining usable native 3.3 V GPIOs on a 2/2.54 mm control header, lower priority and no minimum count. Finish required display/service/power resources before assigning spares | A-02, S-05 |
| Manufacturing inputs | Owner handles production; Mellow manufactures and performs initial tests. Document design-critical stack-up/assembly assumptions and per-board BOM quantities. Batch size, purchasing, production budget and scheduling are not assistant prerequisites | B-01/B-02, L-02, P-01; external P-02/P-05 |

## Compatibility actions

| Finding | Action | Status | Completion evidence needed |
| --- | --- | --- | --- |
| MECH-01 | Create and lock the complete V2.1 PCB mechanical baseline | Planned | DEC-018 corrects the initial WIP assumption: no V3 PCB exists. Compare fresh L-01 geometry with archived V2.1, including outline/corners, holes and connector fixings |
| MECH-02 | Preserve DB9 fixing drills, shell overhang and mating geometry | Planned | Selected connector drawing matched to the archived placed footprint |
| MECH-03 | Establish J8 power connector identity and preserve actual mating geometry | In progress | Exact manufacturer drawing/pad mapping; no automatic stock-footprint substitution by name |
| MECH-04 | Preserve connector side, rotation, key/latch direction and pad-to-function mapping | Planned | Connector compatibility matrix and cable/plug fit check |
| MECH-05 | Design actual driver/heatsink assemblies and relocate conflicting internal components | Planned | Placement/collision review including capacitors and access to motor/EXP plugs |
| MECH-06 | Replace unrealistic archived stack-up metadata with a real fabrication stack-up | Planned | Mellow stack-up, thickness and connector-Z assumptions documented before routing |
| MECH-07 | Define actual new display and programming-fixture interfaces | Waiting | Selected display pinout and factory fixture/contact geometry |
| ELEC-01 | Correct the four 5 V buffer input-threshold/enable implementations | Planned | Selected part satisfies 3.3 V input-high, output drive and power-off/reset behavior |
| ELEC-02 | Isolate/select J3 versus MAX3232 receive sources | Planned | Retained connector mapping with no competing receiver drive in supported modes |
| ELEC-03 | Separate raw PD and service/controller/accessory net names and protection references | Planned | Native connectivity review proves no accidental VBUS merge or high-voltage USB clamp connection |
| ELEC-04 | Extract the complete MCU support circuit across reference sheet boundaries | Planned | RF/core supplies, reset, boot and USB support remain complete after PMIC removal |
| ELEC-05 | Close memory/strapping/peripheral pin constraints | In progress | Exact A-02 matrix, including memory voltage and reliable recovery states |
| ELEC-06 | Record operating limits and apply the requested Fly/heatsink reference | Planned | DEC-016 settles scope; R-08 identifies reference. Review ordinary manufacturer implementation in S-03/L-02 and record normal bring-up observations; no formal thermal model or continuous 1.5 A RMS claim |
| ELEC-07 | Implement complete bare-IC TMC2209 channels and sensing contract | Planned | Datasheet support circuit, fitted sensing/OTP assumptions and firmware units agree |
| ELEC-08 | Handle motor-driver reset while controller service power remains present | Planned | Power validity, hardware inhibition and deliberate reinitialization contract checked in P-02/P-04 |
| ELEC-09 | Account for local motor capacitance and regenerative/fault energy | Planned | Power-switch, clamp and discharge assessment plus measured rail excursion |
| ELEC-10 | Define inactive-display isolation and verify signal levels | Waiting | Selected modules, connection rules, pin pull-up rails and power-off limits known |
| ELEC-11 | Complete Type-C service and factory recovery interface | Planned | CC/data/power paths and GPIO0/EN fixture access verified in all adopted service modes |
| ELEC-12 | Revalidate antenna placement/matching in V3 | Planned | Exact antenna identity, clearance/stack-up and tuning provisions; measured RF evidence |
| ELEC-13 | Close the 5 V load/transient budget before reducing converter rating | Waiting | Representative servo and selected-display demand plus controller losses quantified |
| FW-01 | Specify the ESP32 platform and initialization contract | Planned | Document SDK/toolchain choice, task-stack/startup differences and application handoff; test-target implementation is downstream |
| FW-02 | Complete both display modes' pin/resource/reset ownership | In progress | A-02 matrix covers power/service/diagnostic signals and justified spare I/O count |
| FW-03 | Document ESP32 GPIO/interrupt migration requirements | Planned | Address high-numbered GPIOs and queue-initialization ordering in static feasibility; Mellow/downstream firmware owner performs implementation and tests |
| FW-04 | Establish waveform peripheral/clock/timing contract | Planned | Specify MCPWM/LEDC/RMT allocation and concurrent-interface test needs; measured timing remains external P-02/P-04 |
| FW-05 | Specify driver UART and current-unit contract | Planned | Addresses, transport, fitted sensing and RMS units match schematic; communication/current measurement is external P-02/P-04 |
| FW-06 | Qualify display-driver feasibility and exclusive initialization contract | Waiting | Resolve A-05 hardware-affecting driver/interface facts; actual demonstration remains Mellow/owner P-03 |
| FW-07 | Define QSPI input and future UI/mirroring contract | Waiting | Preserve Mini12864 controls and allocate the selected touch interface; touch runtime test belongs to external P-03 |
| FW-08 | Budget fitted flash/PSRAM/internal memory | Planned | Specify memory configuration and selected-panel buffer/DMA allocation; actual memory tests are external P-02 |
| FW-09 | Define controller-only service and restart output behavior | Planned | Complete power/reset/output-state contract; source isolation needs external measurement and is not proved by firmware state alone |
| FW-10 | Specify native USB loading and ROM recovery | Planned | Pin/boot/fixture access and recovery procedure defined; Mellow performs actual blank-board loading and recovery checks |
| FW-11 | Document EEPROM schema/CRC/identity handoff | Planned | Read-only legacy fixtures and an explicit compatibility/migration policy; full migration implementation is separate |
| FW-12 | Document radio/serial hardware and application expectations | Planned | Record network/API/status and UART interface contracts with downstream physical checks; application port remains separate |
| DISP-01..04 | Disposition documented Mellow products against the strict QSPI requirement | Done | [Sourced candidate comparison](COMPATIBILITY_RESEARCH.md): ordinary SPI, UART smart screen, host computer and HDMI/DSI alternatives do not meet the present requirement |
| DISP-05 | Qualify selected TDO QSPI candidate for Mellow sourcing | Waiting | R-09 desk evidence complete; exact driver/WAIT/touch/power/cable/drawing and sample/supplier confirmation remain before BOM approval; no order or supplier contact made |

## Current decisions that should not be reopened without cause

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
  Static firmware feasibility remains required; owner/Mellow handle production
  and physical testing. Full application/OTA/test-firmware implementation is
  separate (DEC-019).
- Servo baseline is MG90S as specified in the OpenTrickler sourcing guide;
  model/source selection is settled and should not be asked again (DEC-019).

## Change log

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
