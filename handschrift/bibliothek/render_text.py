"""Stichpunkte in Sangs Handschrift (Bibliothek SP-k1) auf Karo-Seiten 1414 x 2000 px, mit Zeilenumbruch.

python3 render_text.py TEXTMODUL AUSGABEPRÄFIX
TEXTMODUL (im selben Ordner oder auf sys.path) definiert TITLE, LINES und optional HEADER_LEFT/HEADER_RIGHT = [(art, text), ...]:
  art "h"  Überschrift (unterstrichen), "b" Stichpunkt mit Strich, "+"/"−" Pro/Contra, ">" Folgerung mit Pfeil, "s" eingerückter Unterpunkt,
  "p" normale Zeile, "" Leerzeile.
Ergebnis: PRÄFIX_p1_alpha.npy, PRÄFIX_p2_alpha.npy … und Vorschau-PNGs; weiter mit ../werkzeug/kuli.py.
"""
import importlib
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, HERE)
from render_loesung import GRID, GRID0, H_PAGE, SPACE, W_PAGE, Hand, paste  # noqa: E402

X0, X_MAX = 50, 1360
BULLET_X, TEXT_X, SUB_X = 60, 95, 130
FIRST_LINE, LAST_LINE = 3, 51          # Rasterzeilen der Grundlinien


def words_of(h, text):
    return [(w, h.run(w)) for w in text.split(" ") if w]


def render(mod, seed=7):
    h = Hand(seed)
    pages, canvas, row = [], None, None

    def new_page():
        nonlocal canvas, row
        if canvas is not None:
            pages.append(canvas)
        canvas = np.zeros((H_PAGE, W_PAGE), np.float32)
        row = FIRST_LINE

    def line_y():
        return GRID0 + row * GRID

    new_page()
    if getattr(mod, "HEADER_LEFT", ""):                       # Kopfzeile wie in Sangs Präsentationen
        hp, _ = h.run(mod.HEADER_LEFT)
        paste(canvas, hp, X0, GRID0 + 1 * GRID)
    if getattr(mod, "HEADER_RIGHT", ""):
        hp, hw = h.run(mod.HEADER_RIGHT)
        paste(canvas, hp, X_MAX - hw, GRID0 + 1 * GRID)
    parts, w = h.run(mod.TITLE)
    paste(canvas, parts, X0, line_y())
    g = h.pick("FRACBAR")
    paste(canvas, [(h.stretch(g["alpha"], w + 12), 0, 7)], X0 - 4, line_y())
    row += 3
    for kind, text in mod.LINES:
        if kind == "":
            row += 1
            continue
        if row > LAST_LINE:
            new_page()
        if kind == "h":
            parts, w = h.run(text)
            paste(canvas, parts, X0, line_y())
            g = h.pick("FRACBAR")
            paste(canvas, [(h.stretch(g["alpha"], w + 6), 0, 6)], X0 - 2, line_y())
            row += 2
            continue
        x_start = {"b": TEXT_X, "+": TEXT_X, "−": TEXT_X, ">": TEXT_X + 18, "s": SUB_X + 30, "p": X0}[kind]
        if kind in "b+−>" or kind == "s":
            mark = {"b": "-", "+": "+", "−": "−", "s": "-", ">": "→"}[kind]
            mp, _ = h.run(mark)
            paste(canvas, mp, BULLET_X if kind != "s" else SUB_X, line_y())
        x = x_start
        for word, (parts, w) in words_of(h, text):
            if x + w > X_MAX and x > x_start:
                row += 2
                if row > LAST_LINE:
                    new_page()
                x = x_start
            paste(canvas, parts, x, line_y())
            x += w + SPACE + 3
        row += 2
    pages.append(canvas)
    return pages


if __name__ == "__main__":
    mod = importlib.import_module(sys.argv[1])
    out = sys.argv[2]
    pages = render(mod)
    for k, c in enumerate(pages, 1):
        np.save(f"{out}_p{k}_alpha.npy", c)
        bg = np.full((H_PAGE, W_PAGE, 3), 255, np.uint8)
        for i in range(0, (W_PAGE - GRID0) // GRID + 1):
            bg[:, GRID0 + i * GRID] = 205
        for i in range(0, (H_PAGE - GRID0) // GRID + 1):
            bg[GRID0 + i * GRID, :] = 205
        ink = np.clip(c, 0, 1)[..., None]
        Image.fromarray((bg * (1 - ink) + np.array([18, 18, 23]) * ink).astype(np.uint8)).save(f"{out}_p{k}.png")
    print(len(pages), "Seiten")
