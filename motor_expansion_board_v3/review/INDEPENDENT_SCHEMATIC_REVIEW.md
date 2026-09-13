# B1 independent controller schematic review

Review date: 2026-09-13 NZST (2026-09-12 UTC). Reviewer: independent electrical-review agent; not the schematic author. Only this report was edited by the reviewer.

**Verdict: suitable for owner schematic review, with the bounded qualifications below. No definitive remaining schematic connection blocker was found.** This is not PCB approval, fabrication release, a measured current rating, or a claim of application operation. The owner's approval of the exact reviewed package remains required by REQ-PROC-007/G-02.

The review covers the corrected five-sheet B1 controller: one directly fitted ESP32-S3R8, two TMC2209 ICs, retained V2.1 interfaces and an external display connector. It follows DEC-020/021 and the latest hardware-only scope. The rejected 15-sheet architecture is not a baseline. No firmware-port analysis, thermal design exercise or additional power modes are introduced.

## Findings and disposition

| ID | Severity / confidence | Finding and bounded action | Requirement / stage |
| --- | --- | --- | --- |
| ISR-01 | Warning, resolved; high, manufacturer and native evidence | Q2 originally used 2N7002K, whose published low-voltage drive guarantees were weaker than Q1's device. The author changed Q2 to BSS138LT1G, retaining G=1, S=2, D=3. The amended native symbol, MPN/manufacturer and XML pins were checked. No remaining correction. | REQ-DISP-004, REQ-IF-002; schematic correction closed |
| ISR-02 | Warning, open; high that evidence is incomplete | C8's retained Honor RVT1V331M1010 now has a source-backed package/ripple basis, but no switching-frequency ESR specification. TPS5450 internal compensation depends on the output filter. Obtain suitable ESR/impedance evidence or qualify an equivalent capacitor against the TPS5450 filter requirements before final component/PCB commitment. Retaining the old capacitor identity does not establish stability. | REQ-PWR-001, REQ-SRC-001; component qualification before PCB/BOM freeze |
| ISR-03 | Warning, open; high for documentation gap, moderate for interface suitability | J14 follows the TDO numbered pin table, but the supplied assembly's FFC contact face, cable pin-1 mapping, maximum/inrush load and WAIT/TP-INT output electrical specification remain unconfirmed. Confirm those exact interfaces; the PDF has inconsistent direction labels for WAIT/SDO. Do not infer guaranteed MCU input-high margins from the display's input-threshold table. | REQ-IF-002, REQ-DISP-004; supplier/package qualification and external interface test |
| ISR-04 | Warning, open; high, native and source evidence | The Mini12864 EXP2.8 button input has a dedicated 5 V-tolerant Schmitt buffer, but compatibility still depends on the supplied panel's KILL link not shorting its +5 V supply when pressed. Confirm the exact Mini revision/link/cable. The controller buffer cannot fix a short within the panel. | REQ-IF-001, REQ-DISP-001; supplied-panel qualification |
| ISR-05 | Warning, bounded; high for circuit facts, unmeasured behavior | Power-up, repeated/slow power cycling, motor deceleration, combined servo/display loads and USB attach/detach remain hardware checks. Raw PD VBUS is intentionally not voltage-qualified or reverse-blocked. The schematic does not guarantee rejection of an actual 5/9 V fallback or absorb a specified regenerative energy. These are limitations of the retained baseline, not requests to restore the rejected eFuse/comparator architecture. | REQ-PWR-002, REQ-USB-001/002, REQ-ACC-001; external prototype checks |
| ISR-06 | Warning, open; high, BOM/native evidence | Many commodity passives still lack exact MPNs. Select their stated ratings, effective ceramic capacitance, shunt construction and mechanical variants during preliminary-BOM/PCB work. D4 already nominates MDD SS54, C22452, SMA/DO-214AC; its exact source/package qualification remains pending. This package is not order-ready. | REQ-SRC-001, REQ-PROC-003/004; preliminary BOM and PCB-stage tasks |

There is no requested circuit expansion associated with ISR-02 through ISR-06. Any substitution that changes an electrical value, pin map, supply behavior or connector assignment needs the affected schematic check renewed.

## Exact review snapshot

Paths are relative to `motor_expansion_board_v3/`. SHA-256 values were read from the files, independently of `connectivity-check.json`. This snapshot includes the bounded drawing-only renewal recorded at the end of the report.

| Native schematic | SHA-256 |
| --- | --- |
| `pcb/motor_expansion_board_v3.kicad_sch` | `40645ebb151ab6495bef7ab9d88cccd5e624aa68e4fd15b8e546a6289acedbb5` |
| `pcb/power.kicad_sch` | `f48cb38867dae5f4169983fb76b84d42da3aefc9785074f143782099cf5f55d4` |
| `pcb/motors.kicad_sch` | `a83bd6036476dbe141f3a2d9b3e4499390c32ea9066d38b732e1b968aadab0f5` |
| `pcb/interfaces.kicad_sch` | `0d891e1cc6a53087163b59ecb9d11a5b2300da12e4081eb6dbd96973b40028b0` |
| `pcb/display_connector.kicad_sch` | `0e6c9d366cbc12420a4b152898c2b9118bc336b9ed7ef222d652a23a6ea4f0b7` |

| Supporting artifact | SHA-256 at review |
| --- | --- |
| `review/netlist.xml` | `3bf286ebff8c21899d526ba58faae1e93ec27ede2f30546632dff2ad159f5589` |
| `review/erc.json` | `a7220582c6426394f16e0ee7226a73011c6a29ed0bcb09dfb9572ddeb14a60ba` |
| `review/motor_expansion_board_v3.pdf` | `f04ffaf10e90bada036e72d9160b490ae499f370102fb54cd66aeded19d44d46` |
| `review/connectivity-check.json` | `268d332f08374250b515d6d2048644afd64112f9ad3b6c25607f340f6bba1ef8` |
| `review/schematic-analysis.json` | `8cae66cc087a2528585c2386bfdaebbace87775daa6710d7d3b32d4e4446b618` |
| `design/net-intent.json` | `05bfc6f607892d36325c893f9d068717b1d3d630f8a244c62a467590dac9c2c2` |
| `design/net-endpoints.json` | `7155dd7219fca4dfac477c339f1cc13f3b838f78d123a61ff9e9535e3f3df9ee` |
| `pcb/motor_expansion_board_v3.kicad_pro` | `30f39d970265a233fdad4cf0dc368b2cf8e4852a9e6562571b3bfc7d5e2acbab` |
| `review/sheet-1.png` | `e5ea59b16c4fc392ba426c3c7a9569cc5aaabeb29155efdb5d427acf8c1f0286` |
| `review/sheet-2.png` | `c12488ea9147eb847b6f9bab580f55d03f8328f8ff643c6702d4e6ee708765b8` |
| `review/sheet-3.png` | `daf4501aab1d5a437c17538ef819fe5c95ee153b8147d5c8f259d80ec4bad51a` |
| `review/sheet-4.png` | `6a768d632bb607eb82e54773e2cf99a613ebbd49aa13891d2151f7135220f6d9` |
| `review/sheet-5.png` | `69c067581fc420905e264271f9ae9f6c9e1ea4123a14ed95215381b9e8e2db87` |

L4 was amended during review from provisional 3.9 uH to MWSA0603S-4R7MT, 4.7 uH. Q2 was amended as ISR-01. These changes are included in the hashes above. Earlier hashes and the rejected draft's reviews do not describe this verdict.

## Verification basis and hierarchy

- Read the root AGENTS instructions, current requirements/progress, V2 study, power/use-case context, and the KiCad review/report and datasheet workflow guidance. The active restart decisions take precedence over historical proposals.
- Independently parsed all five native schematics, including embedded pin geometry, wires, labels, junctions, hierarchy ports and no-connect markers. Reconstructed the electrical groups in memory and compared endpoint sets against native KiCad XML: **166 component instances, 588 physical endpoints, 37 explicit NC, 116 connected nets and 551 connected endpoints; zero group mismatches**. The Q2 part-only amendment was checked separately against the unchanged three-pin connections.
- Inspected all five rendered sheets and rechecked the final refreshed power and display PNGs. They show L4=4.7 uH and Q2=BSS138LT1G, matching the final native CAD/XML.
- The hierarchy has one root and four children, matching named sheet ports. There are **zero global signal labels**. Ordinary global ground symbols are expected.
- Native KiCad 10.0.4 ERC reports **zero errors and zero warnings** on all five sheets. The project has no ERC exclusions. The ERC export lists four ignored check categories: single global label, four-way junction, simulation-model issue and footprint-filter mismatch. These limits are disclosed; ERC is not a physical package or electrical-performance certificate.
- The supplied schematic analyzer was inspected and triaged below. Its automatic per-datasheet verification coverage is zero; manual manufacturer checks provide the electrical evidence in this report.

## Power and service review

| Domain | Actual source and principal destinations | Result |
| --- | --- | --- |
| `VMOTOR` | J8 raw VBUS; U10/U11 VS; IC1 VIN; U3 input resistors | Retained V2 topology. Compatible 12 V PD source required. |
| `V5V` | IC1 TPS5450, L1/D4/C8; accessories, display main supply, IC2 | 5 A-class converter retained; assembled capacity unmeasured. |
| `V3V3` / `V3V3_RF` | IC2 AP63203; U1, U2, U4, U10/U11 VCC_IO, U12/U14, U13; RF through L2 | One board-powered controller. No service power feed. |
| `VDD_SPI` | U1 pin 29; external U9 flash and local capacitors | Intended 3.3 V memory domain; GPIO45 held low. |
| `V3V0` | U13 TLV75530 from V3V3 | Touch power, reset pullup and shared I2C pullups; always fitted. |
| `SERVICE_VBUS` | J16 or TP1 only; D7 reference, Q1 gate network, R28/C39 | Presence/protection network only; no connection to a board supply input. |

**CH224K:** native U3 pins 9/2/3 are respectively GND/GND/PD_VDD, the 0/0/1 12 V strap. Pins 7/6 connect CC1/CC2; 1 has R8=1 kOhm and C6=1 uF; 8 senses VBUS through R7=10 kOhm; 4/5 are joined locally; PG is deliberately NC. These match the CH224K-specific reference in the [WCH datasheet](https://www.wch-ic.com/downloads/CH224DS1_PDF.html), locally cached as `datasheets/CH224K.pdf`, v2.1 pp. 2–3, 9. The embedded ground pad is numbered 11 in the stock symbol/footprint and 0 in WCH's drawing; both denote the exposed ground pad. CH224A/Q tables must not be substituted for the K variant. At 12.6 V with about 3.3 V on VDD, R8 dissipates approximately 87 mW; its stated 0.125 W minimum is not a 20 V-operation qualification.

**TPS5450:** IC1 uses the stock TPS5430 symbol with the matching physical pin functions, explicitly identified as TPS5450DDAR. VIN=7, PH=8, BOOT=1, VSENSE=4, GND=6/9; pins 2/3 are NC and EN=5 floats enabled. C7 is 10 nF between BOOT/PH; D4 cathode faces PH. R9/R10 give `1.221 × (1 + 10000/3160) = 5.0849 V`. Combining the specified full-range reference limits with 1% resistors gives **4.9059–5.2645 V**, excluding ripple/transients. This fits the display/AHCT 4.5–5.5 V steady-state range. The 15 uH/330 uF filter and 2 × 4.7 uF input topology follow the retained circuit; C8 qualification remains ISR-02. [TI datasheet](https://www.ti.com/lit/ds/symlink/tps5450.pdf), pp. 3, 6, 13–15.

**AP63203:** IC2 pin 1 senses V3V3 directly; pins 2/3 connect V5V, 4 is GND, 5 feeds L4, and 6 has 100 nF to SW. C35=10 uF, C37/C38=22 uF each. The fixed-output variant is correct. Table 2's default is 3.9 uH, but section 10 permits approximately 2.2–10 uH, so the amended **4.7 uH** is not a wrong-variant substitution. Calculated ripple at 5.085 V/3.3 V/1.1 MHz is 0.224 A p-p; L−20% and frequency−6% give about 0.299 A p-p, or 2.150 A peak at a hypothetical 2 A load. This is a component check, not a board load rating. The CCM output limits are 3.27–3.33 V. Select the actual capacitors by effective capacitance and ripple capability. [Diodes datasheet](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf), pp. 2, 5, 13–14.

**U13/touch rail:** TLV75530 DBV pin map 1=IN, 2=GND, 3=EN, 4=NC, 5=OUT is correct; IN/EN are tied to V3V3, with 2.2 uF input/output capacitors. A regulated 3.0 V output is within TDO's 2.8–3.3 V touch range; even the broader 1.5% accuracy interval is 2.955–3.045 V. The 3.3-to-3.0 V headroom does not establish full 500 mA regulation at every corner: this variant has a 300 mV maximum dropout specification at 500 mA through 85°C. Actual touch load and transient behavior remain unmeasured. [TI TLV755P](https://www.ti.com/lit/ds/symlink/tlv755p.pdf), pp. 3, 5–6, 15–17.

**USB isolation:** U12 common D+/D− pins 4/6 face the host; D1 pins 2/8 face the MCU through R29/R30=22 Ohm. S=1 is grounded; unused D2 pins 3/7 are NC; VCC=10 is V3V3. Q1 pulls OE=9 low only when service VBUS is present, against R25=10 kOhm. Q1's insulated gate, not a transistor base junction, receives VBUS through R26=1 kOhm; R27=100 kOhm pulls it down. R28=3.3 kOhm and C39=100 nF discharge/reference the service input. D7's VBUS pin is on SERVICE_VBUS, not V3V3. [TI TS3USB30E](https://www.ti.com/lit/ds/symlink/ts3usb30e.pdf), pp. 3–5, 12; [onsemi BSS138L](https://www.onsemi.com/pdf/datasheet/bss138lt1-d.pdf), pp. 1–2; [ST USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), pin diagram.

| Main PD | Service VBUS | Hardware behavior |
| --- | --- | --- |
| Off | Absent | Board off. |
| Off | Present | Board still off; U12's specified power-off isolation limits host-data leakage. |
| On | Absent | Board powered; Q1 off and OE pulled high, disconnecting MCU USB pullups from the host-facing ports. |
| On | Present | Board powered from main PD; USB data path enabled for service. |

J16 is optional/DNP. TP1–TP6 provide service VBUS/data/GND/BOOT/CHIP_PU access; TP7 is measurement-only V3V3. Neither PC-only nor fixture-only board powering is implemented. Both service connector CC pins have their own 5.1 kOhm pulldown. Main J8 is the six-contact power/CC receptacle, not a data connector.

The MOSFET circuit is a **presence detector**, not a precision VBUS-valid detector. It does not prove the 4.35/4.75 V voltage behavior described in [Espressif's self-powered USB guidance](https://docs.espressif.com/projects/esp-usb/en/latest/esp32s3/usb_device.html#self-powered-device). Ordinary absent-host disconnect and unpowered-board isolation are supported by the topology. Full USB voltage/timing compliance, host removal and ROM enumeration need the external checks in ISR-05; no blanket compliance claim is made.

## Controller, memory and pin suitability

U1 is exactly one ESP32-S3R8. Native supply connections cover pins 2/3 through the RF supply filter, pins 20/46/55/56 on V3V3 and exposed pad 57 on GND. C19–C28 provide the intended local/bulk and memory decoupling. Pin 29 powers U9; it is not accidentally shorted to an unrelated rail.

The R8-specific reserved pads **28 and 38–42 are NC**. External Quad flash uses pads 30–35 on the shared memory bus. GPIO45 is pulled low by R20, selecting the required 3.3 V memory supply; GPIO46 is pulled low by R21 and GPIO0 high by R19. BOOT and CHIP_PU have independent grounded switches/pads. R18/C31 provide the usual 10 kOhm/1 uF reset delay. The RC is not proof of reset timing under arbitrary slow or repeated supply cycles. [ESP32-S3 datasheet v2.2](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf), tables 1-1, 2-11, 2-14 and section 3; [hardware checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html), power/reset and memory sections.

| Function | Allocated MCU GPIOs | Hardware assessment |
| --- | --- | --- |
| Native USB | 19 D−, 20 D+ | Correct fixed USB pins, physical pads 25/26. |
| Driver 1 / driver 2 | STEP 38/39, DIR 40/41, EN 42/48 | Ordinary usable outputs. Pad 36 is GPIO48; its SPICLK_N symbol name does not make it an R8-reserved pad. |
| Driver UART / scale UART | 17/18 and 15/16 | Separate routable serial pairs; no assigned pin overlaps. |
| Servo/pixel outputs | 4, 5, 6 | Hardware PWM/data-capable GPIOs through AHCT buffers. |
| Shared display | CS10, SCK12, D0=11, D1=13, D2=14, D3=1, reset43, DC/touch-reset44 | Routable display signals; single-display use is mandatory. GPIO1's power-up glitch and UART0 reset-time activity must not be treated as valid commands. CS has a pullup. |
| WAIT / button / interrupt | 47, 21, 9 | Separate usable inputs. WAIT does not share the protected Mini reset button. |
| I2C | 7 SCL, 8 SDA | Common open-drain bus with pullups to 3.0 V. |
| J15 spare signals | 2, 3, 45, 46 | GPIO2 is the ordinary spare; the others have explicit strap restrictions. Header wiring must preserve reset straps. |

This establishes pin/peripheral suitability only. It does not assess the application port, throughput, driver implementation or runtime parity.

U9's SOIC-8 map is correct: 1 CS, 2 IO1, 3 IO2, 4 GND, 5 IO0, 6 CLK, 7 IO3, 8 VCC. The fitted W25Q128JVSIQ is the 3.3 V/208-mil package choice, with local bypass and CS pullup. [Winbond datasheet](https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf), pp. 5, 60, 67, 75.

Y1 uses crystal terminals 1/3 and grounded case pads 2/4. The 40 MHz/24 nH series circuit and initial load capacitors retain the selected OWMC reference approach. The exact Q22FA12800101 ordering specification, frequency/loading and drive level remain source/PCB qualification, not a measured oscillator result. [Epson FA-128](https://download.epsondevice.com/td/pdf/app/FA-128_en.pdf), p. 6. AE1 correctly uses feed pin 1 and electrically NC anchor pin 2; solder the anchor and implement the antenna keepout/matching during PCB work. [Johanson drawing](https://www.johansontechnology.com/docs/3827/Antenna-2450AT18A0100001E-Rev4.0.pdf), pp. 2–3.

## Motor and retained-interface review

U10/U11 physical pins were checked against [ADI TMC2209 rev. 1.09](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf), pp. 9–11, 14, 52–55, 74–79. Both use:

- VS pins 22/28 on VMOTOR, VCC_IO=15 on V3V3, ground pins 3/18/29 and permitted unused pin 25 on GND.
- 22 nF CPO–CPI, 100 nF VCP–VMOTOR, 2.2 uF on 5VOUT, local VS/VIO bypass and a 100 uF bulk capacitor.
- Separate BRA/BRB 0.11 Ohm, 1%, 1 W low-inductance shunts; grounded CLK/SPREAD/STDBY; 10 kOhm EN pullups and STEP/DIR pulldowns.
- Addresses 0 and 1 from MS1/MS2, shared PDN_UART, TX through R1=1 kOhm and direct RX. DIAG/INDEX are intentionally unused.

With external sensing and digital scaling, the nominal full-scale calculation is `0.325 / ((0.11 + 0.020) × sqrt(2)) = 1.768 A RMS`. This spans the requested configurable range; it is not the default board current or a continuous rating. The 20 kOhm/20 kOhm VREF networks provide an analog reference, but VREF loading/tolerance must not be ignored if analog scaling is used. The documented 800 mA RMS default requires configuration before enabling; EN pullups support that sequence. Do not substitute preprogrammed OTP/internal-sense behavior without checking it. No thermal performance was inferred from IC or shunt ratings.

The ordinary reference implementation and passive-heatsink/ground-pad practices remain appropriate PCB inputs. The [official Fly reference schematic](https://github.com/Mellow-3D/Fly-Drivers/blob/c0ffd6f2027eac64d2768ec59325dbcfd9f7e5f4/2209/Fly-2209-Schematic.pdf) is corroborating implementation evidence, not certification of this assembled board.

The following connections were independently compared with pads in the archived V2.1 native PCB, not only with the V3 contract:

| Connector | Preserved electrical role |
| --- | --- |
| J6/J7 | 1=B2, 2=B1, 3=A1, 4=A2. No swapped winding or shunt connection found. |
| J1 EXP1 | 2 click/IRQ, 3 CS, 4 DC, 5 reset, 6 buffered pixel, 9 GND, 10 +5 V; original NC positions retained. |
| J2 EXP2 | 2 clock, 3/5 encoder, 6 MOSI, 8 panel reset button, 9 GND, 10 +5 V; original NC positions retained. |
| J3 | 1 board RX, 2 board TX, 3 GND; specified 3.3 V TTL. |
| J9/J10 | Existing 2×2 TX/RX routing and DB9 pins 2/3/5; unused DB9 contacts remain NC. |
| J11/J12/J13 | 1 GND, 2 +5 V, 3 buffered signal; PWM2/PWM1/PWM3 roles preserved. |
| J8 | CC1/CC2, VBUS and ground roles preserved; mating-plane placement remains a PCB requirement. |

U4's MAX3232 uses 3.3 V logic power, four 100 nF pump/storage capacitors plus bypass, and the correct T1/R1 pins. Unused receiver/driver inputs are grounded. Added J17 selects TTL versus RS232 RX so the two receiver outputs are not joined; the shunt must select one input. TX is shared intentionally. [MAX3232 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX3222-MAX3241.pdf), pin configuration and capacitor-selection table.

U5–U8 are specified as **SN74AHCT1G125DBVR**, despite the generic symbol value. Their 2.0 V VIH requirement at 4.5–5.5 V makes the 3.3 V-to-5 V interface intentional. OE=1 is grounded; input=2, GND=3, output=4, VCC=5. All four have bypass and input pulldowns. Their outputs supply signals, not servo/LED power. [TI AHCT datasheet](https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf), pp. 3–5.

U2 retains address 0x50 and WP low. R5/R6 pull I2C to V3V0, not 3.3 V: a nominal regulated 3.0 V high exceeds both the MCU's 0.75×VDD threshold and CAT24C256's 0.7×VCC threshold, including the stated rail tolerances. Actual touch leakage, bus capacitance and optional internal pullups still determine margins/rise time. Do not enable 3.3 V pullups on the shared touch bus. [CAT24C256](https://www.onsemi.com/pdf/datasheet/cat24c256-d.pdf), pp. 1–3.

## External display details

J14's 20 pins match [TDO B1617A specification v1.0](https://www.shtdo.com/Admin/Others/DownloadsPage.aspx?nid=28&id=1563&ref=claproducts&pre=1&t=92726061be261a19), pp. 5–9, also saved under `references/vendor/`. Pins 13 (bridge touch IRQ) and 14 (ordinary-SPI D/C) are NC for direct-touch QSPI. Pin 19 receives V3V0, while pin 2 receives V5V. The supplied module must have its QSPI straps set; this controller PCB does not implement the display bridge itself.

The display specifies 4.5–5.5 V main power, 2.8–3.3 V touch power and 3.3 V-class host inputs. The static controller rails fit those values. Q2/R48 implement a 3.0 V open-drain touch reset: MCU high asserts reset low; low releases it. R49's 100 kOhm gate pulldown does not guarantee release during MCU reset: GPIO44/U0RXD has an internal weak pullup at and after reset. With the nominal 45 kOhm internal pullup, the gate divider would be about 2.28 V. Treat the touch-reset state during startup as potentially asserted until GPIO44 is driven low; this is a startup behavior to accommodate, not a further circuit blocker. [ESP32-S3 datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf), table 2-1 and DC characteristics. U14 is a 3.3 V-powered **SN74LVC1G17DBVR** with a 5 V-tolerant Schmitt input on Mini EXP2.8; its dedicated output goes to GPIO21. [TI Schmitt-buffer datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf), pin/electrical tables.

Single-display operation and power-off cable changes are essential because Mini and QSPI share direct signals. No simultaneous operation, hot plugging or separately powered display is qualified. TDO's 180 mA typical pattern figure is not its maximum combined/inrush current; its input-level specification is not a WAIT/IRQ output guarantee (ISR-03).

## Component and PCB-stage qualifications

- Native symbols/footprints use installed KiCad assets; the library audit reports zero custom symbols/footprints. Embedded symbol definitions are normal schematic storage, not a new project library. The TPS5430/TPS5450 numbered-pin reuse is explicit and checked.
- Ordinary resistor, ceramic-capacitor and indicator footprints retain the V2 0805 hand-solder intent. RF/clock 0402, 1206 current shunts, new IC packages and electrolytics are explicit functional exceptions. No blanket shrink to 0402 was made.
- L4 now has the manufacturer-specific stock MWSA0603S footprint. The [Sunlord-authored family specification](https://media.digikey.com/pdf/Data%20Sheets/Shenzhen%20Sunlord/MWSA-S_Series_DS.pdf), pp. 10–12, lists 4.7 uH±20% and 33 mOhm maximum DCR for MWSA0603S-4R7MT. Its current columns should be cited as printed, not relabelled as guaranteed minimums. Physical rating/layout checks remain distinct from the ripple calculation above.
- [Honor RVT source](https://datasheet.lcsc.com/datasheet/pdf/4ec4cfc2b89f173d2532ed891957b1a7.pdf?productCode=C19606), visually checked pp. 1, 3–4: C8 is 330 uF/35 V/±20%, Ø10×10.2 mm nominal. The ripple table gives 247 mA at 105°C/120 Hz and a 1.50 multiplier at ≥10 kHz, or 370.5 mA. The ideal nominal 12 V/15 uH/500 kHz buck output-capacitor ripple is about 0.113 A RMS, so that rating alone does not reveal a nominal incompatibility. It does not supply the missing ESR or transient qualification. Cached PDF SHA-256: `285ae57abc097a56fae89388feef643b79f8d7c2901d6457de4bc00a5f91ce1b`.
- Confirm actual connector land/mating dimensions and switch height, especially J8's retained mating datum, J14's FFC contact geometry and SW1/SW2's selected Kinghelm height versus the stock model. J1/J2 correctly use vertical IDC footprints.
- Board outline, mounting datums, connector positions, ground return continuity, exposed-pad solder/vias, shunt Kelvin routing, regulator loops, RF keepout and USB impedance are PCB-stage requirements. The `.kicad_pro`/net-class starter widths do not establish impedance or current capacity without a stackup and layout.

## Analyzer false positives and evidence limits

The reviewed analyzer snapshot reports 80 findings: 6 errors, 8 warnings and 66 information items, with mixed trust. Its BOM-derived counts are not the count of 166 physical instances.

| Rule / automatic claim | Independent disposition |
| --- | --- |
| PP-001: U3 VDD has no DC power path | False positive. R8 connects VMOTOR to U3.1 and C6 bypasses it, matching WCH's reference. |
| PU-001: AE1 needs a pullup | False positive. Antenna pin 2 is a mechanical anchor and electrically NC. |
| PU-001: IC1 EN needs a pullup | False positive. TPS5450 explicitly permits floating EN for enable. |
| PU-001: U3 PG needs a pullup | False positive for this use. PG is unconsumed and explicitly NC. |
| Four VM-001 rail crossings at PWM/pixel inputs | False positives. The selected AHCT parts are the level-conversion stages; their VIH is compatible. |
| UC-003: J8 lacks external CC pulldowns | False positive. CH224K handles the main sink CC interface; do not add duplicate generic Rd resistors. |
| UC-004: 0.1 uF service VBUS capacitance too small | Not a missing supply reservoir: this rail does not power the board. Its decay is intentionally relevant to disconnect behavior. |
| UC-002: J16 VBUS has no protection | Incomplete detector result: D7 includes its VBUS clamp/reference connection. Layout/system ESD performance remains unmeasured. |
| UC-002: J8 lacks a discrete VBUS TVS | True topology observation; retained baseline/prototype transient qualification, not a demonstrated schematic fault. |
| SS-001 / missing MPN coverage | Valid fabrication-readiness limitation, ISR-06. It does not invalidate the manually checked circuit topology. |
| LC-DET: L3/C29 is a 324.9 MHz LC filter | A passive-network calculation, not a prediction that the 40 MHz crystal oscillates at 324.9 MHz. The crystal and parasitics are not represented by that calculation. |

The separate lifecycle attempt carries no usable positive lifecycle/stock evidence for this final BOM. At inspection its preserved finding was LC-DET, which is not a lifecycle result; snapshot metadata alone is not a per-MPN response record. No active/available status is claimed. Failed downloads recorded by the author were supplemented with direct manufacturer web datasheets for this review; exact commodity part coverage remains incomplete.

No new analyzer files or source caches were written by this reviewer. The author supplied the native ERC/netlist, connectivity report and schematic-analyzer outputs; the independent native reconstruction, source checks and calculations described above were run separately in memory.

## Not performed / boundaries

- No V3 PCB exists: PCB DRC, schematic-to-PCB pad reconciliation, Gerber, EMC/cross-domain and fabrication analyses are not applicable yet.
- No SPICE simulation: ngspice, LTspice and Xyce were not found on PATH. Values were checked algebraically; no analog transient/stability simulation is claimed.
- No thermal model, continuous 1.5 A RMS qualification, production management or procurement. Passive heatsinks and ordinary manufacturer layout practices remain the agreed basis.
- No physical USB, display, regulator, motor, RF, current, servo or firmware tests. Mellow/owner downstream testing must establish those results.
- No firmware-port analysis or application-runtime claim. This review checks hardware pin and peripheral suitability only.
- No automatic delta against the rejected architecture: its scope is not an accepted predecessor. The relevant deltas are the V2.1 substitutions and the two bounded B1 amendments recorded above.

**Owner-review conclusion:** the corrected B1 drawing and native connectivity are coherent and suitable for the owner to review. Keep ISR-02/03/04/06 visible through PCB and preliminary-BOM work, and ISR-05 as explicit external verification. This review does not itself authorize PCB implementation or close the owner's G-02 approval.

## Bounded renewal after drawing polish

Renewed on 2026-09-13 NZST (2026-09-12, approximately 15:09 UTC). Scope: shorten each page's revision field to `B1` and consolidate the motor IC ground drawing. No new electrical architecture or manufacturer research was needed. ISR-01 through ISR-06 and the substantive review above are preserved.

- For the controller, power, interfaces and display sheets, replacing only `(rev "B1")` with the previously reviewed `(rev "B1 - schematic review")` **in memory** reproduced each earlier SHA-256 exactly. This proves their only native-file change was the revision text.
- On `motors.kicad_sch`, directly checked the embedded symbol coordinates and native wires. U10's stacked pins 3/18/29 at `(77.47, 146.05)` connect to the GND symbol at `(77.47, 149.86)`; pin 25 at `(80.01, 146.05)` joins that same ground by the added horizontal/vertical wire. U11 has the equivalent connections at `(284.48, 146.05)`, `(284.48, 149.86)` and `(287.02, 146.05)`. No stacked ground endpoint was removed. Motor component values, MPNs, footprints and symbol identities still match the unchanged intended circuit.
- Independently compared full endpoint sets from the refreshed native XML against the intended contract: **116 connected nets, 551 connected endpoints, zero missing or unexpected connected groups**. All **37 unconnected singleton endpoints** exactly match the explicit NC assignments in the unchanged `net-intent.json`. The XML still places U10/U11 pins 3/18/25/29 on GND. There remain 166 component instances and five sheets.
- Inspected all five refreshed PNGs. Every `Rev: B1` field is readable within its title block, and each driver has one readable external GND label at the consolidated connection. The affected ground graphics no longer overlap.
- Read the refreshed native ERC: **0 errors / 0 warnings**, with the same four ignored check categories. The refreshed analyzer remains at 80 findings, with 6 errors, 8 warnings and 66 information items; the existing dispositions and evidence limits still apply. The project-settings and circuit-intent file hashes are unchanged.
- Read the current native/export/image hashes from disk and replaced the exact snapshot above. This renewal changes only this review report.

**Renewed verdict: suitable for owner schematic review, with no new schematic blocker and the existing bounded qualifications unchanged.** The owner's explicit approval of this exact package remains the next G-02 step; this renewal is not that approval or a PCB release.
