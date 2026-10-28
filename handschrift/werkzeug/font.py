"""Buchstaben-„Schrift“ aus Sangs Proben: einzelne Buchstaben, jeder genau auf die Grundlinie gesetzt.

Quellen: alte Foto-Bibliothek (170 Wörter mit Buchstabengrenzen) für Kleinbuchstaben, neue Probe SP-k1 für
Großbuchstaben, Ziffern, Zeichen und k/j/z. Alle Zeichen werden auf gleiche Maße gebracht (x-Höhe, Oberlänge,
Großbuchstabenhöhe) und mit der Unterkante des Buchstabenkörpers auf die Grundlinie gesetzt.
"""
import os
import pickle

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SP = "/tmp/claude-0/-home-user-second-bran/77087009-95da-55ff-8987-fa95a510b3dd/scratchpad/"
XH, ASC, CAP, DESC = 13.0, 19.0, 19.0, 12.0
BASE_OLD = 53                     # Grundlinie in den alten Wort-Alphas
XL, AS, DE = set("acemnorsuvwxzäöü"), set("bdfhklt"), set("gjpqy")


def _clean(sub):
    """Reste der Nachbarbuchstaben (Verbindungsstriche am Schnittrand) entfernen."""
    lab, n = ndi.label(sub > 0.25, structure=np.ones((3, 3)))
    if n == 0:
        return sub
    sizes = ndi.sum(sub > 0.25, lab, range(1, n + 1))
    big = sizes.max()
    keep = np.zeros(sub.shape, bool)
    objs = ndi.find_objects(lab)
    for k, (s, sl) in enumerate(zip(sizes, objs), 1):
        touches = sl[1].start <= 1 or sl[1].stop >= sub.shape[1] - 1
        if s >= 0.35 * big or (s >= 4 and not touches):
            keep |= lab == k
    return sub * ndi.binary_dilation(keep, iterations=1)


def _crop(a):
    ys, xs = np.where(a > 0.12)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1], ys.min(), ys.max() + 1


def _scale(a, f):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    im = im.resize((max(1, round(a.shape[1] * f)), max(1, round(a.shape[0] * f))), Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 255


def normalize(ch, a, base):
    """a = Alpha mit Grundlinie in Zeile base -> (Alpha, top relativ zur Grundlinie), auf Zielmaße skaliert."""
    g, y0, y1 = _crop(a)
    body_top, body_bot = y0, min(y1, base + 1)
    if ch in XL or ch in DE:
        target, h = XH, max(1, base - y0 if ch in DE else y1 - y0)
    elif ch in AS:
        target, h = ASC * (0.82 if ch == "t" else 1.0), max(1, y1 - y0)
    elif ch == "i" or ch == "j":
        target, h = XH * 1.45, max(1, (y1 if ch == "i" else base) - y0)
    elif ch.isupper() or ch.isdigit():
        target, h = CAP, max(1, y1 - y0)
    else:
        return g, float(y0 - base)
    f = target / h
    f = min(max(f, 0.6), 1.6)
    g2 = _scale(g, f)
    if ch in DE or ch == "j":
        top = -(base - y0) * f
    else:
        top = -g2.shape[0]
    return g2, float(top)


def old_candidates():
    S = pickle.load(open(SP + "hw/lib2.pkl", "rb"))
    out = {}
    for wi, t in enumerate(S["lib"]):
        a = t["alpha"]
        for li, (ch, x0, x1) in enumerate(t["letters"]):
            if not ch.islower():
                continue
            sub = _clean(a[:, max(0, x0 - 1):x1 + 1].copy())
            if (sub > 0.3).sum() < 6:
                continue
            g, top = normalize(ch, sub, BASE_OLD)
            bt = t["btype"]
            left_gap = li == 0 or bt[li - 1] in ("gap",)
            right_gap = bt[li] in ("gap", "end")
            out.setdefault(ch, []).append({"alpha": g, "top": top, "src": f"old:{t['text']}#{li}",
                                           "clean": int(left_gap) + int(right_gap), "w": g.shape[1]})
    return out


def new_candidates():
    L = pickle.load(open(SP + "bib/library.pkl", "rb"))["glyphs"]
    out = {}
    for ch, vs in L.items():
        if len(ch) != 1:
            continue
        for k, g in enumerate(vs):
            a = g["alpha"]
            h = a.shape[0]
            base = int(round(-g["top"]))          # Grundlinie relativ zur Oberkante
            pad = np.zeros((max(h, base) + 20, a.shape[1]), np.float32)
            pad[:h] = a
            if ch.isalnum():
                n, top = normalize(ch, pad, base)
            else:
                n, top = g["alpha"] * 1.0, g["top"] * (XH / 13.0)
                n = _scale(n, XH / 13.0) if ch not in "“„" else n
            out.setdefault(ch, []).append({"alpha": n, "top": top, "src": f"new:{g['src']}#{k}", "clean": 2,
                                           "w": n.shape[1]})
    return out


if __name__ == "__main__":
    old, new = old_candidates(), new_candidates()
    pickle.dump({"old": old, "new": new}, open(SP + "eng/font_candidates.pkl", "wb"))
    print("alt:", {k: len(v) for k, v in sorted(old.items())})
    print("neu:", "".join(sorted(new)))
