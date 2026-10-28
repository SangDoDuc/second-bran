"""IQB 2026 Stochastik 2.2 (Zahlencodes) – Lösungsweg in Sangs Handschrift, 1 Seite Karo 1414 x 2000 px.

Baut auf render_loesung.py (Hand, paste) auf. Zusätzliche Auszeichnung:
  T̄        T mit Überstrich (Gegenereignis)
  _{A}     tiefgestellt (P_{A}(B))
Weiter: python3 ../werkzeug/kuli.py --out AUSGABE --title "..." stoch_p1_alpha.npy
"""
import os
import random
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, HERE)
from render_loesung import GAP, GRID, GRID0, H_PAGE, W_PAGE, Hand, paste  # noqa: E402


class Hand2(Hand):
    def run(self, s):
        out, x = [], 0
        toks = [t for t in re.split(r"(T̄|_\{[^}]*\})", s) if t]
        prev_space = True
        for tok in toks:
            if tok == "T̄":
                parts, w = self.glyph("T")
                top = min(t for _, _, t in parts)
                bar = self.stretch(self.pick("−")["alpha"], w + 2)
                parts = parts + [(bar, -1, top - 5 - bar.shape[0])]
                lead = not prev_space
                trail = False
            elif tok.startswith("_{"):
                p, w = Hand.run(self, tok[2:-1])
                f = 0.62
                parts = [(self.scale(a, f), dx * f, t * f + 8) for a, dx, t in p]
                w = w * f
                lead = False
                x -= 2
                trail = False
            else:
                parts, w = Hand.run(self, tok)
                lead = not prev_space and not tok.startswith(" ")
                trail = tok.endswith(" ")
            if lead:
                x += GAP
            out += [(a, dx + x, t) for a, dx, t in parts]
            x += w
            prev_space = trail
        return out, x


def hand_line(canvas, pts, rng, width=3.2):
    """Leicht unruhige Linie (Skizze) in den Alpha-Canvas zeichnen."""
    im = Image.new("F", (W_PAGE, H_PAGE), 0.0)
    d = ImageDraw.Draw(im)
    (x0, y0), (x1, y1) = pts
    n = max(2, int(np.hypot(x1 - x0, y1 - y0) / 18))
    poly = []
    for i in range(n + 1):
        t = i / n
        wob = rng.uniform(-0.9, 0.9) if 0 < i < n else 0
        poly.append((x0 + (x1 - x0) * t + wob, y0 + (y1 - y0) * t + wob))
    d.line(poly, fill=1.0, width=int(width), joint="curve")
    np.maximum(canvas, np.asarray(im), out=canvas)


TITLE = "IQB 2026 – Stochastik 2.2: Zahlencodes"
# (Rasterzeile der Grundlinie, Label, Text)
LINES = [
    (6, "", "T: Code enthält Folge   →   P(T) = p"),
    (8, "", "T̄: nicht   →   P(T̄) = 1 − p"),
    (10, "", "2 Codes, unabhängig   →   Baum:"),
    (19, "a)", "p = 0,1"),
    (21, "", "P(genau einer) = 0,1 · 0,9 + 0,9 · 0,1"),
    (23, "", "= 2 · 0,1 · 0,9 = 0,18"),
    (26, "b)", "A: mind. einer enthält Folge   (Bedingung)"),
    (28, "", "B: nicht beide   (gesucht)"),
    (30, "", "P(A) = 1 − P(keiner) = 1 − (1−p)²"),
    (32, "", "A und B: genau einer"),
    (34, "", "P(A und B) = p · (1−p) + (1−p) · p"),
    (37, "", "P_{A}(B) = F{p · (1−p) + (1−p) · p}{1 − (1−p)²}"),
    (40, "", "Probe (p = 0,1): 0,18 / 0,19 = 0,947 (gerundet)"),
]


def tree(canvas, h, rng, x0, yc):
    """Baum mit 2 Stufen: Wurzel (x0, yc), Stufe 1 bei x0+120, Stufe 2 bei x0+250, Pfadprodukte rechts."""
    L1, L2, DY1, DY2 = 120, 250, 58, 27
    n1 = [(x0 + L1, yc - DY1), (x0 + L1, yc + DY1)]
    for (x1, y1), top in zip(n1, (True, False)):
        hand_line(canvas, ((x0, yc), (x1 - 6, y1)), rng)
        lab, w = h.run("p" if top else "1−p")
        mx, my = (x0 + x1) / 2, (yc + y1) / 2
        paste(canvas, lab, mx - w / 2 - 14, my - (16 if top else -26))
        node, wn = h.run("T" if top else "T̄")
        paste(canvas, node, x1 + 2, y1 + 8)
        for (x2, y2), top2 in (((x1 + L2 - L1, y1 - DY2), True), ((x1 + L2 - L1, y1 + DY2), False)):
            hand_line(canvas, ((x1 + wn + 10, y1), (x2 - 6, y2)), rng)
            lab2, w2 = h.run("p" if top2 else "1−p")
            paste(canvas, lab2, (x1 + x2) / 2 + 6 - w2 / 2, y2 - (14 if top2 else -24))
            node2, wn2 = h.run("T" if top2 else "T̄")
            paste(canvas, node2, x2 + 2, y2 + 8)
            prod = {(True, True): "p²", (True, False): "p · (1−p)", (False, True): "(1−p) · p",
                    (False, False): "(1−p)²"}[(top, top2)]
            pp, _ = h.run(prod)
            paste(canvas, pp, x2 + wn2 + 40, y2 + 8)


def render(seed=5):
    h = Hand2(seed)
    rng = random.Random(seed + 100)
    canvas = np.zeros((H_PAGE, W_PAGE), np.float32)
    X0, XC = 40, 112
    yb = GRID0 + 3 * GRID
    parts, w = h.run(TITLE)
    paste(canvas, parts, X0, yb)
    g = h.pick("FRACBAR")
    paste(canvas, [(h.stretch(g["alpha"], w + 12), 0, 7)], X0 - 4, yb)
    widths = []
    for row, label, text in LINES:
        yb = GRID0 + row * GRID
        if label:
            p, _ = h.run(label)
            paste(canvas, p, X0, yb)
        p, w = h.run(text)
        widths.append(int(w))
        paste(canvas, p, XC, yb)
    tree(canvas, h, rng, XC + 20, GRID0 + 14 * GRID)
    return canvas, widths


if __name__ == "__main__":
    canvas, widths = render(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    np.save(HERE + "stoch_p1_alpha.npy", canvas)
    bg = np.full((H_PAGE, W_PAGE, 3), 255, np.uint8)
    for k in range(0, (W_PAGE - GRID0) // GRID + 1):
        bg[:, GRID0 + k * GRID] = 205
    for k in range(0, (H_PAGE - GRID0) // GRID + 1):
        bg[GRID0 + k * GRID, :] = 205
    ink = np.clip(canvas, 0, 1)[..., None]
    out = (bg * (1 - ink) + np.array([18, 18, 23]) * ink).astype(np.uint8)
    Image.fromarray(out).save(HERE + "stoch_p1.png")
    print("Breiten:", widths, "max erlaubt", W_PAGE - 112 - 30)
