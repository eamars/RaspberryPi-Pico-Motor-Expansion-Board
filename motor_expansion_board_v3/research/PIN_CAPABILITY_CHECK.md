# ESP32 pin-capability check

Independent read-only check by the firmware_feasibility agent, 2026-09-13.
The owner limited this check to pin suitability (DEC-022). Application-port,
SDK, task timing, UI, OTA and storage-migration work are excluded.

The physical pin map and R8 memory reservations were checked against
[Espressif's ESP32-S3 datasheet, pin and boot tables](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf).
The allocation supports independent motor STEP/DIR/EN, shared addressed UART,
scale UART, three control outputs, native USB, EEPROM I2C and either display.
Package pin 36 is GPIO48; pin 37 is GPIO47. Earlier research that accepted the
reverse is superseded. GPIO42/48 replace GPIO1/2 for motor enables because the
latter have documented low pulses at power-up. The pulsed pins serve pixel/D3
and spare-control roles instead.

GPIO46 is listed as I/O/T in the current manufacturer table; input use is a
board allocation restriction here, not a claim that the silicon cannot output.
GPIO3/45/46 remain boot-strapping pins and external circuits must respect reset
levels. Header GPIO2 can pulse low at boot. Only one display assembly attaches.

The 3.0 V shared open-drain I2C pullups meet the ESP32 and 3.3 V EEPROM input-high
thresholds; do not enable conflicting internal 3.3 V pullups. The touch supply is
3.0 V, with an open-drain reset transistor. Source:
[CAT24C256 electrical characteristics](https://www.onsemi.com/pdf/datasheet/cat24c256-d.pdf).

The electrical review also checked the UART0 reset states. GPIO43 can carry ROM
UART output on the display-reset connection. GPIO44's reset-time weak pullup can
assert the touch-reset transistor despite its 100 kOhm external pulldown. Touch
reset is released by driving GPIO44 low; an automatically released reset at
power-up is not claimed. These pins remain suitable for their allocated purpose.

| GPIO | Physical package pin | Board signal |
| --- | --- | --- |
| 0 | 5 | BOOT_N |
| 1 | 6 | DISP_D3_PIXEL |
| 2 | 7 | GPIO2 |
| 3 | 8 | GPIO3_STRAP |
| 4 | 9 | PWM1 |
| 5 | 10 | PWM2 |
| 6 | 11 | PWM3_PIXEL |
| 7 | 12 | I2C_SCL |
| 8 | 13 | I2C_SDA |
| 9 | 14 | DISP_BTN_IRQ |
| 10 | 15 | DISP_CS |
| 11 | 16 | DISP_D0_MOSI |
| 12 | 17 | DISP_SCK |
| 13 | 18 | DISP_D1_EN1 |
| 14 | 19 | DISP_D2_EN2 |
| 15 | 21 | SCALE_TX |
| 16 | 22 | SCALE_RX |
| 17 | 23 | TMC_TX |
| 18 | 24 | TMC_RX |
| 19 | 25 | USB_DN |
| 20 | 26 | USB_DP |
| 21 | 27 | MINI_BUTTON |
| 38 | 43 | M1_STEP |
| 39 | 44 | M2_STEP |
| 40 | 45 | M1_DIR |
| 41 | 47 | M2_DIR |
| 42 | 48 | M1_EN_N |
| 43 | 49 | DISP_RESET |
| 44 | 50 | DISP_DC_TPRST |
| 45 | 51 | GPIO45_STRAP |
| 46 | 52 | GPIO46_STRAP_IN |
| 47 | 37 | DISP_WAIT |
| 48 | 36 | M2_EN_N |

Physical pads 28 and 38-42 are reserved/NC for the R8 configuration. Flash uses
the dedicated memory interface and VDD_SPI; USB uses GPIO19/20. These checks
establish pin capability, not a running firmware implementation. Native-export
reconciliation of the captured schematic is recorded under review/.
