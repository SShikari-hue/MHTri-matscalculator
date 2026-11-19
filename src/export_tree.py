import sys,json; sys.path.insert(0,'.')
from calc import *
from classify import cls, label, COINS
from config import GAME
ITW=load(GAME+'/DATA/files/00/data00_ita.bin')
KMAP={'GS':(1,0),'SnS':(1,1),'Hammer':(1,2),'LS':(1,3),'SwAxe':(1,4),'Lance':(1,5),'Frame':(2,0),'Barrel':(2,1),'Stock':(2,2)}
KORD=['GS','LS','SnS','Hammer','Lance','SwAxe','Frame','Barrel','Stock']
D=lambda c:{str(k):v for k,v in c.items() if v>0}
weap=[];items=set()
for key,v in W.items():
    k,w=key; b,l=KMAP[k]
    how,s=step(v); a=acquire(key)
    e=dict(id=f'{k}:{w}',k=k,n=v['name'],it=ITW[b][l][w],
      cr=D(C(v['create'])) if v['create'] is not None else None,
      up=D(C(v['up'])) if v['up'] and v['parents'] else None,
      p=[f'{k}:{x}' for x in v['parents']], c=[f'{k}:{x}' for x in v['children'] if (k,x) in W],
      once=D(s),how=how,coll=D(a))
    if k=='Frame':
        g=frame_growth(w); bb=GB[g*7]; cap=3 if bb else 6
        m,cond=v['raw']; e['cap']=cap; e['hrf']=bool(bb)
        e['lv']=[D(C(gun_level_mats(m,cond,bb,L))) for L in range(2,cap+1)]
    for d in (e['cr'] or {},e['up'] or {},e['coll'],*e.get('lv',[])): items|=set(map(int,d))
    weap.append(e)
SHOP={'GS':[(1,0,28),(42,0,28),(12,16,31),(45,20,33)],'SnS':[(1,0,28),(30,0,28),(12,16,31),(32,20,33)],
 'Hammer':[(1,0,28),(38,0,28),(41,16,31),(5,20,33)],'Lance':[(1,0,28),(40,0,28),(4,16,31),(43,20,33)],'Frame':[(1,0,28),(2,0,28),(3,0,28)]}
BYID={e['id']:e for e in weap}
for k,rows in SHOP.items():
    for i,off,on in rows:
        BYID[f'{k}:{i}']['buy']=dict(off=off,on=on)
        if k=='Frame':
            for kk in ('Barrel','Stock'): BYID[f'{kk}:{i}']['buy']=dict(off=off,on=on,set=f'Frame:{i}')
for e in weap: e.pop('once',None); e.pop('coll',None); e.pop('how',None)
weap.sort(key=lambda e:(KORD.index(e['k']),int(e['id'].split(':')[1])))
meta={}
for it in sorted(items):
    c=cls(it); m=dict(en=label(it),it=ITA[it].strip())
    if c: m['g']='m'; m['mon']=c[0]; m['r']=c[1]
    elif it in COINS or 'Coin' in IT[it] or 'Seal' in IT[it]: m['g']='coin'
    elif it in GENERIC: t,r=owner(it); m['g']='gen'; m['r']='LR' if 0 in r else 'HR'
    else: m['g']='oth'
    meta[it]=m
order=['Great Jaggi','Qurupeco','Royal Ludroth','Barroth','Great Baggi','Gigginox','Gobul','Rathian','Lagiacrus','Barioth','Agnaktor','Uragaan','Rathalos','Diablos','Deviljho','Rathian + Rathalos','Ceadeus','Alatreon','Jhen Mohran','Draghi anziani (Ceadeus/Alatreon/Jhen)']
KN={'GS':'Spadone','LS':'Spada lunga','SnS':'Spada e scudo','Hammer':'Martello','Lance':'Lancia','SwAxe':'Ascia cangiante','Frame':'Base','Barrel':'Canna','Stock':'Elsa'}
LANGS={'en':'eng','it':'ita','fr':'fre','es':'spa','de':'ger'}
SL={l:load(f'{GAME}/DATA/files/00/data00_{f}.bin') for l,f in LANGS.items()}
for e in weap:
    k,i=e['id'].split(':'); b,l=KMAP[k]; i=int(i)
    e['n']={lg:SL[lg][b][l][i].strip() for lg in LANGS}; e.pop('it',None)
for it,m in meta.items():
    m['n']={lg:SL[lg][0][0][it].strip() for lg in LANGS}
    if it==457:
        for lg,suf in [(lg,' (HR)') for lg in LANGS]: m['n'][lg]+=suf
    m.pop('en',None); m.pop('it',None)
TEAM={'Great Jaggi':12,'Qurupeco':3,'Royal Ludroth':16,'Barroth':8,'Great Baggi':14,'Gigginox':4,'Gobul':18,'Rathian':1,'Lagiacrus':15,'Barioth':5,'Agnaktor':19,'Uragaan':9,'Rathalos':2,'Diablos':6,'Deviljho':7,'Ceadeus':20,'Alatreon':24,'Jhen Mohran':25}
JA={'Great Jaggi':'ドスジャギィ','Qurupeco':'クルペッコ','Royal Ludroth':'ロアルドロス','Barroth':'ボルボロス','Great Baggi':'ドスバギィ','Gigginox':'ギギネブラ','Gobul':'チャナガブル','Rathian':'リオレイア','Lagiacrus':'ラギアクルス','Barioth':'ベリオロス','Agnaktor':'アグナコトル','Uragaan':'ウラガンキン','Rathalos':'リオレウス','Diablos':'ディアブロス','Deviljho':'イビルジョー','Ceadeus':'ナバルデウス','Alatreon':'アルバトリオン','Jhen Mohran':'ジエン・モーラン'}
ZH={'Rathian':'雌火龙','Rathalos':'火龙','Diablos':'角龙','Deviljho':'恐暴龙','Barioth':'冰牙龙','Alatreon':'煌黑龙','Royal Ludroth':'水兽','Barroth':'土砂龙','Uragaan':'爆锤龙'}
mnames={}
for m in order:
    if m in TEAM:
        d={lg:SL[lg][4][64][TEAM[m]].strip() for lg in LANGS}
        mnames[m]=d
json.dump(dict(w=weap,items=meta,mons=order,mnames=mnames,kinds=[[k,KN[k]] for k in KORD]),open(sys.argv[1],'w'),ensure_ascii=False,separators=(',',':'))
print(len(weap),len(meta))
