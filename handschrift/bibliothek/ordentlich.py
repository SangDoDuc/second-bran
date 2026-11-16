"""„Ordentlich“-Modus für render_text.py (Sangs Wunsch 15.11.2026: gerade in einer Reihe, nicht kreuz und quer).

Jeder Buchstabe aus der Bibliothek wird auf feste Maße gebracht und exakt auf die Grundlinie gesetzt:
  x-Höhe 13 px, Oberlänge/Großbuchstaben/Ziffern 19 px, Unterlänge hängt unter der Linie.
Kein zufälliges Hoch/Runter mehr, keine ganzen Wortbilder (die hatten eigene Größen), gleiche Abstände.
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

XH, ASC, CAP = 13.0, 19.0, 19.0
XL = set("acemnorsuvwxzäöü")
AS = set("bdfhklß")
DE = set("gjpqy")


def _scale(a, f):
    im = Image.fromarray(a.astype(np.float32), "F")
    return np.asarray(im.resize((max(1, round(a.shape[1] * f)), max(1, round(a.shape[0] * f))), Image.BILINEAR))


def _body(a):
    """Zeilen/Spalten des Buchstabenkörpers (ohne Punkte, Umlautpunkte, kleine Reste)."""
    lab, n = ndi.label(a > 0.25, structure=np.ones((3, 3)))
    if n == 0:
        return None
    sizes = ndi.sum(a > 0.25, lab, range(1, n + 1))
    keep = [k + 1 for k, s in enumerate(sizes) if s >= 0.25 * sizes.max()]
    ys, xs = np.where(np.isin(lab, keep))
    return ys.min(), ys.max() + 1


def norm(ch, g):
    a = g["alpha"]
    base = -g["top"]                                # Grundlinie als Zeile in a
    b = _body(a)
    if b is None or not ch.isalnum():
        return dict(g)                              # Satzzeichen bleiben, wie Sang sie schreibt
    y0, y1 = b
    if ch in DE or ch in "ij":
        h, target = max(1.0, base - y0), XH * (1.0 if ch in DE else 1.0)
    elif ch in XL:
        h, target = y1 - y0, XH
    elif ch in AS:
        h, target = y1 - y0, ASC
    elif ch == "t":
        h, target = y1 - y0, ASC * 0.82
    else:                                            # Großbuchstaben, Ziffern
        h, target = y1 - y0, CAP
    f = min(max(target / max(h, 1), 0.55), 1.7)
    s = _scale(a, f)
    if ch in DE or ch in "ij":
        top = -(base - 0) * f                       # alte Grundlinie bleibt Grundlinie
        top = -(base * f)
    else:
        top = -(y1 * f)                             # Unterkante des Körpers genau auf die Linie
    return dict(g, alpha=s.astype(np.float32), top=float(top))


def apply(render_loesung_module):
    """Bibliothek im geladenen render_loesung-Modul auf ordentliche Maße umstellen."""
    G = render_loesung_module.G
    for ch in list(G):
        if len(ch) == 1:
            G[ch] = [norm(ch, g) for g in G[ch]]
    render_loesung_module.WORDS.clear()             # ganze Wortbilder aus: eigene, ungleiche Größen
    render_loesung_module.LGAP = 2
    render_loesung_module.SPACE = 12
    H = render_loesung_module.Hand

    def glyph(self, key):                           # ohne zufälliges Hoch/Runter
        g = self.pick(key)
        return [(g["alpha"], 0, g["top"])], g["alpha"].shape[1]
    H.glyph = glyph
