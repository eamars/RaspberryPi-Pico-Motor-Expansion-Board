# Raspberry Pi Pico Motor Expansion Board

The Raspberry Pi Pico Motor Expansion Board is designed to be used as the controller for [OpenTrickler](https://github.com/eamars/OpenTrickler). The board is designed to trickle certain amount of charges (e.g, gun powder) from the reservoir by reading measurements from the attached precision digital balance and actuate corresponding motors. 

![3d_view](resources/3d_view.png)

Join our [discord server](https://discord.gg/ZhdThA2vrW) for help and development information. 

## Peripherals

* RS232 IO port with either straight through or NULL modem type of connection via on board DB9 connectors. Used to communicate with the precision digital balance. 
* 2x Stepper motor driver socket designed for TMC stepstick drivers. TMC2209 with UART is recommended. 
* 2x EXP ports for [RepRap 12864 LED display](https://reprap.org/wiki/RepRapDiscount_Full_Graphic_Smart_Controller)
* A 40 pin socket for Raspberry Pi Pico or Pico W. 

## Power

The expansion board is designed to be powered by 12V or 24V DC supply. 

## PCB

The board is designed to be manufactured with 4 layer PCB. Traces are placed at top and bottom layers. Two mid layers are for power (Vcc, 5V) and GND. 

![top_view](resources/top_view.png)

## Manufacturing

The board is designed with hand soldering in mind. The board can also be manufactured by SMT. 

![assembly](resources/assembly.jpg)

BOM and gerber files are provided under [production](motor_expansion_board/production) directory. [Instructions](motor_expansion_board/production/README.md) are also provided regarding the PCB contract manufactoring with JLCPCB. 

## Enclosure

A 3D printable enclosure is also supplied in [enclosure](motor_expansion_board/enclosure) directory. 

## Revisions

* v0.1: Initial release.
* v0.2: Add 2x 100uF caps for stepper motor driver power supply. 
* v0.3: Fix issues found on v0.2 design. See details at [release](https://github.com/eamars/RaspberryPi-Pico-Motor-Expansion-Board/releases/tag/v0.3) page. 
  Noted the NEOPIXEL output is moved from GP26 to GP13 from this revision. 
* v1.0: Add missing ground PIN for RS232 female connector. First release. 
* v1.0.1: Fix the LCSC part number for on-board DB9 male connector. Note there is no board silkscreen update. 

## Errata

### v1.0 -> v1.0.1

In v1.0 the incorrect LCSC part number for DB9 male connector was recorded. If you've ordered the PCBA from JLCPCB by building the v1.0 release, the DB9 connector is likely incorrect. 

**How to tell?**

If you have DB9 female connector assembled, you will have the incorrect part. 

**How to fix?**

You can de-solder the DB9 female connector and replace with the DB9 male connector. If you would like to order from LCSC, the part number is [C426221](https://www.lcsc.com/product-detail/_FOXCONN-_C426221.html).

The v1.0.1 already includes the fix. 

# PWM Expansion Board

The PWM Expansion Board is designed to extend the output capability for the existing v1.x of the Raspberry Pi Pico Motor Expansion Board. The PWM Expansion Board added additional 3x 5V PWM output that are suitable for servo motors and Neopixel LEDs. 

![assembly](resources/pwm_expansion_board_install.jpg)

## Peripherals

GPIO26, 27 and 28 are now wired to the PWM output terminals. 

## Power

The PWM Expansion Board is powered by the Raspberry Pi Pico Motor Expansion Board with 5V supply. 

## PCB

The board is designed to be manufactured with 2 layer PCB. Traces are placed at top and bottom layers. GND and 5V are poured to the top and bottom layers. 

## Manufacturing

The board is designed with hand soldering in mind. The board can also be manufactured by SMT with limited selection of components. 

![assembly](resources/pwm_expansion_board_assembly.jpg)

BOM and gerber files are provided under [production](pwm_expansion_board/production) directory. [Instructions](motor_expansion_board/production/README.md) are also provided regarding the PCB contract manufactoring with JLCPCB. 

## Sourcing

You may need to source the following components from third party: 

* Right angle JST XH connector [Aliexpress](https://www.aliexpress.com/item/1005005424915227.html)
* **20x1** long pin (11mm) header [Aliexpress](https://www.aliexpress.com/item/1005005965643878.html)

## Revisions

* v1.0: Initial Release
