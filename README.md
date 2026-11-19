# Armi di Monster Hunter Tri

Strumenti per pianificare le armi di **Monster Hunter Tri** (Wii, versione PAL RMHP08): quali materiali servono, di quale mostro e in quale rank, quali armi si comprano al negozio e qual è il percorso più breve per arrivare a un'arma.

**Sito:** https://sshikari-hue.github.io/MHTri-matscalculator/

- **Albero armi** (`docs/index.html`): le 378 armi del gioco divise per tipo. Spunti quelle che hai e vedi i materiali che mancano, per mostro, LR/HR e tipo d'arma, con il percorso più breve per ogni arma.
- **Fucina** (`docs/fucina.html`): il riepilogo dei materiali per mostro, senza spunte.
- **`materiali.py`**: legge il tuo salvataggio Dolphin e calcola cosa ti manca, con modalità `--watch`, `--pronte` e `--arma`.

Lingue: italiano, inglese, spagnolo, francese e tedesco, con i nomi ufficiali della versione europea.

## Script sul salvataggio

Serve Python 3, senza dipendenze esterne.

```
./materiali.py                      riepilogo per mostro (LR/HR): serve, hai, manca
./materiali.py --watch              lo ristampa a ogni salvataggio
./materiali.py --pronte             armi che puoi fare adesso
./materiali.py --arma "doris"       percorso più breve per un'arma
./materiali.py --tipo martello,lancia --mostro rathalos
./materiali.py --lingua en          nomi in en, it, fr, es, de
./materiali.py --help
```

Di default cerca il salvataggio di Dolphin installato come Flatpak su Linux. Per altri percorsi usa `--save /percorso/data00`, il file in `Wii/title/00010000/524d4850/data/nocopy/`.

## Da dove vengono i dati

`tree.json` è estratto dai file del disco PAL:

| Dati | File |
|---|---|
| Ricette di creazione e potenziamento | `lobby_data.rso` (`buki_sei_tbl*`, `kakou_tbl*`) |
| Negozio della fucina | `main.dol` |
| Intagli, catture, rotture di parti | `em_data.rso` |
| Ricompense delle quest | `quest_data.rso` (`rem_item_tbl_em_*`) |
| Nomi nelle 5 lingue | `data00_*.bin`, `data11_*.bin` |

Le strutture sono state ricostruite con l'aiuto della decompilazione [InusualZ/mhtri-decomp](https://github.com/InusualZ/mhtri-decomp).

Per rigenerare i dati serve una copia del gioco estratta con `dolphin-tool extract`. Il repository non contiene file di gioco.

```
cd src
MHTRI_GAME=/percorso/estrazione python3 export_tree.py ../tree.json
cd .. && python3 build.py          # rigenera docs/ (sito) e web/*-tri.html
```

## Pubblicazione

Licenza del codice: MIT (vedi `LICENSE`). Il sito è servito da GitHub Pages dalla cartella `docs/` del ramo `main`. Dopo una modifica: `python3 build.py`, poi commit e push.

## Note

Progetto amatoriale, non affiliato a Capcom. Monster Hunter e i suoi nomi sono marchi e proprietà di Capcom. I nomi e i valori di gioco sono riportati a scopo di consultazione.
