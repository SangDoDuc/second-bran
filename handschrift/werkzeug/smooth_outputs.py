"""Handschrift-Seiten (Alpha 1414 x 2000) -> .goodnotes + PDF mit GLATTEN Strichen.

Neu (28.10.2026, Sangs Hinweis „pixelig“): Die Striche aus dem Skelett haben im Schnitt nur ~7 Punkte und wirken
eckig. Hier werden sie leicht entrauscht, an echten Ecken getrennt und als zentripetaler Catmull-Rom-Spline dicht
(alle ~0,3 pt) abgetastet. Die PDF wird aus denselben Strichen gezeichnet (Vektor, runde Enden) statt aus einer
nachgezeichneten Bitmap.

python3 smooth_outputs.py ALPHA_PREFIX OUT_DIR NAME "GoodNotes-Titel" "PDF-Titel"
   (liest ALPHA_PREFIX1_alpha.npy, ALPHA_PREFIX2_alpha.npy, …)
"""
import glob
import io
import json
import math
import os
import sys
from multiprocessing import Pool

SP = "/tmp/claude-0/-home-user-second-bran/77087009-95da-55ff-8987-fa95a510b3dd/scratchpad/"
sys.path[:0] = [SP + "pylib3", SP + "pylib2", SP + "pylib", SP + "ek", SP + "hw", SP + "ven"]

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

import gn_writer  # noqa: E402
import strokes as S  # noqa: E402
from make_goodnotes import RGB, karo_pdf, to_points  # noqa: E402
from make_outputs import WIDTH_PT, WIDTH_PX, grid  # noqa: E402

PW, PH = A4
STEP = 0.3          # Abtastabstand in pt
CORNER_DEG = 70     # Richtungswechsel ab dem eine echte Ecke erhalten bleibt
PASSES = int(os.environ.get("SMOOTH_PASSES", "6"))   # Glättungsdurchgänge (Entrauschen)


def _corners(P):
    idx = [0]
    for i in range(1, len(P) - 1):
        a, b = P[i] - P[i - 1], P[i + 1] - P[i]
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na < 1e-6 or nb < 1e-6:
            continue
        ang = math.degrees(math.acos(max(-1, min(1, float(np.dot(a, b) / (na * nb))))))
        if ang > CORNER_DEG:
            idx.append(i)
    idx.append(len(P) - 1)
    return idx


def _resample(P, step=0.8):
    """gleichmäßige Abstände (sonst glättet die Mittelung ungleich)"""
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    if d[-1] < 1e-6:
        return P[:1]
    n = max(2, int(math.ceil(d[-1] / step)) + 1)
    t = np.linspace(0, d[-1], n)
    return np.c_[np.interp(t, d, P[:, 0]), np.interp(t, d, P[:, 1])]


def _denoise(P, passes=PASSES):
    P = _resample(P)
    for _ in range(passes):
        if len(P) < 4:
            break
        Q = P.copy()
        Q[1:-1] = 0.25 * P[:-2] + 0.5 * P[1:-1] + 0.25 * P[2:]
        P = Q
    return P


def _catmull(P):
    if len(P) == 2:
        n = max(2, int(math.ceil(np.linalg.norm(P[1] - P[0]) / STEP)) + 1)
        return [tuple(P[0] + (P[1] - P[0]) * t) for t in np.linspace(0, 1, n)]
    ext = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = [tuple(P[0])]
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        t0 = 0.0
        t1 = t0 + max(np.linalg.norm(p1 - p0), 1e-6) ** 0.5
        t2 = t1 + max(np.linalg.norm(p2 - p1), 1e-6) ** 0.5
        t3 = t2 + max(np.linalg.norm(p3 - p2), 1e-6) ** 0.5
        n = max(2, int(math.ceil(np.linalg.norm(p2 - p1) / STEP)))
        for t in np.linspace(t1, t2, n + 1)[1:]:
            a1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
            a2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
            a3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
            b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
            b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3
            c = (t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2
            out.append((float(c[0]), float(c[1])))
    return out


def smooth(pts):
    if len(pts) < 2:
        return pts
    P = np.asarray(pts, float)
    keep = [0] + [i for i in range(1, len(P)) if np.linalg.norm(P[i] - P[i - 1]) > 1e-3]
    P = P[keep]
    if len(P) < 2:
        return [tuple(P[0])]
    cs = _corners(P)
    out = []
    for a, b in zip(cs, cs[1:]):
        seg = _denoise(P[a:b + 1]) if b - a >= 2 else P[a:b + 1].copy()
        seg[0], seg[-1] = P[a], P[b]
        part = _catmull(seg)
        out += part if not out else part[1:]
    return out


def convert(path):
    a = np.load(path)
    lines, _ = S.page_strokes(a, width=WIDTH_PX)
    return [smooth(to_points(ln)) for ln in lines]


def main(prefix, out, name, title, pdf_title):
    os.makedirs(out, exist_ok=True)
    files = sorted(glob.glob(prefix + "[0-9]_alpha.npy")) + sorted(glob.glob(prefix + "[0-9][0-9]_alpha.npy"))
    with Pool(3) as pool:
        page_strokes = pool.map(convert, files)
    c = canvas.Canvas(out + name + ".pdf", pagesize=A4)
    c.setTitle(pdf_title)
    c.setAuthor("Sang Duc Do")
    for strokes in page_strokes:
        grid(c)
        c.setStrokeColorRGB(*RGB)
        c.setFillColorRGB(*RGB)
        c.setLineWidth(WIDTH_PT)
        c.setLineCap(1)
        c.setLineJoin(1)
        for s in strokes:
            if len(s) == 1:
                c.circle(s[0][0], PH - s[0][1], WIDTH_PT * 0.55, stroke=0, fill=1)
                continue
            p = c.beginPath()
            p.moveTo(s[0][0], PH - s[0][1])
            for x, y in s[1:]:
                p.lineTo(x, PH - y)
            c.drawPath(p, stroke=1, fill=0)
        c.showPage()
    c.save()
    pages = [(PW, PH, strokes) for strokes in page_strokes]
    first = np.load(files[0]) > 0.3
    prev = np.full(first.shape, 255, np.uint8)
    prev[first] = 18
    tb = io.BytesIO()
    Image.fromarray(prev).resize((298, 421), Image.LANCZOS).convert("RGB").save(tb, "JPEG", quality=85)
    res = gn_writer.write(out + name + ".goodnotes", title, pages, karo_pdf, tb.getvalue(), WIDTH_PT, RGB)
    json.dump({"title": title, "width_pt": WIDTH_PT, "pages": [p[2] for p in pages]}, open(out + name + ".ink.json", "w"))
    pts = [len(s) for st in page_strokes for s in st]
    print(len(files), "Seiten,", len(pts), "Striche, Punkte je Strich Median", sorted(pts)[len(pts) // 2], res)


if __name__ == "__main__":
    main(*sys.argv[1:6])
