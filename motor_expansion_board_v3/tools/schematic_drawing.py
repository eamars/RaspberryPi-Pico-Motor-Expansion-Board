"""Small native KiCad drawing helpers; installed symbols keep their library IDs.

Coordinates used by the drawing are 50 mil grid units. This is capture tooling,
not an electrical autorouter. Explicit wires and placed symbols form the drawing.
"""
from collections import defaultdict
import json, math, re, uuid
from cad_support import PROJECT, symbol, pin_table

NAME='motor_expansion_board_v3'
G=1.27
def q(s): return json.dumps(str(s),ensure_ascii=False)
def f(n): return f'{n*G:.4f}'.rstrip('0').rstrip('.') if n else '0'
def uid(key): return str(uuid.uuid5(uuid.NAMESPACE_URL,NAME+'/B1/'+key))
def effects(size=1,justify='left',hide=False):
    return f'(effects (font (size {f(size)} {f(size)})) (justify {justify})'+(' (hide yes)' if hide else '')+')'

class Page:
    def __init__(self,name,number,title,parts,ports=None):
        self.name=name; self.number=number;self.title=title
        self.path='/'+uid('root')+('' if name=='root' else '/'+uid('sheet:'+name))
        self.parts={p['ref']:p for p in parts if p['sheet']==name}
        self.ports=ports or {};self.used_ports=set();self.items=[];self.symbols={}
        self.placed={};self.handled=set();self.count=0;self.dots=set();self.wires=set();self.labels=[]
    def key(self,stem):
        self.count+=1;return uid(self.name+'/'+stem+'/'+str(self.count))
    def line(self,a,b,graphic=False):
        a,b=tuple(a),tuple(b)
        if a==b:return
        if not graphic:
            assert a[0]==b[0] or a[1]==b[1],(a,b)
            k=tuple(sorted((a,b)))
            if k in self.wires:return
            self.wires.add(k)
        self.items.append(f'({"polyline" if graphic else "wire"} (pts (xy {f(a[0])} {f(a[1])}) (xy {f(b[0])} {f(b[1])})) (stroke (width {"0.2" if graphic else "0"}) (type default)) (uuid "{self.key("line")}"))')
    def route(self,*points):
        for a,b in zip(points,points[1:]):
            if a[0]!=b[0] and a[1]!=b[1]:self.line(a,(b[0],a[1]));self.line((b[0],a[1]),b)
            else:self.line(a,b)
    def dot(self,xy):
        xy=tuple(xy)
        if xy in self.dots:return
        self.dots.add(xy)
        self.items.append(f'(junction (at {f(xy[0])} {f(xy[1])}) (diameter 0) (color 0 0 0 0) (uuid "{self.key("dot")}"))')
    def text(self,s,x,y,size=1):
        self.items.append(f'(text {q(s)} (at {f(x)} {f(y)} 0) {effects(size,"left top")} (uuid "{self.key("text")}"))')
    def heading(self,s,x,y,width):
        self.text(s,x,y,1.35);self.line((x,y+3),(x+width,y+3),True)
    def label(self,net,xy,side='R',hier=False):
        self.labels.append((net,tuple(xy)))
        if net in self.ports and net not in self.used_ports:hier=True
        if hier:
            assert net in self.ports;self.used_ports.add(net)
        angle={'R':0,'L':180,'U':90,'D':270}[side]
        justify='right' if side in ['L','D'] else 'left'
        kind='hierarchical_label' if hier else 'label'
        shape=f'(shape {self.ports[net]})' if hier else ''
        self.items.append(f'({kind} {q(net)} {shape} (at {f(xy[0])} {f(xy[1])} {angle}) {effects(.95,justify if hier else justify+" bottom")} (uuid "{self.key(net)}"))')
    def port(self,net,xy,side='L'):
        # Explicit child boundary; local label joins the named net inside page.
        self.label(net,xy,side,True)
        end=(xy[0]+(5 if side=='L' else -5),xy[1])
        self.line(xy,end);self.label(net,end,'R' if side=='L' else 'L')
    def place(self,ref,x,y,angle=0,fields=None,value=None):
        assert ref not in self.placed,ref
        c=self.parts[ref];lib=c['symbol'];raw=symbol(lib);self.symbols[lib]=raw
        pt=pin_table(raw);theta=math.radians(angle)
        pins={}
        for pn,p in pt.items():
            px,py,a=p['at'];rx=(px*math.cos(theta)-py*math.sin(theta))/G;ry=(px*math.sin(theta)+py*math.cos(theta))/G
            pins[pn]=(round(x+rx,6),round(y-ry,6),(a+angle)%360)
        self.placed[ref]=pins
        simple=len(pt)==2 and ref[0] in 'RCL'
        if fields is None:
            if simple:
                fields=(x+2.5,y-1) if angle in (0,180) else (x-3,y-5)
            else:
                fields=(min(t[0] for t in pins.values()),min(t[1] for t in pins.values())-7)
        fx,fy=fields
        val=value or c['value']
        if c['properties'].get('DNP') and 'DNP' not in val:val+=' (DNP)'
        attrs=[('Reference',ref,fx,fy,False),('Value',val,fx,fy+2.2,False),
               ('Footprint',c['footprint'],x,y,True),('MPN',c['mpn'],x,y,True),
               ('Manufacturer',c['manufacturer'],x,y,True)]
        for k,v in c['properties'].items():
            if k not in ['DNP','in_bom']:attrs.append((k,v,x,y,True))
        body=[f'(symbol (lib_id {q(lib)}) (at {f(x)} {f(y)} {angle}) (unit 1) (exclude_from_sim no) (in_bom {"no" if c["properties"].get("in_bom") is False else "yes"}) (on_board yes) (dnp {"yes" if c["properties"].get("DNP") else "no"}) (uuid "{uid(ref)}")']
        for k,v,ax,ay,hide in attrs:body.append(f'(property {q(k)} {q(v)} (at {f(ax)} {f(ay)} {angle%180}) {effects(1 if k=="Reference" else .9,"left",hide)})')
        for pn in pt:body.append(f'(pin {q(pn)} (uuid "{uid(ref+"."+pn)}"))')
        body.append(f'(instances (project "{NAME}" (path "{self.path}" (reference {q(ref)}) (unit 1)))))')
        self.items.append('\n'.join(body))
        return ref
    def pin(self,ref,pn):return self.placed[ref][str(pn)][:2]
    def net(self,ref,pn):return self.parts[ref]['pins'][str(pn)]
    def mark(self,ref,pn):
        # Coincident stacked pins must all be handled together.
        pos=self.pin(ref,pn)
        for n,p in self.placed[ref].items():
            if p[:2]==pos:
                assert self.net(ref,n)==self.net(ref,pn),(ref,n,pn)
                self.handled.add((ref,n))
    def connect(self,a,b,via=None):
        assert self.net(*a)==self.net(*b),(a,b,self.net(*a),self.net(*b))
        pa,pb=self.pin(*a),self.pin(*b)
        if via is None:
            points=[pa,pb] if pa[0]==pb[0] or pa[1]==pb[1] else [pa,(pb[0],pa[1]),pb]
        else:points=[pa,*via,pb]
        self.route(*points);self.mark(*a);self.mark(*b)
    def to(self,ref,pn,xy,label=True,side='R'):
        p=self.pin(ref,pn)
        self.route(p,(xy[0],p[1]),xy);self.mark(ref,pn)
        if label:self.label(self.net(ref,pn),xy,side)
    def bank(self,refs,x,y,step=12):
        # Parallel capacitors/pulls with real common buses, no per-part net islands.
        for i,r in enumerate(refs):self.place(r,x+i*step,y)
        for pn in ['1','2']:
            net=self.net(refs[0],pn)
            assert all(self.net(r,pn)==net for r in refs)
            py=self.pin(refs[0],pn)[1]+(-3 if pn=='1' else 3)
            xs=[]
            for r in refs:
                px=self.pin(r,pn)[0];xs.append(px);self.to(r,pn,(px,py),False)
            if len(xs)>1:self.line((xs[0],py),(xs[-1],py))
            for px in xs[1:-1]:self.dot((px,py))
            if net=='GND':self.power_symbol('GND',xs[0],py)
            else:self.label(net,(xs[0],py),'L')
    def auto(self):
        # Only remaining terminals get short local net stubs. Manual wiring wins.
        for ref,pins in self.placed.items():
            done=set()
            for pn,(x,y,a) in pins.items():
                if (ref,pn) in self.handled or (x,y) in done:continue
                done.add((x,y));net=self.net(ref,pn)
                if net is None:
                    self.items.append(f'(no_connect (at {f(x)} {f(y)}) (uuid "{self.key("NC")}"))');continue
                dx,dy,side={0:(-4,0,'L'),180:(4,0,'R'),90:(0,3,'D'),270:(0,-3,'U')}[a]
                e=(x+dx,y+dy);self.line((x,y),e)
                if net=='GND' and side=='D':self.power_symbol('GND',*e)
                else:self.label(net,e,side)
    def power_symbol(self,net,x,y,flag=False):
        lib='power:PWR_FLAG' if flag else 'power:GND';self.symbols[lib]=symbol(lib)
        ref=('#FLG' if flag else '#PWR')+str(self.number*10000+self.count)
        self.items.append(f'''(symbol (lib_id {q(lib)}) (at {f(x)} {f(y)} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid "{self.key(ref)}")
        (property "Reference" {q(ref)} (at {f(x)} {f(y)} 0) {effects(.8,'left',True)})
        (property "Value" {q('PWR_FLAG' if flag else 'GND')} (at {f(x+2)} {f(y+2)} 0) {effects(.8,'left',flag)})
        (pin "1" (uuid "{self.key(ref+'.1')}"))
        (instances (project "{NAME}" (path "{self.path}" (reference {q(ref)}) (unit 1)))))''')
        if flag:self.label(net,(x,y),'L')
        else:self.labels.append(('GND',(x,y)))
    def sheet(self,name,number,title,ports,x,y,w):
        h=max(14,8+len(ports)*2)
        body=[f'(sheet (at {f(x)} {f(y)}) (size {f(w)} {f(h)}) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid "{uid("sheet:"+name)}")',
              f'(property "Sheetname" {q(title)} (at {f(x)} {f(y-2)} 0) {effects(1)})',
              f'(property "Sheetfile" {q(name+".kicad_sch")} (at {f(x)} {f(y+h+2)} 0) {effects(.8,"left",True)})']
        for i,(net,direction) in enumerate(ports.items()):
            py=y+5+i*2
            body.append(f'(pin {q(net)} {direction} (at {f(x)} {f(py)} 180) {effects(.85)} (uuid "{uid(name+"/port/"+net)}"))')
            self.line((x-4,py),(x,py));self.label(net,(x-4,py),'L')
        body.append(f'(instances (project "{NAME}" (path "/{uid("root")}" (page "{number}")))))')
        self.items.append('\n'.join(body))
    def finish(self):
        assert set(self.parts)==set(self.placed),(self.name,set(self.parts)-set(self.placed))
        self.auto()
        self.name_wired_nets()
        assert set(self.ports)==self.used_ports,(self.name,set(self.ports)-self.used_ports)
        embedded='\n'.join(re.sub(r'^\(symbol "[^"]+"','(symbol '+q(lib),raw,count=1) for lib,raw in self.symbols.items())
        doc=f'''(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0")
        (uuid "{uid('root') if self.name=='root' else uid('document:'+self.name)}") (paper "A3")
        (title_block (title {q('Motor Expansion Board V3 - '+self.title)}) (date "2026-09-13") (rev "B1")
          (comment 1 "V2.1 compatible controller PCB | Review required before PCB"))
        (lib_symbols {embedded})
        {' '.join(self.items)}
        {'(sheet_instances (path "/" (page "1")))' if self.name=='root' else ''}
        (embedded_fonts no))\n'''
        target=PROJECT/'pcb'/((NAME if self.name=='root' else self.name)+'.kicad_sch')
        target.write_text(doc,encoding='utf-8')
        return target
    def name_wired_nets(self):
        # Add one local name to explicit wired circuits that have no label yet.
        # Endpoints and T junctions connect; a bare wire crossing does not.
        points={xy for ab in self.wires for xy in ab}|{xy for _,xy in self.labels}|self.dots
        terminals=[]
        for ref,pins in self.placed.items():
            for pn,p in pins.items():
                if self.net(ref,pn) is not None:
                    points.add(p[:2]);terminals.append((p[:2],self.net(ref,pn),ref+'.'+pn))
        parent={pt:pt for pt in points}
        def find(a):
            while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
            return a
        def join(a,b):parent[find(a)]=find(b)
        for a,b in self.wires:
            for pt in points:
                if (a[0]==b[0]==pt[0] and min(a[1],b[1])<=pt[1]<=max(a[1],b[1])) or (a[1]==b[1]==pt[1] and min(a[0],b[0])<=pt[0]<=max(a[0],b[0])):join(a,pt)
        groups=defaultdict(list)
        for pt,net,ref in terminals:groups[find(pt)].append((net,ref))
        named={find(pt) for _,pt in self.labels}
        for key,entries in groups.items():
            names={net for net,ref in entries}
            assert len(names)==1,('Drawing short',self.name,entries)
            if key in named:continue
            segs=[(a,b) for a,b in self.wires if find(a)==key]
            if not segs:continue
            horizontal=[(a,b) for a,b in segs if a[1]==b[1]]
            candidates=horizontal or segs
            a,b=max(candidates,key=lambda s:abs(s[0][0]-s[1][0])+abs(s[0][1]-s[1][1]))
            self.label(next(iter(names)),a if a<b else b,'R' if horizontal else 'U')
