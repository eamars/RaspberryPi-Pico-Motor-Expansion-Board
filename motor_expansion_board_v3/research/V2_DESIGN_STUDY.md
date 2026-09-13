# V2 circuit baseline and OWMC schematic-style study

Read on 2026-09-13 after the owner stopped the expanded draft. This is a study
record, not a new design approval or progress tracker. Live status belongs in
[PROGRESS.md](../PROGRESS.md).

## Scope correction

The deliverable is the Motor Expansion Board V3: preserve the V2.1 board's
functions and external compatibility, replace its Pico with one directly fitted
ESP32-S3R8, replace its two StepStick modules with onboard TMC2209 circuits, and
add a connector for an external QSPI display. The earlier agreed load, USB service,
sourcing and review requirements still apply. OpenTrickler supplies application
context. OWMC supplies a selective MCU reference and the owner's schematic style.
Neither project's complete product architecture is the new board's specification.

The assistant expanded uncertain interface and power cases into implementation
requirements before establishing the simpler V2 baseline. The resulting draft has
15 sheets and 268 component instances; 83 instances belong to display selection,
Mini12864 adaptation and QSPI adaptation alone. Those additions were not adequately
justified. Some increase over V2 is necessary because the Pico and StepStick
modules contain support components absent from the carrier BOM; a raw total-count
comparison cannot measure the excess by itself.

## V2 source evidence

**High confidence, local native CAD/document evidence.** Read all four rendered
schematic pages, the fresh native XML netlist, archived PCB footprint/net data,
the repository's board illustrations, BOM and manufacturing instructions:

- [Root schematic](../../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_sch).
- [Power supply](../../archive/motor_expansion_board_v2/pcb/power_supply.kicad_sch).
- [RS232 interface](../../archive/motor_expansion_board_v2/pcb/rs232_transceiver.kicad_sch).
- [5 V outputs](../../archive/motor_expansion_board_v2/pcb/5v_pwm_output.kicad_sch).
- [Placed V2.1 PCB](../../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb)
  and [project settings](../../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pro).
- [V2 README](../../README.md#manufacturing) and
  [production instructions](../../archive/motor_expansion_board_v2/production/README.md).

The older illustrations carry V2.0 markings. The owner-selected archived native
PCB remains the authority for V2.1 geometry and pad mapping.

| Existing block | What V2 actually implements | Bounded V3 change |
| --- | --- | --- |
| Controller | One Pico module; +5 V feeds VSYS, its 3V3 output powers carrier logic, and its USB VBUS pin is unconnected on the carrier. Programming USB is on the module. | Replace the module and its required support functions with the ESP32 core, board 3.3 V supply and initial programming/recovery access. Adapt pins to this board. |
| Motors | Two StepStick sockets; individual STEP/DIR/EN, shared UART with addresses 0/1, and 100 uF bulk capacitance per channel. | Fit two complete bare-IC TMC2209 circuits using the agreed Fly reference. Preserve motor cable positions and phase order: 1=B2, 2=B1, 3=A1, 4=A2. |
| Display | EXP1/EXP2 Mini12864 headers with display/control signals and 5 V power. One separate buffer drives display NeoPixel data. | Retain these connections and add the selected external QSPI display connection. Establish the actual signal/voltage needs; one-display-at-a-time does not by itself require an elaborate electronic selector. |
| Input and 5 V power | CH224K strapped for 12 V; negotiated VBUS directly supplies driver VM and the TPS5450 input. TPS5450, SS54, 15 uH inductor and 330 uF output capacitor provide 5 V. | Start with this topology. Evaluate any converter reduction against the agreed loads. Keep service 5 V from energizing motors without inventing extra operating modes. |
| Serial | MAX3232, DB9 and a 2x2 straight/null-modem jumper; TTL connector shares the MCU UART. RX/TX activity LEDs are present. | Preserve the existing serial function and connection geometry. Check any actual electrical incompatibility as a specific correction. |
| Outputs/storage | Three buffered 5 V signal headers, each GND/+5 V/signal; CAT24C256 I2C EEPROM with pullups; reset and rail indicators. | Preserve functionality. Recheck signal thresholds and the controller change without replacing these with a generalized I/O subsystem. |

V2's power circuitry does not contain the draft's added input eFuse/MOSFET chain,
motor-rail qualification logic, display-rail comparator network or USB fixture
selection logic. Any such addition would need its own demonstrated requirement
and a comparison with a simpler solution before being retained.

## Footprint and layout intent

**High confidence, native footprint instances and explicit manufacturing text.**

- Four copper layers; 91.694 x 66.802 mm outline; four grounded 3.2 mm mounting
  holes on an 81.534 x 56.642 mm pattern. Retain full outline and mating datums.
- All 16 resistors use KiCad's 0805 hand-solder footprint; all 15 ceramic
  capacitors use its 0805 hand-solder footprint; all five indicator LEDs also use
  0805 hand-solder pads. Larger pads are deliberate, not obsolete clutter.
- The README explicitly states hand soldering as an objective. V2.1 moved vias
  off pads to reduce SMT failures. Preserve this practical assembly intent;
  justify local package exceptions where a new IC's implementation needs them.
- J1/J2 are **vertical** 2x5 IDC headers, rotated 90 degrees in the PCB plane.
  Earlier draft documentation calling them right-angle connectors was incorrect.
- Prefer the installed KiCad symbols/footprints. Keep only genuinely custom or
  modified assets locally, with provenance. Self-contained project resources do
  not require duplicating standard KiCad libraries.
- The native archive contains 68 component/footprint instances including four
  mounting holes. The Pico and StepStick modules' internal components are not
  expanded in that count.

## OWMC drawing style

**High confidence, direct source and visual inspection.** Read the owner's
`C:/workspace/OpenWeaponMountComputer/pcb/owmc.kicad_sch` and
`power_supplies.kicad_sch`, including both freshly rendered A3 pages. The power
child already has an uncommitted owner change; it was read without alteration.
These source paths identify the study, not project dependencies.

- The project has **two sheets total**: a populated parent and one coherent
  `Power Supplies` child. Related small circuits remain together on a page.
- The parent sheet symbol exposes ten named interface pins, including `USB_DP`,
  `USB_DN`, `CHIP_PU`, the I2C pair and supply rails. The child uses matching
  hierarchical labels. Ordinary labels connect local circuits to the parent
  symbol. Neither source file contains `global_label` objects.
- Circuit sections have clear headings, divider lines and short boxed notes
  explaining pin restrictions, component placement or implementation choices.
  Support components are drawn with their functional block.
- Apply this structure and density to V3, using at most five sheets total. A
  compact grouping is parent/controller, power/service, both motor channels, and
  external interfaces; settle boundaries against readability before capture.
- Use explicit hierarchical ports for inter-sheet connections and local labels
  within each sheet. Assign electrical port directions for V3 itself rather than
  blindly inheriting the reference's pin types or application-specific nets.

## Limits and effect on the draft

This study establishes existing connectivity, construction intent and drawing
style. It is not a fresh electrical qualification or fabrication release of V2,
OWMC or V3. Native PDF/netlist exports and schematic/PCB analyzers were used;
no new EMC, SPICE, thermal, lifecycle or production review was performed.

The 15-sheet draft and its intended netlist are rejected as the implementation
baseline. Passing ERC or matching that intended netlist does not validate its
scope. Before any resumed capture, the intended connectivity, numeric rules,
sheet plan and library choices must be revised around the three requested
changes. No CAD was modified during this study. Independent schematic review
and explicit owner approval still precede PCB work.
