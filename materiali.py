#!/usr/bin/env python3
"""Materiali mancanti per le armi di Monster Hunter Tri (PAL RMHP08), letti dal tuo salvataggio Dolphin.

Usa gli stessi dati e le stesse regole dell'artefatto "Albero armi di Tri" (tree.json accanto a questo file):
armi possedute = cassa equipaggiamento del salvataggio, materiali posseduti = cassa oggetti + borse.

Esempi:
  ./materiali.py                      riepilogo per mostro (LR/HR): serve, hai, manca
  ./materiali.py --watch              lo ristampa a ogni salvataggio
  ./materiali.py --tipo martello,lancia
  ./materiali.py --mostro rathalos    dettaglio materiale per materiale
  ./materiali.py --pronte             armi che puoi fare adesso con quello che hai
  ./materiali.py --arma "doris"       percorso piu' breve per un'arma, con cosa ti manca
  ./materiali.py --armi               elenco armi possedute / mancanti per tipo
"""
import argparse, json, os, struct, sys, time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.expanduser('~/.var/app/org.DolphinEmu.dolphin-emu/data/dolphin-emu/Wii/title/'
                          '00010000/524d4850/data/nocopy/data00')
# tipo d'arma nel salvataggio (_EQUIP.kind) -> sigla usata in tree.json
KIND = {7: 'GS', 8: 'SnS', 9: 'Hammer', 10: 'Lance', 11: 'Frame', 12: 'Barrel', 13: 'Stock', 14: 'LS', 15: 'SwAxe'}
ALIAS = {'spadone': 'GS', 'gs': 'GS', 'spada lunga': 'LS', 'lunga': 'LS', 'ls': 'LS', 'spada e scudo': 'SnS',
         'sns': 'SnS', 'spada': 'SnS', 'martello': 'Hammer', 'hammer': 'Hammer', 'lancia': 'Lance', 'lance': 'Lance',
         'ascia cangiante': 'SwAxe', 'ascia': 'SwAxe', 'spadascia': 'SwAxe', 'swaxe': 'SwAxe', 'base': 'Frame', 'basi': 'Frame',
         'telaio': 'Frame', 'canna': 'Barrel', 'canne': 'Barrel', 'elsa': 'Stock', 'else': 'Stock', 'calcio': 'Stock', 'balestra': 'Frame,Barrel,Stock'}

# --- colori terminale (spenti se l'uscita non e' un terminale o con NO_COLOR)
TTY = sys.stdout.isatty() and not os.environ.get('NO_COLOR')
def c(code, s): return f'\033[{code}m{s}\033[0m' if TTY else str(s)
LR = lambda s: c('36', s)
HR = lambda s: c('33', s)
OK = lambda s: c('32', s)
DIM = lambda s: c('2', s)
B = lambda s: c('1', s)


LANG = 'it'
def N(o):  return o['n'].get(LANG) or o['n']['en']
def N2(o): return '' if LANG == 'en' else o['n']['en']
MNAMES = {}
def MN(k):
    if k == 'Rathian + Rathalos': return k
    if k.startswith('Draghi anziani'): return {'it': 'Draghi anziani', 'en': 'Elder Dragons', 'fr': 'Dragons anciens', 'es': 'Dragones ancianos', 'de': 'Ältere Drachen'}[LANG]
    m = MNAMES.get(k); return (m.get(LANG) or N(m)) if m else k


def load_data():
    p = os.path.join(HERE, 'tree.json')
    if not os.path.exists(p):
        sys.exit(f'manca {p}: rigeneralo con src/export_tree.py')
    D = json.load(open(p, encoding='utf-8'))
    W = {w['id']: w for w in D['w']}
    IT = {int(k): v for k, v in D['items'].items()}
    for w in D['w']:
        for f in ('cr', 'up'):
            if w.get(f) is not None:
                w[f] = {int(k): v for k, v in w[f].items()}
        if 'lv' in w:
            w['lv'] = [{int(k): v for k, v in l.items()} for l in w['lv']]
    MNAMES.update(D.get('mnames', {}))
    return D, W, IT


def read_save(path, slot=None):
    d = open(path, 'rb').read()
    if len(d) != 0x14000:
        sys.exit(f'file di salvataggio inatteso: {path}')
    if struct.unpack('>I', d[4:8])[0] != sum(d[8:]) & 0xFFFFFFFF:
        print('attenzione: checksum del salvataggio non valido', file=sys.stderr)
    used = list(d[0x1A:0x1D])
    if slot is None:
        slot = d[0x19] if used[d[0x19]] else used.index(1)
    u = d[0x48 + 0x6000 * slot: 0x48 + 0x6000 * (slot + 1)]
    name = u[3:0x14].split(b'\0')[0].decode('latin1')
    hr = struct.unpack('>H', u[0x3DE4:0x3DE6])[0]
    zenny = struct.unpack('>i', u[0x18:0x1C])[0]
    items = Counter()
    for off, n in ((0xA0, 0x18), (0x100, 0x20), (0x180, 800)):   # borsa lama, borsa artigliere, cassa
        for i in range(n):
            it, cnt = struct.unpack('>Hh', u[off + 4 * i: off + 4 * i + 4])
            if it and cnt > 0:
                items[it] += cnt
    owned, levels = set(), {}
    for i in range(800):                                          # cassa equipaggiamento
        k, dc, it = struct.unpack('>BBH', u[0xE00 + 12 * i: 0xE00 + 12 * i + 4])
        if it and k in KIND:
            wid = f'{KIND[k]}:{it}'
            owned.add(wid)
            if k == 11:
                levels[wid] = max(levels.get(wid, 1), dc or 1)
    return dict(slot=slot, name=name, hr=hr, zenny=zenny, items=items, owned=owned, levels=levels)


# --- stesse regole dell'artefatto
def U(c, metric='all', IT=None):
    return sum(n for i, n in c.items() if metric == 'all' or IT[i]['g'] == 'm')

def add(a, b):
    o = Counter(a); o.update(b or {}); return o

def all_paths(W, wid, owned, target, depth=0):
    w, o = W[wid], []
    if owned is not None and wid in owned and wid != target:
        o.append((Counter(), [('own', wid, None, None)]))
    if w.get('buy'):
        o.append((Counter(), [('buy', wid, None, None)]))
    if w.get('cr') is not None:
        o.append((Counter(w['cr']), [('create' if w['cr'] else 'other', wid, w['cr'], None)]))
    if w.get('up') and depth < 30:
        for p in w['p']:
            for cost, steps in all_paths(W, p, owned, target, depth + 1):
                o.append((add(cost, w['up']), steps + [('up', wid, w['up'], p)]))
    return o

def sort_paths(paths, metric, IT):
    return sorted(paths, key=lambda x: (U(x[0], metric, IT), U(x[0], 'all', IT), len(x[1])))

FRESH = {}
def fresh(W, IT, wid):
    if wid not in FRESH:
        FRESH[wid] = sort_paths(all_paths(W, wid, None, wid), 'all', IT)[0][0]
    return FRESH[wid]

def step(w, IT):
    if w.get('buy'):
        return Counter()
    o = [Counter(x) for x in (w.get('cr'), w.get('up') if w['p'] else None) if x is not None]
    return min(o, key=lambda x: U(x, 'all', IT)) if o else Counter()

def needs(D, W, IT, st, mode, kinds, levels_on):
    byk = defaultdict(Counter)
    for w in D['w']:
        if w['k'] not in kinds:
            continue
        if w['id'] not in st['owned']:
            byk[w['k']].update(fresh(W, IT, w['id']) if mode == 'coll' else step(w, IT))
        if levels_on and 'lv' in w:
            cur = st['levels'].get(w['id'], 1) if w['id'] in st['owned'] else 1
            for L in range(2, w['cap'] + 1):
                if L > cur:
                    byk[w['k']].update(w['lv'][L - 2])
    tot = Counter()
    for v in byk.values():
        tot.update(v)
    return tot, byk


# --- stampa
def header(st, args, D, kinds):
    kn = dict(D['kinds'])
    own = sum(1 for w in D['w'] if w['id'] in st['owned'] and w['k'] in kinds)
    tot = sum(1 for w in D['w'] if w['k'] in kinds)
    mode = 'tenerle tutte' if args.mode == 'coll' else 'ogni arma una volta'
    tipi = 'tutti i tipi' if len(kinds) == len(kn) else ', '.join(kn[k] for k in kinds)
    print(B(f"{st['name']}  HR {st['hr']}  ·  {st['zenny']} z  ·  slot {st['slot']}"))
    print(f'armi possedute {own}/{tot}  ·  conto: {mode}  ·  {tipi}'
          + ('  ·  con livelli basi' if args.livelli else ''))

def summary(D, IT, st, tot, args):
    rows = []
    for m in D['mons']:
        r = {}
        for rk in ('LR', 'HR'):
            serve = sum(n for i, n in tot.items() if IT[i].get('mon') == m and IT[i].get('r') == rk)
            hai = sum(min(n, st['items'][i]) for i, n in tot.items() if IT[i].get('mon') == m and IT[i].get('r') == rk)
            r[rk] = (serve, hai, serve - hai)
        if r['LR'][0] or r['HR'][0]:
            rows.append((m, r))
    print()
    print(f"{'mostro':<26}" + LR(f"{'LR serve':>8}{'hai':>5}{'manca':>7}") + '   ' + HR(f"{'HR serve':>8}{'hai':>5}{'manca':>7}"))
    tl, th = [0, 0, 0], [0, 0, 0]
    for m, r in rows:
        a, b = r['LR'], r['HR']
        cell = lambda x, f: f(f'{x[0]:>8}{x[1]:>5}{x[2]:>7}') if x[0] else DIM(f'{"-":>8}{"":>5}{"":>7}')
        done = OK('  completo') if a[2] == 0 and b[2] == 0 else ''
        print(f'{MN(m)[:25]:<26}' + cell(a, LR) + '   ' + cell(b, HR) + done)
        for t, x in ((tl, a), (th, b)):
            for k in range(3): t[k] += x[k]
    print(B(f"{'totale':<26}{tl[0]:>8}{tl[1]:>5}{tl[2]:>7}   {th[0]:>8}{th[1]:>5}{th[2]:>7}"))
    print(DIM('"hai" conta solo fino al necessario. --mostro NOME per il dettaglio, --tutto per i materiali generici.'))

def detail(D, IT, st, tot, byk, names, show_all):
    kn = dict(D['kinds'])
    groups = defaultdict(list)
    for i, n in tot.items():
        m = IT[i]
        key = m.get('mon') or {'gen': 'Materiali generici', 'oth': 'Minerali, insetti e altro', 'coin': 'Monete e sigilli'}[m['g']]
        groups[key].append(i)
    order = [m for m in D['mons']] + ['Materiali generici', 'Minerali, insetti e altro', 'Monete e sigilli']
    for g in order:
        if g not in groups:
            continue
        if names and not any(n in g.lower() or n in MN(g).lower() for n in names):
            continue
        if not names and not show_all and g not in D['mons']:
            continue
        print('\n' + B(MN(g) if g in D['mons'] else g))
        for i in sorted(groups[g], key=lambda i: (IT[i].get('r', ''), -tot[i])):
            m = IT[i]; n = tot[i]; h = st['items'][i]; miss = max(0, n - h)
            rk = (LR if m.get('r') == 'LR' else HR)(m.get('r', '  ')) if m.get('r') else '  '
            per = ', '.join(f'{kn[k]} {byk[k][i]}' for k in byk if byk[k][i])
            st_ = OK('ok') if miss == 0 else f'manca {miss}'
            print(f"  {rk} {N(m)[:22]:<23}{DIM(N2(m)[:17]):<{17 + (8 if TTY else 0)}} serve {n:>3}  hai {h:>3}  {st_:<10} {DIM(per)}")

def weapons_list(D, st, kinds):
    kn = dict(D['kinds'])
    for k in kinds:
        ws = [w for w in D['w'] if w['k'] == k]
        own = [w for w in ws if w['id'] in st['owned']]
        print('\n' + B(f'{kn[k]}  {len(own)}/{len(ws)}'))
        for w in ws:
            mark = OK('✔') if w['id'] in st['owned'] else ' '
            lv = f" Lv{st['levels'].get(w['id'], 1)}/{w['cap']}" if 'cap' in w and w['id'] in st['owned'] else ''
            print(f"  {mark} {N(w)}{lv}" + DIM(f"  {N2(w)}") + (OK('  [negozio]') if w.get('buy') else ''))

def ready(D, W, IT, st, kinds):
    """Armi mancanti che puoi ottenere adesso: un solo passo, materiali gia' in cassa."""
    kn = dict(D['kinds']); out = []
    for w in D['w']:
        if w['k'] not in kinds or w['id'] in st['owned']:
            continue
        opts = []
        if w.get('buy'):
            opts.append(('compra al negozio', Counter()))
        if w.get('cr'):
            opts.append(('crea', Counter(w['cr'])))
        if w.get('up'):
            for p in w['p']:
                if p in st['owned']:
                    opts.append((f"potenzia {N(W[p])}", Counter(w['up'])))
        for how, cost in opts:
            if all(st['items'][i] >= n for i, n in cost.items()):
                out.append((w, how, cost)); break
    print()
    if not out:
        print('Nessuna arma mancante si puo\' fare adesso con i materiali in cassa.'); return
    print(B(f'Pronte da fare adesso ({len(out)}):'))
    for w, how, cost in out:
        m = ', '.join(f"{N(IT[i])} ×{n}" for i, n in cost.items())
        print(f"  {kn[w['k']]:<14} {N(w):<26} {how}" + DIM(f'  {m}' if m else ''))
    print(DIM('Potenziare consuma l\'arma di partenza.'))

def path(D, W, IT, st, q, metric):
    q = q.lower()
    hits = [w for w in D['w'] if any(q in x.lower() for x in w['n'].values())]
    if not hits:
        sys.exit(f'nessuna arma trovata per "{q}"')
    exact = [w for w in hits if any(q == x.lower() for x in w['n'].values())]
    if len(hits) > 1 and not exact:
        print('Piu\' armi corrispondono, scegline una:')
        for w in hits[:30]:
            print(f"  {dict(D['kinds'])[w['k']]:<14} {N(w)}  " + DIM(N2(w)))
        return
    w = (exact or hits)[0]
    paths = sort_paths(all_paths(W, w['id'], st['owned'], w['id']), metric, IT)
    cost, steps = paths[0]
    print('\n' + B(f"{N(w)}") + DIM(f"  {N2(w)} · {dict(D['kinds'])[w['k']]}"))
    if w['id'] in st['owned']:
        print(OK('La possiedi gia\': questa e\' la strada per una seconda copia.'))
    for n, (how, wid, mats, frm) in enumerate(steps, 1):
        n_ = N(W[wid])
        if how == 'own': t = f'parti da {n_} (posseduta, il potenziamento la consuma)'
        elif how == 'buy':
            st_ = W[wid]['buy'].get('set')
            t = f"compra il set {N(W[st_])} al negozio (base+canna+elsa)" if st_ else f'compra {n_} al negozio'
        elif how == 'create': t = f'crea {n_}'
        elif how == 'other': t = f'ottieni {n_} fuori dalla fucina (es. arma antica da scavo o ricompensa)'
        else: t = f"potenzia {N(W[frm])} in {n_}"
        print(f'  {n}. {t}')
        for i, k in (mats or {}).items():
            have = st['items'][i]
            flag = OK('ok') if have >= k else f'manca {k - have}'
            print(DIM(f"       {N(IT[i])} ×{k}") + f'  (hai {have}, {flag})')
    miss = {i: n - st['items'][i] for i, n in cost.items() if st['items'][i] < n}
    print(f"  totale {U(cost, 'all', IT)} materiali, {U(cost, 'mon', IT)} di mostro"
          + ('  ·  ' + OK('hai gia\' tutto') if not miss else f"  ·  ti mancano {sum(miss.values())} pezzi:"))
    for i, n in sorted(miss.items(), key=lambda x: -x[1]):
        m = IT[i]
        print(f"     {N(m)} ×{n}" + DIM(f"  {MN(m['mon']) if m.get('mon') else ''} {m.get('r', '')}"))
    if len(paths) > 1:
        print(DIM('  alternative: ' + ' | '.join(
            f"{N(W[s[0][1]])} ({'posseduta' if s[0][0] == 'own' else {'buy': 'negozio', 'create': 'crea', 'other': 'altro'}[s[0][0]]}) {U(c_, 'all', IT)}"
            for c_, s in paths[1:5])))


def run(args, D, W, IT):
    st = read_save(args.save, args.slot)
    kinds = [k for k, _ in D['kinds']]
    if args.tipo:
        want = []
        for t in args.tipo.split(','):
            t = t.strip().lower()
            if t not in ALIAS:
                sys.exit(f'tipo sconosciuto "{t}". Validi: ' + ', '.join(sorted(ALIAS)))
            want += ALIAS[t].split(',')
        kinds = [k for k in kinds if k in want]
    if args.arma:
        header(st, args, D, kinds); path(D, W, IT, st, args.arma, args.metric); return
    header(st, args, D, kinds)
    if args.armi:
        weapons_list(D, st, kinds); return
    if args.pronte:
        ready(D, W, IT, st, kinds); return
    tot, byk = needs(D, W, IT, st, args.mode, kinds, args.livelli)
    if args.mostro or args.tutto:
        detail(D, IT, st, tot, byk, [m.strip().lower() for m in (args.mostro or '').split(',') if m.strip()], args.tutto)
    else:
        summary(D, IT, st, tot, args)


def main():
    ap = argparse.ArgumentParser(description='Materiali mancanti per le armi di MH Tri, dal salvataggio Dolphin.',
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__.split('Esempi:')[1])
    ap.add_argument('--save', default=SAVE, help='file data00 del salvataggio')
    ap.add_argument('--slot', type=int, help='slot personaggio (0-2), di default quello in uso')
    ap.add_argument('--una-volta', dest='mode', action='store_const', const='once', default='coll',
                    help='conta ogni arma mancante una volta sola (il potenziamento consuma la precedente); '
                         'di default ogni arma mancante e\' una copia nuova, cosi\' tieni quelle che hai')
    ap.add_argument('--tipo', help='solo questi tipi, separati da virgola (spadone, spada lunga, spada e scudo, '
                                   'martello, lancia, ascia cangiante, base, canna, elsa, balestra)')
    ap.add_argument('--livelli', action='store_true', help='includi i livelli delle basi fino al massimo')
    ap.add_argument('--mostro', help='dettaglio dei materiali di questi mostri (virgola)')
    ap.add_argument('--tutto', action='store_true', help='dettaglio di tutti i materiali, anche generici e minerali')
    ap.add_argument('--armi', action='store_true', help='elenco delle armi possedute e mancanti')
    ap.add_argument('--pronte', action='store_true', help='armi mancanti che puoi fare adesso')
    ap.add_argument('--arma', help='percorso piu\' breve per l\'arma (nome inglese o italiano, anche parziale)')
    ap.add_argument('--mostro-solo', dest='metric', action='store_const', const='mon', default='all',
                    help='con --arma: minimizza solo i materiali di mostro')
    ap.add_argument('--lingua', choices=['it', 'en', 'fr', 'es', 'de'], default='it',
                    help='lingua dei nomi di gioco (quelle della versione PAL): it, en, fr, es, de')
    ap.add_argument('--watch', action='store_true', help='ristampa a ogni nuovo salvataggio (Ctrl+C per uscire)')
    args = ap.parse_args()
    global LANG
    LANG = args.lingua
    D, W, IT = load_data()
    if not os.path.exists(args.save):
        sys.exit(f'salvataggio non trovato: {args.save} (usa --save)')
    if not args.watch:
        run(args, D, W, IT); return
    last = None
    try:
        while True:
            m = os.stat(args.save).st_mtime
            if m != last:
                time.sleep(0.5 if last else 0)       # lascia finire la scrittura di Dolphin
                if TTY: print('\033[2J\033[H', end='')
                print(DIM(time.strftime('aggiornato %H:%M:%S')))
                try: run(args, D, W, IT)
                except SystemExit as e: print(e)
                last = m
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
