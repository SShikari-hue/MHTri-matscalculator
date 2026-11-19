# Armi, armature e gioielli di Monster Hunter Tri

Sito per pianificare armi, armature e gioielli di **Monster Hunter Tri** (Wii, versione PAL RMHP08): quali materiali servono, di quale mostro e in quale rank, quali armi si comprano al negozio e qual è il percorso più breve per arrivare a un'arma.

**Sito:** https://sshikari-hue.github.io/MHTri-matscalculator/

- **Albero armi** (`docs/index.html`): le 378 armi del gioco divise per tipo. Spunti quelle che hai e vedi i materiali che mancano, per mostro, LR/HR e tipo d'arma, con il percorso più breve per ogni arma.
- **Riepilogo** (`docs/fucina.html`): per ogni mostro, i materiali che servono per tutte le armi, le armature e i gioielli. Le colonne sono Armi, Armature, Gioielli e Totale, ciascuna divisa in LR, HR e LR+HR. Il dettaglio è materiale per materiale, senza spunte.
- **Armature** (`docs/armature.html`): i 144 set di armatura (628 pezzi), divisi tra spadaccino e artigliere e tra LR e HR. Spunti i pezzi che hai e vedi i materiali mancanti per mostro e per parte. Per ogni set mostra difesa, spazi, rarità e abilità.

- **Gioielli** (`docs/gioielli.html`): i 131 gioielli con spazi, abilità e ricetta. Spunti quelli che hai e vedi i materiali mancanti per mostro e rank.
- **Il mio set** (`docs/mio-set.html`): scegli liberamente armi e pezzi d'armatura e ottieni il totale dei materiali da raccogliere, per mostro e rank. Le armi seguono il percorso più breve. Se vuoi, parte dalle armi che hai spuntato nell'albero e salta i pezzi spuntati in Armature. Per i pezzi d'armatura scelti mostra difesa, spazi e somma delle abilità. Si possono aggiungere anche gioielli, con la quantità.
- **Ricerca abilità** (`docs/abilita.html`, dentro Il mio set): scegli le abilità da attivare e trova i set d'armatura possibili, con spazi dell'arma, talismano e gioielli, sullo stile di Athena's ASS. I risultati, al massimo 100 per ordinamento, si ordinano per meno materiali, per drop più facili (stima dalle probabilità di intaglio, cattura, rottura e ricompensa) o per difesa, e si aggiungono a Il mio set con un tocco.

Lingue: italiano, inglese, spagnolo, francese e tedesco, con i nomi ufficiali della versione europea.

Le pagine sono statiche e autonome: dati, stili e codice sono dentro ciascun file HTML. Le spunte restano salvate nel browser di chi le usa.

## Da dove vengono i dati

I dati sono estratti dai file del disco PAL:

| Dati | File |
|---|---|
| Ricette di creazione e potenziamento | `lobby_data.rso` |
| Pezzi d'armatura: difesa, spazi, abilità, serie | `com_data.rso` |
| Gioielli (ricette, spazi, abilità) e attivazione delle abilità | `lobby_data.rso`, `main.dol` |
| Negozio della fucina (armi e armature) | `main.dol` |
| Intagli, catture, rotture di parti | `em_data.rso` |
| Ricompense delle quest | `quest_data.rso` |
| Nomi e termini nelle 5 lingue | `data00_*.bin`, `data10_*.bin`, `data11_*.bin` |

Le strutture sono state ricostruite con l'aiuto della decompilazione [InusualZ/mhtri-decomp](https://github.com/InusualZ/mhtri-decomp). Il repository non contiene file di gioco.

## Note

Licenza del codice: MIT (vedi `LICENSE`). Il sito è servito da GitHub Pages dalla cartella `docs/` del ramo `main`.

Progetto amatoriale, non affiliato a Capcom. Monster Hunter e i suoi nomi sono marchi e proprietà di Capcom. I nomi e i valori di gioco sono riportati a scopo di consultazione.
