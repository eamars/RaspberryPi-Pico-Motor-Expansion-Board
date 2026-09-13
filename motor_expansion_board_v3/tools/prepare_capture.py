"""Record the explicit endpoint, resource, hierarchy and clearance gate before CAD."""
import hashlib,json,datetime
from collections import defaultdict
from cad_support import PROJECT,footprint_path,symbol,pin_table,parse,children

raw=(PROJECT/'design/net-intent.json').read_bytes();d=json.loads(raw)
assert not d['resource_checks']
nets=defaultdict(list)
for c in d['components']:
    for pin,net in c['pins'].items():
        if net is not None:nets[net].append({'ref':c['ref'],'pin':pin,'sheet':c['sheet']})
ports={}
for s in ['power','motors','interfaces','display_connector']:
    ports[s]={}
    for net,endpoints in nets.items():
        sheets={p['sheet'] for p in endpoints}
        if net=='GND' or s not in sheets or len(sheets)<2:continue
        direction='bidirectional'
        if s=='power':direction='output' if net in ['VMOTOR','V5V','V3V3'] else 'bidirectional'
        elif s=='motors':direction='bidirectional' if net=='TMC_RX' else 'input'
        elif s=='interfaces':direction='output' if net=='SCALE_RX' else 'input'
        elif s=='display_connector':
            direction='output' if net in ['V3V0','MINI_BUTTON','DISP_WAIT'] else 'bidirectional' if net in ['I2C_SDA','I2C_SCL','DISP_D1_EN1','DISP_D2_EN2','DISP_BTN_IRQ'] else 'input'
        ports[s][net]=direction
hier={'total_sheets':5,'paper':'A3','style':'Populated parent, four coherent children. Matching named sheet pins and hierarchical labels; local labels inside each sheet; GND power symbols only. No global_label objects.',
      'ports':ports,'pages':{'root':'ESP32 core, flash/clock/RF/reset, EEPROM, spare header and four child instances',
       'power':'V2 PD/5V supply, added3.3V regulator, separate USB service and indicators/pads',
       'motors':'Both TMC2209 channels, local support and shared addressed UART',
       'interfaces':'V2 serial alternatives/selection and all three5V outputs',
       'display_connector':'Retained Mini headers and external QSPI connector, touch supply/reset'}}
rules={'units':'mm','stage':'Pre-capture design constraints; Mellow stackup confirmation and current-path calculation required before routing',
       'board':{'copper_layers':4,'nominal_thickness':1.6,'min_clearance':0.15,'min_track_width':0.15,'min_via_diameter':0.6,'min_via_drill':0.3,'copper_to_edge':0.3,'courtyard_clearance':0.25},
       'classes':[
           {'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.6,'via_drill':0.3,'nets':'All unassigned3.3/5V control signals'},
           {'name':'MotorPower','clearance':0.25,'track_width':1.2,'via_diameter':0.8,'via_drill':0.4,'nets':'VMOTOR and motor phase outputs; planes/wider copper where needed'},
           {'name':'Accessory5V','clearance':0.25,'track_width':1.2,'via_diameter':0.8,'via_drill':0.4,'nets':'V5V; wide pours for combined servo load'},
           {'name':'LogicSupply','clearance':0.2,'track_width':0.5,'via_diameter':0.6,'via_drill':0.3,'nets':'V3V3, V3V3_RF, VDD_SPI, V3V0'},
           {'name':'USB','clearance':0.2,'track_width':0.27,'via_diameter':0.6,'via_drill':0.3,'diff_pair_width':0.27,'diff_pair_gap':0.2,'nets':'USB_DP/DN, USB_SW_DP/DN, SERVICE_DP/DN;90ohm target'},
           {'name':'ClockMemoryDisplay','clearance':0.2,'track_width':0.2,'via_diameter':0.6,'via_drill':0.3,'nets':'FLASH_*, XTAL_*, DISP_* and I2C; keep clocks over continuousGND'},
           {'name':'SwitchSense','clearance':0.25,'track_width':0.5,'via_diameter':0.6,'via_drill':0.3,'nets':'BUCK*_SW/BOOT and M*_SENSE_*; compact switch loops / separate Kelvin sense returns'}],
       'localized_exceptions':'0.15mm width/clearance only for fine-pitch breakout, reviewed in PCB DRC. Package pad gaps are audited against actual footprints; never waive unrelated routing.',
       'impedance_basis':'USB starter geometry assumes0.18mm top dielectric,Er4.2,35um copper;approx90ohm. RF50ohm starter0.35mm over same dielectric. Recalculate with Mellow stackup before routing; these are not measured/guaranteed impedances.',
       'routing_notes':['Power widths are starting minima, not a5A or motor continuous-current qualification. Use short/wide pours and multiple vias.','Keep return plane continuous under USB/RF/clock/QSPI. Avoid switch-node copper below the antenna/crystal.','Do not place vias in0805 pads. Exposed-pad vias follow IC reference and Mellow assembly practice.']}
assets=[]
for fp in sorted({c['footprint'] for c in d['components']}):
    path=footprint_path(fp);raw_fp=path.read_bytes()
    pads={p[1] for p in children(parse(raw_fp.decode()),'pad') if p[1]}
    refs=[c['ref'] for c in d['components'] if c['footprint']==fp]
    missing={c['ref']:sorted(set(c['pins'])-pads) for c in d['components'] if c['footprint']==fp and set(c['pins'])-pads}
    assert not missing,(fp,missing)
    assets.append({'lib_id':fp,'source':'Installed KiCad10 library; not copied','refs':refs,'sha256':hashlib.sha256(raw_fp).hexdigest()})
for name,data in [('hierarchy.json',hier),('net-classes.json',rules),('net-endpoints.json',nets),('library-audit.json',{'custom_symbols':0,'custom_footprints':0,'footprints':assets})]:
    (PROJECT/'design'/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
gate={'ready_for_capture':True,'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'intent_sha256':hashlib.sha256(raw).hexdigest(),
      'component_instances':len(d['components']),'named_nets':len(nets),'total_sheets':5,
      'basis':['Owner Proceed authorization, V2/OWMC study and83-file reversible cleanup','Exact numbered endpoints and NC intent, all installed symbols/footprints resolve and all symbol pins have footprint pads','Numeric net classes and routing/stackup assumptions recorded before capture','Independent pin-capability check: corrected GPIO36/37 and glitch-free motor enables'],
      'later_checks':['Retained C8 ESR/loop and exact source package check before PCB','FFC contact orientation/assembly max current and Mini KILL-link compatibility before producing prototype','No firmware-port work: owner clarified pin suitability is sufficient']}
(PROJECT/'design/pre-capture-gate.json').write_text(json.dumps(gate,indent=2)+'\n')
print(json.dumps({'gate':'Ready for schematic capture','parts':len(d['components']),'nets':len(nets),'ports':{s:len(p) for s,p in ports.items()},'custom_assets':0},indent=2))
