import sys; sys.path.insert(0,'.')
from model import *
W={}  # (kind,id) -> dict(name, create, up, parents, children)
for k,(s,kk,N) in KINDS.items():
    cre={it:[(x,y) for x,y in m if x and y>0] for it,m,cond in sei(s)} if kk is not None else None
    if kk is None:
        for it,m,cond in sei(s):
            W[(k,it)]=dict(name=N[it],create=gun_level_mats(m,cond,0,0),up=None,parents=[],children=[],raw=(m,cond))
        continue
    K=kak(kk)
    # radici fuori dalla fucina (armi antiche da scavo, Barbarian Blade): righe con potenziamenti ma senza origine
    for i,(m,nx) in enumerate(K):
        if i and nx and i not in cre and not any(i in n2 for _,n2 in K): cre[i]=[]
    nodes=set(cre); stack=list(cre)
    while stack:
        w=stack.pop()
        for c in K[w][1]:
            if c not in nodes: nodes.add(c); stack.append(c)
    for w in nodes:
        W[(k,w)]=dict(name=N[w],create=cre.get(w),up=K[w][0] or None,parents=[],children=[x for x in K[w][1]])
    for w in nodes:
        for c in K[w][1]: W[(k,c)]['parents'].append(w)
