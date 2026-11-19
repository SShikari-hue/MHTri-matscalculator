import sys,struct; sys.path.insert(0,'.')
from rso import RSO; from strs import load
from config import GAME
r=RSO(GAME+'/DATA/files/01/lobby_data.rso'); d=r.d
c=RSO(GAME+'/DATA/files/01/com_data.rso')
S=load(GAME+'/DATA/files/00/data00_eng.bin'); IT=S[0][0]
# kind tag -> (sei tbl, kakou tbl, names)
KINDS={'GS':(0,0,S[1][0]),'SnS':(1,1,S[1][1]),'Hammer':(2,2,S[1][2]),'Lance':(3,3,S[1][5]),
       'LS':(7,7,S[1][3]),'SwAxe':(8,8,S[1][4]),
       'Frame':(4,None,S[2][0]),'Stock':(5,None,S[2][2]),'Barrel':(6,None,S[2][1])}
KLEN={0:94,1:92,2:86,3:98,7:44,8:62}
GB=[0,20,20,30,10,10,10,0,20,20,20,20,10,10,0,20,20,10,20,20,10,0,10,10,20,20,20,20,0,10,10,10,30,20,20,1,10,10,10,0,0,0,1,20,10,10,0,0,0,1,20,20,10,0,0,0,1,20,20,20,0,0,0,1,30,20,20,0,0,0,0,0]
def sei(t):
    a=r.sym['buki_sei_tbl0%d'%t]; gun=t in (4,5,6); rs=0x24 if gun else 0x18; out=[]
    o=a
    while True:
        row=d[o:o+rs]; k,_,it=struct.unpack('>BBH',row[:4])
        if it==0xFFFF: break
        n=6 if gun else 4
        m=[struct.unpack('>Hh',row[4+4*j:8+4*j]) for j in range(n)]
        cond=list(row[4+4*n:4+5*n])
        out.append((it,m,cond)); o+=rs
    return out
def kak(t):
    a=r.sym['kakou_tbl0%d'%t]; out=[]
    for i in range(KLEN[t]):
        row=d[a+0x18*i:a+0x18*i+0x18]
        m=[struct.unpack('>Hh',row[4*j:4*j+4]) for j in range(3)]
        out.append(([(x,y) for x,y in m if x and y>0],[x for x in struct.unpack('>4H',row[12:20]) if x]))
    return out
def gun_level_mats(m,cond,b,L):
    res=[]
    for (it,n),cc in zip(m,cond):
        h=cc>>4
        if   h==0: inc=L==0
        elif h==1: inc= L==0 or (b==0 and L<4)
        elif h==2: inc= L==0 or b!=0 or L>3
        elif h==3: inc= L!=0 and (b!=0 or L>2)
        elif h==4: inc= L!=0 and (b!=0 or L>=6) and (b!=1 or L>=3)
        elif h==5: inc= L!=0 and b==0 and L<4
        elif h==6: inc= L!=0 and (b!=0 or L>3)
        elif h==7: inc= L!=0
        if inc and it and n>0 and len(res)<4: res.append((it,n))
    return res
fd=c.sym['frame_data']
def frame_growth(i): return c.d[fd+0x24*i+3]
