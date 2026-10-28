"""Kuli-Umwandlung: Tinten-Alpha (Seite 1414 x 2000 px, aus render_*.py) -> Mittellinien-Striche -> GoodNotes + PDF.

Ablauf je Seite:
  1. Alpha binarisieren, Zhang-Suen-Skelett (numpy, ohne OpenCV/skimage)
  2. Skelett in Pfade zerlegen (Endpunkt -> Endpunkt/Verzweigung), kurze Sporen entfernen
  3. an Verzweigungen die geradlinigste Fortsetzung verbinden -> ein Strich pro Linienzug
  4. glätten, vereinfachen, px -> pt (A4: 1414 px = 595,28 pt)
  5. .goodnotes (gn_writer, Karo-Hintergrund als PDF je Seite) und PDF (reportlab) schreiben

Aufruf: python3 kuli.py --out AUSGABE_OHNE_ENDUNG --title "Titel" seite1_alpha.npy [seite2_alpha.npy ...]
"""
import argparse
import io
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn_writer  # noqa: E402

PX_W, PX_H = 1414, 2000
PT_W, PT_H = 595.2755905511812, 841.8897637795277
PX2PT = PT_W / PX_W
GRID0_PT, CELL_PT = 15.576518281749436, 15.997505262337258
WIDTH_PT = 1.1                              # Sangs Kuli (CLAUDE.md: 1,05–1,14 pt)
INK = (0.07, 0.07, 0.09)


# --------------------------------------------------------------------------- 1. Skelett
def thin(img):
    """Zhang-Suen-Ausdünnung auf einem bool-Array."""
    img = img.copy()
    while True:
        changed = False
        for step in (0, 1):
            P = np.pad(img, 1)
            p2, p3, p4 = P[:-2, 1:-1], P[:-2, 2:], P[1:-1, 2:]
            p5, p6, p7 = P[2:, 2:], P[2:, 1:-1], P[2:, :-2]
            p8, p9 = P[1:-1, :-2], P[:-2, :-2]
            seq = [p2, p3, p4, p5, p6, p7, p8, p9, p2]
            B = sum(s.astype(np.uint8) for s in seq[:8])
            A = sum(((~seq[i]) & seq[i + 1]).astype(np.uint8) for i in range(8))
            if step == 0:
                cond = ~(p2 & p4 & p6) & ~(p4 & p6 & p8)
            else:
                cond = ~(p2 & p4 & p8) & ~(p2 & p6 & p8)
            rem = img & (B >= 2) & (B <= 6) & (A == 1) & cond
            if rem.any():
                img[rem] = False
                changed = True
        if not changed:
            return img


NB8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def _neighbors(sk, y, x):
    """8er-Nachbarn ohne überflüssige Diagonalen: ein diagonaler Nachbar zählt nicht, wenn er 4-benachbart zu
    einem orthogonalen Nachbarn ist (sonst wird jede Treppenstufe des Skeletts zur Verzweigung)."""
    h, w = sk.shape
    orth, diag = [], []
    for dy, dx in NB8:
        yy, xx = y + dy, x + dx
        if 0 <= yy < h and 0 <= xx < w and sk[yy, xx]:
            (orth if dy == 0 or dx == 0 else diag).append((yy, xx))
    out = list(orth)
    for q in diag:
        if not any(abs(q[0] - o[0]) + abs(q[1] - o[1]) == 1 for o in orth):
            out.append(q)
    return out


# --------------------------------------------------------------------------- 2. Pfade
def trace(sk):
    """Skelett -> Liste von Pfaden [(y, x), ...] zwischen Endpunkten/Verzweigungen (+ geschlossene Schleifen)."""
    ys, xs = np.where(sk)
    pts = list(zip(ys.tolist(), xs.tolist()))
    deg = {p: len(_neighbors(sk, *p)) for p in pts}
    nodes = {p for p in pts if deg[p] != 2}
    visited_edges = set()
    paths = []

    def walk(start, nxt):
        path = [start, nxt]
        prev, cur = start, nxt
        while cur not in nodes:
            nbs = [q for q in _neighbors(sk, *cur) if q != prev]
            if not nbs:
                break
            prev, cur = cur, nbs[0]
            path.append(cur)
            if cur == start:
                break
        return path

    for n in sorted(nodes):
        for q in _neighbors(sk, *n):
            key = (min(n, q), max(n, q))
            if key in visited_edges:
                continue
            path = walk(n, q)
            for a, b in zip(path, path[1:]):
                visited_edges.add((min(a, b), max(a, b)))
            paths.append(path)
    # geschlossene Schleifen ohne Knoten (z. B. "o")
    covered = {p for path in paths for p in path}
    for p in pts:
        if p not in covered and deg[p] == 2:
            q = _neighbors(sk, *p)[0]
            path = walk(p, q)
            covered.update(path)
            paths.append(path)
    return paths, nodes


def prune(paths, nodes, min_len=4):
    """Sporen (kurze Pfade, die an einem Endpunkt enden und an einer Verzweigung hängen) entfernen."""
    deg = {}
    for path in paths:
        for e in (path[0], path[-1]):
            deg[e] = deg.get(e, 0) + 1
    out = []
    for path in paths:
        a, b = path[0], path[-1]
        spur = len(path) < min_len and ((deg.get(a, 0) == 1) != (deg.get(b, 0) == 1)) and a != b
        if not spur:
            out.append(path)
    return out


# --------------------------------------------------------------------------- 3. Verbinden
def _dir(path, at_end, n=5):
    seg = path[-n:] if at_end else path[:n][::-1]
    (y0, x0), (y1, x1) = seg[0], seg[-1]
    d = math.hypot(y1 - y0, x1 - x0)
    return ((y1 - y0) / d, (x1 - x0) / d) if d else (0.0, 0.0)


def merge(paths, max_turn_deg=55, n_dir=5):
    """An jedem Knoten die Pfadenden paarweise verbinden, deren Richtungen am besten zusammenpassen."""
    ends = {}
    for i, path in enumerate(paths):
        if path[0] == path[-1]:
            continue
        ends.setdefault(path[0], []).append((i, False))
        ends.setdefault(path[-1], []).append((i, True))
    link = {}          # (i, at_end) -> (j, at_end_j)
    cos_max = math.cos(math.radians(max_turn_deg))
    for node, lst in ends.items():
        cands = []
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                (i, ei), (j, ej) = lst[a], lst[b]
                if i == j:
                    continue
                di, dj = _dir(paths[i], ei, n_dir), _dir(paths[j], ej, n_dir)   # beide zeigen zum Knoten hin
                c = -(di[0] * dj[0] + di[1] * dj[1])               # 1 = geradlinige Fortsetzung
                cands.append((c, lst[a], lst[b]))
        used = set()
        for c, A, B in sorted(cands, reverse=True):
            if c < cos_max or A in used or B in used:
                continue
            link[A] = B
            link[B] = A
            used.update((A, B))
    # Ketten aufbauen
    done = [False] * len(paths)
    strokes = []
    for i, path in enumerate(paths):
        if done[i]:
            continue
        if path[0] == path[-1]:
            done[i] = True
            strokes.append(list(path))
            continue
        # zum Kettenanfang zurücklaufen
        cur, at_end = i, False
        seen = {i}
        while (cur, at_end) in link:
            j, ej = link[(cur, at_end)]
            if j in seen:
                break
            seen.add(j)
            cur, at_end = j, not ej
        # von dort vorwärts
        chain = []
        cur, at_end = cur, at_end
        seen = set()
        while True:
            seen.add(cur)
            done[cur] = True
            p = list(paths[cur]) if not at_end else list(paths[cur])[::-1]
            chain += p if not chain else p[1:]
            key = (cur, not at_end)
            if key not in link:
                break
            j, ej = link[key]
            if j in seen:
                break
            cur, at_end = j, ej
        strokes.append(chain)
    return strokes


# --------------------------------------------------------------------------- 4. Glätten
def smooth(pts, passes=2):
    a = np.asarray(pts, np.float64)
    closed = len(a) > 3 and np.allclose(a[0], a[-1])
    for _ in range(passes):
        if len(a) < 3:
            break
        b = a.copy()
        b[1:-1] = (a[:-2] + a[1:-1] + a[2:]) / 3
        if closed:
            b[0] = b[-1] = (a[-2] + a[0] + a[1]) / 3
        a = b
    return a


def simplify(a, eps=0.35):
    """Douglas-Peucker."""
    if len(a) < 3:
        return a
    keep = np.zeros(len(a), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(a) - 1)]
    while stack:
        s, e = stack.pop()
        if e <= s + 1:
            continue
        p, q = a[s], a[e]
        d = q - p
        L = np.hypot(*d)
        seg = a[s + 1:e]
        if L < 1e-9:
            dist = np.hypot(*(seg - p).T)
        else:
            dist = np.abs(d[1] * (seg[:, 0] - p[0]) - d[0] * (seg[:, 1] - p[1])) / L
        k = int(np.argmax(dist))
        if dist[k] > eps:
            idx = s + 1 + k
            keep[idx] = True
            stack.append((s, idx))
            stack.append((idx, e))
    return a[keep]


def _dots(sk):
    P = np.pad(sk, 1)
    nb = sum(P[1 + dy:P.shape[0] - 1 + dy, 1 + dx:P.shape[1] - 1 + dx].astype(np.uint8) for dy, dx in NB8)
    return [[(int(y), int(x))] for y, x in zip(*np.where(sk & (nb == 0)))]


def alpha_to_strokes(alpha, thresh=0.5, up=3, min_px=3):
    """Alpha (H x W, 0..1) -> Striche als [(x_pt, y_pt), ...], Ursprung oben links.

    Jede zusammenhängende Tintenfläche wird einzeln bearbeitet und vorher `up`-fach bilinear vergrößert:
    so bleiben enge Lücken (h-Bogen am Schaft, e-Schleife) erhalten, und die Mittellinie wird glatter."""
    from PIL import Image
    from scipy import ndimage as ndi
    lab, n = ndi.label(alpha > 0.1, structure=np.ones((3, 3)))
    strokes = []
    for k, sl in enumerate(ndi.find_objects(lab), 1):
        y0, y1 = max(0, sl[0].start - 2), min(alpha.shape[0], sl[0].stop + 2)
        x0, x1 = max(0, sl[1].start - 2), min(alpha.shape[1], sl[1].stop + 2)
        sub = alpha[y0:y1, x0:x1] * (lab[y0:y1, x0:x1] == k)
        big = np.asarray(Image.fromarray(sub.astype(np.float32), "F").resize((sub.shape[1] * up, sub.shape[0] * up), Image.BILINEAR))
        sk = thin(big > thresh)
        if not sk.any():
            continue
        paths, nodes = trace(sk)
        paths = prune(paths, nodes, min_len=4 * up) + _dots(sk)
        for s in merge(paths, n_dir=4 * up):
            if len(s) < min_px * up:
                y, x = s[len(s) // 2]
                px, py = x0 + (x + 0.5) / up - 0.5, y0 + (y + 0.5) / up - 0.5
                strokes.append([(px * PX2PT, py * PX2PT), ((px + 0.6) * PX2PT, (py + 0.3) * PX2PT)])
                continue
            a = simplify(smooth(s, passes=up), eps=0.35 * up)
            strokes.append([((x0 + (x + 0.5) / up - 0.5) * PX2PT, (y0 + (y + 0.5) / up - 0.5) * PX2PT) for y, x in a])
    return strokes


# --------------------------------------------------------------------------- 5. Ausgabe
def karo_pdf():
    from reportlab.pdfgen.canvas import Canvas
    buf = io.BytesIO()
    c = Canvas(buf, pagesize=(PT_W, PT_H))
    c.setStrokeColorRGB(0.80, 0.80, 0.80)
    c.setLineWidth(0.4)
    x = GRID0_PT
    while x <= PT_W:
        c.line(x, 0, x, PT_H)
        x += CELL_PT
    y = GRID0_PT
    while y <= PT_H:
        c.line(0, PT_H - y, PT_W, PT_H - y)
        y += CELL_PT
    c.showPage()
    c.save()
    return buf.getvalue()


def write_pdf(path, pages):
    from reportlab.pdfgen.canvas import Canvas
    c = Canvas(path, pagesize=(PT_W, PT_H))
    for strokes in pages:
        c.setStrokeColorRGB(0.80, 0.80, 0.80)
        c.setLineWidth(0.4)
        x = GRID0_PT
        while x <= PT_W:
            c.line(x, 0, x, PT_H)
            x += CELL_PT
        y = GRID0_PT
        while y <= PT_H:
            c.line(0, PT_H - y, PT_W, PT_H - y)
            y += CELL_PT
        c.setStrokeColorRGB(*INK)
        c.setLineWidth(WIDTH_PT)
        c.setLineCap(1)
        c.setLineJoin(1)
        for s in strokes:
            p = c.beginPath()
            p.moveTo(s[0][0], PT_H - s[0][1])
            for x, y in s[1:]:
                p.lineTo(x, PT_H - y)
            c.drawPath(p, stroke=1, fill=0)
        c.showPage()
    c.save()


def preview_png(path, strokes, scale=2.0):
    from PIL import Image, ImageDraw
    W, H = int(PT_W * scale), int(PT_H * scale)
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    x = GRID0_PT
    while x <= PT_W:
        d.line((x * scale, 0, x * scale, H), fill=(205, 205, 205))
        x += CELL_PT
    y = GRID0_PT
    while y <= PT_H:
        d.line((0, y * scale, W, y * scale), fill=(205, 205, 205))
        y += CELL_PT
    for s in strokes:
        d.line([(x * scale, y * scale) for x, y in s], fill=(18, 18, 23), width=max(1, int(round(WIDTH_PT * scale))), joint="curve")
    im.save(path)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alphas", nargs="+")
    ap.add_argument("--out", required=True, help="Ausgabepfad ohne Endung")
    ap.add_argument("--title", required=True)
    ap.add_argument("--thresh", type=float, default=0.5, help="Alpha-Schwelle fürs Binarisieren (nach 3x-Vergrößerung)")
    args = ap.parse_args()
    pages = []
    for f in args.alphas:
        a = np.load(f)
        assert a.shape == (PX_H, PX_W), a.shape
        pages.append(alpha_to_strokes(a, args.thresh))
    write_pdf(args.out + ".pdf", pages)
    im = preview_png(args.out + "_p1.png", pages[0])
    for k, s in enumerate(pages[1:], 2):
        preview_png(args.out + f"_p{k}.png", s)
    tb = io.BytesIO()
    im.resize((298, 421)).save(tb, "JPEG", quality=85)
    paper = karo_pdf()
    gp = [(PT_W, PT_H, s, paper) for s in pages]
    res = gn_writer.write(args.out + ".goodnotes", args.title, gp, None, tb.getvalue(), WIDTH_PT, INK)
    print({"seiten": len(pages), "striche": [len(s) for s in pages], "punkte": [sum(len(x) for x in s) for s in pages]}, res)


if __name__ == "__main__":
    main()
