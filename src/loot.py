import sys,struct; sys.path.insert(0,'.')
from rso import RSO; from strs import load
from config import GAME
IT=load(GAME+'/DATA/files/00/data00_eng.bin')[0][0]
r=RSO(GAME+'/DATA/files/01/em_data.rso'); d=r.d
def lst(p):
    out=[]
    while True:
        w,v=struct.unpack('>HH',d[p:p+4]); p+=4
        if w==0xffff: break
        out.append((w,v))
    return out
BASES=[0xbd628,0xbd9c0,0xbdd58]
TBL=[[lst(r.rel[b+4*i]) if b+4*i in r.rel else None for i in range(230)] for b in BASES]
def team_ptrs(sym,n=41):
    a=r.sym[sym]; return [r.rel.get(a+4*i) for i in range(n)]
def lot_region(t,end):
    out=[];cur=[]
    o=t
    while o<end:
        it,c,p=struct.unpack('>HBB',d[o:o+4]); o+=4
        if it==0:
            out.append(cur);cur=[]
        else: cur.append((it,c,p))
    return out
def lot_arrays():
    a=r.sym['em_drop_tbl_1']; e=r.sym['em_bui_tbl_1']
    alltg=sorted(set(t for s,t in r.rel.items() if a<=t<e))
    res={}
    for name,base in (('bui_l',0xbef00),('bui_h',0xbefa4),('x_l',0xbf044),('x_h',0xbf0e8)):
        res[name]={}
        for i in range(41):
            t=r.rel.get(base+4*i)
            if t is None: continue
            nxt=[x for x in alltg if x>t]; end=nxt[0] if nxt else e
            res[name][i]=lot_region(t,min(end,base))
    return res
