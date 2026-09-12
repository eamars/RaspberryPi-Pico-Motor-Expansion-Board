# V3 development summary

Research date: 2026-09-12. This document describes the architecture, evidence
and design process. All live work status is maintained in the single
[master progress tracker](PROGRESS.md); agreed requirements are maintained in
[REQUIREMENTS.md](REQUIREMENTS.md).

The requested mechanical, electrical, firmware and display investigations are
consolidated in [COMPATIBILITY_RESEARCH.md](COMPATIBILITY_RESEARCH.md).
They identify concrete carryover corrections, including 5 V buffer thresholds,
the shared serial receive path, conflicting global VBUS meanings and the
copied OWMC geometry that is not the V3 baseline. Initial static assessment supports a one-MCU approach,
but final pin/display allocation and operating validation remain open.

The design uses exactly **one ESP32-S3R8 MCU** on a V2.1-compatible board,
with the proven MCU core as a reference, two integrated TMC2209 drivers,
retained Mini12864 headers, and a selected 3.5-4 inch QSPI display demonstrated
on the first prototype. QSPI mode requires no encoder or physical buttons;
Mini12864 controls remain supported. Customers select one display type at a
time. Initial resource accounting supports this direction,
with **approximately two additional direct 3.3 V GPIOs in the conservative
scenario below, before new power/status signals**. Display selection, driver
diagnostics, power sensing, and any separate Wi-Fi indicator must be allocated
before that count becomes a commitment.

The practical application is examined in
[USE_CASE_RESEARCH.md](USE_CASE_RESEARCH.md). The supported accessory-power
envelope is now **two MG90S servos plus four external NeoPixels**, with
display lighting additional and longer chains externally powered. The inherited
5 V converter may be reduced once the real load budget supports it. Mellow/Fly
may supply missing parts and its own TMC2209 stock; LCSC remains preferred.

**System overview and design choices.** Confirmed product requirements and
proposed implementation choices are distinguished below. Dedicated PD, motor
driver, memory, and interface ICs support the single MCU.

| Block | Agreed function | Implementation work / proposal |
| --- | --- | --- |
| MCU core | One directly fitted ESP32-S3R8 | Adapt the reference clock, reset/boot, decoupling, memory and RF circuits; 16 MB external flash is the reference-based starting point |
| Input power | Compatible 12 V USB-PD PSU at the V2.1 USB-C position | Autonomous PD negotiation, voltage qualification, protection, source-current budget and defined failed-negotiation state |
| Motor channels | Two onboard TMC2209s; 800 mA RMS default and adjustment up to 1.2-1.5 A RMS | Preserve existing motor connectors; Fly StepStick reference and passive heatsinks; no separate thermal design or continuous upper-current rating |
| Accessory and controller rails | Two sourcing-guide MG90S servos, four external pixels, one selected display, controller and interface loads | Separate 5 V accessory and 3.3 V logic budgets; choose a smaller 5 V converter only if the load/transient evidence supports it |
| Display interfaces | Existing Mini12864 EXP1/EXP2 plus a working selected 3.5-4 inch QSPI display on prototype one, without encoder/buttons in QSPI mode | Qualify TDO TS040WVS02CP-B1617A for Mellow sourcing; verify exact driver/touch, power and cable, electrical display selection and GPIO/peripheral allocation |
| Retained interfaces | Existing serial/RS232 connections, three buffered output channels, settings persistence and networking behaviour | Check cable pinouts and levels; preserve settings functionality with an explicit migration/storage format; EEPROM retention is the initial hardware approach |
| Additional I/O | Remaining usable native GPIOs on a 2/2.54 mm header, for 3.3 V control signals only | Lower priority and no minimum count; start with a 2.54 mm header and document ground references, reset states and electrical limits |
| Service and recovery | Separate initial-programming/debug access alongside main PD power | Optional vertical USB connector and fixture pads; controller-only PC power proposed; retain boot/reset access even if routine updates use OTA |
| Mechanical and manufacturing | V2.1 outline, holes and external connection positions; no additional existing-case restriction; Mellow assembly with LCSC preferred | Establish internal heatsink/antenna/service clearances and Mellow's stack-up, assembly, sourcing and factory-test requirements |

The assistant delivers the complete schematic, PCB layout and first preliminary
BOM, plus static firmware-feasibility and design-review evidence (DEC-019).
The owner manages production; Mellow manufactures and performs initial functional
testing. Physical bring-up and application/OTA/test-firmware implementation are
downstream work. Retained hardware acceptance criteria still apply, but the
assistant's handoff does not claim that those physical tests have passed.

ESP32-S3R8 includes 8 MB of octal PSRAM and no in-package flash. External flash
capacity and firmware partitioning must cover both the application and display
assets. OTA also needs space for the supported update/recovery arrangement.
[ESP32-S3 datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf),
[ESP-IDF OTA documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/ota.html).

The proposed initial PCB stack-up is four layers, consistent with Espressif's
chip-layout guidance. Final copper, thickness and impedance rules depend on
Mellow's process, retained mechanical fit, and ordinary power/reference layout requirements.
Reusing the reference circuit does not establish RF performance in the new
board geometry and enclosure; antenna placement and validation remain work.
[Espressif PCB layout guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html).

**Compatibility baseline.** Native KiCad measurements of the archived PCB
marked v2.1 give the following geometry. The user has confirmed this archived
revision as the baseline. These are design-file measurements; acceptable
manufacturing tolerances and as-built fit checks remain open.

| Item | Archived V2 measurement / interface |
| --- | --- |
| Board extents | 91.694 x 66.802 mm |
| Primary mounting | Four 3.2 mm holes; rectangular spacing 81.534 x 56.642 mm |
| Display | J1 EXP1 and J2 EXP2, 2x5 IDC headers, 2.54 mm pitch |
| Motors | J6 and J7, four-pin JST-XH connectors |
| Serial connections | J3 three-pin header and J10 DB9 path; they share one MCU UART |
| Existing output connections | J11, J12, J13; three buffered 5 V logic outputs |
| Power connection | J8 USB-C; retain the V2 input-power behaviour when defining the new power tree |

The [measurement and net inventory](research/design-inventory.json) records
source hashes, mounting coordinates, and connector footprint anchors and
rotations. Anchors are not necessarily mating-face datums. Matching board size
alone will not establish cable compatibility: connector orientation, pinout,
voltage, and mating clearance need individual checks. The internal StepStick
module sockets are candidates for replacement by the onboard drivers; the motor
cable connectors remain part of the compatibility baseline.

The native V2 netlist contains 26 named MCU GPIO nets, but `SPI0_MISO` connects
only to the MCU. There are **25 GPIOs with external connections**. The current
schematic does not establish display-header SD-card support; that must not be
inferred merely from the EXP connector names.

**Reference reuse and current V3 state.** The reference project is
`C:/workspace/OpenWeaponMountComputer`, at Git commit
`dce2f2533f86f468a69d2141414c9320d7366f53`. Its working copy has an uncommitted
`pcb/power_supplies.kicad_sch` change. The user's proven-board experience is
valuable evidence, but the proven revision must be identified before attributing
that evidence to the current power sheet.

Reuse candidates are the MCU, external flash, clock, boot/reset, decoupling, and
USB support circuits, with application-specific assignments reviewed afresh.
The reference's battery PMIC, IMU, and display-specific circuitry require a V3
use case before inclusion. V2's existing input-power requirements should drive
the power architecture.

ESP32-S3R8 provides 8 MB of octal PSRAM and requires external flash. The reference
uses a W25Q128 device; its LCSC identity resolves to the 16 MB W25Q128JVSIQ
candidate below. Memory capacity remains a design choice. Check the new MCU
layout, supply, clock, and antenna arrangement against the manufacturer guidance
when adapting the reference to V2's board geometry.
[ESP32-S3 datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf),
[Espressif hardware design guidance](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32s3/index.html).

The user clarified that **no V3 schematic or PCB exists yet** (DEC-018). The
imported OWMC PCB and partially prepared sheet files are reference/scaffolding
assets, not a V3 implementation. Audit and quarantine them before creating a
fresh project; retain only useful reference evidence with provenance. Neither
their geometry, library setup nor design rules are adopted automatically.

**Power and USB.** Motor operation requires 12 V from USB-PD. Debug USB must
not power the motors. The agreed arrangement retains the PD connector
location and provides separate programming/debug access. A vertical USB service
connector, optional production population, and programming/recovery pads are
being considered. Qualify the
12 V input before feeding the stepper rail and the main 5 V converter. A
protected PC power branch may feed the controller, with no path to the stepper
or servo supply. Controller-only PC operation remains a proposal.

The [power architecture proposal](POWER_ARCHITECTURE.md) includes the block
diagram, operating cases, and load-budget inputs. It also accounts for the
inherited TPS5450's 5.5 V minimum input, which excludes ordinary 5 V PC USB as
a valid input to that converter. Exact servo peak demand and display current
remain necessary before choosing a lower converter rating.
[TI TPS5450 specification](https://www.ti.com/product/TPS5450).

CH224K is an option; an autonomous PD sink controller is the recommended class
of solution. Ordinary USB-A-to-C cables can serve the USB 2.0 debug connection,
but cannot negotiate this board's USB-C PD supply. Native PCB inspection confirms
J8 has no data pads, despite its footprint/value naming. Keep it dedicated to
power and choose the service footprint independently. The PD source must
explicitly support the required 12 V. Protocol references and proposed service
assembly variants are in [POWER_ARCHITECTURE.md](POWER_ARCHITECTURE.md).

**Display and GPIO planning.** Mini12864 is the confirmed baseline, retaining
EXP1/EXP2 and adding the new connector. Mellow publishes 12864 documentation and
a Mini12864 configuration covering the LCD, encoder, and lighting. Exact product
revision and cable orientation still need a compatibility check.
[Mellow 12864 documentation](https://mellow.klipper.cn/en/docs/ProductDoc/Screen/12864/),
[Mellow display configuration](https://mellow-3d.github.io/fly_super8_pro_h723_klipper_mcu_config.html).

No qualifying 3.5-4 inch direct-QSPI Mellow product has been verified. The
documented FLY-TFT-V2 is ordinary SPI. A TDO TS040WVS02CP-B1617A display-only
QSPI assembly is the user-selected qualification target for Mellow sourcing,
subject to supplier, driver, interface and load verification. It is not yet an
approved production part. See [the sourced comparison](COMPATIBILITY_RESEARCH.md)
for exact listings, evidence and access limits.
The external TDO display contains a TR230S bridge with a RISC-V core and supplied
firmware; V3 itself retains one ESP32-S3R8. Its official ESP32 QSPI example
supports transport feasibility but targets a different resolution/touch IC.
The exact B1617A driver and power-off behavior therefore remain qualification
work. [TDO bridge description](https://www.shtdo.com/AboutStd_833.html),
[desk qualification evidence](COMPATIBILITY_RESEARCH.md#tdo-desk-qualification).
The first prototype is now required to demonstrate a selected QSPI display,
so this selection is needed before its schematic, connector and pin allocation
are fixed. QSPI identifies a bus arrangement; it does not specify a universal
display connector. Panel controller, resolution, supply, touch interface,
backlight control, cable length, and any tearing-effect signal must be known
before fixing the new connector. Allocate it to a general-purpose SPI
peripheral, preserving the MCU's memory interface.

Espressif documents 45 GPIOs. Reserving GPIO26-37 for flash/PSRAM leaves 33;
reserving GPIO19/20 for native USB and the four boot-strapping pins leaves a
conservative pool of 27. USB retention and avoiding all strapping pins are
planning choices, rather than user requirements.
[Espressif GPIO restrictions](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html).

| Allocation within that 27-pin pool | GPIOs |
| --- | ---: |
| Two motor channels: separate STEP, DIR, and ENABLE | 6 |
| Shared TMC UART, retaining separate MCU TX/RX | 2 |
| Existing external serial channel | 2 |
| Shared I2C for EEPROM and compatible future peripherals | 2 |
| Existing three logic outputs | 3 |
| One active display mode | 10 |
| **Provisional remaining GPIOs before new power/status signals** | **2** |

This is an inferred allocation, not a pin-level feasibility proof. The ten-pin
display allowance matches V2's connected UI signals. TDO's direct-touch option
uses twelve signals, or ten new pins if its I2C bus can share the allocated pair;
the bridge-touch option uses nine but is unverified. Sharing requires compatible
addresses, voltages and power-off behavior. The estimate reserves no separate runtime debug UART,
TMC DIAG/INDEX inputs, or additional sensors. Each extra dedicated signal reduces
the remaining count. Power-valid/VBUS sensing and a separate replacement for
the Pico's Wi-Fi indicator are also absent from this allocation. Firmware
research identifies those as additional decisions in
[USE_CASE_RESEARCH.md](USE_CASE_RESEARCH.md).

One-display-at-a-time operation permits pin reuse after electrical selection,
inactive-device behaviour, and firmware configuration are defined. It does not
by itself prevent contention or back-powering. More direct pins might be
recovered after reviewing boot-strapping constraints. Expose the remaining
usable native pins on a 2.54 mm control-signal header after required allocation,
with no minimum count. Keep the existing 5 V output functionality and document
the additional header's reset states and electrical limits. An expander is not
required for the optional header.

**Integrated motor drivers.** TMC2209 supports STEP/DIR control and an addressable
single-wire UART bus, allowing the two drivers to share configuration wiring.
Mellow's FLY E3 Pro V3 also uses onboard TMC2209s, providing a relevant ecosystem
reference. That does not establish a current rating for this custom layout.
[ADI TMC2209 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf),
[Mellow FLY E3 Pro V3](https://mellow-3d.github.io/fly_e3_pro_v3.html).

The user has confirmed **800 mA RMS default per channel, adjustable up to
1.2-1.5 A RMS**. The upper software setting is not a qualified continuous-current
rating or the recommended normal operating point. The
firmware's peak-current comment conflicts with the linked library's RMS
calculation; preserving RMS interpretation is now an explicit decision
(DEC-008). This is a source-code finding, not a current measurement; evidence
is in [USE_CASE_RESEARCH.md](USE_CASE_RESEARCH.md).

The user specifies room-temperature use, potentially inside a case, with
passive heatsinks and the Fly TMC2209 StepStick reference. A separate thermal
design/optimization exercise and a guaranteed continuous 1.5 A RMS rating are
outside scope. Follow ordinary manufacturer/reference layout practices and
normal hardware bring-up observations. Electrical power budgeting remains
necessary for the supply and support-component choices.

**Sourcing and manufacturing.** The core parts have LCSC catalog entries. The
stock figures below were displayed on the official pages on 2026-09-12 and are
not reserved inventory.

| Part | Quantity per board | LCSC | Research status |
| --- | ---: | --- | --- |
| ESP32-S3R8 | 1 | [C2913194](https://www.lcsc.com/product-detail/C2913194.html) | Target MCU; 3,571 displayed in stock |
| TMC2209-LA-T | 2 | [C2150710](https://www.lcsc.com/product-detail/C2150710.html) | Driver candidate; 3,332 displayed in stock |
| W25Q128JVSIQ | 1 | [C97521](https://www.lcsc.com/product-detail/C97521.html) | Reference flash candidate; catalog identity checked, availability not established here |

The schematic inventory found LCSC fields on 64 of 68 V2 components and 76 of 83
reference components, including mechanical entries. These are a useful starting
point, not a verified V3 BOM. Neither inventory had dedicated MPN fields; some
identities are present in component values. Populate full manufacturer/MPN,
LCSC code, package, and critical specifications during part selection, then
check every fitted line and record the actual supplier. Mellow/Fly sourcing is
an accepted route for missing components; its TMC2209 stock is user-reported
and still needs an exact ordering identity and production allocation. No full-board price or
all-parts availability conclusion is supported yet.

Mellow is the selected manufacturing partner. Agree its stack-up, assembly
limits, preferred connectors, acceptable substitutes, programming, and production
test process before layout is fixed. LCSC availability does not establish
Mellow's assembly approval. The eventual handoff should include fabrication
files, drill files, stack-up notes, BOM, placement data, assembly drawings,
firmware, and an agreed test procedure. Display procurement remains through
Mellow, as requested.

**Uncovered decisions and their impact.** The MCU identity, 12 V PSU policy,
passive heatsinks, and first-prototype QSPI demonstration are settled. Avoid
reopening them without a new reason. The remaining product choices are:

| Requirement question | Missing decision | Why it affects the design |
| --- | --- | --- |
| OQ-008 | Qualify TDO TS040WVS02CP-B1617A for Mellow sourcing and establish the retained Mini12864 revision | QSPI is retained; actual module revision, connector, driver, included touch, cable and maximum load still need closure |
| OQ-015 | Internal placement, heatsink, service-access and antenna clearances | Engineering work within the preserved outline/holes/connector contract; no existing community case is mandatory |
| OQ-011 | Adapt the identified Fly TMC2209 StepStick reference with verified component ratings | Official revision 1.0 evidence is recorded; scope is room-temperature use with passive heatsinks, without a separate thermal design or continuous upper-current rating |
| OQ-012 | MG90S current/transient evidence | Model/source is settled by the sourcing guide, including item 1005004550692203; quantify overlapping demand through engineering sources and downstream Mellow measurements |
| OQ-009/016 | Final spare-pin header allocation and reset/electrical documentation | Scope is settled: unused usable native GPIOs, 2/2.54 mm pitch, control signals only and no minimum count; required functions take priority |
| OQ-006 | Interface contract and settings compatibility for the separately scoped application port | Scope is settled: complete schematic/PCB and first preliminary BOM, with static firmware feasibility; physical testing and firmware implementation are downstream |
| OQ-013/017 | Service population variant and design provisions for programming/test access | Owner handles production quantities, budget and schedule; Mellow handles manufacturing/initial tests. Provide relevant design notes without taking over factory execution |
| OQ-016/017 | Fault/restart expectations and operating/test environment | Defines startup, brownout, loss-of-power, interface-protection and EMC/radio validation objectives |

Proposed engineering defaults are controller-only PC service power, actuator
outputs disabled during reset/invalid power/firmware loading, boot/reset recovery
access, reference-based 16 MB flash, and a four-layer PCB. These are proposals,
not additional user-confirmed requirements. Part values, power thresholds,
trace dimensions, decoupling, and protection selections are engineering work;
the user supplies the operating conditions and desired behaviour.

**Development sequence and acceptance evidence.** Each step produces a
reviewable artifact and evidence for the next. No hardware implementation or
prototype result is claimed by this plan.

1. **Clean and specify before drawing.** Audit copied schematics/libraries and
   quarantine unsuitable material with rollback evidence. Retain only needed
   references; organize adopted symbols, footprints and models with provenance
   and project-relative paths. There is no existing V3 CAD to continue.
   Maintain the requirement IDs,
   produce the V2.1 connector compatibility matrix and mechanical overlay, and
   select the actual display. Prepare the power budget, GPIO/peripheral matrix,
   service modes and firmware-interface contract. Resolve the missing inputs
   affecting each block before fixing that block. Complete the intended
   net/endpoint specification, numeric net-class/clearance rules and deliberate
   parent/child sheet conventions before schematic implementation (G-01).
2. **Establish static feasibility and test needs.** Check memory/peripheral
   allocation, driver evidence, power/reset behavior and interface contracts.
   Define the necessary physical checks for Mellow, including selected-display
   behavior and concurrent waveform timing. Record gaps honestly; static analysis
   does not establish runtime results. Test-firmware implementation and physical
   probes are downstream work under DEC-019.
3. **Build schematic and BOM together.** Use hierarchical sheets for the MCU,
   power/service paths, drivers, displays and retained/extra interfaces. Check
   every selected critical IC's pins, rails, support components and footprint
   against its manufacturer documentation. Keep MPN, supplier, LCSC identity
   where applicable, alternatives and population information in symbol
   properties, with source evidence.
4. **Review electrical behaviour.** Resolve ERC findings, check power sequencing,
   USB source isolation, unpowered I/O paths, reset defaults, current settings,
   voltage levels and electrical load calculations. Simulate suitable
   subcircuits when a simulator is available; record remaining bench validation.
   ERC alone does not establish correct part pinouts or electrical operation.
   Reconcile the exported netlist with the pre-schematic contract. An independent
   agent must review the exact schematic against every requirement, including
   sheet organization and readability. Resolve its findings and present the
   complete package for explicit owner approval (G-02) before PCB implementation.
5. **Place and route within the mechanical contract.** Lock the V2.1 outline,
   mounting geometry and retained connector datums. Fit heatsinks and service
   access; place the RF/core and switching/high-current circuitry with the
   required return paths. Route against Mellow's agreed stack-up and rules,
   maintaining appropriate ground continuity, USB/RF geometry and thermal paths.
6. **Review the layout and prepare the design handoff.** Run DRC and schematic-
   to-PCB comparisons; inspect critical footprints, mating orientation,
   reference-layout/EMC risks and the actual exported fabrication files. Prepare Gerbers, drills,
   BOM, placement files, assembly/variant drawings, stack-up notes, STEP model,
   interface/recovery notes and proposed physical acceptance checks. Document every
   unresolved finding and any validation that still requires hardware.
7. **Deliver the first preliminary BOM and stop.** Handoff the completed native
   schematic/PCB, required reviews and approval record, static design evidence
   and per-board BOM with exact parts/packages, sourcing identities, population
   notes and unresolved procurement/validation items. This is the assistant's
   P-01 endpoint; batch quantities and purchasing are the owner's responsibility.
8. **Owner/Mellow downstream work.** The owner manages production. Mellow builds
   the boards and performs initial functional tests, including power/service
   behavior and the required first-prototype QSPI demonstration. They arrange
   test images/fixtures and record measured results, production substitutions and
   any subsequent revisions. These external tasks remain visible in the master
   tracker but are not assistant delivery requirements.

The known requirements support specification and cleanup work now. Schematic
implementation waits for G-01; PCB implementation waits for the independent
schematic review and owner approval in G-02. Keep existing READMEs, references
and generated artifacts current as the design changes. No final layout or
manufacturing release is implied by completion of this overview.

**Tooling and research scope.** Workspace electronics skills were traced to
`aklofas/kicad-happy` and brought from v2.1.0 to the pinned v2.2.1 release, with
the missing SPICE skill added. Provenance, backups, and validation are recorded
in [the skills maintenance record](../.agents/SKILLS.md). The updated analyzers
were exercised on copied project files; no SPICE simulator is installed.

This summary uses targeted schematic analysis, a native KiCad netlist, native
PCB measurements, and manufacturer/distributor documentation. It does not
constitute a complete electrical, thermal, EMC, or fabrication review. No V3
hardware testing was performed during this research.
