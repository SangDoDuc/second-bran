"""Zeichen-Bibliothek aus Sangs Schriftprobe SP-k1 (28.10.2026).

Jedes Zeichen = Tinten-Alpha + Lage zur Grundlinie (top = Oberkante relativ zur Grundlinie, nach unten positiv).
Quellen: Einzelfelder (A–Z, 0–9, Zeichen), Mathe-Ausdrücke (Pfeil, große Klammern, Wurzel, Bruchstrich,
Hoch-/Tiefzahlen, Malpunkt) und Ausschnitte aus Wörtern (Kleinbuchstaben, ganze Wörter).
"""
import os, pickle
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from scipy import ndimage as ndi

from comps import F, comps


def _cut(fid, ranks=None, xr=None):
    """Komponenten (Ränge wie in comps.py) und/oder x-Bereich eines Feldes -> (alpha, top, left)."""
    r = F[fid]
    a = r["alpha"]
    if ranks is not None:
        lab, cs = comps(fid)
        m = np.zeros(a.shape, bool)
        for k in ranks:
            m |= lab == cs[k]["label"]
        m = ndi.binary_dilation(m, iterations=1)
        a = a * m
    if xr is not None:
        b = np.zeros_like(a)
        b[:, xr[0]:xr[1]] = a[:, xr[0]:xr[1]]
        a = b
    ys, xs = np.where(a > 0.12)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    a = np.clip(a * 1.35, 0, 1)            # helle (dünne) Striche verstärken, sonst fallen sie bei der Kuli-Umwandlung weg
    return {"alpha": a[y0:y1, x0:x1].astype(np.float32), "top": float(y0 - r["baseline"]), "src": fid,
            "ranks": ranks, "xr": xr}


def _iso(prefix, ch):
    return _cut(f"{prefix}_U+{ord(ch):04X}") if prefix != "upper" else _cut(f"upper_{ch}")


def build():
    G = {}

    def add(key, g):
        G.setdefault(key, []).append(g)

    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        add(ch, _iso("upper", ch))
    for ch in "0123456789":
        add(ch, _iso("digit", ch))
    for ch in "()|+−=→√?!%/-„“,:":
        if ch == "·":
            continue
        add(ch, _iso("punct", ch))
    # weitere Varianten aus den Mathe-Ausdrücken
    add("A", _cut("math_vec_ac", [0])); add("C", _cut("math_vec_ac", [2]))
    add("A", _cut("math_abs", [2])); add("C", _cut("math_abs", [3])); add("C", _cut("math_points", [0]))
    add("1", _cut("math_abs", [8])); add("1", _cut("math_abs", [11])); add("2", _cut("math_abs", [12]))
    add("2", _cut("math_plane", [3])); add("2", _cut("math_plane", [10])); add("6", _cut("math_plane", [15]))
    add("3", _cut("math_points", [3])); add("6", _cut("math_points", [6])); add("9", _cut("math_points", [8]))
    add("3", _cut("math_exp", [3]))
    add("=", _cut("math_vec_ac", [3])); add("=", _cut("math_frac", [1])); add("=", _cut("math_abs", [5, 6]))
    add("=", _cut("math_exp", [2]))
    add("+", _cut("math_plane", [6])); add("+", _cut("math_plane", [9]))
    add("(", _cut("math_points", [1])); add(")", _cut("math_points", [9]))
    add("−", _cut("math_points", [2])); add("−", _cut("math_points", [5]))
    add("|", _cut("math_points", [4])); add("|", _cut("math_points", [7]))
    add(":", _cut("math_plane", [1, 2]))
    add("x", _cut("math_frac", [0])); add("x", _cut("math_plane", [4])); add("x", _cut("math_plane", [7]))
    add("x", _cut("math_plane", [11]))
    add("·", _cut("math_exp", [4]))
    add("₁", _cut("math_plane", [5])); add("₂", _cut("math_plane", [8])); add("₃", _cut("math_plane", [12]))
    add("²", _cut("math_exp", [7])); add("⁻", _cut("math_exp", [6])); add("ˣ", _cut("math_exp", [8]))
    # Bauteile
    add("ARROW", _cut("math_vec_ac", [1])); add("ARROW", _cut("math_abs", [1]))
    add("BIGPAREN_L", _cut("math_vec_ac", [4])); add("BIGPAREN_R", _cut("math_vec_ac", [10]))
    add("ROOT", _cut("math_abs", [7]))
    add("FRACBAR", _cut("math_frac", [2]))
    add("½", _cut("math_frac", [2, 3, 4]))
    add("ABS", _cut("math_abs", [0])); add("ABS", _cut("math_abs", [4]))
    # Kleinbuchstaben aus Wörtern
    add("a", _cut("sent1_w10", [2], (730, 744)))
    add("b", _cut("sent0_w05", [2]))
    add("d", _cut("sent2_w04", [0], (243, 255)))
    add("e", _cut("sent1_w11", [2]))
    add("i", _cut("word_ist", [0, 1]))
    add("k", _cut("sent1_w11", [0], (793, 804)))
    add("m", _cut("word_mit", [0], (32, 52)))
    add("n", _cut("word_nicht", [0]))
    add("o", _cut("sent1_w10", [3]))
    add("r", _cut("sent0_w03", [3]))
    add("t", _cut("word_mit", [2]))
    # Ergänzung 28.10.2026 (Stochastik-Lösung): p c g h l s u ä ö, weitere e, Punkt. Aus den Sätzen geschnitten;
    # x-Bereiche so gewählt, dass Ein-/Ausläufe der Nachbarbuchstaben draußen bleiben (geprüft über ein Glyph-Blatt)
    add("e", _cut("sent1_w01", [2], (125, 134)))          # li-e-gen
    add("e", _cut("sent1_w01", [4], (144, 154)))          # lieg-e-n
    add("e", _cut("sent2_w06", [0], (385, 396)))          # s-e-it
    add("e", _cut("sent0_w04", [1], (434, 443)))          # qu-e-r
    add("p", _cut("sent0_w01", [3], (162, 171)))          # Boxkäm-p-fer
    add("ä", _cut("sent0_w01", [2], (136, 146)))          # Boxk-ä-mpfer
    add("c", _cut("sent0_w09", [0], (834, 844)))          # Dei-c-h
    add("c", _cut("sent1_w09", [1], (652, 661)))          # dur-c-h
    add("c", _cut("word_Gleichung", [4], (95, 106)))      # Glei-c-hung
    add("h", _cut("sent0_w09", [0], (847, 865)))          # Deic-h
    add("h", _cut("sent1_w09", [1], (663, 679)))          # durc-h
    add("h", _cut("sent1_w08", [0], (569, 582)))          # ge-h-t
    add("h", _cut("word_Gleichung", [4], (108, 120)))     # Gleic-h-ung
    add("g", _cut("sent1_w01", [3]))                      # lie-g-en
    add("g", _cut("sent1_w08", [0], (544, 557)))          # g-eht
    add("g", _cut("word_Gleichung", [5], (146, 163)))     # Gleichun-g
    add("l", _cut("sent1_w01", [0]))                      # l-iegen
    add("l", _cut("word_Gleichung", [1]))                 # G-l-eichung
    add("s", _cut("word_dass", [2]))                      # das-s
    add("s", _cut("word_dass", [1], (52, 62)))            # da-s-s
    add("s", _cut("sent2_w06", [0], (373, 384)))          # s-eit
    add("u", _cut("sent0_w04", [1], (421, 432)))          # q-u-er
    add("u", _cut("sent1_w09", [0], (629, 642)))          # d-u-rch
    add("u", _cut("word_Gleichung", [5], (120, 134)))     # Gleich-u-ng
    add("ö", _cut("sent0_w00", [1, 2]))                   # Zw-ö-lf
    add(".", _cut("sent0_w09", [2]))                      # Deich-.
    add(".", _cut("sent2_w08", [2]))                      # ca-.
    # ganze Wörter
    W = {"und": _cut("word_und"), "gegenüber": _cut("sent1_w05"), "Diagonale": _cut("sent1_w14", [0, 1, 2, 3, 4]),
         "der": _cut("sent2_w04"), "Würfel": _cut("word_Würfel"), "Vektor": _cut("word_Vektor"),
         "Richtung": _cut("word_Richtung"), "also": _cut("sent1_w10", [2, 3]), "keine": _cut("sent1_w11"),
         "Kante": _cut("sent1_w12"), "durch": _cut("sent1_w09"), "in": _cut("sent2_w10"), "den": _cut("sent2_w11")}
    G["="] = [_open_equals(g) for g in G["="]]
    return G, W


def _open_equals(g, min_gap=5):
    """Gleichheitszeichen: Abstand zwischen den beiden Strichen auf >= min_gap px (sonst verschmelzen sie
    beim Umwandeln in gleichmäßige Kuli-Striche)."""
    a = g["alpha"]
    p = (a > 0.3).sum(axis=1)
    rows = np.where(p > 0)[0]
    if len(rows) < 3:
        return g
    mid = rows[0] + int(np.argmin(p[rows[0]:rows[-1] + 1][1:-1])) + 1 if rows[-1] - rows[0] > 2 else rows[0] + 1
    upper, lower = a[:mid], a[mid:]
    upper = np.clip(upper / max(upper.max(), 0.2), 0, 1)     # beide Striche gleich kräftig
    lower = np.clip(lower / max(lower.max(), 0.2), 0, 1)
    a = np.concatenate([upper, lower])
    gap = 0
    r = mid
    while r < a.shape[0] and p[r] <= 1:
        gap += 1; r += 1
    extra = max(0, min_gap - gap)
    new = np.concatenate([upper, np.zeros((extra, a.shape[1]), a.dtype), lower]) if extra else a
    return dict(g, alpha=new, top=g["top"] - extra / 2)


if __name__ == "__main__":
    G, W = build()
    pickle.dump({"glyphs": G, "words": W}, open("library.pkl", "wb"))
    print(len(G), "Zeichen,", sum(len(v) for v in G.values()), "Varianten,", len(W), "ganze Wörter")
