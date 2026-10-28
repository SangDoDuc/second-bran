"""Text in Sangs Handschrift aus einzelnen, sauber auf die Grundlinie gesetzten Buchstaben (font.py).

Seite 1414 x 2000 px, Karo 38 px, Schreiblinie alle 2 Kästchen. Abstände eng (Buchstaben 1 px, Wörter ~15 px).
python3 render_font.py TEXTMODUL PRÄFIX   (TEXTMODUL wie ek_text: HEADER_LEFT/RIGHT, TITLE, BLOCKS)
"""
import importlib
import pickle
import random
import sys

import numpy as np
from PIL import Image

SP = "/tmp/claude-0/-home-user-second-bran/77087009-95da-55ff-8987-fa95a510b3dd/scratchpad/"
sys.path[:0] = [SP + "eng"]
from font import CAP, XH, _scale  # noqa: E402

C = pickle.load(open(SP + "eng/font_candidates.pkl", "rb"))
OLDLIB = pickle.load(open(SP + "hw/lib2.pkl", "rb"))
W_PAGE, H_PAGE, GRID0, GRID = 1414, 2000, 37, 38
LINE = 2 * GRID
X0, X_MAX = 40, 1372
FIRST_BODY, FIRST_NEXT, LAST = 265, 113, 1937
INDENT = 34
LGAP, WGAP = 1, 15

PICK = {  # Sheet-Indizes (alt zuerst, dann neu) – nach der Kuli-Umwandlung geprüft am 28.10.2026 (lesbar)
    "a": [71, 6, 58, 20, 21, 22, 30], "b": [10, 5, 1, 8, 7], "c": [20, 21, 1, 8, 28], "d": [7, 19, 18, 26],
    "e": [27, 43, 114, 74, 31, 2], "f": [10, 15, 18, 12], "g": [12, 10, 11, 5], "h": [33, 6],
    "i": [62, 30, 34, 23, 54, 11], "k": [0], "l": [1, 35, 3, 23], "m": [8, 15], "n": [15, 36, 18, 20],
    "o": [21, 13, 24, 59, 18], "p": [9, 1, 7, 11], "q": [2, 1], "r": [2, 32, 6, 50, 62], "s": [5, 71, 19, 35, 3],
    "t": [71, 52, 1, 49], "u": [1, 21, 14, 25], "v": [2], "w": [6, 11, 10, 1], "x": [4, 7, 6, 5],
    "y": [13, 3, 5, 12],
}


def _cand(ch, i):
    old = C["old"].get(ch, [])
    return old[i] if i < len(old) else C["new"][ch][i - len(old)]


def _from_cap(ch):
    """kleines v/z = Großbuchstabe V/Z auf x-Höhe (Druckschrift-Form)"""
    out = []
    for g in C["new"][ch.upper()]:
        a = _scale(g["alpha"], XH / g["alpha"].shape[0])
        out.append({"alpha": a, "top": -a.shape[0]})
    return out


def _old_punct(kind):
    out = []
    for p in OLDLIB["punct"]:
        if p["kind"] != kind:
            continue
        a = p["alpha"]
        ys, xs = np.where(a > 0.12)
        if not len(ys) or (kind == "." and (a > 0.3).sum() > 14):
            continue
        g = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        out.append({"alpha": g.astype(np.float32), "top": float(ys.min() - 53)})
    return out


def _dot(r):
    """runder, kräftiger Punkt (die Punkte der alten Probe sind so klein, dass sie beim Umwandeln verschwinden)"""
    n = int(2 * r + 3)
    yy, xx = np.mgrid[0:n, 0:n]
    c = (n - 1) / 2
    a = np.clip(r + 0.5 - np.hypot(yy - c, xx - c), 0, 1).astype(np.float32)
    return {"alpha": a, "top": -n + 1.0}


def _with_dot(g):
    """i ohne Punkt -> Punkt über den Strich setzen"""
    a = g["alpha"]
    lab_n = (a > 0.3).sum(axis=1)
    rows = np.where(lab_n > 0)[0]
    gaps = np.where(np.diff(rows) > 2)[0]
    if len(gaps):                        # hat schon einen Punkt (getrennte Zeilen oben)
        return g
    a = _scale(a, XH / a.shape[0])       # Strich ohne Punkt: nur x-Höhe hoch
    g = {"alpha": a, "top": -float(a.shape[0])}
    rows = np.where((a > 0.3).sum(axis=1) > 0)[0]
    d = _dot(1.5)["alpha"]
    top_cols = np.where(a[rows[0]] > 0.3)[0]
    cx = int(top_cols.mean()) + 1
    h = a.shape[0] + d.shape[0] + 3
    w = max(a.shape[1], cx + d.shape[1])
    out = np.zeros((h, w), np.float32)
    out[h - a.shape[0]:, :a.shape[1]] = a
    x0 = max(0, cx - d.shape[1] // 2)
    out[:d.shape[0], x0:x0 + d.shape[1]] = np.maximum(out[:d.shape[0], x0:x0 + d.shape[1]], d[:, :w - x0])
    return {"alpha": out, "top": g["top"] - (d.shape[0] + 3)}


def build_font():
    F = {ch: [_cand(ch, i) for i in idx] for ch, idx in PICK.items()}
    F["i"] = [_with_dot(g) for g in F["i"]]
    F["v"] = F["v"] + _from_cap("v")
    F["z"] = _from_cap("z")
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        F[ch] = C["new"][ch]
    for ch in "()-?!:/%+=":
        if ch in C["new"]:
            F[ch] = C["new"][ch]
    F["."] = [_dot(r) for r in (1.7, 1.9, 2.0)]
    F[","] = _old_punct(",")
    F["'"] = [{"alpha": g["alpha"], "top": -CAP + 1} for g in F[","]]
    q = C["new"]["“"]
    F["“"] = F["”"] = [{"alpha": _scale(g["alpha"], 0.8), "top": -CAP + 1} for g in q]
    F["–"] = F["-"]
    return F


class Writer:
    def __init__(self, text_mod, seed=4):
        self.T = importlib.import_module(text_mod)
        self.F = build_font()
        self.rng = random.Random(seed)
        self.last = {}
        self.pages = []
        self.new_page()

    def new_page(self):
        self.canvas = np.zeros((H_PAGE, W_PAGE), np.float32)
        self.pages.append(self.canvas)

    def glyph(self, ch):
        vs = self.F[ch]
        k = self.rng.randrange(len(vs))
        if len(vs) > 1 and k == self.last.get(ch):
            k = (k + 1) % len(vs)
        self.last[ch] = k
        return vs[k]

    def word(self, w):
        """-> [(alpha, dx, top)], Breite"""
        parts, x = [], 0
        for i, ch in enumerate(w):
            if ch == " ":
                x += WGAP - LGAP
                continue
            g = self.glyph(ch)
            if i and ch in ".,'":
                x -= 1
            parts.append((g["alpha"], x, g["top"]))
            x += g["alpha"].shape[1] + LGAP
        return parts, x - LGAP

    def paste(self, parts, x0, yb):
        for a, dx, top in parts:
            x, y = int(round(x0 + dx)), int(round(yb + top))
            h, w = a.shape
            if y < 0 or x < 0 or y + h > H_PAGE or x + w > W_PAGE:
                continue
            sub = self.canvas[y:y + h, x:x + w]
            np.maximum(sub, a, out=sub)

    def underline(self, x0, x1, yb):
        g = self.glyph("-")
        a = np.asarray(Image.fromarray((g["alpha"] * 255).astype(np.uint8)).resize((int(x1 - x0), g["alpha"].shape[0]),
                       Image.BILINEAR)).astype(np.float32) / 255
        self.paste([(a, 0, 6)], x0, yb)

    def words(self, text, x_start, x_wrap, underline=False):
        x = x_start
        line_x0 = x_start
        for tok in text.split(" "):
            if not tok:
                continue
            parts, w = self.word(tok)
            if x > line_x0 and x + w > X_MAX:
                if underline:
                    self.underline(line_x0 - 2, x - WGAP + 4, self.yb)
                self.newline(LINE)
                x = line_x0 = x_wrap
            self.paste(parts, x, self.yb)
            x += w + WGAP + self.rng.choice((-2, -1, 0, 1, 2))
        if underline:
            self.underline(line_x0 - 2, x - WGAP + 4, self.yb)

    def newline(self, step):
        self.yb += step
        if self.yb > LAST:
            self.new_page()
            self.yb = FIRST_NEXT

    def run(self):
        T = self.T
        self.yb = GRID0 + GRID
        self.words(T.HEADER_LEFT, X0, X0)
        self.words(T.HEADER_RIGHT, 232, 232)
        self.yb = GRID0 + 3 * GRID
        self.words(T.TITLE, X0, X0, underline=True)
        self.yb = FIRST_BODY
        prev = None
        for kind, text in T.BLOCKS:
            if prev is not None:
                step = LINE if (prev == "h" or (kind == "li" and prev == "li")) else LINE + GRID
                if kind == "h":
                    step = LINE + 2 * GRID
                self.newline(step)
                if kind == "h" and self.yb + LINE > LAST:
                    self.new_page()
                    self.yb = FIRST_NEXT
            if kind == "h":
                self.words(text, X0, X0, underline=True)
            elif kind == "li":
                self.paste(self.word("-")[0], X0 + 2, self.yb)
                self.words(text, X0 + INDENT, X0 + INDENT)
            else:
                self.words(text, X0, X0)
            prev = kind
        return self.pages


def preview(pages, prefix):
    for i, a in enumerate(pages, 1):
        np.save(f"{prefix}{i}_alpha.npy", a)
        bg = np.full((H_PAGE, W_PAGE, 3), 255, np.uint8)
        for k in range(0, (W_PAGE - GRID0) // GRID + 1):
            bg[:, GRID0 + k * GRID] = 205
        for k in range(0, (H_PAGE - GRID0) // GRID + 1):
            bg[GRID0 + k * GRID, :] = 205
        ink = np.clip(a, 0, 1)[..., None]
        Image.fromarray((bg * (1 - ink) + np.array([18, 18, 23]) * ink).astype(np.uint8)).save(f"{prefix}{i}.png")


if __name__ == "__main__":
    pages = Writer(sys.argv[1]).run()
    preview(pages, sys.argv[2])
    print(len(pages), "Seiten")
