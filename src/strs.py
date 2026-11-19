import struct,sys
def load(path):
    d=open(path,'rb').read()
    u=lambda b,o:struct.unpack('>I',b[o:o+4])[0]
    out=[]
    for i in range(u(d,4)):
        off,sz=u(d,8+8*i),u(d,12+8*i); b=d[off:off+sz]
        first=u(b,0); lists=[]
        for p in range(0,first,8):
            to,c=u(b,p),u(b,p+4)
            L=[]
            for k in range(c):
                so=u(b,to+4*k); e=b.index(b'\0',so); L.append(b[so:e].decode('utf8','replace'))
            lists.append(L)
        out.append(lists)
    return out
if __name__=='__main__':
    o=load(sys.argv[1])
    for i,bl in enumerate(o):
        for j,L in enumerate(bl): print(i,j,len(L),L[:4])
