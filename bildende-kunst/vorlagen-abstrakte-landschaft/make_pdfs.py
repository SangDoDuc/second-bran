"""Druckvorlagen A4 quer für Kunst (abstrakte Landschaft) + Übersicht.

Pro Motiv eine PDF mit 3 Seiten:
  1. ganzes Bild (zum Vergleich / falls die Lehrerin selbst schneiden lässt)
  2. Bild auf 2/3, das freie Drittel an der empfohlenen Seite (gerade Kante)
  3. dasselbe, freies Drittel auf der anderen Seite
Bild randlos bis auf 5 mm Druckrand, Seitenverhältnis bleibt (zugeschnitten, nicht verzerrt).
"""
import json
import sys

from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

HERE = sys.argv[1].rstrip("/") + "/"
OUT = sys.argv[2].rstrip("/") + "/"
pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
W, H = landscape(A4)
M = 14.17  # 5 mm

MOTIVE = [
    ("lavendel", "Lavendelfeld (Valensole, Provence)", "rechts",
     "Die Lavendelreihen laufen wie Strahlen auf einen Punkt zu. Du verlängerst die Streifen ins freie Drittel und machst sie dort immer freier: Wellen, Farbbänder in Lila, Blau, Ocker.",
     "mittel", "Fluchtlinien sauber weiterführen, Lila-Töne mischen"),
    ("tulpen", "Tulpenfelder (Sint-Gillis-Waas, Belgien)", "rechts",
     "Rote, gelbe und weiße Streifen in Perspektive. Im freien Drittel werden aus den Reihen reine Farbbahnen: perfekt für einen klaren Übergang vom Foto zur Abstraktion.",
     "leicht bis mittel", "kräftige Grundfarben, gerade Bahnen"),
    ("duenen", "Dünen im Abendlicht (Namib-Naukluft, Namibia)", "oben",
     "Fast schon abstrakt: große Farbflächen in Rot, Orange und Violett mit weichen Kanten. Lass das obere Drittel frei und setze die Farbschichten als Bänder fort.",
     "mittel bis anspruchsvoll", "weiche Farbverläufe (nass in nass), warme Töne"),
    ("reisterrassen", "Reisterrassen (Longsheng, China)", "links",
     "Viele geschwungene Linien, die wie Höhenlinien wirken. Im freien Drittel nimmst du nur noch die Kurven und Farben (Gold, Grün, Braun) auf. Wirkt sehr anspruchsvoll.",
     "anspruchsvoll", "viele Linien, Geduld beim Übergang"),
    ("toskana", "Sonnenuntergang über der Val d'Orcia (Toskana)", "oben",
     "Himmel mit Verlauf von Gelb über Orange zu Violett, darunter Hügelschichten. Das freie obere Drittel wird ein abstrakter Farbhimmel: Verlauf + Formen.",
     "mittel", "Farbverlauf im Himmel, Schichten der Hügel"),
    ("polarlicht", "Polarlicht über den Lofoten (Norwegen)", "rechts",
     "Grüne und violette Lichtbänder auf Dunkelblau. Im freien Drittel malst du die Schwünge frei weiter. Dunkler Grund + leuchtende Farben wirkt stark, ist aber anspruchsvoll.",
     "anspruchsvoll", "dunkler Hintergrund zuerst, dann Leuchtfarben in Schichten"),
]


def crop_to(img, ratio):
    """Bild mittig auf Seitenverhältnis ratio (B/H) zuschneiden."""
    w, h = img.size
    if w / h > ratio:
        nw = int(h * ratio)
        x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = int(w / ratio)
    y = (h - nh) // 2
    return img.crop((0, y, w, y + nh))


def draw_img(c, img, x, y, w, h, dpi=240):
    """Als JPEG einbetten (sonst landen die Pixel unkomprimiert in der PDF), höchstens 300 dpi."""
    import io
    im = crop_to(img, w / h)
    maxw = int(w / 72 * dpi)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    buf.seek(0)
    c.drawImage(ImageReader(buf), x, y, w, h)


def part(c, img, free):
    """2/3 Bild, 1/3 frei. free: links/rechts/oben/unten."""
    iw, ih = W - 2 * M, H - 2 * M
    if free in ("links", "rechts"):
        bw = iw * 2 / 3
        src = img.crop((0, 0, int(img.width * 2 / 3), img.height)) if free == "rechts" else \
            img.crop((int(img.width / 3), 0, img.width, img.height))
        x = M if free == "rechts" else M + iw / 3
        draw_img(c, src, x, M, bw, ih)
    else:
        bh = ih * 2 / 3
        src = img.crop((0, int(img.height / 3), img.width, img.height)) if free == "oben" else \
            img.crop((0, 0, img.width, int(img.height * 2 / 3)))
        y = M if free == "oben" else M + ih / 3
        draw_img(c, src, M, y, iw, bh)


OTHER = {"rechts": "links", "links": "rechts", "oben": "unten", "unten": "oben"}
meta = json.load(open(HERE + "meta.json"))
done = []
for key, name, free, idea, level, focus in MOTIVE:
    try:
        img = Image.open(HERE + f"full/{key}.jpg").convert("RGB")
    except Exception:
        print("fehlt:", key)
        continue
    full = crop_to(img, (W - 2 * M) / (H - 2 * M))
    c = Canvas(OUT + f"Vorlage_{key}_A4.pdf", pagesize=(W, H))
    c.setTitle(f"Vorlage {name}")
    for mode in (None, free, OTHER[free]):
        if mode is None:
            draw_img(c, full, M, M, W - 2 * M, H - 2 * M)
        else:
            part(c, full, mode)
        c.showPage()
    c.save()
    done.append((key, name, free, idea, level, focus))
    print("ok", key)

# Übersicht: ein Motiv pro Zeile, Bild links, Text rechts, 3 pro Seite
def wrap(c, text, font, size, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if c.stringWidth(t, font, size) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = t
    lines.append(cur)
    return lines


c = Canvas(OUT + "Uebersicht_Vorlagen_abstrakte_Landschaft.pdf", pagesize=(W, H))
c.setTitle("Vorlagen abstrakte Landschaft")


def header(c, page):
    c.setFont("DVB", 17)
    c.drawString(40, H - 45, "Vorlagen: abstrakte Landschaft (Acryl, 1/3 frei)" + ("" if page == 0 else " – Fortsetzung"))
    c.setFont("DV", 9.5)
    c.drawString(40, H - 62, "Je Motiv eine Druck-PDF (A4 quer): Seite 1 ganzes Bild, Seite 2 Drittel frei (Empfehlung), Seite 3 Drittel frei (andere Seite).")


header(c, 0)
ROW = 160
for i, (key, name, free, idea, level, focus) in enumerate(done):
    if i and i % 3 == 0:
        c.showPage()
        header(c, 1)
    r = i % 3
    top = H - 80 - r * ROW
    tw, th = 210, 140
    img = Image.open(HERE + f"full/{key}.jpg").convert("RGB")
    draw_img(c, img, 40, top - th, tw, th, dpi=150)
    x, width = 40 + tw + 18, W - (40 + tw + 18) - 40
    y = top - 12
    c.setFont("DVB", 12)
    c.drawString(x, y, f"{i + 1}. {name}")
    y -= 17
    c.setFont("DV", 9.5)
    for ln in wrap(c, idea, "DV", 9.5, width):
        c.drawString(x, y, ln)
        y -= 12.5
    y -= 4
    c.setFont("DVB", 9.5)
    c.drawString(x, y, f"Freies Drittel: {free}      Niveau: {level}")
    y -= 13
    c.setFont("DV", 9.5)
    c.drawString(x, y, f"Worauf es ankommt: {focus}")
    y -= 15
    m = meta[key]
    c.setFont("DV", 7.5)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(x, y, f"Foto: {m['artist']} | {m['license']} | Wikimedia Commons: {m['title']}"[:140])
    c.setFillColorRGB(0, 0, 0)
c.showPage()
c.save()
print("Übersicht mit", len(done), "Motiven")
