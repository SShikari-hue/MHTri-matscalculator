"""Minimal RSO loader for MH Tri em_data.rso: sections in-file, internal relocations resolved to file offsets."""
import struct
class RSO:
    def __init__(s, path):
        d = s.d = open(path, 'rb').read()
        g = s.u32
        so, n = g(0xc), g(0x8)
        s.secs = [(g(so+8*i) & ~1, g(so+8*i+4)) for i in range(n)]
        io, isz = g(0x30), g(0x34)
        s.rel = {}
        for k in range(isz // 12):
            off, info, add = struct.unpack('>III', d[io+12*k:io+12*k+12])
            if info & 0xff == 1:  # R_PPC_ADDR32
                s.rel[off] = s.secs[info >> 8][0] + add
        eo, es, en = g(0x40), g(0x44), g(0x48)
        s.sym = {}
        for k in range(es // 16):
            no, off, sec, h = struct.unpack('>IIII', d[eo+16*k:eo+16*k+16])
            s.sym[d[en+no:d.index(b'\0', en+no)].decode()] = s.secs[sec][0] + off
    def u32(s, o): return struct.unpack('>I', s.d[o:o+4])[0]
    def ptr(s, o): return s.rel.get(o)
