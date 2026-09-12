# V3 compatibility research

Research date: 2026-09-12. This report consolidates the requested independent,
read-only investigations. [PROGRESS.md](PROGRESS.md) is the sole task/status
tracker; this file records findings, evidence, consequences and verification
limits. [REQUIREMENTS.md](REQUIREMENTS.md) remains the specification.

This research covers PCB interfaces and static firmware feasibility. DEC-019
sets assistant delivery at the completed schematic, PCB layout and first
preliminary BOM. The owner manages production and Mellow manufactures/performs
initial functional testing. Application/OTA/test-firmware implementation and
physical bring-up are downstream work. Exactly one ESP32-S3R8 is required.
No schematic/layout changes,
hardware operation, purchases or supplier messages were part of this research.

Later user decisions retain QSPI and select the TDO candidate for Mellow sourcing
qualification (DEC-015), exclude a separate thermal-design exercise in favour of
the Fly TMC2209 StepStick/passive-heatsink reference for room-temperature use
(DEC-016), and limit extra I/O to remaining usable native GPIOs on a 2/2.54 mm
control header, with no minimum count (DEC-017).

DEC-018 clarifies that the copied files were reference/scaffolding only: **no V3
schematic or PCB exists yet**. The geometry findings below identify requirements
for the new design, not defects in an existing V3 implementation. Findings
distinguish inherited circuit issues from risks in adopting V2/reference assets.
A source-file observation is not a
physical test. Targeted investigations do not constitute a complete ERC/DRC,
thermal, EMC or fabrication-readiness assessment.

**Assessment.** One ESP32-S3R8 has plausible peripheral resources for the
required board functions. Production feasibility remains conditional on the
selected QSPI assembly, complete GPIO/peripheral allocation, power-domain
corrections and measured operating limits. The existing boards and Pico
firmware cannot be copied unchanged. The most consequential concrete carryover
issues are ELEC-01/02/03, with mechanical replacement required under MECH-01.

## Mechanical compatibility

The OWMC reference PCB is not the V3 starting layout. Coordinates below
are absolute KiCad millimetres (X right, Y down). Confidence is high for the
reported native CAD geometry; actual mating parts and clearances were not
physically measured. No existing community enclosure is mandatory.

| ID / severity | Finding and evidence | Required design action |
| --- | --- | --- |
| MECH-01 / High design constraint | The [OWMC reference PCB](references/owmc/owmc.kicad_pcb:18224) is 28.6 x 43.5 mm, with 2.2 mm primary drills on a 17 x 32 mm pattern. The [archived V2.1 outline](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:21264) is 91.694 x 66.802 mm with R2.286 corners and four 3.2 mm primary mounts. DEC-018 confirms that no V3 PCB exists. | Create a fresh V3 PCB from the complete archived outline, corners and mounting datums after the schematic approval gate; OWMC geometry is not adopted. |
| MECH-02 / High | [V2 J10](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:9700) adds two 3.2 mm DB9 fixing holes at (152.331669, 91.650) and (152.331669, 116.650). Its F.Fab shell nose extends about 6.054 mm beyond the right board edge. | Preserve the full DB9 footprint, fixing holes, shell setback and mating direction. Verify the actual sourced connector against these datums. |
| MECH-03 / High | [V2 J8](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:11739) uses an HRO library name but references a [GCT USB4125 model](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:12082). Its anchor is (141.986, 77.978), 180 degrees; the drawn front is 0.410 mm inside the top board edge. It has the previously confirmed six electrical contacts and four shield slots. The model reference does not prove its MPN. | Preserve the placed mating geometry and establish the actual manufacturer drawing. Do not replace it automatically using the misleading library name. |
| MECH-04 / High | [EXP1](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:8828) and [EXP2](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:14994) are top-side, 90-degree keyed headers with openings facing the lower board edge. J6/J7 motor pins run B2, B1, A1, A2 from top to bottom. J11/J12 are 0 degrees and J13 is 180 degrees, all using pin 1 GND, pin 2 +5 V, pin 3 signal. | Preserve side, rotation, pin 1, key/latch direction and electrical mapping for every retained connector. Check cable insertion and removal access. |
| MECH-05 / Medium | [J4](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:19215) and [J5](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:17476) socket spaces contain 6.3 x 7.7 mm electrolytics C2 and C1. The lower socket courtyard is only 2.44 mm above EXP2's courtyard. | Removing elevated modules does not make empty heatsink volumes. Reposition internal components and check the complete heatsink/attachment/overhang assembly against plugs and ribbon access. |
| MECH-06 / Medium | [V2 stack-up metadata](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:6) specifies 0.19 mm total thickness and three 0.01 mm dielectric layers; [OWMC](references/owmc/owmc.kicad_pcb:6) specifies 1.6 mm. The archived order guidance does not establish actual manufactured thickness. | Select and document a real Mellow stack-up and connector/mounting Z assumptions. Do not treat the 0.19 mm metadata as an as-built measurement. |
| MECH-07 / Medium | Reference-derived [J1](references/owmc/owmc.kicad_pcb:15582) is a 30-contact AXE530127 on B.Cu; [J2 labelled Pogo USB Connector](references/owmc/owmc.kicad_pcb:3353) is a four-pin 2.54 mm through-hole header. | Select the actual display/harness connector and define a real programming fixture with contact side, lands, locating features, probe travel and boot/reset access. These reference assets do not establish either new interface. |

The mechanical acceptance artifact should overlay the complete retained
connector bodies, keys and fixing drills with the new heatsinks and service/
display interfaces. A physical mating check remains necessary for the selected
parts. Source measurements are anchored by the hashes in
[design-inventory.json](research/design-inventory.json).

## Mellow/Fly display investigation

No verified Mellow/Fly 3.5-4 inch direct-QSPI offering was established in the
official catalog, repositories and accessible AliExpress metadata. This is a
sourcing gap; it does not establish that Mellow cannot obtain a qualifying
panel. QSPI remains required until the user changes REQ-DISP-004/REQ-IF-002.

| Candidate | Evidence | Compatibility assessment |
| --- | --- | --- |
| FLY-TFT-V2, 3.5 inch, 320 x 480; [AliExpress listing 1005006565478090](https://www.aliexpress.com/item/1005006565478090.html) | The [official repository](https://github.com/Mellow-3D/FLY-TFT) and [pinned device-tree source](https://raw.githubusercontent.com/Mellow-3D/FLY-TFT/be76e27f47ecdc450f7c7b7111bf7c6787d2954d/rpi-overlays/fly-tft-v2.dts) use ST7796 ordinary SPI with separate D/C, reset and backlight control. Configurations include I2C capacitive touch or SPI resistive touch. | DISP-01: matches the size, but the documented host interface does not satisfy QSPI. [FLY-Pi wiring](https://mellow.klipper.cn/en/docs/ProductDoc/SBC/fly-pi-v3/host/screen/) describes a 16-contact, 0.5 mm reverse-contact 400 mm FPC for that host; it is not an approved V3 harness. |
| Fly_Nova 3.5, 480 x 320 | [Official specifications](https://mellow.klipper.cn/en/docs/ProductDoc/Screen/nova35/) identify TX/RX/5V/GND, its own SSD210 processor, ST7796S LCD and FT6336U touch controller. No exact AliExpress item was established. | DISP-02: UART smart screen with its own processor, not the direct-QSPI peripheral being specified. |
| Fly-MINI-Pad, 3.5 inch; [AliExpress listing 1005006116091326](https://www.aliexpress.com/item/1005006116091326.html) | [Official specifications](https://mellow.klipper.cn/en/docs/ProductDoc/SBC/fly-mini-pad/) describe an Allwinner H3 host, 512 MB DDR3 and FlyOS with a separate 5 V supply. | DISP-03: a host computer/display system, not a direct-QSPI panel for this MCU. |
| FLY-LCD43/50/70; [AliExpress listing 1005005257187800](https://www.aliexpress.com/item/1005005257187800.html) | [Official repository](https://github.com/Mellow-3D/FLY-LCD) describes HDMI/DSI products. Repository/listing identities indicate 4.3, 5 and 7 inches. The [English family page](https://mellow.klipper.cn/en/docs/ProductDoc/Screen/fly-lcd/) uses conflicting 4-inch wording. | DISP-04: documented interface mismatch and sizes outside the requested range; no verified 4.0-inch variant established. |

The [official Mellow site](https://mellow.klipper.cn/en/) links to
[mellow.aliexpress.com](https://mellow.aliexpress.com/). The research agent's
public HTTP reads resolved that alias to store 1100991286 with a Mellow 3D
Official Store title and canonical links using 1531088. The item URLs above
exposed product metadata, but dynamic SKU/stock, regional orderability and each
item's seller assignment were not exposed. These are listing-identification
leads, not confirmed current stock or an approved BOM.

A qualifying display still needs an exact model/revision, evidence that pixel
data travels over QSPI, LCD initialization/driver support, a numbered connector
drawing, cable/contact orientation, supply and backlight limits, and any touch,
reset, interrupt or tearing-effect signals. The absence of encoder/buttons in
QSPI mode is agreed; touch as its local input method remains to be established.

**Selected qualification target; production BOM approval pending.** The user
directed qualification of
**TDO TS040WVS02CP-B1617A**, marketed as 4.0 inch and specified as 3.95 inch,
480 x 480, with capacitive touch. A dedicated TR230S bridge exposes genuine
four-lane pixel writes; it does not require an additional ESP32/Linux host.
[Manufacturer catalog](https://www.shtdo.com/ProductsSt_qspimodule_003.html).

The manufacturer specification gives 4.5-5.5 V input, 180 mA typical demand,
an integrated backlight driver, 3.3 V logic and a 2.8-3.3 V touch supply. It
identifies a 20-contact 0.5 mm FPC interface and an alternate 2 mm 2x7 header.
Maximum/inrush current, WAIT behavior, driver support, cable constraints and
exact assembly dimensions still need verification. An adapter drawing names
a different model. These gaps prevent committing its connector or load budget.
[Specification v1.0, 2025-01-11](https://www.shtdo.com/Admin/Others/DownloadsPage.aspx?nid=28&id=1563&ref=claproducts&pre=1&t=92726061be261a19).

The catalog links [Taobao item 910286109433](https://item.taobao.com/item.htm?id=910286109433&sku_properties=29656%3A1892821924).
Current stock, price, delivered revision and Mellow's ability to source it are
unverified. The reviewed 18-page PDF is retained in
[project references](references/vendor/TDO-TS040WVS02CP-B1617A-v1.0.pdf); PDF SHA-256 is
`265c5bbb3b0a8cfda705843115c8a8a1db7eb76795a48f349305c5d2949fb3d9`.
DISP-05 records this qualification task. QSPI remains a fixed requirement;
ordinary SPI is not the selected direction.

### TDO desk qualification

The TR230S is a dedicated display bridge containing a RISC-V core and supplied
firmware. It resides in the proposed external display assembly; V3 retains one
ESP32-S3R8 on its PCB. This introduces a display-firmware dependency that must
be controlled with the supplied assembly revision.
[Manufacturer bridge description](https://www.shtdo.com/AboutStd_833.html).

The following is an evidence transcription for qualification, **not an approved
V3 connector pinout**. Directions describe intended operation relative to the
host. The source is the [B1617A specification](https://www.shtdo.com/Admin/Others/DownloadsPage.aspx?nid=28&id=1563&ref=claproducts&pre=1&t=92726061be261a19),
pages 5-9; ambiguous direction labels are called out below.

| 20-contact pin | Signal | Host relationship |
| --- | --- | --- |
| 1, 3, 5 | GND | Module ground |
| 2 | VCC | 4.5-5.5 V power into module |
| 4 | CS# | Output, active-low select |
| 6 | SDO1 | QSPI D1 output during pixel writes; SPI MISO direction ambiguous |
| 7 | SDO0 | QSPI D0 / SPI MOSI output |
| 8 | SCL | Clock output |
| 9 | SDO3 | QSPI D3 output during pixel writes |
| 10 | SDO2 | QSPI D2 output during pixel writes |
| 11 | RESET# | Active-low output to bridge/LCD |
| 12 | WAIT# | Expected input; low inhibits commands; source direction labels conflict |
| 13 | QSPI-INT | Expected input for bridge-proxied touch; output type/polarity unresolved |
| 14 | D/C# | Unconnected in QSPI mode |
| 15 | TP-INT | Direct-touch interrupt input |
| 16 | TP-SDA | Bidirectional touch I2C |
| 17 | TP-SCL | Touch I2C clock output |
| 18 | TP-RST | Touch reset output; polarity unverified |
| 19 | TP-VCC | Touch power; stated operating range 2.8-3.3 V |
| 20 | TP-GND | Touch ground |

The stated mating part is Omron XF2M-2015-1A or equivalent. The alternate
2 mm 2x7 interface reverses the first two power positions (pin 1 VCC, pin 2 GND),
then follows signals 3-14; it omits direct-touch connections. QSPI requires
IM0=1/IM1=0, whose assembly strapping is not exposed by either pin table.

Our GPIO accounting is:

| Connection strategy | Total signals | Incremental allocation if existing I2C can be shared |
| --- | --- | --- |
| Pixels, dedicated reset and WAIT | 8 | 8 |
| Above plus direct touch SDA/SCL/INT/reset | 12 | 10, subject to address/voltage/power-off compatibility |
| Above plus bridge touch interrupt | 9 | 9, only if supplied bridge firmware/protocol is confirmed |

This is allocation arithmetic, not a completed pin assignment. Reserve the
conservative direct-touch option until proxy support is established; remaining
native GPIOs then determine the lower-priority control header. No encoder or
physical buttons are needed in QSPI mode.

**Actual ESP32 example evidence.** TDO's [example page](https://www.shtdo.com/claprod_kflc.html)
links an [ESP32 QSPI archive](https://www.shtdo.com/Admin/Others/DownloadsPage.aspx?id=1805&nid=28&pre=1&ref=claproducts&t=ce1e104a43dbc409).
The investigation recovered ten complete source members from a partial download,
verifying their ZIP member sizes and CRCs and recording SHA-256 hashes. The whole
archive was not downloaded or verified. No source was compiled or executed.

The inspected BSP uses SPI3_HOST, DMA, half-duplex operation and
SPI_TRANS_MODE_QIO, sending the single-lane `12 00 2C 00` header followed by quad
pixel data. Its configuration is 720 x 720 RGB565 with GT9xxx touch; it does not
check WAIT in the inspected QSPI source, and its hardware-reset call is commented
out. It is therefore transport-feasibility evidence, not a qualified 480 x 480
B1617A/ICNT8952BN driver. The [evidence manifest](research/tdo-example-evidence.json)
is retained with the project. Complete inspected members remain in the local
research cache under `.git/v3-development-research-20260912/TDO-ESP32-QSPI-extract/`;
none has been adopted as production firmware.

Espressif documents a Quad Output transaction with a single-lane command/address
phase. An 8-bit command, 24-bit address and quad data phase is a plausible mapping
for the panel header; this remains an engineering inference requiring the exact
panel's reset, WAIT, format and readback contract.
[ESP-IDF SPI master documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/spi_master.html).

The remaining supplier evidence is concrete:

- The exact B1617A assembly/SKU, current controlled documentation, programmed
  bridge firmware, QSPI strapping and included cables; Mellow availability,
  sample quantity, MOQ, price, lead time and revision/substitution control.
- A corrected complete assembly drawing: page 17 names B1620A. Confirm connector
  pin-1 views, contact sides and straight/reversed cable requirements.
- Maximum and inrush currents for module and touch rails. The 180 mA value is
  typical only. Resolve touch-rail tolerance at its stated 3.3 V upper limit;
  the integrated backlight driver does not require a separate host 12.8 V rail.
- Reset, WAIT and interrupt direction/output type/timing, supply sequence and
  power-off limits. The specification prohibits driving inputs with logic power
  absent, affecting controller-only service and any shared I2C pull-ups.
- A buildable B1617A package: SDK version, initialization, backlight behavior,
  WAIT handling and pixel packing. Resolve the documented RGB888 waveform versus
  the sample's RGB565. Direct touch needs ICNT8952BN address/register/reset/IRQ
  information; proxy touch needs its read protocol and bridge-firmware support.

Desk qualification establishes a credible candidate with identified gaps.
Supplier evidence and a sample demonstration of cold start/reset, color/window
writes, touch, current and power-off behavior remain necessary. No supplier
contact, stock commitment or sample test occurred in this research.

## Electrical compatibility

The electrical investigation checked native connectivity/raw PCB pads and
primary manufacturer documentation. High confidence in topology or a component
limit does not establish board-level timing, current or thermal performance.
Items described as integration risks have not been observed as electrical faults
on V3 hardware.

| ID / severity | Finding and evidence | Required action / remaining evidence |
| --- | --- | --- |
| ELEC-01 / High | V2 U5-U8 are 5 V-powered SN74LVC1G125 devices with OE grounded and inputs from the 3.3 V MCU. [Output sheet](../archive/motor_expansion_board_v2/pcb/5v_pwm_output.kicad_sch:2119). [TI specifies](https://www.ti.com/lit/ds/symlink/sn74lvc1g125.pdf) VIH of at least 0.7 x VCC over 4.5-5.5 V, requiring 3.5 V at nominal 5 V. Thus input-high recognition is not guaranteed. | Replace/rework the four translation channels with suitable input thresholds, output drive, power-off protection and reset/enable states. The existing TI part has Ioff; powered-off backfeed is not an established defect of that part. |
| ELEC-02 / High, conditional on TTL receive | [J3 pin 1](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:3121) and [U4 pin 12](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_pcb:4846) share SCALE_UART_RX. [MAX3232 documentation](https://www.ti.com/lit/ds/symlink/max3232.pdf) specifies a driven high receiver output with its RS232 input open. A push-pull transmitter on J3 can contend with it even with DB9 unplugged. J9 swaps RS232 routing; it does not isolate the receiver. | Preserve connector locations while providing receive-source selection/isolation. Specify permitted J3 levels and both powered/unpowered connection cases. |
| ELEC-03 / High integration risk | V2 global VBUS is negotiated PD; the reference's identically named rail feeds [USBLC6-2 protection pin 5](references/owmc/power_supplies.kicad_sch:10155). [ST's limits](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) do not permit using this USB protection rail as a continuous 12 V clamp. | Use explicit separate PD input, qualified motor, service USB 5 V, accessory 5 V and controller rails. Check every transplanted protection/diode reference. This is a merge hazard, not a claim that the disconnected WIP already joins them. |
| ELEC-04 / High reuse risk | Essential reference MCU support crosses sheets: [RF supply filter L2](references/owmc/power_supplies.kicad_sch:8899), [CHIP_PU/AXP2101 PWROK and RC network](references/owmc/power_supplies.kicad_sch:5603), and USB support reside on the power sheet. | Extract a coherent MCU circuit and replace the removed PMIC's rail/reset functions deliberately. Review power ramp and reset release against [Espressif guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html). Copying only the MCU sheet is insufficient. |
| ELEC-05 / High allocation constraint | R8 uses 3.3 V memory, 8 MB octal PSRAM and external flash; memory and strapping pins constrain expansion. [Reference flash](references/owmc/owmc.kicad_sch:11648), [ESP32-S3 datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf), [GPIO restrictions](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html). | Keep display QSPI on a general-purpose SPI peripheral. Complete the pin/reset matrix including memory voltage, download/JTAG strapping, power/service status and diagnostics before committing spare I/O. |
| ELEC-06 / Operating-limit note; scope settled by DEC-016 | R8's normal maximum local ambient is 65 C; PSRAM ECC permits 85 C with reduced usable capacity. [Espressif Table 1-1](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf). [TMC2209 guidance](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf) makes sustained high-current performance dependent on PCB construction. | Follow the Fly reference and ordinary manufacturer layout/heatsink practices for room-temperature use. Normal bring-up observations remain; no separate thermal design, optimization or two-channel continuous 1.5 A RMS qualification is required. The upper software setting is not a continuous board rating or the recommended normal operating point. |
| ELEC-07 / High integration requirement | V2 module CLK contacts are unconnected, but the bare TMC2209 needs its full oscillator/supply/charge-pump/sense/exposed-pad implementation. Its 5VOUT is not an accessory supply. [V2 sockets](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_sch:9330), [ADI application circuits and sensing guidance](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf). | Design two complete IC channels and match actual fitted sensing mode/resistors to the RMS firmware contract. External sensing is the preliminary direction for the requested upper range. Verify exact Mellow part identity and OTP-dependent defaults; do not assume modules and bare ICs expose equivalent support. |
| ELEC-08 / High sequencing requirement | TMC2209 VS loss resets registers; VCC_IO alone does not power its internal logic. [ADI reset/power descriptions](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf). Service power can therefore preserve MCU state while the driver restarts. The [TPS5450](https://www.ti.com/product/TPS5450) also cannot accept ordinary 5 V USB within its 5.5 V minimum input rating. | Define valid-power sensing, deliberate driver reinitialization and output inhibition after PD returns. Hardware source isolation and firmware enable behavior need separate verification. Keep a suitable service-controller supply path. |
| ELEC-09 / High power-path consideration | Motor energy can return to VS, especially when the motor rail is separated from bulk capacitance; see [ADI section 3.1](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf). Energy magnitude is unquantified here. | Keep appropriate local motor capacitance downstream of switching and assess clamp/discharge behavior against the load/fault envelope. Reverse blocking alone does not control motor-rail overvoltage. |
| ELEC-10 / Medium, panel dependent | Retained EXP headers carry +5 V and direct MCU signals; one active display does not establish the inactive module's pull-up voltages or powered-off behavior. [V2 display connections](../archive/motor_expansion_board_v2/pcb/pico_expansion_board.kicad_sch). | Define cable/population exclusivity or isolation, verify every selected module's signal levels and unpowered states, and allocate actual touch/reset/interrupt/backlight/TE signals. |
| ELEC-11 / Medium service implementation | The [reference four-contact service header](references/owmc/power_supplies.kicad_sch:7956) does not implement Type-C CC termination; retained J8 lacks data contacts. [TI Type-C guidance](https://www.ti.com/lit/wp/slyy109b/slyy109b.pdf). | Design the new optional service receptacle and fixture interface explicitly, including native USB data, permitted service power, ground and boot/reset recovery. [Espressif recovery guidance](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/usb-serial-jtag-console.html). |
| ELEC-12 / Medium RF reuse risk | [Reference antenna/matching assets](references/owmc/owmc.kicad_sch:13949) do not establish V3 tuning. [Johanson's antenna guidance](https://www.johansontechnology.com/docs/3827/Antenna-2450AT18A0100001E-Rev4.0.pdf) depends on customer-board layout and clearance. | Reserve antenna/matching space before placing heatsinks, confirm exact antenna identity and stack-up, and validate RF under the declared installation conditions. No existing case is mandated. |
| ELEC-13 / High selection gap | Four reference RGBW pixels account provisionally for about 0.30 A; the [MG90S manufacturer page](https://towerpro.com.tw/product/mg90s-3/) does not establish servo stall current. [Pixel reference](https://www.adafruit.com/product/4776). Both servo transients and the selected display contribute to the 5 V demand. | Obtain representative servo and display load evidence, include conversion/transient/thermal margins, and then select the converter. No reduced current rating is established by permission to downsize. |

### Fly TMC2209 reference implementation

The bounded follow-up found Mellow's **Fly-2209 schematic revision 1.0,
2021-11-21**, drawn by `jays_s_uk`. This identifies the published drawing,
not a verified current-production module revision.
[Official StepStick page](https://mellow-3d.github.io/fly_tmc2209_general.html),
[pinned schematic](https://github.com/Mellow-3D/Fly-Drivers/blob/c0ffd6f2027eac64d2768ec59325dbcfd9f7e5f4/2209/Fly-2209-Schematic.pdf).

| Circuit | Published reference values / connections |
| --- | --- |
| External sensing | R5/R6: 0.11 ohm, BRA/BRB to ground |
| Charge pump | C3: 22 nF CPO-CPI; C5: 100 nF VCP-motor supply |
| Decoupling | C4: 2.2 uF on 5VOUT; C2: 100 nF on VCC_IO; C1: 1 uF and C6/C7: 100 nF each on motor supply |
| Default disable | ENN: R2 20 kohm pull-up to VCC_IO; STDBY and exposed pad grounded |
| VREF adjustment | 20 kohm resistor plus 20 kohm potentiometer from 5VOUT |
| Address / diagnostic | MS1_AD0 and MS2_AD1 exposed; DIAG switch to external contact |

These are high-confidence schematic facts. Capacitor ratings and resistor
tolerance/power ratings are unspecified. The three-pad R7 labelled 20K is
ambiguous; the [official UART illustration](https://mellow-3d.github.io/images/fly-2209/fly-2209_uart.webp)
instead shows 1 kohm between MCU TX and the shared RX/PDN_UART connection.
Do not derive an onboard production BOM from that ambiguous R7 label.

The [official module photograph](https://mellow-3d.github.io/images/fly-2209/fly-2209_general.webp)
shows a finned heatsink and exposed copper landing with a via array, supporting
the requested construction approach. [Current Mellow documentation](https://mellow.klipper.cn/en/docs/ProductDoc/ModuleDrive/tmc2209/)
distinguishes the Fly 2209 DIAG switch from the 2209C direct DIAG connection,
specifies 0.110 ohm sensing and shows a 0.8 A configuration example. That example
is not a measured continuous-current rating.

Use manufacturer guidance when adapting the module: ground CLK directly near
the IC for its internal oscillator, assign the two UART addresses deliberately,
and configure current-control/sensing registers after each driver power-up.
No module-specific OTP programming is needed for ordinary register configuration.
The module's local capacitors do not establish the board's total bulk-capacitance
requirement. [ADI TMC2209 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf).

No native PCB, production BOM, OTP record, current supplied revision or heatsink
specification was found in the [Fly-Drivers repository](https://github.com/Mellow-3D/Fly-Drivers).
Those limits do not reopen the user's excluded thermal-design scope.
Reviewed PDF SHA-256:
`058bc43b17b2a06ca5bd18efb575b5384883d345d63df6c61516b2a26b33978a`.
The [reviewed schematic PDF](references/vendor/Fly-2209-Schematic-v1.0.pdf) is
retained in project references. Local rendered evidence remains under
`.git/v3-development-research-20260912/`.

## Static firmware feasibility

The existing firmware cannot be ported through a pin-header change alone.
However, no identified peripheral-resource class requires a second MCU. A
candidate arrangement uses MCPWM for two STEP outputs, LEDC for the two servo
signals, RMT for the two pixel chains, two UARTs, shared I2C and SPI2/3 for the
selected display. Using RMT for all STEP and pixel outputs would consume all
four TX channels in Mini12864 mode. This is a proposed allocation, not a
pin-level or timing proof. [ESP32-S3 peripheral descriptions](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf).

| Function | Proposed resource / GPIO demand | Qualification |
| --- | --- | --- |
| Two STEP/DIR/ENABLE channels | MCPWM plus GPIO / 6 | Timing/stop behavior must be specified and measured |
| Driver and external serial paths | Two UARTs / 4 | Retain driver addresses and fix external RX source selection |
| EEPROM and compatible touch | Shared I2C / 2 | Exact touch bus/address/power still unknown |
| Two servo signals and external pixels | LEDC plus RMT / 3 | Distinct power-domain/reset behavior required |
| Mini12864 mode | General SPI, controls and separate RMT lighting / 10 | Retain its encoder/buttons and lighting |
| Alternative QSPI mode | General SPI / 6 bus signals plus actual controls | No encoder/buttons; panel and input method must be selected |
| Service/power status, indicators, diagnostics and extra I/O | TBD | Not covered by the former two-spare estimate |

The conservative 27 ordinary GPIO candidates are 1, 2, 4-18, 21, 38-44, 47 and
48 after memory, native USB and uncomplicated boot reservations. GPIO43/44
also need review for their default UART0 behavior. Twenty-five are provisionally
allocated in Mini12864 mode before added status/diagnostic signals. Final
allocation may use reviewed strapping pins where reset/recovery remains reliable.
Remaining usable native GPIOs go to the requested control header; an expander
is not required and no spare-pin count is promised. [GPIO documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html).

| ID / severity | Source incompatibility or unresolved contract | Action within hardware/feasibility scope |
| --- | --- | --- |
| FW-01 / High | [Build configuration](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/CMakeLists.txt#L16) imports Pico SDK/RP FreeRTOS and links RP/CYW43 libraries. [app.c](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/app.c#L32) starts the scheduler explicitly. ESP-IDF instead schedules before app_main and uses byte-based task-stack sizes. [IDF startup](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/startup.html), [FreeRTOS differences](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos_idf.html). | Provide an independent ESP32 bring-up target; document platform replacement, stack-size conversion and initialization barriers for the separately scoped application port. |
| FW-02 / High | Memory, USB and boot reservations make extra GPIO conditional; see [current board assignments](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/targets/raspberrypi_pico_w_config.h#L12). | Complete a per-display pin/resource/reset/power matrix, including every status/diagnostic/recovery signal and inactive-device behavior. |
| FW-03 / High | [Interrupt dispatcher](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/gpio_irq_handler.h#L40) silently rejects GPIO above 28 and uses Pico core APIs. [Mini12864 initialization](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/mini_12864_module.cpp#L231) enables interrupts before its queue is created. | Use ESP32-native interrupt handling in bring-up; record the dispatcher and queue-order replacement in the application handoff. High ESP32 GPIOs cannot use the existing helper unchanged. |
| FW-04 / High | [STEP](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/stepper.pio#L1) and [pixel](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/neopixel_led.c#L153) generation use PIO; [servo updates](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/servo_gate.c#L47) directly write paired RP PWM registers. | Define peripheral/clock/buffering/stop contracts and exercise them with representative concurrent interface traffic. [MCPWM](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/mcpwm.html), [LEDC](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/ledc.html), [RMT](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/rmt.html). Static resource availability does not establish timing. |
| FW-05 / High | [Driver transport](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/motors.c#L75) writes RP UART registers. [Persistent current/sense settings](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/motors.c#L270) feed the library's [RMS/milliohm contract](https://github.com/terjeio/Trinamic-library/blob/d7debfaffcb6e3d62c025455a629be6bd7e4d22d/tmc2209.c#L235). | Define bounded single-wire UART transport, echo/reply handling and addresses 0/1; align fitted sense components, current limits and startup polarity with the board contract. |
| FW-06 / High | [Startup](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/app.c#L38) initializes Mini12864/lighting unconditionally; the [LCD backend](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/mini_12864_module.cpp#L356) is UC1701 SPI, with no QSPI panel backend. | Select actual panel/controller/driver, prove each display mode separately, and ensure exclusive initialization/pin ownership. [ESP-IDF SPI LCD support](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/lcd/spi_lcd.html) does not establish universal panel compatibility. |
| FW-07 / High | [Menus](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/menu.c#L49) expect encoder/button events; the [reset-labelled input](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/mini_12864_module.cpp#L167) is a software event. [Web mirroring](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/html/display_mirror.html#L27) assumes 128 x 64 data. | Preserve Mini12864 controls; define QSPI input and future UI/mirroring contracts without adding excluded buttons. Allocate/test actual touch signals if touch is selected. Never wire the Mini12864 software button to EN solely from its label. |
| FW-08 / High | The [current 128 KiB heap configuration](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/FreeRTOSConfig.h#L75) and application allocations do not establish an ESP32 memory budget. PSRAM has [DMA/cache restrictions](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/external-ram.html); descriptors need internal memory. | Pin SDK and memory configuration; budget internal RAM, PSRAM, stacks, display buffers and flash partitions. External 16 MB flash is a reference-based choice, not proof that an unbuilt future application/OTA layout fits. |
| FW-09 / High | [Driver initialization failure](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/motors.c#L665) enters an error loop before the present scheduler starts; [servo GATE_DISABLED](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/servo_gate.c#L97) changes state without stopping existing PWM. Absent motor power causing initialization failure has not been demonstrated. | Define service independently of application peripheral initialization, with hardware power isolation and explicit output/re-enable behavior. Bench-test reset, main-power loss and unpowered interfaces. |
| FW-10 / High | Existing service relies on [Pico BOOTSEL/UF2](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/manuals/firmware_update_via_usb.md#L6) and [RP watchdog reboot](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/system_control.c#L13). | Expose native USB GPIO19/20, the selected protected service supply, ground and GPIO0/EN recovery, preserving valid download strapping. Define ESP32 fixture/image instructions and recovery from USB-disabling firmware. [Espressif service guidance](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/usb-serial-jtag-console.html). |
| FW-11 / High | [Settings reads](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/common.c#L107) and [writes](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/common.c#L186) include CRC32 over raw struct bytes, legacy revision handling and automatic default writes on invalid data. Types include enum/bool/padding. [Board ID](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/eeprom.c#L42) uses RP oscillator registers. | Document schema/CRC/migration/default and identity behavior for the future port. Use read-only legacy fixtures before any migration/default write test. Retaining EEPROM hardware alone does not establish cross-compiler data compatibility. |
| FW-12 / Medium | [Networking and indicator](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/wireless.c#L283) depend on CYW43; [external serial configuration](https://github.com/eamars/OpenTrickler-RP2040-Controller/blob/4e384a384d714200eb5157a08e33d424e8e49f85/src/scale.c#L90) uses multiple formats. | Record network/API/status-indicator and serial contracts. Demonstrate ESP32 radio and UART hardware without claiming the complete web application is ported. [ESP Wi-Fi](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/network/esp_wifi.html), [UART](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/uart.html). |

## Acceptance boundary and handoff

Static assessment must finish with the exact MCU/flash/PSRAM and SDK selection,
selected panel and control method, a complete per-mode pin/peripheral/reset
matrix, power/service-state contract, driver addresses and RMS/sense units,
serial formats, settings schema policy and programming/recovery procedure.
Application implementation tasks must remain clearly assigned to the separate
firmware scope.

Hardware acceptance then requires a reproducible ESP32 bring-up image, memory
and interface checks, blank-board/recovery programming through the actual
contacts, both selected display modes independently, concurrent interface
waveform checks, and power/reset/source-isolation measurements. RF checks and
ordinary operating observations use recorded conditions. A separate thermal
design and continuous 1.5 A RMS qualification are outside scope. These are planned acceptance
checks; none passed through this static investigation.
Under DEC-019 these physical checks belong to the owner/Mellow. The assistant
delivers static feasibility, design constraints and test needs at P-01; it does
not implement or run the downstream bring-up firmware. Read the action descriptions
above in that ownership context.

Firmware research used clean commit
`4e384a384d714200eb5157a08e33d424e8e49f85`. Mechanical measurements used native
KiCad 10 and raw-file inspection. Electrical evidence combines raw/native
connectivity with the cited manufacturer limits. All investigated CAD and
firmware sources were left unchanged. Full ERC/DRC, SPICE, thermal simulation,
EMC, exported-Gerber and lifecycle review were outside this targeted research.

## Reference cleanup and project independence

After DEC-018, the mechanical agent independently audited the imported tree and
its dependencies. Its findings support keeping only the actual OWMC schematic
pair and PCB as embedded 2D evidence. The old project included stale personal
export paths, mismatched symbol/footprint aliases, missing placeholder libraries,
application-specific models and historical scaffolding. None was adopted for V3.
The archive's V2.1 assets serve the compatibility baseline and were left intact.

Root moved all 203 imported files (50,481,575 bytes) into a local rollback copy
and verified every hash afterward. [The cleanup record](research/asset-cleanup.json)
preserves their inventory; [selected references](references/README.md) contain the
exact inspected OWMC source pair/PCB plus the TDO and Fly specifications, with
source hashes and purposes. The OWMC power sheet includes the source's recorded
uncommitted change, not an assumption about the proven revision.

[The active CAD area](pcb/README.md) now contains only process/library documents.
No V3 CAD has been created. The reference snapshot does not promise complete
3D rendering or original configured ERC/DRC; production assets must be separately
vendored and checked. Pinned [application/firmware source citations](research/source-citations.json)
replace machine-specific documentation links. No other local project is needed
to read the retained evidence or resolve future production assets under the
required library policy.

Live work and corrective actions are tracked only in [PROGRESS.md](PROGRESS.md).
