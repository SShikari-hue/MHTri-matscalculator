import sys,json; sys.path.insert(0,'.')
from tree import *
from attr import owner, MON, src
from collections import Counter
from strs import load
from config import GAME
ITA=load(GAME+'/DATA/files/00/data00_ita.bin')[0][0]
GENERIC={153,154,155,595,357,359,183,556,566,304,559,106,509,104,105,560,341,548}
SHARED={171:'Rathian + Rathalos',284:'Rathian + Rathalos',385:'Rathian + Rathalos',279:'Rathian + Rathalos',175:'Rathian + Rathalos',466:'Draghi anziani (Ceadeus/Alatreon/Jhen)'}
COINS={379:'Agnaktor',584:'Rathalos',586:'Barioth',588:'Diablos',589:'Deviljho',608:'Barroth',609:'Royal Ludroth',610:'Rathian',611:'Lagiacrus',612:'Uragaan'}
def classify(it):
    if it in GENERIC: return None
    if it in SHARED:
        t,r=owner(it); return SHARED[it], 'LR' if 0 in r else 'HR'
    t,r=owner(it)
    if len(t)!=1: return None
    return MON[t[0]], 'LR' if 0 in r else 'HR'
C=lambda L: Counter({x:y for x,y in L}) if L else Counter()
units=lambda c: sum(c.values())
def step(v):
    opts=[]
    if v['create'] is not None: opts.append(('create',C(v['create'])))
    if v['up'] and v['parents']: opts.append(('up',C(v['up'])))
    return min(opts,key=lambda o:units(o[1]))
memo={}
def acquire(key):
    if key in memo: return memo[key]
    k,w=key; v=W[key]; opts=[]
    if v['create'] is not None: opts.append(C(v['create']))
    if v['up']:
        for p in v['parents']: opts.append(C(v['up'])+acquire((k,p)))
    memo[key]=min(opts,key=units); return memo[key]
once=Counter(); coll=Counter(); per_kind_once={}
for key,v in W.items():
    s=step(v)[1]; once+=s; per_kind_once.setdefault(key[0],Counter()); per_kind_once[key[0]]+=s
    coll+=acquire(key)
# frame levels
lev=Counter()
for (k,w),v in W.items():
    if k!='Frame': continue
    g=frame_growth(w); b=GB[g*7]; cap=3 if b else 6
    m,cond=v['raw']
    for L in range(2,cap+1): lev+=C(gun_level_mats(m,cond,b,L))
