import sys,json; sys.path.insert(0,'.')
from calc import *
from collections import defaultdict  # noqa
HRONLY={'Alatreon'}
def cls(it):
    c=classify(it)
    if c is None: return None
    m,r=c
    if m in HRONLY: r='HR'
    return m,r
def label(it):
    n=IT[it].strip()
    if it==457: n='Diablos Ridge (HR)'
    return n
