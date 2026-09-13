# Motor Expansion Board V3 design overview

This is a controller PCB update based on archived V2.1. Its three core changes
are one directly fitted ESP32-S3R8 replacing the Pico, two onboard TMC2209s
replacing the StepSticks, and an external display connector. The supplied
display assembly is outside this PCB design. V2.1 defines the board outline,
mounting holes, connector positions, mating orientation and retained pinouts.

The corrected schematic has five A3 pages: a populated controller parent and
four coherent children. All parts currently use installed KiCad 10 symbols
and footprints, including V2-style 0805 hand-solder pads where suitable.
Required QFN packages and RF/clock parts are the stated small-package exceptions.
Read [the V2/OWMC study](research/V2_DESIGN_STUDY.md) for baseline evidence.

| Page | Contents |
| --- | --- |
| Controller parent | ESP32-S3R8, external flash, clock/RF/reset, EEPROM, spare GPIO and child-sheet connections |
| Power / service | V2 PD and 5 V converter, added 3.3 V supply, separate USB service, indicators and contact pads |
| Motor drivers | Both TMC2209 channels, current sensing, local decoupling and shared addressed UART |
| Serial / outputs | Existing TTL/RS232 alternatives, DB9 routing and three buffered 5 V outputs |
| External displays | Retained Mini12864 headers, external QSPI connector and required touch supply/reset interface |

Child-sheet pins match named hierarchical labels. Local labels connect signals
within each page; GND uses standard power symbols. No global signal labels are
used. Parent/child style follows the owner's OWMC reference; its PCB and power
architecture are not the starting design.

## Electrical changes that support the three requested features

The core adds the support circuitry that the Pico previously contained.
External flash remains separate from the R8's internal octal PSRAM; reserved
memory pads are not general-purpose I/O. Motor enable pins use GPIO42/48 to
avoid GPIO1/2 power-up low pulses. The four spare-header signals are GPIO2 and
restricted boot-strapping GPIO3/45/46; GPIO46 is assigned to input use here.
The independent pin check confirms the required peripheral functions are
available. Firmware rework and application-port analysis are excluded by the
owner's latest clarification (DEC-022).

The board retains V2's power circuit and 5 V converter class. A separate USB
service port/pads require main PD power and cannot feed the motor rail.
See [power and USB design](POWER_ARCHITECTURE.md) for operating cases and load
assumptions. Both motor channels retain 800 mA RMS default settings, adjustable
to 1.2-1.5 A RMS, with passive heatsinks and no continuous upper-current claim.

The three existing accessory buffers and Mini lighting buffer use the
pin-compatible AHCT logic family so a 3.3 V input is guaranteed high at a 5 V
supply. A simple receiver-selection jumper keeps the V2 TTL and RS232
alternatives without joining two active outputs. Connector semantics remain
unchanged, including V2's J11=PWM2 and J12=PWM1 mapping.

Only one display assembly is connected at a time. The retained Mini12864 uses
its existing headers and controls. The added 20-contact FFC targets the selected
TDO TS040WVS02CP-B1617A QSPI assembly. The PCB contains the connector and needed
logic-level interfaces only; it does not implement the display module. Cable
contact orientation, module maximum current, Mini KILL-link population and
Mellow sourcing remain supplier/sample qualification items.

## Design process

1. Preserve archived V2.1 and reversibly remove the rejected CAD/library draft.
2. Record numbered net endpoints, GPIO use, numeric net classes/clearances,
   hierarchy and standard-library audit before capture (G-01).
3. Capture the five native KiCad sheets; export and compare the implementation
   netlist against the written contract; run ERC and inspect rendered pages.
4. Have an independent agent review the completed schematic against requirements
   and source evidence. Resolve findings, then obtain the owner's approval of
   the exact package (G-02).
5. After approval, create a fresh PCB with locked V2.1 mechanical datums. Place,
   route, check DRC/netlist/return paths and document manufacturing assumptions.
6. Deliver the schematic, completed PCB and first preliminary BOM. The owner
   manages production; Mellow manufactures and performs initial functional tests.

All work status, dependencies, review findings and gates belong in the single
[master progress tracker](PROGRESS.md). The [requirements brief](REQUIREMENTS.md)
records decisions. Research files and native export reports are evidence, not
additional progress trackers. No PCB implementation occurs before owner approval.
