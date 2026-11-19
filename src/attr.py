import sys; sys.path.insert(0,'.')
import loot, rem
from strs import load
from config import GAME
S=load(GAME+'/DATA/files/00/data00_eng.bin'); IT=S[0][0]; MON=S[4][64]
LARGE=[1,2,3,4,5,6,7,8,9,12,14,15,16,18,19,20,24,25]
BREAK={1:1,2:1,3:2,4:2,5:3,6:3,7:4,8:4,9:5,10:5,11:6,12:7,13:8,14:9,15:9,16:12,17:14,18:15,19:15,20:15,21:15,22:16,23:16,24:18,25:19,26:19,27:19,28:19,29:20,30:20,31:20,32:24,33:24,34:24,35:25,36:25,37:25}
REMT={1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:12,11:15,12:16,13:18,14:19,15:20,16:24,17:25,18:14}
src={}  # item -> set((team,rank,how))
def add(it,team,rank,how): src.setdefault(it,set()).add((team,rank,how))
for rk in (0,1):
    T=loot.TBL[rk]
    for i,L in enumerate(T):
        if not L: continue
        team = i if i<=29 else i-45 if 46<=i<=69 else i-90 if 91<=i<=119 else {146:8,201:18,208:25,209:25}.get(i)
        if team is None: continue
        for w,v in L: add(v,team,rk,'carve' if i<90 else 'drop')
R=loot.lot_arrays()
for rk,nm in ((0,'bui_l'),(1,'bui_h')):
    for team,Ls in R[nm].items():
        for l in Ls:
            for it,c,p in l: add(it,team,rk,'capture')
for rk,nm in ((0,'x_l'),(1,'x_h')):
    for b,Ls in R[nm].items():
        for l in Ls:
            for it,c,p in l: add(it,BREAK[b],rk,'break')
for n,L in rem.REM.items():
    rk=0 if n<100 else 1
    for it,c,p in L: add(it,REMT[n%100],rk,'reward')
def owner(it):
    s=src.get(it,set())
    teams=sorted({t for t,r,h in s if t in LARGE})
    ranks=sorted({r for t,r,h in s if t in LARGE})
    return teams,ranks
