#!/usr/bin/env python3
"""Costruisce le pagine da web/*-app.html + web/style.css + web/i18n.js + tree.json.

  docs/index.html, docs/fucina.html   sito statico completo (GitHub Pages, cartella /docs)
  web/albero-tri.html, web/fucina-tri.html   versioni per gli artefatti claude.ai (senza <html>/<head>)

Variabili facoltative: REPO_URL (link al codice nel piè di pagina),
ALBERO_URL / FUCINA_URL (link tra le due pagine nelle versioni artefatto).
"""
import os
H = os.path.dirname(os.path.abspath(__file__))
w = lambda p: os.path.join(H, 'web', p)
data = open(os.path.join(H, 'tree.json'), encoding='utf-8').read().replace('</', '<\\/')
css = open(w('style.css'), encoding='utf-8').read()
i18n = open(w('i18n.js'), encoding='utf-8').read()
REPO = os.environ.get('REPO_URL', 'https://github.com/SShikari-hue/MHTri-matscalculator')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700'
         '&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">')
# il riquadro degli artefatti aggiunge questo reset da solo; il sito statico deve averlo
RESET = ('html{color-scheme:light}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'body{margin:0;font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}img{max-width:100%}'
         '[hidden]{display:none!important}a{color:var(--accent)}')
PAGES = (('albero-app.html', 'albero-tri.html', 'index.html', 'Albero armi di Tri'),
         ('fucina-app.html', 'fucina-tri.html', 'fucina.html', 'Fucina di Tri'))

def body(app, links):
    b = open(w(app), encoding='utf-8').read().replace('__DATA__', data).replace('__I18N__', i18n)
    for k, v in links.items():
        b = b.replace(k, v)
    src = f'\n    <p><a href="{REPO}" data-t="source"></a></p>' if REPO else ''
    return b.replace('__SOURCE__', src)

os.makedirs(os.path.join(H, 'docs'), exist_ok=True)
for app, art, site, title in PAGES:
    # versione artefatto
    links = {'__ALBERO_URL__': os.environ.get('ALBERO_URL', 'https://claude.ai/artifact/2yyTX5gind4y3qoknvPbRB'),
             '__FUCINA_URL__': os.environ.get('FUCINA_URL', 'https://claude.ai/artifact/SXPgvUPWYQnV9ot4NvbUHZ')}
    out = (f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n'
           f'<style>\n{css}\n</style>\n' + body(app, links))
    open(w(art), 'w', encoding='utf-8').write(out)
    # sito statico
    links = {'__ALBERO_URL__': 'index.html', '__FUCINA_URL__': 'fucina.html'}
    out = ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           f'<title>{title}</title>\n<meta name="description" content="Monster Hunter Tri: armi, materiali per mostro e rank, percorso più breve. Nomi ufficiali PAL in 5 lingue.">\n'
           f'{FONTS}\n<style>\n{RESET}\n{css}\n</style>\n</head>\n<body>\n' + body(app, links) + '\n</body>\n</html>\n')
    open(os.path.join(H, 'docs', site), 'w', encoding='utf-8').write(out)
    print(site, os.path.getsize(os.path.join(H, 'docs', site)), '+', art)
open(os.path.join(H, 'docs', '.nojekyll'), 'w').close()
