"""Percorso dei file di gioco estratti (dolphin-tool extract del disco PAL RMHP08).
Imposta MHTRI_GAME o crea un collegamento `game` nella cartella da cui lanci gli script."""
import os
GAME = os.environ.get('MHTRI_GAME', 'game')
