# OpenTrickler hardware use case and V3 implications

OpenTrickler combines an external precision balance, two stepper channels, two
small servos, a local display, accessory lighting, and network configuration.
Its controller replacement therefore needs to preserve a complete set of
electrical and service interfaces. The general hardware compatibility findings
below support the V3 requirements; they do not establish measured performance
of a new board.[^system][^firmware]

The principal development decisions are now clearer. The main supply is 12 V
USB-PD. The supported board-powered accessory envelope is two MG90-class servos
and four external NeoPixels, with the selected display counted separately.
Longer LED chains have an external supply. A dedicated programming/debug
connection with a separate controller power path is the recommended way to
support a PC connection alongside PD power. These decisions and proposals are
distinguished in [REQUIREMENTS.md](REQUIREMENTS.md).

Subsequent requirements fix the V3 PCB to one ESP32-S3R8 MCU, retain the
master project's required 12 V PD PSU, specify passive cooling with heatsinks,
and require a selected 3.5-4 inch QSPI display to work on the first prototype,
without encoder/buttons in that mode. Later decisions remove additional
existing-case restrictions and limit this work to PCB/hardware bring-up plus
static firmware feasibility; a full application/OTA port is separate (DEC-009
through DEC-014). DEC-015 selects TDO TS040WVS02CP-B1617A for QSPI qualification
through Mellow. DEC-016 specifies room-temperature use and the Fly TMC2209
StepStick/heatsink reference, without a separate thermal design or continuous
1.5 A RMS rating. DEC-017 assigns remaining usable native GPIOs to a lower-priority
2/2.54 mm control header. The panel's exact interface and sourcing still need
qualification; see the updated
[development summary](DEVELOPMENT_SUMMARY.md) for the process and decision list.

The inherited 5 V converter may be reduced, but its replacement rating cannot
yet be calculated honestly. Four of the referenced RGBW pixels account for
approximately 0.30 A at full output. Both servos must be budgeted together, and
their exact peak demand remains unknown. The display, controller supply, and
conversion losses must be added before applying thermal and transient
margin.[^pixels][^servo-code][^servo-maker]

**Physical installation and external interfaces.** The system repository
contains assembly, sourcing, and enclosure material; the firmware is a separate
linked project. Its current documentation covers Pico W and Pico 2W, whereas
V3 targets a directly fitted ESP32-S3R8. The user has confirmed the archived
v2.1 KiCad PCB as the mechanical baseline. An annotated board illustration is marked v2.0,
so it is useful for identifying interface roles but should not override the
v2.1 native measurements or netlist.[^system][^sourcing][^board-image]

| Interface / load | Established context | V3 implication |
| --- | --- | --- |
| Two stepper channels | Existing external motor connectors and TMC2209 support | Integrate two driver ICs while retaining the cable interfaces; motor power comes from the specified 12 V PD source |
| Two MG90-class servos | Two separate accessory outputs; current firmware updates both channels together | Preserve two independent control signals and budget overlapping supply demand |
| External lighting | One chain output; default configuration is two RGBW pixels | Preserve RGB/RGBW data support; power up to four externally connected pixels from V3 |
| Mini12864 | LCD, encoder, button inputs, and three lighting pixels | Preserve the full local interface and count its lighting separately |
| Balance connection | DB9 and an alternate logic-level serial connector share one MCU UART | Preserve electrical levels, cable selection, and both transmit and receive functions |
| EEPROM | Existing firmware persists settings through an I2C EEPROM interface | Specify settings preservation and recovery as well as the physical bus |
| Network access | Wi-Fi station/access-point modes, web interface, REST endpoints, and discovery | Include these behaviours in the compatibility checklist |
| USB service access | The Pico has its own USB connector in addition to the board's PD connector | Check existing service access before fixing the location and height of the replacement connector |

These are source-derived compatibility candidates under REQ-FUNC-001, not
independent approval of every implementation detail. The associated source
files and their revisions are indexed in
[research/application-inventory.json](research/application-inventory.json).

The display and motor cable connectors, DB9 body, jumper access, and original
Pico USB access all affect practical fit. The earlier connector inventory
records PCB footprint anchors; it does not locate the USB receptacle mounted
on the removable Pico module. Enclosure fit therefore needs a three-dimensional
check in addition to the preserved board outline and mounting holes. The system
repository's generic mechanical interface image describes a different assembly
interface and must not substitute for the PCB mounting pattern.[^system][^board-image]

**Servo and lighting demand.** The source exposes two servo outputs through a
hardware PWM peripheral, and its low-level update writes both channels
together. This establishes that there is no basis for assuming mutually
exclusive electrical demand. It does not reveal actual motor current: that
depends on the selected servo, its supply, mechanical load, and transient
conditions.[^servo-code]

The sourcing guide names MG90S; the agreed requirement currently says
MG90-class. The precise supplied variant matters. TowerPro's MG90S product page
provides operating and mechanical information but no stall-current limit.
An exact supplier specification or measurements of the intended parts are still
needed. A numerical current copied from a different small servo would not close
this gap.[^sourcing][^servo-maker]

The external lighting modification specifies two Adafruit 4776 RGBW button
PCBs. Current firmware independently defaults to a two-pixel RGBW chain and
allows RGB/RGBW configuration. This is stronger evidence than the loose
"NeoPixel" or "WS2812" naming in the assembly material. The linked product is
an RGBW part with a fourth white channel, so procurement and firmware must agree
on the actual pixel type.[^led-mod][^led-code][^pixels]

Adafruit's technical details give approximately 75 mA maximum per pixel.
Consequently, four of that reference product provisionally add 0.30 A to the
5 V budget. That allowance is specific to the identified reference; a Mellow
substitute still needs its own specification checked.[^pixels]

The firmware's chain-count enumeration runs from one to sixteen pixels. It
describes the number of pixels on the single external chain, rather than
sixteen independently wired chains. The newly agreed four-pixel limit concerns
power supplied by the board. Longer externally powered chains can retain their
existing data capability. Their harness must leave the board's 5 V feed
disconnected from the external supply and provide the appropriate common signal
reference.[^led-code]

The Mini12864 has a separate three-pixel lighting chain in the firmware. These
pixels are additional to the external four. One display type at a time permits
separate budgets for Mini12864 and a future QSPI panel, but it does not remove
the external lighting load from either normal operating case.[^led-code]

**Power budget and the converter decision.** Native V2 connectivity places
both driver-module motor-supply pins on the incoming power rail. The 5 V buck
instead supplies the controller input, display headers, accessory power, and
buffers. The 3.3 V loads are downstream of the controller supply arrangement.
The two motor-power budgets must therefore be kept distinct: stepper winding
power is on the 12 V side, while the MG90 servos are genuine 5 V loads.[^native]

| Budget term | Current evidence | Selection consequence |
| --- | --- | --- |
| Servo A and Servo B | Two present; overlapping demand possible; exact peak currents unknown | Add both relevant load envelopes |
| Four external RGBW pixels | Approximately 0.30 A for the referenced Adafruit product | Include full required brightness rather than the dim default alone |
| Mini12864 | Three lighting pixels plus LCD electronics; exact module current unknown | Obtain the selected Fly module's load information |
| Future QSPI panel | No exact panel/controller/backlight selected | Compute its own operating case before committing the connector supply |
| ESP32 and support circuitry | A 3.3 V supply capability and transient requirement, not a fixed measured load | Include regulator conversion losses and the actual supported operating modes |
| Other logic and buffers | Existing connections identified | Add datasheet load and output-current effects |

For a downstream switching 3.3 V regulator, its approximate contribution to the
5 V input current is `3.3 * I_3V3 / (5 * efficiency)`, plus applicable overhead.
For an LDO it is approximately the 3.3 V load current plus quiescent current.
Calculate each permitted display mode, then size for the most demanding
supported combination. Startup, recovery, and thermal conditions can govern the
selection even when average consumption is low.

Espressif recommends a 3.3 V supply capable of at least 500 mA for its MCU
power-supply design. This is neither an instruction to allocate exactly 500 mA
at 5 V nor a complete-board load measurement.[^esp-power]

The TPS5450's 5 A component rating is not evidence of a 5 A application demand,
and it does not establish the assembled board's continuous thermal capacity.
Its minimum specified input is 5.5 V, which also explains why the inherited
conversion path cannot simply accept ordinary 5 V PC USB power.[^buck]

A smaller converter remains an authorized option. Selecting 1 A, 2 A, or another
rating now would conceal the unresolved servo and display demand. The immediate
deliverable is an agreed load envelope and component evidence, followed by a
converter choice with stated margin. No replacement regulator is selected in
this report.

**USB power and servicing.** The existing update guide explicitly requires
disconnecting the main supply before using the Pico's USB port. It establishes
a documented maintenance procedure, not proof that simultaneous main-power and
PC operation was validated. V3's requirement to support both connections is a
deliberate addition to that service behaviour.[^usb-guide]

The V2 connector also has a naming trap: its value text mentions USB2.0_14P,
but the actual library symbol is a power-only connector with no USB data pins
in the netlist. Its CH224K CC connections belong to the power interface.
Reusing the visible connector value as an electrical specification would miss
that distinction.[^native]

Type-C PD signalling uses CC and USB 2.0 data uses D+/D-, so the protocols can
coexist on a suitable single port. Two independent ports are recommended here
to accommodate a charger and a PC concurrently while preserving the original
PD input location.[^pd]

The proposed architecture in [POWER_ARCHITECTURE.md](POWER_ARCHITECTURE.md)
qualifies an acceptable 12 V input before feeding both the stepper rail and the
main 5 V converter. A separate PC branch may power the controller through
protected source selection. It supplies neither the steppers nor the 5 V
servos. PD negotiation must start without depending on an already booted ESP32,
avoiding a circular startup dependency.

| Service condition | Proposed behaviour |
| --- | --- |
| Valid 12 V PD | Main controller and peripheral power available |
| PC USB alone | Controller-only service; all actuator supply paths off |
| PD and PC together | Main power preferred for the controller; PC programming/debug data active |
| PD at initial 5 V or unsuccessful negotiation | Actuator supplies disconnected; controller can use the separate PC service source if present |
| Main power removed with PC connected | Controller may remain available for service; actuator supply paths turn off |

This proposal requires source backfeed prevention, USB current/attach handling,
defined reset states, and checks of signals entering unpowered peripherals.
It is a power-path concept rather than a completed protective circuit.
Controller-only PC operation and the new connector geometry remain proposed
choices; the prohibition on debug USB powering motors is confirmed.

ESP32-S3 native USB Serial/JTAG supports flashing, console access, and JTAG.
The existing Pico UF2 release and update procedure cannot simply be carried
across unchanged. Keep boot/reset recovery access and specify the new firmware
package and service instructions with the chosen implementation.[^esp-usb]

**Firmware dependencies that affect the PCB.** The firmware build imports the
Pico SDK and an RP-family FreeRTOS port. Its board header contains the pin
assignments; the implementation also directly uses Pico peripherals, PIO, and
the CYW43 networking interface. Changing the board header alone will therefore
not produce an ESP32 application. The MCU support circuitry can be reused from
the ESP32 reference while firmware compatibility is evaluated separately.[^build][^board-config]

Several less obvious dependencies deserve explicit parity checks:

- The display implementation uses UC1701 through SPI and u8g2. Its receive-pin
  setup is commented out, agreeing with the unconnected V2 MISO net. A future
  QSPI panel needs its own driver and mode-specific initialization; leaving the
  Mini12864 initialization unconditional would undermine shared-pin planning.[^display]
- The display connector's reset-labelled button generates a software event. It
  must not automatically be reassigned to the ESP32 chip-reset input based on
  its label alone.[^display]
- Display-buffer access is exposed to the web interface. A different display
  backend has implications for remote display behaviour as well as the local
  connector.[^display-buffer]
- Settings are persisted through an I2C EEPROM backend with defined address
  regions and per-structure versions. Preserving settings requires a data-format
  decision; retaining a similar physical memory device alone is insufficient.[^storage]
- Wi-Fi access-point/station operation, discovery, and the web service use the
  Pico wireless stack. The Pico's status LED is also accessed through its
  wireless device rather than a normal RP MCU GPIO.[^network][^board-config]

For the integrated TMC2209s, hardware and firmware configuration must agree on
the current-sense components. A source comment incorrectly calls the stored
value `110` ohms; the linked library explicitly defines the parameter in
milliohms. This is a documentation-unit discrepancy to resolve during the
hardware/firmware cross-check, not a new V3 resistor selection.[^tmc-units]

The user subsequently specified an 800 mA default and an adjustable upper
range of 1.2-1.5 A per channel, initially described as peak. Inspection found
that `src/motors.c` passes `current_ma` directly into `driver->config.current`,
while the linked library's `_set_rms_current` applies the RMS conversion and
its setter explicitly documents RMS units. The user then confirmed preserving
the existing RMS interpretation (DEC-008). Record 800 mA RMS default and
1.2-1.5 A RMS adjustment. The user subsequently clarified that the upper setting
is not the recommended normal operating point and excluded a separate thermal
design (DEC-016). Follow the Fly StepStick reference with passive heatsinks for
room-temperature use, potentially inside a case. The software limit does not
establish measured winding current or a continuous board-current rating.
[^tmc-current]

**Startup and controller-only service.** The application initializes storage,
lighting, the local display, and wireless configuration before driver
initialization. A driver-initialization error enters a loop before the main
scheduler starts. This is a source-code observation; no claim is made that every
unpowered driver necessarily produces that error.[^startup]

The practical implication is that powering the ESP32 without motor power must
not be assumed to provide the normal application interface. Define what is
required in controller-only service: ROM recovery, flashing, console/debug
access, or some explicitly limited application functions. Keep actuator power
disconnected in that mode. This separates a service requirement from any
assumption that all peripheral initialization succeeds.

**GPIO and compatibility accounting.** The earlier calculation left two
ordinary GPIOs after conservative memory, USB, and strapping reservations and
the 25 connected V2 functions. Firmware inspection supports reclaiming the
unused display MISO assignment, but it also reveals a previously unbudgeted
status-indicator consideration. A separate replacement for the Pico's Wi-Fi
LED consumes a pin unless its role is provided elsewhere. New power-valid,
VBUS-sense, or control signals can consume more.

Accordingly, the two-pin figure remains a scenario before those additions.
Possible choices include combining indicators, using hardware-only power
control where appropriate and reviewing boot-safe pin reuse. The user requests
only remaining usable native GPIOs, with no minimum count or expander requirement.
Use a 2.54 mm control-signal header as the starting point, with ground references.
The final count follows complete display, service and power-status allocation.

**Evidence strength and remaining decisions.** Confidence is high for the
reported source connections, configured peripheral capabilities, and documented
USB procedure. The power topology and compatibility checklist are engineering
proposals. Servo current, exact display demand, component substitutions, voltage
qualification, and prototype behaviour remain open. The report does not imply
that the firmware was executed on ESP32 or that V3 electrical tests have passed.

The next concrete inputs are the exact servo supply identity and current
evidence, the retained Mini12864 revision and the chosen TDO assembly's interface,
power and cable details. No existing enclosure fit is mandatory; service access
and fixture geometry are engineering choices. These determine the final power
budget and pin allocation. Mellow/Fly is
an accepted source for unavailable parts and its TMC2209 inventory; record the
actual manufacturer and part identity when selecting the BOM. Its reported
inventory is a sourcing lead rather than a reserved manufacturing allocation.

## Sources

Local source revisions recorded on 2026-09-12:
`OpenTrickler` at `6a0b9711194d59aa796af89c6224d7331031c4ff`, and
`OpenTrickler-RP2040-Controller` at
`4e384a384d714200eb5157a08e33d424e8e49f85`. File hashes and selected line references
are in [the application inventory](research/application-inventory.json).
Manufacturer pages were accessed on the same date.

[^system]: OpenTrickler project, [system README](https://github.com/eamars/OpenTrickler/blob/6a0b9711194d59aa796af89c6224d7331031c4ff/readme.md), controller links and mechanical-interface context.
[^firmware]: OpenTrickler controller project, [firmware README](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/README.md), supported hardware and connectivity.
[^sourcing]: OpenTrickler project, [sourcing guide](https://github.com/eamars/OpenTrickler/blob/6a0b9711194d59aa796af89c6224d7331031c4ff/Manual/sourcing_guide.md), servo, display, cable, and Pico variants.
[^board-image]: Motor expansion board project, [annotated v2.0 board image](../resources/opentrickler_pcb_v2_peripheral_annotation.drawio.png), interface roles. The user-confirmed archived v2.1 native PCB governs board measurements.
[^servo-code]: OpenTrickler controller project, [servo peripheral source](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/servo_gate.c#L47), paired PWM update and peripheral setup.
[^servo-maker]: TowerPro, [MG90S product page](https://towerpro.com.tw/product/mg90s-3/), manufacturer information; no stall-current limit published on the accessed page.
[^led-mod]: OpenTrickler community contribution, [NeoPixel LED modification](https://github.com/eamars/OpenTrickler/blob/6a0b9711194d59aa796af89c6224d7331031c4ff/CommunityContributions/eamars/neopixel_led_mod/readme.md), accessory product identity and two-pixel configuration.
[^led-code]: OpenTrickler controller project, [LED source](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/neopixel_led.c#L45) and [LED configuration types](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/neopixel_led.h#L39), default RGBW mode, chain count, and separate display lighting.
[^pixels]: Adafruit, [NeoPixel RGBW Mini Button PCB, product 4776](https://www.adafruit.com/product/4776), technical details and current rating.
[^native]: Motor expansion board project, [V2 schematic](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_sch) and [power sheet](../archive/motor_expansion_board_v2/pcb/power_supply.kicad_sch); native connectivity summarized in [design inventory](research/design-inventory.json).
[^esp-power]: Espressif, [ESP32-S3 schematic checklist: power supply](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html).
[^buck]: Texas Instruments, [TPS5450 product specification](https://www.ti.com/product/TPS5450).
[^usb-guide]: OpenTrickler controller project, [Firmware Update via USB](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/manuals/firmware_update_via_usb.md), documented power-disconnection procedure.
[^pd]: Texas Instruments, [A Primer on USB Type-C and Power Delivery Applications and Requirements, revision B](https://www.ti.com/lit/wp/slyy109b/slyy109b.pdf).
[^esp-usb]: Espressif, [ESP32-S3 USB Serial/JTAG Controller Console](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/usb-serial-jtag-console.html).
[^build]: OpenTrickler controller project, [CMake configuration](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/CMakeLists.txt), platform and peripheral-library dependencies.
[^board-config]: OpenTrickler controller project, [board configuration](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/targets/raspberrypi_pico_w_config.h), GPIO and peripheral assignments.
[^display]: OpenTrickler controller project, [Mini12864 implementation](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/mini_12864_module.cpp#L167), software button handling and display setup.
[^display-buffer]: OpenTrickler controller project, [display buffer interface](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/display.c#L61) and [REST endpoint registration](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/rest_endpoints.c#L100).
[^storage]: OpenTrickler controller project, [EEPROM layout](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/eeprom.h#L9), [storage backend](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/cat24c256_eeprom.c), and [settings implementation](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/eeprom.c).
[^network]: OpenTrickler controller project, [wireless implementation](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/wireless.c#L337) and [access-point implementation](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/access_point_mode.c#L30).
[^tmc-units]: OpenTrickler controller project, [driver configuration](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/motors.c#L48), linked Trinamic library [parameter definition](https://github.com/terjeio/Trinamic-library/blob/d7debfaffcb6e3d62c025455a629be6bd7e4d22d/tmc2209.h#L67) and [unit convention](https://github.com/terjeio/Trinamic-library/blob/d7debfaffcb6e3d62c025455a629be6bd7e4d22d/tmc2209.c#L235).
[^tmc-current]: OpenTrickler controller project, [default current comment](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/motors.c#L45), [direct configuration assignment](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/motors.c#L271), and linked library [RMS calculation](https://github.com/terjeio/Trinamic-library/blob/d7debfaffcb6e3d62c025455a629be6bd7e4d22d/tmc2209.c#L141). Source inspection only; no firmware changes or hardware current measurements.
[^startup]: OpenTrickler controller project, [startup ordering](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/app.c#L32) and [driver initialization error handler](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/motors.c#L665).
