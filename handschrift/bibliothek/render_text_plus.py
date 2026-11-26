"""render_text.py mit Ergänzungen (Stand 26.11.2026):
- Ä/Ö/Ü aus Großbuchstabe + zwei Punkten zusammengesetzt (fehlen in der Schriftprobe)
- Apostroph ' und ’ aus dem Komma, hochgesetzt
- „Z. 12“ / „l. 12“ werden nicht getrennt (geschütztes Leerzeichen, nicht in Überschriften)
- prüft vor dem Rendern, ob alle Zeichen vorhanden sind

python3 render_text_plus.py TEXTMODUL AUSGABEPRÄFIX   (TEXTMODUL liegt in ../texte/), danach ../werkzeug/kuli.py
"""
import importlib
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path[:0] = [HERE, HERE + "../texte"]
import render_text as RT  # noqa: E402  (wendet den Ordentlich-Modus an)
import render_loesung as R  # noqa: E402

G = R.LIB["glyphs"]
NB = " "


def _dot():
    d = G["."][0]["alpha"]
    h, w = d.shape
    im = Image.fromarray((d * 255).astype(np.uint8)).resize((max(2, int(w * .7)), max(2, int(h * .7))), Image.BICUBIC)
    return np.asarray(im).astype(np.float32) / 255


def _umlaut(g):
    a, d = g["alpha"], _dot()
    dh, dw = d.shape
    gap = 2
    W = max(a.shape[1], 2 * dw + 4)
    out = np.zeros((a.shape[0] + dh + gap, W), np.float32)
    out[dh + gap:, :a.shape[1]] = a
    cx = a.shape[1] / 2
    for x0 in (int(cx - dw - 1), int(cx + 1)):
        x0 = max(0, min(W - dw, x0))
        out[:dh, x0:x0 + dw] = np.maximum(out[:dh, x0:x0 + dw], d)
    return dict(g, alpha=out, top=g["top"] - dh - gap)


def extend():
    for big, u in (("A", "Ä"), ("O", "Ö"), ("U", "Ü")):
        if u not in G:
            G[u] = [_umlaut(g) for g in G[big]]
    for ap in ("'", "’"):
        if ap not in G:
            G[ap] = [dict(g, top=-19.0) for g in G[","]]


def missing(h, text):
    bad = set()
    for c in set(text) - {" ", NB}:
        try:
            parts, w = h.run(c)
            if not parts or w <= 0:
                bad.add(c)
        except Exception:
            bad.add(c)
    return sorted(bad)


def main(modname, out):
    extend()
    mod = importlib.import_module(modname)
    mod.LINES = [(k, t if k == "h" else re.sub(r"\b([ZzLl]\.) ", r"\1" + NB, t)) for k, t in mod.LINES]
    RT.words_of = lambda h, text: [(w, h.run(w.replace(NB, " "))) for w in text.split(" ") if w]
    text = "".join([mod.TITLE, getattr(mod, "HEADER_LEFT", ""), getattr(mod, "HEADER_RIGHT", "")] + [t for _, t in mod.LINES])
    bad = missing(R.Hand(7), text)
    if bad:
        sys.exit(f"fehlende Zeichen: {bad}")
    pages = RT.render(mod)
    for k, c in enumerate(pages, 1):
        np.save(f"{out}_p{k}_alpha.npy", c)
        bg = np.full((R.H_PAGE, R.W_PAGE, 3), 255, np.uint8)
        for i in range(0, (R.W_PAGE - R.GRID0) // R.GRID + 1):
            bg[:, R.GRID0 + i * R.GRID] = 205
        for i in range(0, (R.H_PAGE - R.GRID0) // R.GRID + 1):
            bg[R.GRID0 + i * R.GRID, :] = 205
        ink = np.clip(c, 0, 1)[..., None]
        Image.fromarray((bg * (1 - ink) + np.array([18, 18, 23]) * ink).astype(np.uint8)).save(f"{out}_p{k}.png")
    print(len(pages), "Seiten")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
