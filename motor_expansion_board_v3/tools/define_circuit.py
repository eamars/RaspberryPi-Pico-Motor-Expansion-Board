"""Write the intended connectivity BEFORE capture; never writes schematic CAD.

Retained references match V2 where practical. New circuitry is limited to the
three owner-requested substitutions/addition and explicit compatibility fixes.
"""
from collections import Counter
import hashlib, json
from cad_support import PROJECT, pin_table, symbol, footprint_path

parts=[]; rn=16; cn=18
R0805='Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder'
C0805='Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder'
LED0805='Diode_SMD:D_0805_2012Metric_Pad1.15x1.40mm_HandSolder'
JST3='Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical'

def p(ref,sheet,group,lib,value,pins,fp,mpn='',maker='',**props):
    assert ref not in {c['ref'] for c in parts}, ref
    parts.append(dict(ref=ref,sheet=sheet,group=group,symbol=lib,value=value,
                      pins={str(k):v for k,v in pins.items()},footprint=fp,
                      mpn=mpn,manufacturer=maker,properties=props))
    return ref

def r(sheet,group,value,a,b='GND',ref=None,fp=R0805,rating='1%, 0.125W minimum',**props):
    global rn
    if ref is None: rn+=1;ref=f'R{rn}'
    return p(ref,sheet,group,'Device:R',value,{1:a,2:b},fp,Rating=rating,**props)

def c(sheet,group,value,a,b='GND',ref=None,fp=C0805,rating='16V X7R',**props):
    global cn
    if ref is None: cn+=1;ref=f'C{cn}'
    return p(ref,sheet,group,'Device:C',value,{1:a,2:b},fp,Rating=rating,**props)

# All GPIO numbers below are mapped separately to physical chip pins.
# In particular pin 36=GPIO48 and pin 37=GPIO47 (not the opposite).
gpio_pin={0:5,1:6,2:7,3:8,4:9,5:10,6:11,7:12,8:13,9:14,10:15,11:16,
          12:17,13:18,14:19,15:21,16:22,17:23,18:24,19:25,20:26,21:27,
          38:43,39:44,40:45,41:47,42:48,43:49,44:50,45:51,46:52,47:37,48:36}
gpio_net={0:'BOOT_N',1:'DISP_D3_PIXEL',2:'GPIO2',3:'GPIO3_STRAP',4:'PWM1',5:'PWM2',
          6:'PWM3_PIXEL',7:'I2C_SCL',8:'I2C_SDA',9:'DISP_BTN_IRQ',10:'DISP_CS',
          11:'DISP_D0_MOSI',12:'DISP_SCK',13:'DISP_D1_EN1',14:'DISP_D2_EN2',
          15:'SCALE_TX',16:'SCALE_RX',17:'TMC_TX',18:'TMC_RX',19:'USB_DN',20:'USB_DP',
          21:'MINI_BUTTON',38:'M1_STEP',39:'M2_STEP',40:'M1_DIR',41:'M2_DIR',
          42:'M1_EN_N',43:'DISP_RESET',44:'DISP_DC_TPRST',45:'GPIO45_STRAP',
          46:'GPIO46_STRAP_IN',47:'DISP_WAIT',48:'M2_EN_N'}

def core():
    s='root';g='ESP32 core'
    pins={i:None for i in range(1,58)}
    pins.update({1:'RF_FEED',2:'V3V3_RF',3:'V3V3_RF',4:'CHIP_PU',20:'V3V3',
                 29:'VDD_SPI',30:'FLASH_D3',31:'FLASH_D2',32:'FLASH_CS',33:'FLASH_CLK',
                 34:'FLASH_D1',35:'FLASH_D0',46:'V3V3',53:'XTAL_N',54:'XTAL_P',
                 55:'V3V3',56:'V3V3',57:'GND'})
    pins.update({gpio_pin[n]:v for n,v in gpio_net.items()})
    p('U1',s,g,'MCU_Espressif:ESP32-S3','ESP32-S3R8',pins,
      'Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP4x4mm','ESP32-S3R8','Espressif',
      LCSC='C2913194',Datasheet='https://documentation.espressif.com/esp32-s3_datasheet_en.pdf',
      Notes='Exactly one MCU; 8MB internal octal PSRAM. Physical memory pads 28,38-42 stay NC.')
    for pin in [20,46,55,56]:c(s,g,'100n','V3V3',Notes=f'Place at U1 pin {pin}')
    c(s,g,'10u','V3V3',rating='16V X5R; effective >=5uF at 3.3V')
    p('L2',s,g,'Device:L','2nH',{1:'V3V3',2:'V3V3_RF'},'Inductor_SMD:L_0402_1005Metric',
      Notes='OWMC RF-supply reference; >=500mA. 0402 RF exception.')
    c(s,g,'100n','V3V3_RF');c(s,g,'10u','V3V3_RF',rating='16V X5R; effective >=5uF')
    g='Flash and clock'
    p('U9',s,g,'Memory_Flash:W25Q128JVS','W25Q128JVSIQ',
      {1:'FLASH_CS',2:'FLASH_D1',3:'FLASH_D2',4:'GND',5:'FLASH_D0',6:'FLASH_CLK',7:'FLASH_D3',8:'VDD_SPI'},
      'Package_SO:SOIC-8_5.3x5.3mm_P1.27mm','W25Q128JVSIQ','Winbond',Notes='16MB external 3.3V Quad flash')
    r(s,g,'10k','VDD_SPI','FLASH_CS')
    c(s,g,'100n','VDD_SPI',Notes='At U1 VDD_SPI');c(s,g,'1u','VDD_SPI')
    c(s,g,'100n','VDD_SPI',Notes='At flash VCC')
    p('Y1',s,g,'Device:Crystal_GND24','40MHz CL10pF',
      {1:'XTAL_P_LOAD',2:'GND',3:'XTAL_N',4:'GND'},'Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm',
      'Q22FA12800101','Epson',LCSC='C255898',Notes='OWMC candidate; +/-10ppm. Small clock-package exception; source confirmation pending.')
    p('L3',s,g,'Device:L','24nH',{1:'XTAL_P',2:'XTAL_P_LOAD'},'Inductor_SMD:L_0402_1005Metric',
      Rating='5%, RF inductor',Notes='OWMC clock reference; 0402 clock exception')
    for net in ['XTAL_P_LOAD','XTAL_N']:c(s,g,'10p',net,fp='Capacitor_SMD:C_0402_1005Metric',rating='50V C0G',Notes='OWMC initial crystal loading; trim by measurement')
    g='Reset and antenna'
    r(s,g,'10k','V3V3','CHIP_PU');c(s,g,'1u','CHIP_PU')
    r(s,g,'10k','V3V3','BOOT_N');r(s,g,'10k','GPIO45_STRAP');r(s,g,'10k','GPIO46_STRAP_IN')
    for ref,value,net in [('SW1','RESET','CHIP_PU'),('SW2','BOOT','BOOT_N')]:
        p(ref,s,g,'Switch:SW_Push',value,{1:net,2:'GND'},'Button_Switch_SMD:SW_SPST_PTS645Sx43SMTR92',
          'KH-6X6X6H-STM','Kinghelm',LCSC='C2837532',
          Notes='Stock pads match V2 within 0.005mm. Actual switch nominal 6mm high; stock 4.3mm model is not height evidence. SW1 retains reset datum.')
    c(s,g,'DNP','RF_FEED',fp='Capacitor_SMD:C_0402_1005Metric',rating='RF C0G tuning',DNP=True)
    r(s,g,'0R','RF_FEED','ANT_FEED',fp='Resistor_SMD:R_0402_1005Metric',Notes='Single OWMC pi matching network; RF tuning provision')
    c(s,g,'DNP','ANT_FEED',fp='Capacitor_SMD:C_0402_1005Metric',rating='RF C0G tuning',DNP=True)
    p('AE1',s,g,'Device:Antenna_Chip','2450AT18A0100001E',{1:'ANT_FEED',2:None},
      'RF_Antenna:Johanson_2450AT18x100','2450AT18A0100001E','Johanson Technology',
      Datasheet='https://www.johansontechnology.com/docs/3827/Antenna-2450AT18A0100001E-Rev4.0.pdf',
      Notes='Pin 2 is mechanically soldered but electrically NC; preserve vendor RF keepout/tuning')
    g='EEPROM and spare GPIO'
    p('U2',s,g,'Memory_EEPROM:CAT24C256','CAT24C256WI-GT3',
      {1:'GND',2:'GND',3:'GND',4:'GND',5:'I2C_SDA',6:'I2C_SCL',7:'GND',8:'V3V3'},
      'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm','CAT24C256WI-GT3','onsemi',LCSC='C79987',
      Datasheet='https://www.onsemi.com/pdf/datasheet/cat24c256-d.pdf',Notes='V2 address 0x50; fixed address and writable as V2')
    c(s,g,'100n','V3V3')
    for ref,net in [('R5','I2C_SDA'),('R6','I2C_SCL')]:r(s,g,'2.2k','V3V0',net,ref=ref,Notes='Shared EEPROM/touch bus; use open drain, no 3.3V internal pullups')
    p('J15',s,g,'Connector_Generic:Conn_02x03_Odd_Even','SPARE GPIO 3V3',
      {1:'GND',2:'GPIO2',3:'GPIO3_STRAP',4:'GPIO45_STRAP',5:'GPIO46_STRAP_IN',6:'V3V3'},
      'Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical',
      Notes='Control only. GPIO2 ordinary IO with a low power-on glitch. GPIO3/45/46 boot restrictions. GPIO46 allocated to input use on this board, not a claim of a silicon limitation. Do not override boot pulls at reset.')
    for n in range(1,5):p(f'H{n}',s,g,'Mechanical:MountingHole_Pad','M3 GND',{1:'GND'},'MountingHole:MountingHole_3.2mm_M3_Pad_Via',in_bom=False)

def power():
    s='power';g='12V PD input'
    p('J8',s,g,'Connector:USB_C_Receptacle_PowerOnly_6P','12V USB-PD',
      {'A5':'PD_CC1','B5':'PD_CC2','A9':'VMOTOR','B9':'VMOTOR','A12':'GND','B12':'GND','SH':'GND'},
      'Connector_USB:USB_C_Receptacle_GCT_USB4125-xx-x-0190_6P_TopMnt_Horizontal',
      'USB4125-GF-A-0190','GCT',Datasheet='https://gct.co/connector/usb4125',
      Notes='Retain archived mating plane; stock land pattern for actual GCT part. Require 12V PD source.')
    p('U3',s,g,'Interface_USB:CH224K','CH224K / 12V',
      {1:'PD_VDD',2:'GND',3:'PD_VDD',4:'PD_DPDM',5:'PD_DPDM',6:'PD_CC2',7:'PD_CC1',8:'PD_SENSE',9:'GND',10:None,11:'GND'},
      'Package_SO:SSOP-10-1EP_3.9x4.9mm_P1mm_EP2.1x3.3mm','CH224K','WCH',LCSC='C970725',
      Notes='Retain V2 CFG1=0,CFG2=0,CFG3=1 for 12V; PG unused. Pin11 exposed GND.')
    r(s,g,'10k','VMOTOR','PD_SENSE',ref='R7');r(s,g,'1k','VMOTOR','PD_VDD',ref='R8')
    c(s,g,'1u','PD_VDD',ref='C6')
    g='V2 5V converter'
    p('IC1',s,g,'Regulator_Switching:TPS5430DDA','TPS5450DDAR',
      {1:'BUCK5_BOOT',2:None,3:None,4:'BUCK5_FB',5:None,6:'GND',7:'VMOTOR',8:'BUCK5_SW',9:'GND'},
      'Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm','TPS5450DDAR','Texas Instruments',
      LCSC='C114425',Datasheet='https://www.ti.com/lit/ds/symlink/tps5450.pdf',
      SymbolBasis='Stock TPS5430DDA shares the numbered nine-pin function map; actual installed device is TPS5450DDAR.',
      Notes='Retained V2 5A-class converter; floating EN enabled per datasheet. Rating is not measured board capacity.')
    for ref in ['C3','C4']:c(s,g,'4.7u','VMOTOR',ref=ref,rating='50V X7R; retain V2 0805 land pattern, check DC bias')
    c(s,g,'10n','VMOTOR',ref='C5',rating='50V X7R')
    c(s,g,'10n','BUCK5_BOOT','BUCK5_SW',ref='C7',rating='50V X7R')
    p('D4',s,g,'Device:D_Schottky','SS54',{1:'BUCK5_SW',2:'GND'},'Diode_SMD:D_SMA',
      'SS54','MDD',LCSC='C22452',Rating='40V 5A; SMA(DO-214AC)')
    p('L1',s,g,'Device:L','15uH',{1:'BUCK5_SW',2:'V5V'},
      'Inductor_SMD:L_Sunlord_MWSA1004S','MWSA1004S-150MT','Sunlord',LCSC='C151872',
      Datasheet='https://media.digikey.com/pdf/Data%20Sheets/Shenzhen%20Sunlord/MWSA-S_Series_DS.pdf',
      Notes='V2 component identity; use stock manufacturer land pattern instead of old custom pad geometry.')
    p('C8',s,g,'Device:C_Polarized','330uF',{1:'V5V',2:'GND'},'Capacitor_SMD:CP_Elec_10x10.5',
      'RVT1V331M1010','Honor Elec',LCSC='C19606',Rating='330uF 35V; ESR/loop compatibility to be checked',
      Notes='Retained V2 component identity and stock land pattern; detailed source package/ESR check before PCB.')
    c(s,g,'10n','V5V',ref='C9')
    r(s,g,'10k','V5V','BUCK5_FB',ref='R9');r(s,g,'3.16k','BUCK5_FB',ref='R10')
    g='3.3V controller supply'
    p('IC2',s,g,'Regulator_Switching:AP63203WU','AP63203WU-7',
      {1:'V3V3',2:'V5V',3:'V5V',4:'GND',5:'BUCK3_SW',6:'BUCK3_BOOT'},
      'Package_TO_SOT_SMD:TSOT-23-6','AP63203WU-7','Diodes Incorporated',
      Datasheet='https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf',
      Notes='Fixed 3.3V replacement for Pico regulator; use AP63203 component table')
    c(s,g,'10u','V5V',rating='16V X5R; check effective input capacitance')
    c(s,g,'100n','BUCK3_BOOT','BUCK3_SW')
    p('L4',s,g,'Device:L','4.7uH',{1:'BUCK3_SW',2:'V3V3'},'Inductor_SMD:L_Sunlord_MWSA0603S',
      'MWSA0603S-4R7MT','Sunlord',LCSC='C408447',
      Datasheet='https://jlcpcb.com/partdetail/MWSA0603S-4R7MT/C408447',
      Rating='20%,33mOhm max; 9A typical Isat / 6A typical Irms',
      Notes='AP63203 section10 permits2.2-10uH. At5.085V input,2Aload:0.224App nominal,~0.30App with L-20%/f-6%; peak2.15A. Stock manufacturer land pattern.')
    for i in range(2):c(s,g,'22u','V3V3',rating='16V X5R; verify effective capacitance against AP63203 table')
    g='Supply indicators'
    for ref,rr,net,val in [('D1','R2','VMOTOR','4.7k'),('D2','R3','V5V','680R'),('D3','R4','V3V3','300R')]:
        r(s,g,val,net,ref+'_A',ref=rr)
        p(ref,s,g,'Device:LED','GREEN',{1:'GND',2:ref+'_A'},LED0805,Notes='Retained V2 indicator function')

def service():
    s='power';g='Programming and native USB'
    p('J16',s,g,'Connector:USB_C_Receptacle_USB2.0_16P','SERVICE USB (DNP)',
      {'A1':'GND','A4':'SERVICE_VBUS','A5':'SVC_CC1','A6':'SERVICE_DP','A7':'SERVICE_DN','A8':None,'A9':'SERVICE_VBUS','A12':'GND',
       'B1':'GND','B4':'SERVICE_VBUS','B5':'SVC_CC2','B6':'SERVICE_DP','B7':'SERVICE_DN','B8':None,'B9':'SERVICE_VBUS','B12':'GND','SH':'GND'},
      'Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12','TYPE-C-31-M-12','HRO',DNP=True,
      Notes='Optional service receptacle; primary initial loading through pads. Main PD required. SERVICE_VBUS never supplies board rails.')
    for net in ['SVC_CC1','SVC_CC2']:r(s,g,'5.1k',net,Notes='Independent Type-C Rd; socket option')
    p('U12',s,g,'Interface_USB:TS3USB30EDGSR','TS3USB30EDGSR',
      {1:'GND',2:'USB_SW_DP',3:None,4:'SERVICE_DP',5:'GND',6:'SERVICE_DN',7:None,8:'USB_SW_DN',9:'USB_OE_N',10:'V3V3'},
      'Package_SO:TSSOP-10_3x3mm_P0.5mm','TS3USB30EDGSR','Texas Instruments',
      Datasheet='https://www.ti.com/lit/ds/symlink/ts3usb30e.pdf',Notes='Common ports face host; Ioff isolates an unpowered board. Unused D2 branch NC.')
    p('Q1',s,g,'Transistor_FET:BSS138','BSS138LT1G',{1:'USB_PRESENT_GATE',2:'GND',3:'USB_OE_N'},
      'Package_TO_SOT_SMD:SOT-23','BSS138LT1G','onsemi',Datasheet='https://www.onsemi.com/pdf/datasheet/bss138lt1-d.pdf')
    r(s,g,'10k','V3V3','USB_OE_N');r(s,g,'1k','SERVICE_VBUS','USB_PRESENT_GATE')
    r(s,g,'100k','USB_PRESENT_GATE');r(s,g,'3.3k','SERVICE_VBUS')
    c(s,g,'100n','SERVICE_VBUS');c(s,g,'100n','V3V3')
    r(s,g,'22R','USB_DP','USB_SW_DP');r(s,g,'22R','USB_DN','USB_SW_DN')
    p('D7',s,g,'Power_Protection:USBLC6-2SC6','USBLC6-2SC6',
      {1:'SERVICE_DP',2:'GND',3:'SERVICE_DN',4:'SERVICE_DN',5:'SERVICE_VBUS',6:'SERVICE_DP'},
      'Package_TO_SOT_SMD:SOT-23-6','USBLC6-2SC6','STMicroelectronics',Datasheet='https://www.st.com/resource/en/datasheet/usblc6-2.pdf')
    for i,net in enumerate(['SERVICE_VBUS','SERVICE_DP','SERVICE_DN','GND','BOOT_N','CHIP_PU','V3V3'],1):
        p(f'TP{i}',s,g,'Connector:TestPoint',net,{1:net},'TestPoint:TestPoint_Pad_D1.5mm',in_bom=False,
          Notes='Factory 2.54mm grid; BOOT/EN pull to GND. 3.3V is measurement only, not an input.')

def motors():
    s='motors'
    r(s,'Shared driver UART','1k','TMC_TX','TMC_RX',ref='R1')
    for n in [1,2]:
        g=f'Motor {n}';N=lambda x:f'M{n}_{x}'
        p('U'+str(9+n),s,g,'Driver_Motor:TMC2209-LA','TMC2209-LA-T',
          {1:N('B2'),2:N('EN_N'),3:'GND',4:N('CPO'),5:N('CPI'),6:N('VCP'),7:'GND',8:N('5VOUT'),
           9:'GND' if n==1 else 'V3V3',10:'GND',11:None,12:None,13:'GND',14:'TMC_RX',15:'V3V3',
           16:N('STEP'),17:N('VREF'),18:'GND',19:N('DIR'),20:'GND',21:N('A2'),22:'VMOTOR',23:N('SENSE_A'),
           24:N('A1'),25:'GND',26:N('B1'),27:N('SENSE_B'),28:'VMOTOR',29:'GND'},
          'Package_DFN_QFN:VQFN-28-1EP_5x5mm_P0.5mm_EP3.7x3.7mm','TMC2209-LA-T','Analog Devices / Trinamic',
          Datasheet='https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf',
          Source='Mellow TMC2209 inventory; exact supplied suffix confirmation pending',
          Notes=f'Address {n-1}; external 0.11ohm sensing, software current RMS. CLK grounded; passive heatsink/Fly reference.')
        r(s,g,'10k','V3V3',N('EN_N'))
        for suffix in ['STEP','DIR']:r(s,g,'10k',N(suffix))
        for suffix in ['SENSE_A','SENSE_B']:r(s,g,'0.11R',N(suffix),fp='Resistor_SMD:R_1206_3216Metric',rating='1W, 1%, low-inductance current sense',
             Notes='1W,1%, low-inductance current sense; four-terminal routing at pads')
        r(s,g,'20k',N('5VOUT'),N('VREF'));r(s,g,'20k',N('VREF'))
        c(s,g,'22n',N('CPO'),N('CPI'),rating='50V X7R')
        c(s,g,'100n',N('VCP'),'VMOTOR',rating='50V X7R')
        c(s,g,'2.2u',N('5VOUT'));c(s,g,'100n','V3V3')
        for i in [22,28]:c(s,g,'100n','VMOTOR',rating='50V X7R',Notes=f'At VS pin {i}')
        c(s,g,'100n',N('VREF'))
        p('C'+str(n),s,g,'Device:C_Polarized','100uF 35V',{1:'VMOTOR',2:'GND'},
          'Capacitor_SMD:CP_Elec_6.3x7.7','EEHZK1V101XP','Panasonic',LCSC='C454360',
          Datasheet='https://util01.industrial.panasonic.com/ea/utilities/ds/chr-vw/EEHZK1V101XP',
          Rating='100uF 35V, 35mOhm ESR, 1.7A ripple at 100kHz',
          Notes='Same V2 6.3x7.7mm envelope; hybrid capacitor selected for driver ripple current')
        p('J'+str(5+n),s,g,'Connector_Generic:Conn_01x04',f'MOTOR {n}',
          {1:N('B2'),2:N('B1'),3:N('A1'),4:N('A2')},'Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical',
          'B4B-XH-A(LF)(SN)','JST',Notes='Retain V2 mating position and phase order')

def interfaces():
    s='interfaces';g='Scale serial interface'
    p('U4',s,g,'Interface_UART:MAX3232','MAX3232ESE+',
      {1:'RS_C1P',2:'RS_VP',3:'RS_C1N',4:'RS_C2P',5:'RS_C2N',6:'RS_VN',7:None,8:'GND',9:None,10:'GND',
       11:'SCALE_TX',12:'RS_LOGIC_RX',13:'RS_RX',14:'RS_TX',15:'GND',16:'V3V3'},
      'Package_SO:SOIC-16_3.9x9.9mm_P1.27mm','MAX3232ESE+','Analog Devices / Maxim',Notes='Retained V2 function; tie unused receiver/driver inputs low')
    for ref,a,b in [('C10','RS_C1P','RS_C1N'),('C11','V3V3','GND'),('C12','RS_C2P','RS_C2N'),('C13','RS_VP','GND'),('C14','RS_VN','GND')]:c(s,g,'100n',a,b,ref=ref,rating='25V X7R')
    p('J3',s,g,'Connector_Generic:Conn_01x03','SCALE TTL 3V3',{1:'TTL_RX',2:'SCALE_TX',3:'GND'},JST3,'B3B-XH-A(LF)(SN)','JST')
    p('J17',s,g,'Connector_Generic:Conn_01x03','RX SELECT',{1:'TTL_RX',2:'SCALE_RX',3:'RS_LOGIC_RX'},
      'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',Notes='One shunt: 2-3 RS232 default, 1-2 TTL. Removes competing receiver outputs while preserving both V2 alternatives.')
    p('J9',s,g,'Connector_Generic:Conn_02x02_Odd_Even','DB9 ROUTING',{1:'DB9_2',2:'RS_TX',3:'RS_RX',4:'DB9_3'},
      'Connector_PinHeader_2.00mm:PinHeader_2x02_P2.00mm_Vertical',Notes='Retain V2 2mm pitch and routing orientations')
    p('J10',s,g,'Connector:DE9_Pins_MountingHoles','DB9 MALE',
      {1:None,2:'DB9_2',3:'DB9_3',4:None,5:'GND',6:None,7:None,8:None,9:None,'SH':'GND'},
      'Connector_Dsub:DSUB-9_Pins_Horizontal_P2.77x2.84mm_EdgePinOffset7.70mm_Housed_MountingHolesOffset9.12mm',
      LCSC='C426221',Notes='Retain mating plane/fixing drills; stock SH replaces old 0 shell designation. Exact source match pending.')
    for ref,rr,net,color in [('D5','R11','SCALE_TX','RED'),('D6','R12','SCALE_RX','BLUE')]:
        r(s,g,'1k','V3V3',ref+'_A',ref=rr);p(ref,s,g,'Device:LED',color,{1:net,2:ref+'_A'},LED0805)
    g='5V accessory outputs'
    # V2 J11 is firmware PWM2; J12 is PWM1. Preserve external port semantics.
    for u,j,cc,rr,net in [('U5','J11','C15','R13','PWM2'),('U6','J12','C16','R14','PWM1'),('U7','J13','C17','R15','PWM3_PIXEL')]:
        p(u,s,g,'74xGxx:74AHCT1G125','SN74AHCT1G125DBVR',{1:'GND',2:net,3:'GND',4:j+'_OUT',5:'V5V'},
          'Package_TO_SOT_SMD:SOT-23-5','SN74AHCT1G125DBVR','Texas Instruments',
          Datasheet='https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf',Notes='Pin-compatible V2 buffer function; AHCT guarantees 3.3V high at 5V supply')
        c(s,g,'100n','V5V',ref=cc);r(s,g,'4.7k',net,ref=rr)
        p(j,s,g,'Connector_Generic:Conn_01x03',j+' 5V OUT',{1:'GND',2:'V5V',3:j+'_OUT'},JST3,'B3B-XH-A(LF)(SN)','JST')

def display():
    s='display_connector';g='Retained Mini12864 headers'
    fp='Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical'
    p('J1',s,g,'Connector_Generic:Conn_02x05_Odd_Even','EXP1 Mini12864',
      {1:None,2:'DISP_BTN_IRQ',3:'DISP_CS',4:'DISP_DC_TPRST',5:'DISP_RESET',6:'MINI_PIXEL_5V',7:None,8:None,9:'GND',10:'V5V'},fp,
      Notes='Retain V2 position, key and pinout. Only one display assembly attached; no hot-plug.')
    p('J2',s,g,'Connector_Generic:Conn_02x05_Odd_Even','EXP2 Mini12864',
      {1:None,2:'DISP_SCK',3:'DISP_D1_EN1',4:None,5:'DISP_D2_EN2',6:'DISP_D0_MOSI',7:None,8:'MINI_BUTTON_RAW',9:'GND',10:'V5V'},fp,
      Notes='Pin10 remains V2 +5V. Supplied Mini must not fit a reset/KILL link shorting pin10 to GND.')
    p('U8',s,g,'74xGxx:74AHCT1G125','SN74AHCT1G125DBVR',{1:'GND',2:'DISP_D3_PIXEL',3:'GND',4:'MINI_PIXEL_5V',5:'V5V'},
      'Package_TO_SOT_SMD:SOT-23-5','SN74AHCT1G125DBVR','Texas Instruments',Datasheet='https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf')
    c(s,g,'100n','V5V',ref='C18');r(s,g,'4.7k','DISP_D3_PIXEL',ref='R16',Notes='Shared with host-driven QSPI D3, never an external IRQ')
    p('U14',s,g,'74xGxx:74LVC1G17','SN74LVC1G17DBVR',{1:None,2:'MINI_BUTTON_RAW',3:'GND',4:'MINI_BUTTON',5:'V3V3'},
      'Package_TO_SOT_SMD:SOT-23-5','SN74LVC1G17DBVR','Texas Instruments',
      Datasheet='https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf',
      Notes='One 5V-tolerant Schmitt input for the documented Mini reset-button risk. Dedicated GPIO21; cannot contend with QSPI WAIT.')
    c(s,g,'100n','V3V3');r(s,g,'100k','V3V3','MINI_BUTTON_RAW')
    g='External QSPI display connector'
    p('J14',s,g,'Connector_Generic_MountingPin:Conn_01x20_MountingPin','EXTERNAL QSPI / TDO B1617A',
      {1:'GND',2:'V5V',3:'GND',4:'DISP_CS',5:'GND',6:'DISP_D1_EN1',7:'DISP_D0_MOSI',8:'DISP_SCK',
       9:'DISP_D3_PIXEL',10:'DISP_D2_EN2',11:'DISP_RESET',12:'DISP_WAIT',13:None,14:None,15:'DISP_BTN_IRQ',
       16:'I2C_SDA',17:'I2C_SCL',18:'TP_RESET_N',19:'V3V0',20:'GND','MP':'GND'},
      'Connector_FFC-FPC:Hirose_FH12-20S-0.5SH_1x20-1MP_P0.50mm_Horizontal',
      'FH12-20S-0.5SH(55)','Hirose',Datasheet='https://www.hirose.com/en/product/p/CL0586-0524-9-55',
      Notes='Board connector only. 20-contact pin table follows TDO spec pp5-9. FFC contact side/thickness/pin1 map and maximum load require supplier confirmation. Direct touch; bridge IRQ and D/C NC.')
    c(s,g,'10u','V5V',rating='16V X5R',Notes='At external display connector')
    r(s,g,'47k','V3V3','DISP_CS',Notes='Deselect display during reset')
    r(s,g,'47k','V3V3','DISP_WAIT',DNP=True,Notes='Populate only if WAIT output requires a pullup')
    g='Touch supply and reset'
    p('U13',s,g,'Regulator_Linear:TLV75530PDBV','TLV75530PDBVR',
      {1:'V3V3',2:'GND',3:'V3V3',4:None,5:'V3V0'},'Package_TO_SOT_SMD:SOT-23-5',
      'TLV75530PDBVR','Texas Instruments',Datasheet='https://www.ti.com/lit/ds/symlink/tlv755p.pdf',
      Notes='Always fitted: touch supply and shared I2C pullups even in Mini mode. Touch operating range 2.8-3.3V.')
    c(s,g,'2.2u','V3V3');c(s,g,'2.2u','V3V0')
    p('Q2',s,g,'Transistor_FET:BSS138','BSS138LT1G',{1:'DISP_DC_TPRST',2:'GND',3:'TP_RESET_N'},
      'Package_TO_SOT_SMD:SOT-23','BSS138LT1G','onsemi',
      Datasheet='https://www.onsemi.com/pdf/datasheet/bss138lt1-d.pdf',
      Notes='Open-drain 3.0V reset interface; MCU high asserts low. Same device as Q1; Rds(on) specified at2.75V. Avoid 3.3V push-pull injection through shared Mini DC pin.')
    r(s,g,'10k','V3V0','TP_RESET_N');r(s,g,'100k','DISP_DC_TPRST')

if __name__=='__main__':
    core();power();service();motors();interfaces();display()
    problems=[]
    for item in parts:
        expected=set(pin_table(symbol(item['symbol'])))
        if expected!=set(item['pins']):problems.append([item['ref'],'pin mismatch',sorted(expected-set(item['pins'])),sorted(set(item['pins'])-expected)])
        if not footprint_path(item['footprint']).exists():problems.append([item['ref'],'footprint unavailable',item['footprint']])
    output=PROJECT/'design';output.mkdir(exist_ok=True)
    doc={'revision':'B1-V2-reset','purpose':'Intended physical connectivity before schematic capture',
         'gpio_physical_pins':gpio_pin,'gpio_signals':gpio_net,'components':parts,'resource_checks':problems}
    raw=json.dumps(doc,indent=2,ensure_ascii=False)+'\n';(output/'net-intent.json').write_text(raw,encoding='utf-8')
    print(json.dumps({'components':len(parts),'by_sheet':dict(Counter(x['sheet'] for x in parts)),
                      'intent_sha256':hashlib.sha256(raw.encode()).hexdigest(),'resource_checks':problems},indent=2))
