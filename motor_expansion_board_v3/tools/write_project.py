"""Apply the pre-capture numeric constraints to the new KiCad project, no PCB."""
import json,re
from cad_support import PROJECT
p=PROJECT;d=json.loads((p/'design/net-classes.json').read_text());intent=json.loads((p/'design/net-intent.json').read_text())
classes=[]
for c in d['classes']:
    item={k:v for k,v in c.items() if k!='nets'}
    item.update(bus_width=12,wire_width=6,line_style=0,microvia_diameter=.3,microvia_drill=.1,
                pcb_color='rgba(0, 0, 0, 0.000)',schematic_color='rgba(0, 0, 0, 0.000)')
    item.setdefault('diff_pair_width',.27);item.setdefault('diff_pair_gap',.2);item['diff_pair_via_gap']=.2
    classes.append(item)
patterns=[]
for c,nets in [('MotorPower',['VMOTOR','M?_A?','M?_B?']),('Accessory5V',['V5V']),('LogicSupply',['V3V3','V3V3_RF','VDD_SPI','V3V0']),('USB',['USB_D?','USB_SW_D?','SERVICE_D?']),('ClockMemoryDisplay',['FLASH_*','XTAL_*','DISP_*','I2C_*']),('SwitchSense',['BUCK*_SW','BUCK*_BOOT','M?_SENSE_*'])]:
    for net in nets:
        # Hierarchy-qualified names are included as well as parent-level nets.
        for pattern in [net,'*/'+net]:patterns.append({'netclass':c,'pattern':pattern})
project={'meta':{'filename':'motor_expansion_board_v3.kicad_pro','version':1},
         'board':{'design_settings':{'rules':{'min_clearance':.15,'min_track_width':.15,'min_copper_edge_clearance':.3,
          'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_via_annular_width':.15,'min_hole_to_hole':.25,
          'min_silk_clearance':.15,'min_text_height':.8,'min_text_thickness':.12}}},
         'net_settings':{'meta':{'version':3},'classes':classes,'netclass_patterns':patterns,'netclass_assignments':None,'net_colors':None},
         'erc':{'erc_exclusions':[]},'text_variables':{'DESIGN_REVISION':'B1'}}
(p/'pcb/motor_expansion_board_v3.kicad_pro').write_text(json.dumps(project,indent=2)+'\n')
print('New project rules written; no PCB created.')
