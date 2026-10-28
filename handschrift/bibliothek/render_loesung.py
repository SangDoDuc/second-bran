"""Lösungsweg in Sangs Handschrift (Bibliothek aus Schriftprobe SP-k1) auf Karo-Seiten 1414 x 2000 px.

Auszeichnung in den Zeilen:
  ^AC / ^n   Vektorpfeil       ⟨a;b;c⟩   Spaltenvektor      √{...}   Wurzel mit Strich
  F{a}{b}    Bruch             ½         Bruch 1/2 (Probe)  ‖        Betragsstrich (hoch)
  ² ⁻ ˣ      hochgestellt      ₁ ₂ ₃     tiefgestellt       Leerzeichen = Abstand
"""
import os
import pickle
import random
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
LIB = pickle.load(open(HERE + "library.pkl", "rb"))
G, WORDS = LIB["glyphs"], LIB["words"]
W_PAGE, H_PAGE = 1414, 2000
GRID0, GRID = 37, 38
SPACE, GAP, LGAP = 12, 3, 1
VEC_BASE = [-38, -4, 22]          # Grundlinien der 3 Einträge (gemessen in Sangs Spaltenvektor)
ROOT_HOOK = 22                    # Breite des Wurzelhakens in der Probe


class Hand:
    def __init__(self, seed=3):
        self.rng = random.Random(seed)
        self.last = {}

    def pick(self, key):
        vs = G[key]
        if len(vs) == 1:
            return vs[0]
        k = self.rng.randrange(len(vs))
        if k == self.last.get(key):
            k = (k + 1) % len(vs)
        self.last[key] = k
        return vs[k]

    # ------------------------------------------------------------------ Bausteine -> [(alpha, dx, top)], Breite
    def glyph(self, key):
        g = self.pick(key)
        return [(g["alpha"], 0, g["top"] + self.rng.choice((-1, 0, 0, 0, 1)))], g["alpha"].shape[1]

    def word(self, w):
        if w in WORDS:
            g = WORDS[w]
            return [(g["alpha"], 0, g["top"])], g["alpha"].shape[1]
        for k in sorted(WORDS, key=len, reverse=True):          # Endung als ganzes Wort (z. B. "o"+"der")
            if len(k) >= 3 and w.endswith(k) and len(w) > len(k):
                a, wa = self.letters(w[:-len(k)])
                b, wb = self.word(k)
                return a + [(al, dx + wa + LGAP + 1, t) for al, dx, t in b], wa + LGAP + 1 + wb
        return self.letters(w)

    def letters(self, w):
        out, x = [], 0
        for i, ch in enumerate(w):
            parts, wd = self.glyph(ch)
            out += [(a, dx + x, t) for a, dx, t in parts]
            x += wd + (LGAP if i + 1 < len(w) else 0)
        return out, x

    def stretch(self, a, new_w):
        im = Image.fromarray(a.astype(np.float32), "F").resize((max(2, int(new_w)), a.shape[0]), Image.BILINEAR)
        return np.asarray(im)

    def scale(self, a, f):
        im = Image.fromarray(a.astype(np.float32), "F")
        return np.asarray(im.resize((max(1, int(a.shape[1] * f)), max(1, int(a.shape[0] * f))), Image.BILINEAR))

    def arrow(self, inner):
        parts, w = self.run(inner)
        top = min(t for _, _, t in parts)
        g = self.pick("ARROW")
        a = self.stretch(g["alpha"], w + 4)
        return parts + [(a, -1, top - 3 - a.shape[0])], w

    def vec(self, entries):
        rows = [self.run(e) for e in entries]
        wmax = max(w for _, w in rows)
        L, R = self.pick("BIGPAREN_L"), self.pick("BIGPAREN_R")
        out = [(L["alpha"], 0, L["top"])]
        x = L["alpha"].shape[1] + 4
        for (parts, w), base in zip(rows, VEC_BASE):
            off = x + (wmax - w) / 2
            out += [(a, dx + off, t + base) for a, dx, t in parts]
        x += wmax + 4
        out.append((R["alpha"], x, R["top"]))
        return out, x + R["alpha"].shape[1]

    def root(self, inner):
        parts, w = self.run(inner)
        g = self.pick("ROOT")
        a = g["alpha"]
        hook, bar = a[:, :ROOT_HOOK], a[:, ROOT_HOOK:]
        bar = self.stretch(bar, w + 8)
        x0 = ROOT_HOOK + 3
        top = min(t for _, _, t in parts)
        lift = min(0, top - 4 - g["top"])                       # Wurzel höher, falls Radikand hoch reicht
        return ([(hook, 0, g["top"] + lift), (bar, ROOT_HOOK, g["top"] + lift)]
                + [(al, dx + x0, t) for al, dx, t in parts]), ROOT_HOOK + bar.shape[1]

    def frac(self, num, den):
        n, wn = self.run(num)
        d, wd = self.run(den)
        w = max(wn, wd) + 8
        g = self.pick("FRACBAR")
        bar = self.stretch(g["alpha"], w)
        bar_top, bar_bot = g["top"], g["top"] + bar.shape[0]
        n_bot = max(t + a.shape[0] for a, _, t in n)
        d_top = min(t for _, _, t in d)
        out = [(bar, 0, bar_top)]
        out += [(a, dx + (w - wn) / 2, t + (bar_top - 3 - n_bot)) for a, dx, t in n]
        out += [(a, dx + (w - wd) / 2, t + (bar_bot + 3 - d_top)) for a, dx, t in d]
        return out, w

    # ------------------------------------------------------------------ Zeile
    def run(self, s):
        out, x, i = [], 0, 0
        prev_space = True
        while i < len(s):
            ch = s[i]
            if ch == " ":
                x += SPACE
                i += 1
                prev_space = True
                continue
            if not prev_space:
                x += GAP
            prev_space = False
            if ch == "^":
                j = i + 1
                if s[j].isupper():
                    while j < len(s) and s[j].isupper():
                        j += 1
                else:
                    j += 1
                parts, w = self.arrow(s[i + 1:j])
                i = j
            elif ch == "⟨":
                j = s.index("⟩", i)
                parts, w = self.vec(s[i + 1:j].split(";"))
                i = j + 1
            elif s.startswith("√{", i):
                j = self._close(s, i + 1)
                parts, w = self.root(s[i + 2:j])
                i = j + 1
            elif s.startswith("F{", i):
                j = self._close(s, i + 1)
                k = self._close(s, j + 1)
                parts, w = self.frac(s[i + 2:j], s[j + 2:k])
                i = k + 1
            elif ch.isalpha() and ch not in "ˣ":
                j = i
                while j < len(s) and s[j].isalpha() and s[j] not in "ˣ":
                    j += 1
                parts, w = self.word(s[i:j])
                i = j
            elif ch == "‖":
                parts, w = self.glyph("ABS")
                i += 1
            elif ch == "–":
                parts, w = self.glyph("-")
                i += 1
            elif ch in "₁₂₃²⁻ˣ":
                x -= GAP - 1
                parts, w = self.glyph(ch)
                i += 1
            else:
                parts, w = self.glyph(ch)
                i += 1
            out += [(a, dx + x, t) for a, dx, t in parts]
            x += w
        return out, x

    @staticmethod
    def _close(s, i):
        depth = 0
        for j in range(i, len(s)):
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    return j
        raise ValueError(s)


def paste(canvas, parts, x0, yb):
    for a, dx, top in parts:
        x, y = int(round(x0 + dx)), int(round(yb + top))
        h, w = a.shape
        ys, xs = max(0, -y), max(0, -x)
        ye, xe = min(h, H_PAGE - y), min(w, W_PAGE - x)
        if ye > ys and xe > xs:
            sub = canvas[y + ys:y + ye, x + xs:x + xe]
            np.maximum(sub, a[ys:ye, xs:xe], out=sub)


TITLE = "IQB 2024 – Oktaeder im Würfel"
LINES = [
    ("a)", "AC Diagonale → A und C gegenüber → ‖^AC‖ = a", "n"),
    ("", "^AC = ⟨−4;−8;8⟩", "v"),
    ("", "‖^AC‖ = √{(−4)² + (−8)² + 8²} = √{144} = 12", "n"),
    ("", "a = 12", "n"),
    ("b)", "^OM = ½ · (^OA + ^OC) = ½ · ⟨1−3;2−6;1+9⟩ = ⟨−1;−2;5⟩", "v"),
    ("", "M(−1|−2|5)", "n"),
    ("", "H: 2x₁ + x₂ + 2x₃ = 6 → ^n = ⟨2;1;2⟩", "v"),
    ("", "‖^n‖ = √{2² + 1² + 2²} = √{9} = 3", "n"),
    ("", "‖^ME‖ = F{a}{2} = 6 → 2 · ^n", "f"),
    ("", "^OE = ^OM + 2 · ^n = ⟨−1;−2;5⟩ + ⟨4;2;4⟩ = ⟨3;0;9⟩", "v"),
    ("", "E(3|0|9)   oder   F(−5|−4|1)", "n"),
    ("", "Probe: (2 · 3 + 0 + 2 · 9 − 6) : 3 = 6", "n"),
]


def render(seed=3):
    h = Hand(seed)
    canvas = np.zeros((H_PAGE, W_PAGE), np.float32)
    X0, XC = 40, 112
    yb = GRID0 + 3 * GRID
    parts, w = h.run(TITLE)
    paste(canvas, parts, X0, yb)
    g = h.pick("FRACBAR")
    paste(canvas, [(h.stretch(g["alpha"], w + 12), 0, 7)], X0 - 4, yb)
    yb = GRID0 + 6 * GRID
    widths = []
    prev = None
    for label, text, kind in LINES:
        if prev is not None:
            step = 2 * GRID
            if kind in ("v", "f") or prev in ("v", "f"):
                step += GRID
            if label and prev is not None:
                step += GRID
            yb += step
        if label:
            p, _ = h.run(label)
            paste(canvas, p, X0, yb)
        p, w = h.run(text)
        widths.append(w)
        paste(canvas, p, XC, yb)
        prev = kind
    return canvas, widths, yb


if __name__ == "__main__":
    canvas, widths, last = render(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    np.save(HERE + "loes_p1_alpha.npy", canvas)
    bg = np.full((H_PAGE, W_PAGE, 3), 255, np.uint8)
    for k in range(0, (W_PAGE - GRID0) // GRID + 1):
        bg[:, GRID0 + k * GRID] = 205
    for k in range(0, (H_PAGE - GRID0) // GRID + 1):
        bg[GRID0 + k * GRID, :] = 205
    ink = np.clip(canvas, 0, 1)[..., None]
    out = (bg * (1 - ink) + np.array([18, 18, 23]) * ink).astype(np.uint8)
    Image.fromarray(out).save(HERE + "loes_p1.png")
    print("Breiten:", [int(w) for w in widths], "max erlaubt", W_PAGE - 112 - 30, "| letzte Grundlinie", last)
