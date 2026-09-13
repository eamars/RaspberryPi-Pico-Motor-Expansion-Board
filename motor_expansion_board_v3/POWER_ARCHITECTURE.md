# V3 power and USB design

This document describes the corrected Motor Expansion Board V3 schematic.
Live work status is in [PROGRESS.md](PROGRESS.md). Requirements are in
[REQUIREMENTS.md](REQUIREMENTS.md); firmware port work is excluded by DEC-022.

The main USB-C power port retains the V2.1 position and CH224K 12 V request.
Its input directly supplies both TMC2209 motor channels and the retained
TPS5450 5 V converter. The added AP63203 supplies 3.3 V, replacing the Pico's
regulator. A small 3.0 V LDO supplies the external touch interface and shared
I2C pullups. Exactly one ESP32-S3R8 is fitted.

The separate USB service connection carries data and VBUS presence only.
**Main PD power is required during programming. SERVICE_VBUS has no connection
to VMOTOR, V5V or V3V3.** An optional DNP receptacle and seven factory contacts
provide USB data, ground, BOOT, RESET and rail measurement access.

| Rail / function | Circuit and reason |
| --- | --- |
| VMOTOR | CH224K requests 12 V using the V2 straps; same direct VBUS motor rail. A charger explicitly offering 12 V remains required. |
| V5V | V2 TPS5450DDAR, 15 uH Sunlord inductor and 330 uF output capacitor; 10k/3.16k feedback gives about 5.085 V nominal. Retain the 5 A converter class rather than reduce capacity using unmeasured servo peaks. |
| V3V3 | AP63203WU-7, 4.7 uH MWSA0603S-4R7MT, 10 uF input and 2 x 22 uF output. The IC's 2 A rating gives controller transient margin; it is not a measured board rating. |
| V3V0 | TLV75530PDBVR from V3V3, always fitted. The touch interface stays below its 3.3 V maximum and shared I2C high levels satisfy the ESP32/EEPROM thresholds. |
| Service data | TS3USB30E common ports face the PC; powered-off isolation prevents data-line injection into the unpowered controller. A BSS138 senses service VBUS and enables the switch. No power-source selector or PC-powered operating mode is required. |

The 4.7 uH selection differs from AP63203 Table 2's 3.9 uH example but lies
within the manufacturer's 2.2-10 uH range in section 10. Equations 7/8 give
about 0.224 A peak-to-peak ripple at 5.085 V input and 1.1 MHz, about 0.30 A
with -20% inductance and -6% frequency. At a 2 A load, peak current is about
2.15 A; the selected Sunlord part has substantial current margin and 33 mOhm
maximum DCR. This is a calculation, not a transient measurement.
[Diodes AP63203 datasheet, pp.13-14](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf),
[Sunlord component listing](https://jlcpcb.com/partdetail/MWSA0603S-4R7MT/C408447).

## Load basis

Confirmed board-powered accessories are two MG90S servos and four external
NeoPixels. Count the selected display separately. The sourcing guide establishes
the servo identity, but provides no trustworthy electrical peak-current limit.
Consequently the retained converter is not being downsized.

For checking the power path, a **planning allocation**, not measured consumption,
is 1.0 A per servo, 0.32 A for four RGBW pixels, 0.50 A for a selected display,
0.62 A equivalent 5 V input for a 0.8 A/3.3 V controller load at 85% efficiency,
and 0.04 A for interfaces/indicators: about 3.48 A total on 5 V. Servo stall
peaks and actual display maximum current can exceed these assumptions. This
allocation therefore does not establish a guaranteed simultaneous-load rating.
The first preliminary BOM and hardware test notes must preserve that limitation.

Motor current is winding RMS current, not PD input current. Use 800 mA RMS as
the default; 1.2-1.5 A RMS is an adjustable upper range with passive heatsinks,
not a promised continuous rating. Actual motor winding parameters, speed and
mechanical load determine PD demand. V2's documented 12 V/2 A minimum supply
must not be presented as proof that every V3 maximum load can run together.
Mellow/owner measure the aggregate demand and rail droop during initial testing.
No separate thermal-design exercise is in scope.

## Operating cases and limits

| Connected sources | Expected circuit behavior |
| --- | --- |
| Main PD only | Board operates from the required 12 V source; service data switch disabled without PC VBUS. |
| PC service only | No board supply path; controller and motors remain unpowered apart from specified device leakage. |
| Both | Main PD supplies the board; PC provides USB data. Service VBUS enables the isolated data path. |
| Main PD removed first | Board powers down; switch Ioff isolates host-facing USB data. |
| PC removed first | Main-powered operation continues; the presence circuit disables the service data path. |
| Charger without a 12 V profile | Unsupported supply, as in the master project. V2 topology has no added rail qualifier. |

The BSS138 circuit detects VBUS presence; it is not a precision USB VBUS
threshold detector. Formal USB compliance testing is not claimed. Host attach,
detach, ROM download and unpowered leakage must be checked on the prototype.
[TI TS3USB30E datasheet](https://www.ti.com/lit/ds/symlink/ts3usb30e.pdf).

The main input still follows V2's power topology. Retained C8 ESR/loop behavior
and exact source package are explicit component-review items, not a reason to
add a new power-management subsystem. Input/servo transients, display current,
USB behavior and higher motor settings remain physical test responsibilities.
