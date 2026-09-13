"""Small KiCad text helpers. Standard assets stay in installed KiCad libraries."""
from pathlib import Path
import json, os, re

PROJECT = Path(__file__).resolve().parents[1]
KICAD = Path(os.environ.get('KICAD_SHARE', 'C:/Program Files/KiCad/10.0/share/kicad'))

def parse(text):
    stack=[]; root=None
    for token in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text):
        if token=='(':
            node=[]
            if stack: stack[-1].append(node)
            else: root=node
            stack.append(node)
        elif token==')': stack.pop()
        else: stack[-1].append(json.loads(token) if token.startswith('"') else token)
    assert not stack
    return root

def children(node,kind):
    return [x for x in node if isinstance(x,list) and x and x[0]==kind]

def one(node,kind,default=None):
    return next(iter(children(node,kind)),default)

def walk(node,kind):
    for x in node:
        if isinstance(x,list):
            if x and x[0]==kind: yield x
            yield from walk(x,kind)

def balanced(text,start):
    depth=0; quoted=False; escaped=False
    for i in range(start,len(text)):
        char=text[i]
        if escaped: escaped=False
        elif quoted and char=='\\': escaped=True
        elif char=='"': quoted=not quoted
        elif not quoted:
            if char=='(': depth+=1
            elif char==')':
                depth-=1
                if depth==0: return text[start:i+1]
    raise ValueError('Unbalanced KiCad source')

def symbol_source(path,name):
    text=path.read_text(encoding='utf-8')
    m=re.search(r'\(symbol\s+"'+re.escape(name)+r'"\s',text)
    if not m: raise ValueError(f'Missing symbol {path}:{name}')
    raw=balanced(text,m.start()); base=one(parse(raw),'extends')
    if base:
        parent=symbol_source(path,base[1])
        parent=re.sub(r'\(symbol "'+re.escape(base[1])+r'(?=["_])','(symbol "'+name,parent)
        # Derived properties matter (in particular fixed-output regulator variants).
        for prop in children(parse(raw),'property'):
            pm=re.search(r'\(property "'+re.escape(prop[1])+r'"\s',raw)
            old=re.search(r'\(property "'+re.escape(prop[1])+r'"\s',parent)
            if pm and old:
                replacement=balanced(raw,pm.start()); previous=balanced(parent,old.start())
                parent=parent[:old.start()]+replacement+parent[old.start()+len(previous):]
            elif pm:
                parent=parent[:-1]+'\n'+balanced(raw,pm.start())+'\n)'
        return parent
    return raw

def symbol(lib_id):
    lib,name=lib_id.split(':',1)
    path=(PROJECT/'pcb/libraries/symbols'/f'{lib}.kicad_sym' if lib=='MotorExpansionBoardV3'
          else KICAD/'symbols'/f'{lib}.kicad_sym')
    return symbol_source(path,name)

def pin_table(raw):
    result={}
    for p in walk(parse(raw),'pin'):
        number=one(p,'number')[1]
        result[number]={'name':one(p,'name')[1], 'type':p[1],
                        'at':[float(v) for v in one(p,'at')[1:]],
                        'length':float(one(p,'length')[1])}
    return result

def footprint_path(lib_id):
    lib,name=lib_id.split(':',1)
    root=PROJECT/'pcb/libraries/footprints' if lib=='MotorExpansionBoardV3' else KICAD/'footprints'
    return root/(lib+'.pretty')/(name+'.kicad_mod')
