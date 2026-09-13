"""Reconcile native KiCad connectivity, NC intent, libraries and hierarchy."""
from collections import defaultdict
import hashlib,json,xml.etree.ElementTree as ET
from cad_support import PROJECT,parse,children,one

p=PROJECT;intent=json.loads((p/'design/net-intent.json').read_text());expected=defaultdict(set);nc=set()
refs={c['ref'] for c in intent['components']};parts={c['ref']:c for c in intent['components']}
for c in intent['components']:
    for pin,net in c['pins'].items():
        if net is None:nc.add((c['ref'],pin))
        else:expected[net].add((c['ref'],pin))
native=ET.parse(p/'review/netlist.xml').getroot();actual={};errors=[]
for net in native.findall('nets/net'):
    nodes={(n.attrib['ref'],n.attrib['pin']) for n in net.findall('node') if n.attrib['ref'] in refs}
    if nodes:actual[net.attrib['name']]=nodes
for name,nodes in expected.items():
    found=[(n,v) for n,v in actual.items() if v&nodes]
    if len(found)!=1 or found[0][1]!=nodes:errors.append({'intended_net':name,'native_groups':[(n,sorted(v)) for n,v in found]})
for terminal in nc:
    found=[(n,v) for n,v in actual.items() if terminal in v]
    if any(v!={terminal} for n,v in found):errors.append({'NC_joined':terminal,'native':[(n,sorted(v)) for n,v in found]})
for comp in native.findall('components/comp'):
    ref=comp.attrib['ref']
    if ref not in parts:errors.append({'unexpected_component':ref});continue
    if comp.findtext('footprint')!=parts[ref]['footprint']:errors.append({'footprint_mismatch':ref})
missing=refs-{c.attrib['ref'] for c in native.findall('components/comp')}
if missing:errors.append({'missing_components':sorted(missing)})
sheets=list((p/'pcb').glob('*.kicad_sch'))
for path in sheets:
    tree=parse(path.read_text(encoding='utf-8'))
    if children(tree,'global_label'):errors.append({'global_labels':path.name})
    if any(one(s,'lib_id')[1].startswith('MotorExpansionBoardV3:') for s in children(tree,'symbol')):errors.append({'custom_library':path.name})
if len(sheets)!=5:errors.append({'sheet_count':len(sheets)})
erc=json.loads((p/'review/erc.json').read_text());violations=[v for sh in erc['sheets'] for v in sh['violations']]
result={'passed':not errors,'contract_nets':len(expected),'connected_endpoints':sum(map(len,expected.values())),
 'explicit_nc_endpoints':len(nc),'component_instances':len(parts),'schematic_sheets':len(sheets),'global_signal_labels':0,
 'errors':errors,'erc_errors':sum(v['severity']=='error' for v in violations),'erc_warnings':sum(v['severity']=='warning' for v in violations),
 'source_hashes':{str(f.relative_to(p)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in sheets}}
(p/'review/connectivity-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
