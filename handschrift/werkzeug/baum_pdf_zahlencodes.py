"""Sauberes Baumdiagramm mit Erklärung (IQB 2026 Stochastik 2.2, Zahlencodes) als A4-PDF, 2 Seiten."""
import re
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

OUT = sys.argv[1]
F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
W, H = A4
BLUE, GREEN, RED, GREY = (0.04, 0.37, 0.82), (0.10, 0.54, 0.18), (0.75, 0.22, 0.17), (0.35, 0.35, 0.35)


def txt(c, x, y, s, size=11, bold=False, color=(0, 0, 0)):
    c.setFont("DVB" if bold else "DV", size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, s)


def tbar(c, x, y, size=13):
    """T mit Überstrich."""
    c.setFont("DVB", size); c.setFillColorRGB(0, 0, 0); c.drawString(x, y, "T")
    w = c.stringWidth("T", "DVB", size)
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(1.2); c.line(x, y + size * 0.86, x + w, y + size * 0.86)


MAXW = W - 100


def para(c, x, y, lines, size=10.5, lead=15, color=(0, 0, 0)):
    """Absätze mit Zeilenumbruch. Eine Zeile, die mit **Label** beginnt, bekommt das Label fett."""
    for ln in lines:
        label, rest = "", ln
        m = re.match(r"\*\*(.+?)\*\*(.*)", ln)
        if m:
            label, rest = m.group(1), m.group(2)
        cx = x
        if label:
            txt(c, cx, y, label, size, True, color)
            cx += c.stringWidth(label, "DVB", size) + 4
        words = rest.split(" ")
        line = ""
        while words:
            w = words.pop(0)
            test = (line + " " + w).strip() if line else w
            if cx + c.stringWidth(test, "DV", size) > x + MAXW and line:
                txt(c, cx, y, line, size, False, color)
                y -= lead
                cx, line = x, w
            else:
                line = test
        txt(c, cx, y, line, size, False, color)
        y -= lead
    return y


def tree(c, x0, yc, dx1=105, dx2=105, dy1=72, dy2=32, label_paths=True, mark=False):
    """Zweistufiger Baum. Gibt die y-Positionen der 4 Endknoten zurück."""
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(1.6)
    c.setFillColorRGB(0, 0, 0); c.circle(x0, yc, 3, fill=1)
    ends = []
    for s1, top in ((+1, True), (-1, False)):
        x1, y1 = x0 + dx1, yc + s1 * dy1
        c.line(x0 + 4, yc + s1 * 3, x1 - 14, y1)
        mx, my = (x0 + x1) / 2, (yc + y1) / 2
        txt(c, mx - 22 - (0 if top else 10), my + (8 if top else -18), "p" if top else "1 − p", 11, True, BLUE)
        if top:
            txt(c, x1 - 9, y1 - 5, "T", 13, True)
        else:
            tbar(c, x1 - 9, y1 - 5)
        for s2, top2 in ((+1, True), (-1, False)):
            x2, y2 = x1 + dx2, y1 + s2 * dy2
            c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(1.6)
            c.line(x1 + 8, y1 + s2 * 3, x2 - 14, y2)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            txt(c, mx - 10 - (0 if top2 else 10), my + (7 if top2 else -16), "p" if top2 else "1 − p", 11, True, BLUE)
            if top2:
                txt(c, x2 - 9, y2 - 5, "T", 13, True)
            else:
                tbar(c, x2 - 9, y2 - 5)
            ends.append((top, top2, x2, y2))
    if label_paths:
        texts = {(True, True): ("p · p = p²", "beide", GREY),
                 (True, False): ("p · (1 − p)", "nur der erste", GREEN),
                 (False, True): ("(1 − p) · p", "nur der zweite", GREEN),
                 (False, False): ("(1 − p) · (1 − p) = (1 − p)²", "keiner", RED)}
        for top, top2, x2, y2 in ends:
            f, meaning, col = texts[(top, top2)]
            txt(c, x2 + 22, y2 - 4, f, 11)
            txt(c, x2 + 188, y2 - 4, meaning, 10, True, col if mark else GREY)
            if mark and (top, top2) == (False, False):
                c.setStrokeColorRGB(*RED); c.setLineWidth(2)
                c.line(x2 + 18, y2 - 8, x2 + 225, y2 + 3)
    return ends


# ------------------------------------------------------------------ Seite 1
c = Canvas(OUT, pagesize=A4)
txt(c, 50, H - 55, "Baumdiagramm: zwei Zahlencodes", 18, True)
txt(c, 50, H - 75, "IQB 2026, erhöhtes Niveau, Prüfungsteil A, Stochastik 2.2", 10, False, GREY)

y = H - 105
y = para(c, 50, y, [
    "**Die Situation**",
    "Ein Zufallsgenerator erzeugt zwei Zahlencodes. Jeder Code enthält eine bestimmte Ziffernfolge mit Wahrscheinlichkeit p, unabhängig vom anderen Code.",
    "T = „Code enthält die Folge“ mit P(T) = p. Das Gegenereignis (T mit Überstrich) = „enthält sie nicht“ mit 1 − p.",
])

y -= 6
txt(c, 60, y, "1. Stufe: erster Code", 9, False, GREY)
txt(c, 165, y, "2. Stufe: zweiter Code", 9, False, GREY)
txt(c, 292, y, "Pfadwahrscheinlichkeit", 9, False, GREY)
txt(c, 445, y, "Bedeutung", 9, False, GREY)
yc = y - 12 - 72 - 32 - 8
tree(c, 60, yc)
y = yc - 72 - 32 - 30
y = para(c, 50, y, [
    "**So liest man den Baum**",
    "1.  Links die Wurzel: noch ist nichts passiert.",
    "2.  Erste Verzweigung = erster Code. Zwei Äste: T mit p, T mit Überstrich mit 1 − p.",
    "3.  Zweite Verzweigung = zweiter Code. Die Codes sind unabhängig, darum hängen an jedem Knoten wieder dieselben Äste mit denselben Wahrscheinlichkeiten.",
    "4.  Kontrolle an jedem Knoten: p + (1 − p) = 1. Die Äste eines Knotens ergeben immer zusammen 1.",
    "",
    "**Pfadregel (Multiplikation)**",
    "Ein Weg von der Wurzel bis ganz rechts ist ein möglicher Ausgang. Seine Wahrscheinlichkeit ist das Produkt der Äste auf dem Weg. Beispiel oberster Pfad: p · p = p².",
    "",
    "**Summenregel (Addition)**",
    "Ein Ereignis, zu dem mehrere Pfade gehören, bekommt die Summe dieser Pfade.",
    "„Genau einer“ = zweiter und dritter Pfad:  p(1 − p) + (1 − p)p.",
    "",
    "**Kontrolle:** Alle vier Pfade zusammen ergeben 1:  p² + p(1 − p) + (1 − p)p + (1 − p)² = (p + (1 − p))² = 1.",
    "",
    "**Teilaufgabe a) mit p = 0,1:**  P(genau einer) = 0,1 · 0,9 + 0,9 · 0,1 = 2 · 0,1 · 0,9 = 0,18.",
    "Typischer Fehler: nur einen der beiden Pfade nehmen (0,09). Beide Reihenfolgen zählen.",
])
c.showPage()

# ------------------------------------------------------------------ Seite 2
txt(c, 50, H - 55, "b) Bedingte Wahrscheinlichkeit am Baum", 18, True)
y = H - 85
y = para(c, 50, y, [
    "**Aufgabe:** Mindestens einer der beiden Codes enthält die Ziffernfolge. Gesucht ist ein Term für die Wahrscheinlichkeit, dass die Folge nicht in beiden Codes enthalten ist.",
    "",
    "**Zwei Ereignisse benennen**",
    "A = „mindestens einer enthält die Folge“   →  die Bedingung (das wissen wir schon)",
    "B = „nicht beide enthalten die Folge“       →  das Gesuchte (= höchstens einer)",
])

y -= 16
yc = y - 72 - 32 - 8
ends = tree(c, 60, yc, mark=True)
# Markierungen: Nenner-Rahmen (obere drei Pfade), Zähler-Rahmen (mittlere zwei)
xs = ends[0][2] + 16
ys = sorted(e[3] for e in ends)            # 4 y-Werte aufsteigend
c.setStrokeColorRGB(*BLUE); c.setLineWidth(1.2); c.setDash(4, 3)
c.roundRect(xs, ys[1] - 12, 290, ys[3] - ys[1] + 26, 6)
txt(c, xs + 4, ys[3] + 18, "Nenner: A = „mindestens einer“ = obere drei Pfade", 9, True, BLUE)
c.setStrokeColorRGB(*GREEN); c.setLineWidth(1.2)
c.roundRect(xs + 3, ys[1] - 8, 284, ys[2] - ys[1] + 18, 6)
txt(c, xs + 4, ys[1] - 22, "Zähler: A ∩ B = „genau einer“ = mittlere zwei Pfade", 9, True, GREEN)
c.setDash()
txt(c, xs + 4, ys[0] - 20, "fällt weg: „keiner“ widerspricht der Bedingung", 9, True, RED)

y = yc - 72 - 32 - 36
y = para(c, 50, y, [
    "**Schritt 1: Die Bedingung streicht einen Pfad.**",
    "Wir wissen, dass mindestens ein Treffer da ist. Der unterste Pfad „keiner“ kann also nicht passiert sein. Er wird gestrichen. Übrig bleiben die oberen drei Pfade.",
    "",
    "**Schritt 2: Nenner P(A).**",
    "Die drei übrigen Pfade zusammen. Am schnellsten über das Gegenereignis „keiner“:",
    "P(A) = 1 − P(keiner) = 1 − (1 − p)²",
    "Typischer Fehler: 1 − p² schreiben. p² ist „beide“, und 1 − p² wäre P(B), nicht P(A).",
    "",
    "**Schritt 3: Zähler P(A ∩ B).**",
    "A und B gleichzeitig: mindestens einer, aber nicht beide. Das ist genau einer, also die zwei mittleren Pfade.",
    "P(A ∩ B) = p · (1 − p) + (1 − p) · p",
    "",
    "**Schritt 4: Teilen.**",
    "P_A(B) = P(A ∩ B) / P(A) = [ p(1 − p) + (1 − p)p ] / [ 1 − (1 − p)² ]",
    "Warum teilen: Nach dem Streichen ergeben die drei Pfade nicht mehr 1, sondern 1 − (1 − p)². Durch das Teilen wird der Baum auf die neue Welt umgerechnet, in der A sicher ist. Das ist genau der Term im Erwartungshorizont.",
    "",
    "**Probe mit p = 0,1:**  Zähler 0,18, Nenner 1 − 0,81 = 0,19, also 0,18 / 0,19 ≈ 0,947.",
    "Plausibel: Wenn Treffer selten sind, ist bei „mindestens einer“ fast immer nur einer dabei.",
    "",
    "**Zum Vergleich ohne Bedingung:**  P(B) = 1 − p² = 0,99 für p = 0,1. Die Bedingung ändert das Ergebnis deutlich.",
], size=9.8, lead=13.2)
c.showPage()
c.save()
print("ok", OUT)
