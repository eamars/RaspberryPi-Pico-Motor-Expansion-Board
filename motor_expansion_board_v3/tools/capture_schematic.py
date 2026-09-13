"""Capture five coherent sheets from the reviewed pre-capture connection contract.

Generated sheets are normal editable KiCad files. Later regeneration refuses to
overwrite a manually edited sheet; preserve CAD edits before changing the script.
"""
from collections import defaultdict
import hashlib,json
from cad_support import PROJECT
from schematic_drawing import Page,NAME

def root(p,ports):
    p.heading('ESP32-S3R8 / one controller',12,12,130)
    p.text('V2 Pico replacement. 8 MB internal PSRAM; 16 MB external flash.',12,18)
    p.bank(['C19','C20','C21','C22','C23'],23,34,12)
    p.text('100 nF at each supply pin; keep local return paths short.',15,43,.85)
    p.place('U1',69,79,fields=(80,45))
    p.place('L2',113,28,90)
    p.bank(['C24','C25'],113,38,13)
    p.connect(('L2','2'),('C24','1'))
    p.text('R8: pads 28, 38-42 are reserved.\nPin 36 = GPIO48; pin 37 = GPIO47.\nGPIO42/48: motor EN, pulled inactive.\nGPIO1/2 have a short low boot glitch.',15,115,.88)

    p.heading('Flash / 40 MHz clock',150,12,82)
    p.place('U9',195,49,fields=(205,28))
    p.place('R17',162,32)
    p.to('R17','2',(162,43));p.connect(('R17','2'),('U9','1'))
    p.bank(['C26','C27','C28'],161,77,15)
    p.text('VDD_SPI supplies the 3.3 V Quad flash.\nNo external loads on the R8 memory pads.',150,87,.88)
    p.place('Y1',188,106,fields=(177,97))
    p.place('L3',164,106,90)
    p.place('C29',175,118);p.place('C30',206,118)
    p.connect(('L3','2'),('Y1','1'))
    p.connect(('Y1','1'),('C29','1'),via=[(175,106)])
    p.connect(('Y1','3'),('C30','1'),via=[(206,106)])
    p.dot((175,106));p.dot((206,106))
    p.text('OWMC clock reference; 0402 RF/clock exceptions.\nCrystal loading and antenna match checked on hardware.',150,130,.85)

    p.heading('EEPROM / remaining control I/O',245,12,73)
    p.place('U2',275,42,fields=(272,25))
    p.place('C34',298,42);p.place('R5',292,64);p.place('R6',309,64)
    p.place('J15',276,88,fields=(267,77))
    p.text('J15 is 2.54 mm; control signals only.\nGPIO2: ordinary GPIO, low boot glitch.\nGPIO3 / 45 / 46: boot straps; do not override\nthe reset levels. GPIO46 reserved for inputs here.\nI2C pullups use 3.0 V (child display sheet).',245,102,.86)
    for i in range(4):p.place('H'+str(i+1),259+17*i,127,fields=(255+17*i,120))

    p.heading('Antenna / reset / boot',12,130,130)
    p.place('C32',25,151);p.place('R22',38,143,90);p.place('C33',51,151)
    p.place('AE1',65,143,fields=(58,151))
    p.connect(('C32','1'),('R22','1'),via=[(25,143)])
    p.connect(('R22','2'),('C33','1'),via=[(51,143)])
    p.connect(('R22','2'),('AE1','1'))
    p.place('R18',84,145);p.place('C31',84,161);p.place('SW1',100,155,fields=(96,147))
    p.connect(('R18','2'),('C31','1'))
    p.connect(('R18','2'),('SW1','1'),via=[(84,155)])
    p.dot((84,155));p.label('CHIP_PU',(84,155),'L')
    p.place('R19',119,145);p.place('SW2',131,155,fields=(126,147))
    p.connect(('R19','2'),('SW2','1'),via=[(119,155)])
    p.label('BOOT_N',(119,155),'L')
    p.place('R20',159,154);p.place('R21',190,154)

    for name,n,title,x,y,w in [('power',2,'Power / USB service',42,180,45),('motors',3,'Two motor drivers',123,180,46),('interfaces',4,'Serial / 5 V outputs',213,168,44),('display_connector',5,'External displays',286,142,34)]:
        p.sheet(name,n,title,ports[name],x,y,w)
    p.power_symbol('V3V3_RF',118,52,True)
    p.power_symbol('VDD_SPI',224,85,True)

def power(p):
    p.heading('12 V USB-PD / retained V2 topology',12,12,126)
    p.place('J8',27,44,fields=(17,23))
    p.place('U3',87,47,fields=(86,28))
    p.place('R7',75,26);p.place('R8',108,26);p.place('C6',112,48)
    p.connect(('J8','A5'),('U3','7'),via=[(50,48),(50,43)])
    p.connect(('J8','B5'),('U3','6'),via=[(54,50),(54,45)])
    p.connect(('R7','2'),('U3','8'))
    p.connect(('R8','2'),('U3','1'),via=[(108,34),(89,34)])
    p.connect(('U3','1'),('C6','1'),via=[(89,34),(112,34)])
    p.dot((89,34));p.dot((108,34))
    p.connect(('U3','4'),('U3','5'),via=[(75,51),(75,49)])
    p.text('CFG1=0, CFG2=0, CFG3=1 -> 12 V request.\nUse the required 12 V PD PSU. VBUS directly feeds VM.\nThe PD receptacle has no USB data connection.',12,72,.9)

    p.heading('5 V accessories / V2 TPS5450 retained',148,12,170)
    p.bank(['C3','C4','C5'],157,38,12)
    p.place('IC1',221,46,fields=(208,27))
    p.place('C7',247,33)
    p.place('L1',268,46,90)
    p.place('D4',246,63,270)
    p.bank(['C8','C9'],286,57,15)
    p.place('R9',275,67);p.place('R10',275,82)
    p.connect(('IC1','1'),('C7','1'),via=[(238,42),(238,30)])
    p.connect(('IC1','8'),('L1','1'))
    p.connect(('C7','2'),('IC1','8'),via=[(247,46)])
    p.connect(('D4','1'),('IC1','8'),via=[(246,46)])
    p.dot((246,46));p.dot((247,46))
    p.connect(('L1','2'),('C8','1'),via=[(286,46)])
    p.connect(('R9','1'),('L1','2'),via=[(275,46)])
    p.connect(('R9','2'),('R10','1'))
    p.to('IC1','4',(259,75));p.connect(('R9','2'),('IC1','4'),via=[(275,75),(259,75)])
    p.dot((275,75));p.dot((275,46));p.label('V5V',(286,46))
    p.text('Actual IC: TPS5450DDAR; stock TPS5430 symbol uses the same pin map.\nEN left open per TI. 5.085 V nominal from V2 divider.\nKeep the V2 5 A class; actual board capacity needs load testing.',149,92,.9)

    p.heading('3.3 V controller supply / replaces Pico regulator',12,90,125)
    p.place('C35',24,119)
    p.place('IC2',57,120,fields=(46,104))
    p.place('C36',85,127)
    p.place('L4',99,118,90)
    p.bank(['C37','C38'],110,134,13)
    p.connect(('C35','1'),('IC2','3'))
    p.connect(('IC2','2'),('IC2','3'),via=[(44,122),(44,118)])
    p.connect(('IC2','5'),('L4','1'))
    p.connect(('IC2','6'),('C36','1'),via=[(81,120),(81,124)])
    p.connect(('C36','2'),('L4','1'),via=[(90,130),(90,118)])
    p.connect(('L4','2'),('C37','1'),via=[(110,118)])
    p.connect(('IC2','1'),('L4','2'),via=[(75,122),(75,146),(130,146),(130,118)])
    p.dot((90,118));p.dot((110,118))

    p.heading('Native USB service / main PD must be on',148,107,170)
    p.place('J16',167,140,fields=(149,116))
    p.place('D7',208,139,fields=(198,118))
    p.place('U12',265,142,fields=(258,123))
    p.place('R29',294,132,270);p.place('R30',294,143,270)
    p.connect(('R29','2'),('U12','2'),via=[(284,132),(284,138)])
    p.connect(('R30','2'),('U12','8'),via=[(280,143),(280,140)])
    p.place('R23',158,177);p.place('R24',179,177)
    p.place('R28',211,177);p.place('C39',227,177)
    p.connect(('R28','1'),('C39','1'));p.connect(('R28','2'),('C39','2'))
    p.place('R26',260,177,90);p.place('R27',275,187)
    p.place('Q1',287,177,fields=(293,172));p.place('R25',289,160)
    p.connect(('R26','2'),('Q1','1'))
    p.connect(('R27','1'),('Q1','1'),via=[(275,177)])
    p.connect(('R25','2'),('Q1','3'))
    p.dot((275,177));p.label('USB_OE_N',(289,169))
    p.place('C40',309,160)
    p.text('SERVICE_VBUS is a presence input only.\nIt never joins the board supply rails.\nSwitch Ioff isolates an unpowered ESP32.\nJ16 optional; factory pads support ROM recovery.',148,205,.9)

    p.heading('Indicators / factory contact pads',12,155,126)
    for i in range(3):
        x=24+i*27;p.place('R'+str(i+2),x,171);p.place('D'+str(i+1),x,186,90)
        p.connect(('R'+str(i+2),'2'),('D'+str(i+1),'2'))
    for i in range(7):p.place('TP'+str(i+1),18+i*18,209,fields=(16+i*18,202),value='')
    p.text('TP7 = voltage measurement only. Do not inject 3.3 V.',12,219,.85)
    for i,net in enumerate(['VMOTOR','PD_VDD','V5V','V3V3','SERVICE_VBUS','GND']):p.power_symbol(net,150+i*29,102,True)

def motors(p):
    for n,dx in [(1,0),(2,163)]:
        u='U'+str(n+9);r0=31+(n-1)*7;c0=41+(n-1)*7
        R=lambda i:'R'+str(r0+i);C=lambda i:'C'+str(c0+i)
        p.heading(f'Motor {n} / UART address {n-1}',12+dx,12,141)
        p.text('800 mA RMS default; software adjustment to 1.2-1.5 A RMS.\nUpper setting is not a continuous-current rating.',12+dx,19,.88)
        p.bank([C(4),C(5),'C'+str(n)],54+dx,43,18)
        p.place(C(3),28+dx,43)
        p.place(u,61+dx,95,fields=(53+dx,60))
        gx,gy=p.pin(u,'3');nx,ny=p.pin(u,'25')
        p.connect((u,'3'),(u,'25'),via=[(gx,gy+3),(nx,gy+3)])
        p.power_symbol('GND',gx,gy+3)
        p.place(C(1),84+dx,62,90)
        p.place(C(0),88+dx,87)
        p.connect((u,'4'),(C(0),'1'),via=[(85+dx,87),(85+dx,84)])
        p.connect((u,'5'),(C(0),'2'),via=[(83+dx,91),(83+dx,90)])
        p.connect((u,'6'),(C(1),'1'),via=[(65+dx,62)])
        p.place(C(2),131+dx,58)
        p.place(R(5),113+dx,64);p.place(R(6),113+dx,82);p.place(C(6),131+dx,82)
        p.connect((u,'8'),(R(5),'1'),via=[(99+dx,79),(99+dx,55),(113+dx,55)])
        p.connect((R(5),'1'),(C(2),'1'),via=[(113+dx,55)])
        p.connect((R(5),'2'),(R(6),'1'))
        p.connect((u,'17'),(R(6),'1'),via=[(102+dx,83),(102+dx,74),(113+dx,74)])
        p.connect((R(6),'1'),(C(6),'1'),via=[(113+dx,74),(131+dx,74)])
        p.dot((113+dx,55));p.dot((113+dx,74))
        p.place(R(0),26+dx,91);p.connect((R(0),'2'),(u,'2'),via=[(26+dx,101)])
        p.place(R(1),24+dx,120);p.place(R(2),42+dx,133)
        p.place(R(3),94+dx,122);p.place(R(4),112+dx,135)
        p.connect((u,'23'),(R(3),'1'),via=[(94+dx,107)])
        p.connect((u,'27'),(R(4),'1'),via=[(83+dx,109),(83+dx,129),(112+dx,129)])
        p.place('J'+str(n+5),143+dx,110,fields=(124+dx,98))
        p.text('Motor cable: 1=B2, 2=B1, 3=A1, 4=A2 (V2).\n0.11 ohm sense resistors: 1 W / 1%; Kelvin routing.\nCLK grounded; internal oscillator. SPREAD=0.\nPassive heatsink; exposed pad and ground copper\nfollow the Fly / TMC reference implementation.',12+dx,151,.92)
    p.heading('Shared addressed UART',12,187,141)
    p.place('R1',69,204,90)
    p.text('TX through 1k to shared RX / PDN_UART.\nInitialize UART current and chopper settings before enabling.',12,214,.9)

def interfaces(p):
    p.heading('Retained scale connection / TTL or RS232',12,12,177)
    p.place('U4',98,65,fields=(87,28))
    p.place('C10',65,50);p.place('C12',127,50)
    p.connect(('U4','1'),('C10','1'));p.connect(('U4','3'),('C10','2'))
    p.connect(('U4','4'),('C12','1'));p.connect(('U4','5'),('C12','2'))
    p.place('C11',49,40);p.place('C13',145,66);p.place('C14',162,80)
    p.connect(('U4','2'),('C13','1'));p.connect(('U4','6'),('C14','1'),via=[(134,63),(134,77)])
    p.place('J3',28,70,fields=(14,57));p.place('J17',45,103,fields=(33,89))
    p.place('J9',151,113,fields=(139,102));p.place('J10',182,75,fields=(171,55))
    p.text('J17: 2-3 = RS232 (default); 1-2 = TTL.\nUse one shunt. Keeps the alternative V2 interfaces\nwithout joining two receiver outputs.\nJ9 retains V2 2 mm DB9 routing selection.',12,126,.92)
    for i in range(2):
        p.place('R'+str(11+i),77+i*28,117);p.place('D'+str(5+i),77+i*28,132,90)
        p.connect(('R'+str(11+i),'2'),('D'+str(5+i),'2'))

    for i,(u,j,c,r,title) in enumerate([('U5','J11','C15','R13','PWM2 / servo'),('U6','J12','C16','R14','PWM1 / servo'),('U7','J13','C17','R15','PWM3 / external pixels')]):
        y=41+i*57
        p.heading(j+' - '+title,218,y-23,99)
        p.place(u,264,y,fields=(273,y-12),value='74AHCT1G125')
        p.place(j,313,y,fields=(303,y-10));p.place(c,233,y-4);p.place(r,240,y+15)
        p.connect((u,'4'),(j,'3'),via=[(294,y),(294,y+4)])
        p.connect((u,'2'),(r,'1'),via=[(240,y)])
        p.dot((240,y))
    p.text('Connector order retained: 1 GND / 2 +5V / 3 SIGNAL.\nAHCT threshold guarantees a 3.3 V high with a 5 V supply.\nBoard load envelope: two MG90S servos + four external LEDs.',217,190,.92)

def display(p):
    p.heading('V2 Mini12864 headers / unchanged pinout',12,12,145)
    p.place('J1',41,43,fields=(24,29));p.place('J2',119,43,fields=(101,29))
    p.place('U8',69,82,fields=(74,67),value='74AHCT1G125')
    p.place('C18',25,76);p.place('R16',44,100)
    p.connect(('R16','1'),('U8','2'),via=[(44,82)])
    p.dot((44,82))
    p.place('U14',115,119,fields=(120,105),value='74LVC1G17')
    p.place('C55',150,116);p.place('R45',86,108)
    p.connect(('R45','2'),('U14','2'),via=[(86,119)])
    p.text('Use one display assembly at a time; power off before changing.\nMini encoder / click inputs use 3.3 V pullups in the MCU.\nEXP2.8 gets a 5 V tolerant input buffer for the Mini button.\nEXP2.10 stays +5 V: the supplied Mini must have no fitted\nKILL link that shorts this contact when its button is pressed.',12,145,.9)

    p.heading('External QSPI assembly / board connector only',179,12,139)
    p.place('J14',243,56,fields=(221,28),value='TDO B1617A / 20p FFC')
    p.place('C56',293,43);p.place('R46',283,69);p.place('R47',309,69)
    p.text('TDO TS040WVS02CP-B1617A: 3.95 inch, 480 x 480.\nQSPI factory straps required on the supplied display.\nD0..D3 / CLK / CS, RESET, WAIT and direct touch I2C.\nBridge IRQ and D/C unused for this connection.\nFFC: confirm contact side, thickness and pin 1 mapping\nwith the supplied assembly before PCB placement.',180,100,.9)

    p.heading('3.0 V touch power / shared I2C pullups',179,137,139)
    p.place('U13',229,165,fields=(220,150))
    p.place('C57',193,165);p.place('C58',265,165)
    p.connect(('C57','1'),('U13','1'))
    p.connect(('U13','5'),('C58','1'))
    p.place('Q2',290,178,fields=(296,172));p.place('R48',292,164);p.place('R49',270,187)
    p.connect(('R48','2'),('Q2','3'))
    p.connect(('R49','1'),('Q2','1'),via=[(270,178)])
    p.label('TP_RESET_N',(292,171));p.dot((270,178))
    p.text('LDO always fitted, including Mini mode.\nI2C pullups are on root sheet; use open drain.\nGPIO44 high asserts touch RESET low.',179,188,.88)

def main():
    raw=(PROJECT/'design/net-intent.json').read_bytes();intent=json.loads(raw)
    gate=json.loads((PROJECT/'design/pre-capture-gate.json').read_text())
    assert gate['intent_sha256']==hashlib.sha256(raw).hexdigest(),'Update pre-capture contract before capture'
    assert gate['ready_for_capture'] and not intent['resource_checks']
    history=PROJECT/'design/generated-schematic-hashes.json'
    if history.exists():
        for rel,h in json.loads(history.read_text()).items():
            p=PROJECT/rel
            assert not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()==h,f'Manual CAD edit: {rel}; preserve before regeneration'
    ports=json.loads((PROJECT/'design/hierarchy.json').read_text())['ports']
    pages=[]
    for name,n,title,draw in [('root',1,'Controller and hierarchy',root),('power',2,'Power and service',power),('motors',3,'Motor drivers',motors),('interfaces',4,'Serial and accessory outputs',interfaces),('display_connector',5,'External display connections',display)]:
        p=Page(name,n,title,intent['components'],ports.get(name,{}))
        if name=='root':draw(p,ports)
        else:draw(p)
        pages.append(p.finish())
    history.write_text(json.dumps({str(p.relative_to(PROJECT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in pages},indent=2)+'\n')
    print('Captured five native sheets: '+', '.join(p.name for p in pages))

if __name__=='__main__':main()
