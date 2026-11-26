"""Schaubild ontologischer Gottesbeweis in Sangs Handschrift: Kästen + Pfeile, Karo 1414x2000."""
import sys
import numpy as np
from PIL import Image, ImageDraw
REPO = "/home/user/second-bran/handschrift/"
sys.path[:0] = [REPO + "bibliothek"]
import render_text as RT  # wendet Ordentlich-Modus an
import render_loesung as R
G = R.LIB["glyphs"]

def dot():
    d = G["."][0]["alpha"]; h, w = d.shape
    return np.asarray(Image.fromarray((d * 255).astype(np.uint8)).resize((max(2, int(w * .7)), max(2, int(h * .7))))).astype(np.float32) / 255
def uml(g):
    a, d = g["alpha"], dot(); dh, dw = d.shape; gap = 2
    W = max(a.shape[1], 2 * dw + 4); out = np.zeros((a.shape[0] + dh + gap, W), np.float32)
    out[dh + gap:, :a.shape[1]] = a; cx = a.shape[1] / 2
    for x0 in (int(cx - dw - 1), int(cx + 1)):
        x0 = max(0, min(W - dw, x0)); out[:dh, x0:x0 + dw] = np.maximum(out[:dh, x0:x0 + dw], d)
    return dict(g, alpha=out, top=g["top"] - dh - gap)
for big, u in (("A", "Ä"), ("O", "Ö"), ("U", "Ü")):
    G[u] = [uml(g) for g in G[big]]

h = R.Hand(7)
W_PAGE, H_PAGE, GRID0, GRID = R.W_PAGE, R.H_PAGE, R.GRID0, R.GRID
SP = R.SPACE + 3
LX0, LX1, RX0, RX1 = 50, 690, 790, 1364
PAD, LH = 14, GRID

def wrap(text, width):
    lines, cur, x = [], [], 0
    for w in text.split(" "):
        parts, wd = h.run(w.replace(" ", " "))
        if cur and x + wd > width:
            lines.append(cur); cur, x = [], 0
        cur.append((parts, wd, x)); x += wd + SP
    if cur:
        lines.append(cur)
    return lines

def box_h(text, x0, x1):
    return len(wrap(text, x1 - x0 - 2 * PAD)) * LH + 2 * PAD - 6

pages = []
canvas = draw = img = None
def new_page():
    global canvas, img, draw
    if canvas is not None:
        pages.append((canvas, img))
    canvas = np.zeros((H_PAGE, W_PAGE), np.float32)
    img = Image.new("L", (W_PAGE, H_PAGE), 0); draw = ImageDraw.Draw(img)

def line(x0, y0, x1, y1, w=2):
    draw.line([(x0, y0), (x1, y1)], fill=255, width=w)

def rect(x0, y0, x1, y1, double=False):
    line(x0, y0, x1, y0); line(x1, y0, x1, y1); line(x1, y1, x0, y1); line(x0, y1, x0, y0)
    if double:
        line(x0 + 5, y0 + 5, x1 - 5, y0 + 5); line(x1 - 5, y0 + 5, x1 - 5, y1 - 5); line(x1 - 5, y1 - 5, x0 + 5, y1 - 5); line(x0 + 5, y1 - 5, x0 + 5, y0 + 5)

def arrow(x0, y0, x1, y1):
    line(x0, y0, x1, y1)
    v = np.array([x1 - x0, y1 - y0], float); v /= np.linalg.norm(v); n = np.array([-v[1], v[0]])
    for s in (1, -1):
        p = np.array([x1, y1]) - 14 * v + s * 8 * n
        line(x1, y1, p[0], p[1])

def text_box(text, x0, y0, x1, double=False):
    lines = wrap(text, x1 - x0 - 2 * PAD)
    hgt = len(lines) * LH + 2 * PAD - 6
    rect(x0, y0, x1, y0 + hgt, double)
    for i, ln in enumerate(lines):
        yb = y0 + PAD + 22 + i * LH
        for parts, wd, dx in ln:
            R.paste(canvas, parts, x0 + PAD + dx, yb)
    return y0 + hgt

def write(text, x, y, under=False):
    parts, wd = h.run(text); R.paste(canvas, parts, x, y)
    if under:
        line(x - 2, y + 7, x + wd + 4, y + 7)
    return wd

ROWS = [
    ("Rahmen: Gebet an Gott. Anselm glaubt schon und sucht Einsicht mit dem Verstand („Glaube sucht Verstehen“, Z. 1-6)", None),
    ("1. Definition: Gott ist „etwas, worüber hinaus Größeres nicht gedacht werden kann“ (Z. 7-8)", None),
    ("2. Gott ist im Verstand: auch der „Tor“, der sagt „Es ist kein Gott“, versteht diese Worte (Z. 8-14)",
     "Gaunilo (M2): Ein Wort verstehen heißt nicht, dass die Sache wirklich ist. Sonst hätte ich auch alles Falsche und Erfundene im Verstand (Z. 1-11)"),
    ("3. Unterscheidung: nur gedacht oder wirklich? Beispiel Maler: Bild erst im Kopf, nach dem Malen auch in Wirklichkeit (Z. 14-21)", None),
    ("4. Annahme: wirklich existieren ist größer als nur im Denken existieren (Z. 26-30)",
     "Kant (M3): Existenz ist keine Eigenschaft, die etwas größer macht. Vorgestellte 100 Taler mit allen Eigenschaften, trotzdem keins in der Tasche (Z. 1-15)"),
    ("5. Gegenannahme: Gott existiert nur im Denken (Z. 30-31)", None),
    ("6. Widerspruch: dann könnte man etwas Größeres denken (denselben Gott, aber wirklich). Das Größte wäre nicht das Größte (Z. 31-34)", None),
    ("7. Schluss: Gott existiert im Denken und in Wirklichkeit (Z. 34-37)",
     "Gaunilo: verschwundene Insel = vortrefflichste aller Inseln. Nach Anselms Muster müsste sie existieren. Absurd, der Beweis beweist zu viel (Z. 11-42). Kant: aus einer Vorstellung entsteht keine Realität. Bewiesen ist nur, dass Gott möglich ist, nicht dass er existiert (Z. 15-25)"),
    ("8. Verschärfung: Gott kann nicht einmal als nicht existierend gedacht werden. Alles andere schon (Z. 38-64)", None),
    ("Ergebnis Anselm: Gott existiert notwendig",
     "Ergebnis Kritik: vom Denken kann man nicht auf das Sein schließen"),
]

new_page()
write("Ethik", 50, GRID0 + GRID); wd = h.run("26.11.26")[1]; write("26.11.26", 1360 - wd, GRID0 + GRID)
write("Der ontologische Gottesbeweis: Schaubild (A1 + A2)", 50, GRID0 + 3 * GRID, under=True)
write("links Anselm (M1), rechts die Einwände von Gaunilo (M2) und Kant (M3)", 50, GRID0 + 4 * GRID + 10)
y = GRID0 + 5 * GRID + 4
prev_left_bottom = None
for i, (left, right) in enumerate(ROWS):
    hl = box_h(left, LX0, LX1) if left else 0
    hr = box_h(right, RX0, RX1) if right else 0
    need = max(hl, hr) + 50
    if y + need > H_PAGE - 40:
        new_page(); y = GRID0 + 2 * GRID; prev_left_bottom = None
    if left:
        if prev_left_bottom is not None:
            cx = (LX0 + LX1) // 2
            arrow(cx, prev_left_bottom + 4, cx, y + 26)
            y += 30
        last = i == len(ROWS) - 1
        bot = text_box(left, LX0, y, LX1, double=last)
        prev_left_bottom = bot
    else:
        bot = y
    if right:
        ry = y if left else y + 4
        rbot = text_box(right, RX0, ry, RX1, double=(i == len(ROWS) - 1))
        if i != len(ROWS) - 1:
            ym = ry + min(40, (rbot - ry) // 2)
            target_y = ym if left else ry - 30
            arrow(RX0 - 6, ym, LX1 + 8, target_y if left else max(prev_left_bottom - 20, ym - 60))
        bot = max(bot, rbot)
    y = bot + 14
    if not left:
        prev_left_bottom = prev_left_bottom
pages.append((canvas, img))

out = sys.argv[1]
for k, (c, im) in enumerate(pages, 1):
    c = np.maximum(c, np.asarray(im, np.float32) / 255)
    np.save(f"{out}_p{k}_alpha.npy", c)
    bg = np.full((H_PAGE, W_PAGE, 3), 255, np.uint8)
    for i in range(0, (W_PAGE - GRID0) // GRID + 1):
        bg[:, GRID0 + i * GRID] = 205
    for i in range(0, (H_PAGE - GRID0) // GRID + 1):
        bg[GRID0 + i * GRID, :] = 205
    ink = np.clip(c, 0, 1)[..., None]
    Image.fromarray((bg * (1 - ink) + np.array([18, 18, 23]) * ink).astype(np.uint8)).save(f"{out}_p{k}.png")
print(len(pages), "Seiten")
# Linien aus dem PIL-Bild in die Seiten einfügen: jede Seite hat ihr eigenes Bild -> neu zeichnen
