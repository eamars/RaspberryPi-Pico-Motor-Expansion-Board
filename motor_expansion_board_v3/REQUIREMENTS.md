# V3 requirements and design objectives

Status: requirements and reference research; V3 CAD has not started. Updated: 2026-09-12.

This is the working source of truth for V3 requirements. The statements below
capture the user's decisions; they do not claim the current PCB meets them.
Further requirements will be added as the design discussion continues.
Copied OWMC files are reference material only, not a V3 schematic or starting PCB
(DEC-018). Create the V3 design after the cleanup and pre-schematic gates below.

The authorized development scope is **PCB design and hardware bring-up**,
including static analysis of ESP32 firmware feasibility before production.
The full ESP32 application port and OTA implementation are outside this scope.
Minimal firmware needed to bring up and test board interfaces is included.
Implementation progress is tracked only in [PROGRESS.md](PROGRESS.md).
The user excludes a separate thermal-design exercise: follow the Fly TMC2209
StepStick reference and ordinary manufacturer layout/heatsink practices for
room-temperature use. No continuous 1.5 A RMS board rating is required or claimed.

## How we capture requirements

Describe needs in ordinary language. The assistant records each agreed need as
one requirement with a stable ID, a target, and a way to check it. Unknown values
stay `TBD`; suggestions and inferred constraints stay separate from confirmed
requirements. Correct an entry by ID or describe the change in conversation.

- **Requirements** are conditions the design must satisfy.
- **Objectives** describe desired outcomes and guide tradeoffs.
- **Open questions** hold missing information and proposed choices.
- **Decisions** record what was settled, why, and the affected requirements.

Use `Must`, `Should`, or `Could` for priority. Track requirement agreement
(`Proposed`, `Confirmed`, `Superseded`) separately from verification
(`Not checked`, `Pass`, `Fail`). A confirmed requirement is not a passed test.
Add links to schematic sheets, PCB features, calculations, or test results as
evidence becomes available. Keep IDs stable when wording changes.

## Design objectives

| ID | Objective | Basis |
| --- | --- | --- |
| OBJ-001 | Preserve V2 compatibility through the controller change: board dimensions, mounting, external connection locations, and functional behaviour. | User, 2026-09-12; REQ-MECH-001/002, REQ-IF-001, REQ-FUNC-001. |
| OBJ-002 | Use exactly one MCU on the V3 PCB: a directly fitted ESP32-S3R8. | User, 2026-09-12; REQ-MCU-001. MCU identity and quantity are fixed by DEC-009. |
| OBJ-003 | Prefer LCSC-sourced components and compatibility with Mellow/Fly products; Mellow will manufacture the board, supply the display, and may source parts unavailable from LCSC. | User, 2026-09-12; REQ-SRC-001, REQ-MFG-001, REQ-COMPAT-001. |
| OBJ-004 | Size the 5 V supply against actual supported loads, with permission to reduce the inherited V1/V2 converter specification. | User, 2026-09-12; REQ-PWR-001. |

LCSC sourcing and Mellow/Fly compatibility are confirmed preferences. No ranking
of cost, power, performance, or ease of assembly has been agreed.

## Confirmed requirements

All entries below are **Confirmed / Not checked**; priority is shown separately.
The verification methods are proposed checks. Unknown numerical targets,
tolerances, and product selections remain open.

| ID | Priority | Requirement / target | Proposed acceptance check |
| --- | --- | --- | --- |
| REQ-MECH-001 | Must | V3 shall retain the archived v2.1 board's base dimensions. | Compare against the user-confirmed archived v2.1 PCB: 91.694 x 66.802 mm. Manufacturing tolerances remain open under OQ-001. |
| REQ-MECH-002 | Must | V3 shall retain the archived v2.1 board's mounting-hole pattern. | Compare hole count, centres, and mounting fit: four primary 3.2 mm holes on an 81.534 x 56.642 mm pattern. The baseline revision is confirmed; manufacturing tolerances remain open. |
| REQ-IF-001 | Must | V3 shall retain V2's external connection locations to preserve backward compatibility. | Inventory external connections and compare their locations against V2. Confirm connector orientation, mating hardware, pinout, and electrical compatibility under OQ-003. |
| REQ-FUNC-001 | Must | V3 hardware shall support the same functions as V2, subject to explicitly agreed limits such as the powered accessory envelope in REQ-ACC-001 and the QSPI control change in REQ-DISP-004. | Use the source-backed capability inventory to demonstrate hardware interfaces with bring-up firmware and complete the static feasibility assessment. Full application runtime parity depends on the separately scoped ESP32 firmware port and is not claimed by these hardware checks. Detailed performance limits remain TBD. |
| REQ-MCU-001 | Must | V3 shall contain exactly one MCU: a directly fitted ESP32-S3R8. | Inspect the schematic, BOM, and PCB for one ESP32-S3R8 and demonstrate the capabilities required by REQ-FUNC-001. Dedicated PD, driver, memory, and interface ICs remain peripheral functions; no second MCU is planned. |
| REQ-REUSE-001 | Should | Use the user-proven ESP32-S3R8 design in `C:/workspace/OpenWeaponMountComputer` as a reference, adapting application-specific pin assignments for V3. | Identify the proven source revision and reusable MCU support circuits; review every V3 I/O assignment against V3 needs and MCU restrictions. |
| REQ-MOTOR-001 | Must | Provide two onboard TMC2209 motor-driver ICs. | Check the schematic, BOM, and layout for two populated ICs and demonstrate both existing motor channels. Current and cooling scope are specified under REQ-MOTOR-002 and REQ-THERM-001; optional diagnostic pin allocation remains to be established. |
| REQ-MOTOR-002 | Must | Preserve the existing firmware's RMS current interpretation: 800 mA RMS default per channel, with software adjustment up to 1.2-1.5 A RMS. The higher setting is not the recommended normal operating point. | Verify current units, fitted sense configuration and reference/component limits. Do not treat the upper software setting as a qualified continuous-current rating. The user does not require a dedicated 1.5 A continuous thermal design; DEC-016 supersedes the earlier proposed high-current qualification envelope. |
| REQ-THERM-001 | Must | Use passive heatsinks and the Fly TMC2209 StepStick reference for normal room-temperature use, potentially inside a case. A separate thermal-design exercise is outside scope. | Review the reference implementation and retain ordinary manufacturer layout/heatsink practices and normal bring-up observations. No formal thermal model, thermal optimization project or guaranteed continuous 1.5 A RMS rating is required. No existing enclosure fit is mandatory. |
| REQ-DISP-001 | Must | Support Mellow/Fly Mini12864 as the baseline display through the retained V2 EXP1/EXP2 headers. | Test the selected Mini12864 revision and supplied cables, including display, encoder, buttons, and lighting features required for V2 parity. |
| REQ-DISP-002 | Must | Add a new display/expansion connection while retaining the existing V2 display headers. | Inspect both retained headers and the added connector; agree the added connector's model, pinout, supply, and cable specification before layout is fixed. |
| REQ-DISP-003 | Must | Support a customer-selected display type, with one display type operating at a time. | Demonstrate each supported display mode independently and document selection/population rules. Simultaneous display operation is outside the current requirement. |
| REQ-DISP-004 | Must | Demonstrate a selected 3.5-4 inch QSPI display on the first V3 hardware prototype, with Mellow3D/Fly's AliExpress offering as the primary sourcing target. QSPI mode shall not require a rotary encoder or physical buttons. Mini12864 support remains retained separately. | Verify the actual panel's host interface, supply, cable, connector, control method and firmware-driver feasibility, then demonstrate it using hardware bring-up firmware. Test the two display modes independently. Exact model, resolution and touch implementation remain open; touch is a proposed input method, not yet an independently confirmed requirement. |
| REQ-IF-002 | Must | Provide the QSPI display interface needed to meet REQ-DISP-004. | Establish the selected display's electrical and mechanical interface before fixing connector routing and GPIO allocation. A generic expansion header alone does not satisfy the first-prototype display requirement. |
| REQ-IO-001 | Should | Route remaining usable ESP32 GPIOs to a 2 mm or 2.54 mm pitch header for user-defined 3.3 V control signals. This has lower priority than required interfaces, with no minimum count. | Produce the final pin budget and document header pinout, ground references, reset/boot behavior and electrical limits. Use 2.54 mm pitch as the implementation starting point. The header is for control signals; it is not a power-output interface. Additional I/O expansion is not required. |
| REQ-SRC-001 | Should | Prefer LCSC for board components. Mellow/Fly may source missing parts and supply its own TMC2209 inventory. LCSC availability is not a mandatory condition for every part. | Record manufacturer, full MPN, actual supplier, applicable LCSC code, package/specification match, and dated availability for each BOM line. Record Mellow-sourced parts and agreed substitutes. The user reports ample Mellow TMC2209 stock; exact ordering identity, quantity, and allocation remain to be established. |
| REQ-MFG-001 | Must | Use Mellow as the PCB manufacturing/assembly partner and display supplier. | Prepare the fabrication/assembly package to the requirements agreed with Mellow. Production quantity, assembly process, programming, and test responsibilities remain TBD. |
| REQ-COMPAT-001 | Should | Prefer components, mating connectors, and interfaces compatible with the selected Mellow/Fly offerings. | Maintain a product/revision compatibility matrix with exact connector orientation, pinout, voltage, and protocol. Product-family names alone do not establish compatibility. |
| REQ-PWR-001 | Should | Size the 5 V DC-DC supply for the actual supported load envelope. Reducing the inherited V1/V2 converter rating is authorized when retained functions and loads remain supported. | Build a load budget for controller, selected display, accessories, and conversion losses. Check simultaneous loads, startup/stall transients where applicable, voltage droop, and thermal margin. Converter and current rating remain TBD; do not infer them from typical MCU consumption alone. |
| REQ-PWR-002 | Must | Supply the motor power rail from 12 V USB-PD for motor operation, retaining the master project's requirement for a compatible 12 V PD PSU. | Establish V3's required source current/power from the complete load budget. Test the compatible source, initial 5 V negotiation, failed/unsupported negotiation, power loss, and restart. Proposed hardware qualification must keep motor power disconnected outside the allowed 12 V range; threshold tolerances remain TBD. Accepting 15/20 V-only supplies is outside the agreed requirement. |
| REQ-USB-001 | Must | Support ESP32 programming/debugging while the board receives its required 12 V USB-PD motor supply. | Demonstrate both connections together, including reset, flashing, debugging, and cable insertion/removal. A separate service connection is agreed under REQ-USB-003; controller-only PC power remains proposed. |
| REQ-USB-002 | Must | The 5 V debug USB supply shall not power the motors. The power arrangement must prevent unintended backfeed between the PC connection and the board's power sources. | With debug USB alone, demonstrate no motor supply or unintended energization, including during reset and absent firmware. With both sources, verify no board-to-PC or cross-source backfeed and check unpowered-domain signal paths. |
| REQ-USB-003 | Must | Retain the USB-C power input at the archived v2.1 position and provide a separate connection for initial firmware loading and debugging. | Check retained power-port mating geometry and independent service access. Evaluate an optional vertical USB connector and programming contact pads; exact connector orientation, population variant, fixture interface, and PC-only controller power remain design proposals under OQ-013. |
| REQ-ACC-001 | Must | Support two MG90-class servos and up to four external NeoPixels powered from the board. The typical setup uses approximately two external LEDs. Longer LED chains use an external supply. The selected display's own lighting is an additional load. | Budget both servo channels together with four external LEDs and the chosen display. Confirm exact servo and LED variants, transient demand, connector limits, and external-supply wiring. Preserve the existing LED data capability for externally powered chains; do not connect independent 5 V sources together. |
| REQ-VER-001 | Must | Conduct static analysis of firmware feasibility for the one-ESP32-S3R8 hardware architecture before production. | Produce a source-backed matrix of pin/peripheral/memory availability, platform-dependent APIs, interface-driver support, timing assumptions, startup/service behaviour and required migration work. Resolve hardware-affecting incompatibilities or record an agreed scope change before production. Separate static conclusions from runtime claims; hardware bring-up remains required and the full application port is outside scope. |

## Confirmed process requirements

These requirements govern execution and are tracked in the same master
[PROGRESS.md](PROGRESS.md). They are **Confirmed / Not checked**; implementation
and review evidence will be linked when available.

| ID | Priority | Requirement / target | Acceptance evidence |
| --- | --- | --- | --- |
| REQ-PROC-001 | Must | Treat OWMC and existing copied CAD as references only. Audit and clean obsolete, unsuitable and unrelated schematics/libraries before creating fresh V3 CAD. No existing V3 schematic or PCB is assumed. | Inventory, reversible cleanup record and clearly separated reference assets; the active CAD directory contains only deliberately created/adopted V3 files. Preserve archived V2.1 compatibility evidence. |
| REQ-PROC-002 | Must | Update existing project documentation, READMEs and generated artifacts as the design changes. | Documentation and export review at each gate; stale revisions, links and claims are corrected or labelled historical. All implementation status stays in one master tracker. |
| REQ-PROC-003 | Must | Organize project-specific resources, including foreign symbols, footprints and models, with explicit provenance and validation. | Project library structure and manifest identify source/revision/license, purpose, local name and part/pad checks; no unreviewed bulk library import becomes a production dependency. |
| REQ-PROC-004 | Must | Keep the project self-contained. Use other projects as references and retain only needed reminders/evidence; production files must not depend on those workspaces or personal libraries. | A fresh repository checkout on the documented KiCad version resolves adopted symbols, footprints, models and sheets through project-relative paths; custom assets are vendored with provenance. External references are citations, not build dependencies. |
| REQ-PROC-005 | Must | Specify the intended netlist/connectivity and clearance rules before starting schematic implementation. | Complete the pre-schematic net/endpoint and connector-pin contract, named rails, GPIO/peripheral ownership, net classes, clearance matrix and relevant routing/via constraints with their basis. Resolve circuit-affecting TBDs before opening the schematic gate. The later KiCad-exported netlist must reconcile against this specification. |
| REQ-PROC-006 | Must | Follow consistent symbol placement, functional segmentation and parent/child schematic hierarchy. | Document sheet responsibilities and interface directions before drawing; use readable signal flow, aligned symbols/text, explicit junctions, local power/decoupling context and named hierarchical ports. Avoid hidden cross-sheet dependencies and ambiguous global labels. Review rendered sheets as well as connectivity. |
| REQ-PROC-007 | Must | An independent agent must review the schematic against requirements, then the owner must approve it. | Deliver the exact schematic revision, requirement traceability, rendered sheets, ERC/netlist/BOM evidence, independent findings and dispositions as a review package. Record explicit owner approval of that revision before PCB implementation; no self-approval or silence-as-approval. Material schematic changes require renewed review/approval. |

Here, the pre-schematic **netlist specification** means the intended named nets
and endpoints. KiCad generates the implementation netlist after the schematic
exists; that export is compared with the earlier contract. Clearance values
must be numeric and justified before schematic work, rather than silently
inheriting settings from the copied reference.

## Baseline and references

- V3 is a new design. [pcb/](pcb/) is reserved for its future active CAD;
  imported assets have been quarantined after independent audit. Needed
  [reference snapshots](references/README.md) are separate; no imported CAD,
  library or design-rule configuration is adopted for production.
- The archived [V2 PCB](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb)
  and [V2 schematic](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_sch)
  are the user-confirmed v2.1 compatibility baseline (DEC-007). Extracted geometry
  is the design reference; manufacturing tolerances remain under OQ-001.
- The [repository README](../README.md) documents V2. Its feature list is useful
  input to the compatibility inventory; it does not establish additional V3
  requirements by itself.
- The user reports the ESP32 reference design is proven. Its current working
  copy contains an uncommitted `pcb/power_supplies.kicad_sch` change; identify
  which revision was proven before adopting its power circuitry.
- Research findings and planning estimates are in
  [DEVELOPMENT_SUMMARY.md](DEVELOPMENT_SUMMARY.md). Source measurements are in
  [research/design-inventory.json](research/design-inventory.json).
- The proposed power and USB arrangement, load-budget inputs, and operating
  cases are in [POWER_ARCHITECTURE.md](POWER_ARCHITECTURE.md). Separate power
  and service connections are agreed; service-connector population, programming
  pad details, and controller-only PC power remain proposals.
- Practical hardware and firmware context is recorded in
  [USE_CASE_RESEARCH.md](USE_CASE_RESEARCH.md), based on
  `C:/workspace/OpenTrickler` and the linked local
  `C:/workspace/OpenTrickler-RP2040-Controller` checkout. Source-derived
  capabilities support verification planning; they are not automatically new
  user-confirmed requirements.
- Source for the confirmed requirements: user clarifications on 2026-09-12,
  including Mini12864 baseline support and one-display-at-a-time operation.

## Open questions

These are queued for later discussion; no answer is assumed.

| ID | Information to establish | Affects |
| --- | --- | --- |
| OQ-001 | The archived PCB marked v2.1 is confirmed as the compatibility baseline (DEC-007). Establish manufacturing tolerances and account for any as-built deviations during fit checks. | REQ-MECH-001/002; all compatibility checks. |
| OQ-002 | What external connections and functions must be preserved, including any normally unused options? Build the V2 capability inventory. | REQ-IF-001, REQ-FUNC-001. |
| OQ-003 | Define backward compatibility at each connector: mating part, orientation, pinout, voltage levels, protocol, and existing cables/enclosure. Record any permitted exceptions. | REQ-IF-001. |
| OQ-004 | Exactly one ESP32-S3R8 is fixed. Establish external flash capacity, antenna implementation, and support-circuit provenance. The reference's 16 MB flash is the proposed starting point; the selected firmware/assets/OTA layout must fit. | REQ-MCU-001, REQ-REUSE-001. |
| OQ-005 | What operating limits must be retained: input power, output loads, motor modes, duty cycle, and environmental conditions? | REQ-FUNC-001; later electrical requirements. |
| OQ-006 | Development scope is resolved by DEC-014: PCB and hardware bring-up, with static firmware-feasibility analysis before production. The full application/OTA port is separate. Define the handoff contract for local UI, network interfaces, settings format and service/recovery, and identify any needed application-owner input. | REQ-FUNC-001, REQ-DISP-004, REQ-VER-001. |
| OQ-007 | What are the cost, quantity, assembly, schedule, and verification objectives, and how should tradeoffs be ranked? | Later design objectives and production constraints. |
| OQ-008 | Qualify TDO TS040WVS02CP-B1617A for Mellow sourcing as explicitly directed in DEC-015; keep QSPI. Establish exact revision, driver/protocol, included touch interface, connector/cable, signal directions, maximum/inrush current and power-off behavior. Resolve inconsistent adapter drawing identity. Also establish the exact retained Mini12864 revision/cable. | REQ-DISP-001/002/003/004, REQ-IF-002. |
| OQ-009 | Scope resolved by DEC-017: expose remaining usable native GPIOs on a 2/2.54 mm control-signal header, lower priority and no minimum count. Determine count, layout and electrical documentation after required interfaces are allocated. | REQ-IO-001. |
| OQ-010 | Which Mellow/Fly connector series, approved substitutes, assembly rules, and factory programming/test process should this custom board follow? | REQ-SRC-001, REQ-MFG-001, REQ-COMPAT-001. |
| OQ-011 | Thermal scope resolved by DEC-016: room-temperature use, passive heatsinks, Fly TMC2209 StepStick reference, no separate thermal design or guaranteed continuous 1.5 A RMS rating. Verify reference identity and manufacturer implementation requirements. Dedicated diagnostic/stall lines are not a new confirmed requirement; account for any needed status signals within the required-interface budget. | REQ-MOTOR-001/002, REQ-THERM-001, REQ-IO-001. |
| OQ-012 | Two MG90-class servos and four board-powered external LEDs are agreed. Establish exact variants and measured/datasheet peak currents, including overlapping servo demand, selected display lighting, and 3.3 V conversion. The referenced RGBW LED product allows a provisional 0.30 A for four; servo current remains unresolved. | REQ-PWR-001, REQ-ACC-001. |
| OQ-013 | Separate PD and service connections are agreed. Evaluate a vertical service USB footprint populated for development and potentially omitted in production, with programming/recovery contact pads. Confirm fixture requirements with Mellow, enclosure access, controller-only PC operation, and service firmware behaviour. OTA is a desired future service approach, not yet a demonstrated ESP32 capability. | REQ-USB-001/002/003, REQ-IF-001, REQ-MFG-001. |
| OQ-014 | Retain the required 12 V PD PSU. Complete the V3 source power/current budget, cable selection, qualification/protection, service USB attach/current behaviour, and status/control GPIO allocation. The previous two-spare-GPIO estimate excludes new power-status/VBUS-sense pins and any separate replacement for the Pico's Wi-Fi status LED. These implementation calculations are engineering work, rather than requests for the user to choose resistor values or thresholds. | REQ-PWR-002, REQ-USB-001/002, REQ-IO-001. |
| OQ-015 | Existing-case compatibility is not required (DEC-013). Preserve the agreed board outline, mounting geometry and existing connector placement; select other placement/heatsink/service-access geometry as engineering work. Check internal clearances and RF placement in the resulting design without treating any community case as mandatory. | REQ-MECH-001/002, REQ-IF-001, REQ-THERM-001; RF and placement. |
| OQ-016 | Define electrical fault/restart behaviour and any required external inhibit/interlock input. Proposed default: actuator outputs remain disabled through reset, brownout, invalid PD, and firmware loading until deliberately enabled by valid application control. Establish external cable lengths and connector misuse conditions that affect interface protection. | REQ-FUNC-001, REQ-USB-002, REQ-IO-001; protection and startup implementation. |
| OQ-017 | Establish intended operating environment, target markets and any formal EMC/radio/ESD test objectives, prototype/production quantities, target assembled cost, and schedule. Agree Mellow's factory flashing, inspection, test, and rework responsibilities using the prepared handoff package. | REQ-MFG-001, REQ-SRC-001, REQ-COMPAT-001; production and validation plan. |

## Decision log

| ID / date | Decision and reason | Affects |
| --- | --- | --- |
| DEC-001 / 2026-09-12 | Continue V3 as the WIP revision, using V2 as the compatibility baseline. Preserve dimensions, mounting-hole pattern, external connection locations, and functions while changing to a direct ESP32-S3R8 or similar MCU. Reason: backward compatibility. Exact reference revision and MCU choice remain open. | OBJ-001/002; the initial five confirmed requirements. |
| DEC-002 / 2026-09-12 | Use the user-proven ESP32-S3R8 project as the MCU reference, add two onboard TMC2209 ICs and additional 3.3 V digital I/O where pins permit. Prefer LCSC parts and Mellow/Fly compatibility; Mellow is the manufacturing and display partner. | REQ-REUSE-001, REQ-MOTOR-001, REQ-IO-001, REQ-SRC-001, REQ-MFG-001, REQ-COMPAT-001. |
| DEC-003 / 2026-09-12 | Mini12864 is the baseline. Retain V2 display headers and add a new connection. QSPI is preferred but the peripheral is undecided. Customers use one display type at a time, allowing display-resource sharing to be investigated. | REQ-DISP-001/002/003, REQ-IF-002. |
| DEC-004 / 2026-09-12 | The inherited 5 V converter may be reduced to suit real loads. Resolve USB-PD power and ESP32 programming/debug coexistence. Mellow/Fly may supply missing components and its own TMC2209 stock; LCSC remains preferred. | OBJ-003/004; REQ-PWR-001, REQ-USB-001/002, REQ-SRC-001. |
| DEC-005 / 2026-09-12 | Motor operation requires 12 V from USB-PD. The user explicitly excludes powering motors from 5 V debug USB. Separate PD and debug ports with controlled power paths are the proposed solution; controller-only PC power remains a proposal. | REQ-PWR-002, REQ-USB-001/002; OQ-013/014. |
| DEC-006 / 2026-09-12 | The normal accessory use is two MG90-class servos and about two NeoPixels. The agreed board-powered design envelope is two servos plus four external LEDs; larger chains require external power. Display lighting is counted separately. This clarifies the powered load limit without removing firmware support for longer externally powered chains. | REQ-ACC-001, REQ-PWR-001, REQ-FUNC-001. |
| DEC-007 / 2026-09-12 | Use the archived PCB marked v2.1 as the mechanical/interface baseline. Keep one USB-C power input at its existing position and provide separate initial-programming/debug access. The user suggests a vertical, optionally unpopulated service connector and initial-programming pads as OTA may reduce service-port use. Connector and fixture details remain proposals. | REQ-MECH-001/002, REQ-IF-001, REQ-USB-003; OQ-001/013. |
| DEC-008 / 2026-09-12 | Preserve the current firmware library's RMS interpretation: 800 mA RMS default and adjustment up to 1.2-1.5 A RMS. This supersedes the user's initial peak wording after inspection found that the source's peak comment conflicts with the RMS library calculation. Use the upper end for preliminary sizing; cooling and continuous-duty validation remain open. | REQ-MOTOR-002; OQ-011. |
| DEC-009 / 2026-09-12 | Fix the V3 controller to exactly one ESP32-S3R8 MCU. This supersedes the earlier allowance for a similar MCU; the existing reference is reused only for support circuitry appropriate to this part and application. | OBJ-002, REQ-MCU-001; OQ-004. |
| DEC-010 / 2026-09-12 | Retain the OpenTrickler master project's requirement for a compatible 12 V PD PSU. Use passive cooling with heatsinks. No broader 15/20 V-source acceptance requirement was added; source power budget, current duty, ambient limit, and heatsink fit remain to be established. | REQ-PWR-002, REQ-THERM-001; OQ-011/014/015. |
| DEC-011 / 2026-09-12 | The first V3 prototype must demonstrate a selected QSPI display. This upgrades QSPI from a preference to required first-prototype functionality; a generic expansion provision is insufficient. Mini12864 remains supported and only one display type operates at a time. | REQ-DISP-001/003/004, REQ-IF-002; OQ-008. |
| DEC-012 / 2026-09-12 | Target a 3.5-4 inch QSPI display, first checking Mellow3D/Fly's AliExpress offering. QSPI mode requires no encoder or physical buttons. Resolution, actual product/interface, and touch details remain open. This does not remove the retained Mini12864 controls. | REQ-DISP-004; OQ-008. |
| DEC-013 / 2026-09-12 | Preserve connector placement and mounting holes; the user imposes no additional existing-enclosure constraints. The previously confirmed board outline remains the baseline. Other component/heatsink/service-connector geometry is available for engineering decisions. | REQ-MECH-001/002, REQ-IF-001; OQ-015. |
| DEC-014 / 2026-09-12 | Deliver PCB design and hardware bring-up only. Conduct static firmware-feasibility analysis before production; the complete ESP32 application port and OTA implementation are separately scoped. Minimal interface test/bring-up firmware is included. | REQ-FUNC-001, REQ-VER-001; OQ-006. |
| DEC-015 / 2026-09-12 | Keep the QSPI requirement and qualify TDO TS040WVS02CP-B1617A for Mellow sourcing. This selects the qualification direction, not a fully approved/available production part. Do not substitute the Mellow ordinary-SPI model without a new requirement decision. | REQ-DISP-004, REQ-IF-002; OQ-008. |
| DEC-016 / 2026-09-12 | The user specifies room-temperature use, possibly inside a case, says the high-current setting is generally not recommended, and excludes a separate thermal-design exercise. Use the Fly TMC2209 StepStick reference and passive heatsinks. Retain the 800 mA RMS default and adjustable software range, with no claimed continuous 1.5 A RMS board rating. | REQ-MOTOR-002, REQ-THERM-001; OQ-011. |
| DEC-017 / 2026-09-12 | Route unused usable native GPIOs to a 2 mm or 2.54 mm pitch header for user-defined 3.3 V control signals only. This is lower priority, with no minimum signal count and no requirement for an I/O expander. Use 2.54 mm as the initial implementation choice. | REQ-IO-001; OQ-009. |
| DEC-018 / 2026-09-12 | The user clarifies that OWMC is only copied reference material and no V3 PCB/schematic exists. Clean existing assets first; organize and vendor needed project resources; keep the project self-contained and documentation current. Specify connectivity/netlist and clearances before schematic work, use deliberate parent/child hierarchy and placement conventions, and require independent schematic review against requirements followed by explicit owner approval. | REQ-PROC-001 through REQ-PROC-007; all design gates in PROGRESS.md. |

When a later decision changes a confirmed requirement, record the reason here
and update the affected entry. A design implementation choice does not silently
change the requirement it is intended to satisfy.
