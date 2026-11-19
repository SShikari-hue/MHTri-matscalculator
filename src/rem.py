import sys,struct; sys.path.insert(0,'.')
from rso import RSO; from strs import load
from config import GAME
r=RSO(GAME+'/DATA/files/01/quest_data.rso'); S=load(GAME+'/DATA/files/00/data00_eng.bin'); IT=S[0][0]; MON=S[4][64]
def tbl(name):
    a=r.sym[name]; out=[]
    while True:
        it,c,p=struct.unpack('>HBB',r.d[a:a+4]); a+=4
        if it==0: break
        out.append((it,c,p))
    return out
REM={}
for k in r.sym:
    if k.startswith('rem_item_tbl_em_') and k[-1].isdigit():
        n=int(k[-3:]); REM[n]=tbl(k)
if __name__=='__main__':
    for n in sorted(REM): print(n, MON[n%100], [(IT[i],c,p) for i,c,p in REM[n]])
