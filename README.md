# Armi di Monster Hunter Tri

Sito per pianificare le armi di **Monster Hunter Tri** (Wii, versione PAL RMHP08): quali materiali servono, di quale mostro e in quale rank, quali armi si comprano al negozio e qual è il percorso più breve per arrivare a un'arma.

**Sito:** https://sshikari-hue.github.io/MHTri-matscalculator/

- **Albero armi** (`docs/index.html`): le 378 armi del gioco divise per tipo. Spunti quelle che hai e vedi i materiali che mancano, per mostro, LR/HR e tipo d'arma, con il percorso più breve per ogni arma.
- **Fucina** (`docs/fucina.html`): il riepilogo dei materiali per mostro, senza spunte.

Lingue: italiano, inglese, spagnolo, francese e tedesco, con i nomi ufficiali della versione europea.

Le pagine sono statiche e autonome: dati, stili e codice sono dentro ciascun file HTML. Le spunte restano salvate nel browser di chi le usa.

## Da dove vengono i dati

I dati sono estratti dai file del disco PAL:

| Dati | File |
|---|---|
| Ricette di creazione e potenziamento | `lobby_data.rso` |
| Negozio della fucina | `main.dol` |
| Intagli, catture, rotture di parti | `em_data.rso` |
| Ricompense delle quest | `quest_data.rso` |
| Nomi nelle 5 lingue | `data00_*.bin`, `data11_*.bin` |

Le strutture sono state ricostruite con l'aiuto della decompilazione [InusualZ/mhtri-decomp](https://github.com/InusualZ/mhtri-decomp). Il repository non contiene file di gioco.

## Note

Licenza del codice: MIT (vedi `LICENSE`). Il sito è servito da GitHub Pages dalla cartella `docs/` del ramo `main`.

Progetto amatoriale, non affiliato a Capcom. Monster Hunter e i suoi nomi sono marchi e proprietà di Capcom. I nomi e i valori di gioco sono riportati a scopo di consultazione.
