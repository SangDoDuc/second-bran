"""Schriftprobe-Vorlage v2 für Sangs Handschrift: .goodnotes (Hauptweg) + PDF (Ausweichweg) + layout.json.

Raster = dasselbe Karo wie in allen Handschrift-Dateien (Zelle 38 px auf 1414 px = 16 pt), Schreiblinie auf einer
Rasterlinie. layout.json beschreibt jede Schreibfläche in pt (Ursprung oben links, y nach unten), damit die Striche
der ausgefüllten Datei automatisch dem richtigen Zeichen/Wort zugeordnet werden.

v2 nach Prüfung (Usability, Extraktion, Abdeckung) am 28.10.2026:
- Reihenfolge nach Wert (Sätze -> Buchstaben/Ziffern/Zeichen -> Mathe -> Wörter), Abbruch nach jeder Seite möglich
- Anleitung: Kugelschreiber schwarz, keine KI-Korrektur/Formerkennung/Teil-Radierer, Export PDF "Bearbeitbar" + GoodNotes
- Mathe in Klausur-Form gedruckt (Spaltenvektor, Bruch, Pfeil, Wurzelstrich, Integralgrenzen, Binomialkoeffizient)
- hohe Felder +-3 Kästchen mit Bezug "mittlere Zeile auf der Linie", Kalibrierpunkte, Vorlagen-ID in der Kopfzeile

cd handschrift/vorlage && python3 make_vorlage.py OUT_DIR    (braucht reportlab, lz4; PyMuPDF nur für Vorschaubilder)
"""
import hashlib
import io
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "werkzeug"))   # gn_writer

from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
TEMPLATE_ID = "SP-v2"
PW, PH = A4
SX, SY = PW / 1414, PH / 2000
CELL = 38 * SX
COL0, COL1 = 1, 35            # nutzbare Rasterspalten
ROW_LAST = 49                 # letzte erlaubte Grundlinie (Rasterzeile)
BLUE = (0.16, 0.38, 0.78)
NAME = (0.42, 0.48, 0.62)
LIGHT = (0.55, 0.70, 0.95)
DARK = (0.10, 0.20, 0.50)
SEP = 0.62
LABEL_PT = 9.5
GN_SCALE = 132 / 72

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


def gx(k):
    return (37 + 38 * k) * SX


def gy(k):
    return (37 + 38 * k) * SY


def Y(y):
    return PH - y


def tw(text, size=LABEL_PT, font="DV"):
    return pdfmetrics.stringWidth(text, font, size)


# ----------------------------------------------------------------------------- Inhalt
INSTRUCTIONS = [
    "Vorher: Rechtschreibprüfung für Handschrift ausschalten (falls vorhanden). Nie einen roten Vorschlag antippen, kein Lasso, kein Restyle.",
    "Stift: Kugelschreiber (nicht Füller, Pinsel, Bleistift, Textmarker), Farbe Schwarz, Dicke wie sonst. Gleiche Zoomstufe wie beim Mitschreiben.",
    "So klein und so schnell wie im Unterricht, nicht schöner. Die Felder sind extra groß – du musst sie nicht füllen.",
    "Rechts neben die blaue Vorlage auf die hellblaue Linie. Zwischen zwei gestrichelten Linien genau EIN Zeichen bzw. Wort. Nichts kopieren.",
    "Verschrieben? Rückgängig (2 Finger tippen) oder Radierer auf „Ganzer Strich“. Am Strichende nicht stehen bleiben (sonst gerade Form).",
    "Zeichen, die du nie benutzt: leer lassen. Aufhören nach jeder Seite möglich – Seite 1–3 sind am wichtigsten. Dauer ca. 25–30 Minuten.",
    "Fertig (am iPad): Teilen → Exportieren → alle Seiten → PDF „Bearbeitbar“ (Anmerkungen an) UND als GoodNotes → beide an Claude.",
]
SENTENCES = [
    "Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich.",
    "– Wenn die Spannung steigt, wird das Feld stärker, weil E = U/d gilt.",
    "– Warum liegen A und C gegenüber? AC geht durch M, also keine Kante → Diagonale.",
    "Laut Abb. 3 steigt der Anteil seit 2019 (ca. 43 %), z.B. in den USA.",
    "Bei einem Angriff auf ein NATO-Mitglied gilt Art. 5, d.h. alle helfen.",
    "I think it's clear: technology helps, but the causes haven't changed.",
    "Also gilt: |^AC| = a = 12, und E(3|0|9) liegt 6 von H entfernt.",
]
SPECIAL = [  # (id, Vorlage, Schreibbreite in Spalten)
    ("header", "Mathe          29.10.26", 12),
    ("underline", "Schritt 1: Mittelpunkt M   (unterstreichen)", 12),
]
UPPER = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LOWER = list("abcdefghijklmnopqrstuvwxyz")
DIGITS = list("0123456789")
NUMBERS = ["29.10.26", "1954", "1990", "2019", "2024", "43 %", "7,5", "0,25", "9,81", "−17", "1,6 · 10⁻¹⁹", "3,14"]
PUNCT = [(".", ""), (",", ""), (":", ""), ("?", ""), ("!", ""), ("-", "Bindestrich"), ("(", ""), (")", ""),
         ("„", "unten"), ("“", "oben"), ("'", "Apostroph"), ("/", ""), ("%", "")]
SYMBOLS = [("+", "", 2), ("−", "Minus", 2), ("·", "Malpunkt", 2), ("×", "Kreuzprodukt", 2), ("=", "", 2),
           ("≈", "", 2), ("≠", "", 2), ("±", "", 2), ("<", "", 2), (">", "", 2), ("≤", "", 2), ("≥", "", 2),
           ("→", "Pfeil", 4), ("⇒", "", 2), ("⇔", "", 2), ("°", "Grad", 2), ("|", "Strich", 2), ("√", "", 2),
           ("π", "", 2), ("∞", "", 2), ("∫", "", 2), ("Δ", "", 2), ("∈", "Element", 2), ("ℝ", "", 2),
           ("⊥", "senkrecht", 2), ("∥", "parallel", 2), ("∩", "", 2), ("∪", "", 2), ("α", "", 2), ("β", "", 2),
           ("γ", "", 2), ("ε", "", 2), ("λ", "", 2), ("μ", "", 2), ("σ", "", 2), ("φ", "", 2), ("ω", "", 2),
           ("Ω", "", 2)]
# Mathe-Ausdrücke in Klausur-Form. Auszeichnung für die gedruckte Vorlage:
#   ^AB  Pfeil über AB | √{...} Wurzel mit Strich | F{a}{b} Bruch übereinander | V{a;b;c} Spaltenvektor
#   I{u}{o} Integralzeichen mit Grenzen | G{u}{o} Grenzen hinter ] | B{n}{k} Binomialkoeffizient
MATH_TALL = [
    ("vec_ac", "^AC = V{−4;−8;8}", 9),
    ("vec_n", "^n = V{2;1;2}", 8),
    ("vec_om", "^OM = F{1}{2}·V{1−3;2−6;1+9}", 11),
    ("frac", "x = F{1}{2}    y = F{a}{2}", 9),
    ("integral", "I{0}{2} x² dx = [F{1}{3}x³]G{0}{2}", 12),
    ("binom", "P = B{5}{3} · 0,5⁵", 9),
]
MATH_FLAT = [
    ("plane", "H: 2x₁ + x₂ + 2x₃ = 6", 12),
    ("points", "C(−3|−6|9)    M(−1|−2|5)", 13),
    ("abs", "|^AC| = √{144} = 12", 10),
    ("sqrt_sum", "√{16 + 64 + 64}", 9),
    ("mid", "^OM = 1/2·(^OA + ^OC)", 12),
    ("edge", "|^AB| = a/√2 = 6·√2", 11),
    ("func", "f(x) = 2x² − 3x + 1", 11),
    ("deriv", "f'(x) = 4x − 3", 9),
    ("exp", "f(x) = 3·e⁻²ˣ    x = ln(5)/2", 14),
    ("stoch", "P(X ≤ 3) ≈ 0,65", 9),
    ("logic", "2x = 4 ⇔ x = 2    π ≈ 3,14", 14),
    ("phys", "F = q·E    W = q·U", 10),
    ("const", "ε₀    μ₀    λ = 500 nm", 11),
    ("units", "km²    m/s²    20 °C", 11),
]


# ----------------------------------------------------------------------------- gedruckte Mathe-Auszeichnung
def _arg(s, i):
    """liest {…} ab Position i (s[i] == '{'), gibt (Inhalt, Ende) zurück."""
    depth, j = 0, i
    while True:
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1


def markup(c, s, x, base, size=LABEL_PT, draw=True):
    """zeichnet (oder misst) eine Mathe-Auszeichnung ab x auf Grundlinie base; gibt die Breite zurück."""
    x0 = x
    small = size * 0.72
    if draw:
        c.setStrokeColorRGB(*BLUE)
        c.setFillColorRGB(*BLUE)
        c.setLineWidth(0.75)

    def put(t, xx, yy, sz=size):
        if draw:
            c.setFont("DV", sz)
            c.drawString(xx, Y(yy), t)
        return tw(t, sz)

    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "^" and i + 1 < len(s) and s[i + 1].isalpha():
            j = i + 1
            while j < len(s) and s[j].isalpha() and s[j].isupper() == s[i + 1].isupper() and (s[i + 1].isupper() or j == i + 1):
                j += 1
            name = s[i + 1:j]
            w = put(name, x, base)
            if draw:
                ya = base - size * 1.02
                c.line(x + 0.5, Y(ya), x + w, Y(ya))
                c.line(x + w, Y(ya), x + w - 2.6, Y(ya - 1.8))
                c.line(x + w, Y(ya), x + w - 2.6, Y(ya + 1.8))
            x += w
            i = j
        elif s.startswith("√{", i):
            inner, j = _arg(s, i + 1)
            w0 = put("√", x, base)
            w1 = markup(c, inner, x + w0 + 0.5, base, size, draw)
            if draw:
                c.line(x + w0 - 0.6, Y(base - size * 0.93), x + w0 + w1 + 1.5, Y(base - size * 0.93))
            x += w0 + w1 + 2
            i = j
        elif s[i] in "FBGI" and i + 1 < len(s) and s[i + 1] == "{":
            a, j = _arg(s, i + 1)
            b, k = _arg(s, j)
            if s[i] == "F":
                wa, wb = markup(c, a, 0, 0, small, False), markup(c, b, 0, 0, small, False)
                w = max(wa, wb) + 3
                markup(c, a, x + (w - wa) / 2, base - size * 0.42, small, draw)
                markup(c, b, x + (w - wb) / 2, base + size * 0.62, small, draw)
                if draw:
                    c.line(x + 0.5, Y(base - size * 0.3), x + w - 0.5, Y(base - size * 0.3))
                x += w + 1.5
            elif s[i] == "B":
                wa, wb = tw(a, small), tw(b, small)
                w = max(wa, wb) + 2
                if draw:
                    for side, xx in ((-1, x + 3), (1, x + 5 + w)):
                        p = c.beginPath()
                        p.moveTo(xx, Y(base - size * 1.05))
                        p.curveTo(xx + side * 2.6, Y(base - size * 0.6), xx + side * 2.6, Y(base + size * 0.35),
                                  xx, Y(base + size * 0.75))
                        c.drawPath(p, stroke=1, fill=0)
                put(a, x + 4 + (w - wa) / 2, base - size * 0.42, small)
                put(b, x + 4 + (w - wb) / 2, base + size * 0.62, small)
                x += w + 8
            elif s[i] == "I":
                w = put("∫", x, base + size * 0.15, size * 1.45)
                put(a, x + w * 0.55, base + size * 0.7, small * 0.9)
                put(b, x + w * 0.95, base - size * 0.95, small * 0.9)
                x += w + tw(b, small) + 1
            else:   # G: Grenzen hinter ]
                put(b, x + 0.5, base - size * 0.7, small * 0.9)
                put(a, x + 0.5, base + size * 0.35, small * 0.9)
                x += max(tw(a, small), tw(b, small)) + 1.5
            i = k
        elif s.startswith("V{", i):
            inner, j = _arg(s, i + 1)
            ents = inner.split(";")
            w = max(tw(e, size) for e in ents) + 3
            ys = [base - 0.62 * CELL, base, base + 0.62 * CELL]
            top, bot = ys[0] - 0.55 * CELL, ys[2] + 0.25 * CELL
            if draw:
                for side, xx in ((-1, x + 4), (1, x + 6 + w)):
                    p = c.beginPath()
                    p.moveTo(xx, Y(top))
                    p.curveTo(xx + side * 4, Y(top + 6), xx + side * 4, Y(bot - 6), xx, Y(bot))
                    c.drawPath(p, stroke=1, fill=0)
            for e, yy in zip(ents, ys):
                put(e, x + 5 + (w - tw(e, size)) / 2, yy + 3)
            x += w + 11
            i = j
        else:
            j = i
            while j < len(s) and not (s[j] == "^" and j + 1 < len(s) and s[j + 1].isalpha()) \
                    and not s.startswith("√{", j) and not (s[j] in "FBGIV" and j + 1 < len(s) and s[j + 1] == "{"):
                j += 1
            x += put(s[i:j], x, base)
            i = j
    return x - x0


def plain(s):
    """Text ohne Auszeichnung (für layout.json)."""
    out, i = "", 0
    while i < len(s):
        if s[i] == "^" and i + 1 < len(s) and s[i + 1].isalpha():
            out += "→"
            i += 1
        elif s[i] in "FBGIV√" and i + 1 < len(s) and s[i + 1] == "{":
            kind = s[i]
            a, j = _arg(s, i + 1)
            if kind in "FBGI":
                b, j = _arg(s, j)
                out += {"F": f"({a})/({b})", "B": f"({a} über {b})", "G": f"_{a}^{b}", "I": f"∫_{a}^{b}"}[kind]
            else:
                out += f"({a.replace(';', '|')})" if kind == "V" else f"√({a})"
            i = j
        else:
            out += s[i]
            i += 1
    return out


# ----------------------------------------------------------------------------- Layout
class Layout:
    def __init__(self):
        self.pages = []
        self.new_page(first=True)

    def new_page(self, first=False):
        self.page = {"index": len(self.pages) + 1, "items": [], "draw": [], "printed": []}
        self.pages.append(self.page)
        self.row = 4 if not first else 4
        self.col = COL0
        self.mode = None

    def ensure(self, rows_below):
        if self.row + rows_below > ROW_LAST:
            self.new_page()
            self.row = 4

    def next_line(self, step=2):
        self.row += step
        self.col = COL0

    def heading(self, title, sub=None, gap=3):
        self.next_line(gap if self.col != COL0 or self.page["items"] else 1)
        self.ensure(3)
        self.page["draw"].append(("heading", title, self.row, sub))
        self.page["printed"].append({"kind": "heading", "text": title, "baseline": round(gy(self.row), 2)})
        self.col = COL0
        self.row += 0          # erste Schreibzeile folgt mit next_line(2) im ersten slot()
        self.fresh = True

    def _place(self, total, tall):
        """Spalte/Zeile für ein Feld mit total Spalten; Zeilenwechsel, Seitenwechsel."""
        step = 6 if tall else 2
        if getattr(self, "fresh", False):
            self.fresh = False
            self.next_line(4 if tall else 2)
        elif self.col + total > COL1:
            self.next_line(step)
        self.mode = tall
        self.ensure(3 if tall else 1)
        if self.row < 6:
            self.row = 6 if not tall else 7

    def slot(self, sid, part, kind, label, n_cells=1, write_cols=None, cell_cols=2, tall=False, text=None,
             name="", reps=1):
        if label.startswith("§M"):
            lab_w = markup(None, label[2:], 0, 0, LABEL_PT, draw=False)
        else:
            lab_w = tw(label) + (tw(" " + name, 6.2) if name else 0)
        lab_cols = max(1, math.ceil((lab_w + 5) / CELL))
        wcols = write_cols if write_cols else n_cells * cell_cols
        total = lab_cols + wcols
        self._place(total, tall)
        r = self.row
        base = gy(r)
        band = (base - 3 * CELL, base + 3 * CELL) if tall else (base - 1.5 * CELL, base + 0.5 * CELL)
        x0, xw, x1 = gx(self.col), gx(self.col + lab_cols), gx(self.col + total)
        if write_cols is None:
            boxes = [[gx(self.col + lab_cols + k * cell_cols), band[0], gx(self.col + lab_cols + (k + 1) * cell_cols), band[1]]
                     for k in range(n_cells)]
        else:
            boxes = [[xw, band[0], x1, band[1]]]
        item = {"id": sid, "part": part, "kind": kind, "text": text if text is not None else label,
                "label": label, "name": name, "reps": len(boxes) if write_cols is None else reps,
                "baseline": round(base, 2), "band": [round(band[0], 2), round(band[1], 2)],
                "anchor": "middle_row_on_baseline" if tall else "baseline",
                "boxes": [[round(v, 2) for v in b] for b in boxes],
                "label_box": [round(x0, 2), round(band[0], 2), round(xw, 2), round(band[1], 2)], "tall": tall}
        self.page["items"].append(item)
        self.col += total
        return item

    def sentence(self, sid, text):
        """Vorlage über der Linie (im Zwischenraum), Schreiblinie über die ganze Breite; 3 Rasterzeilen je Satz."""
        if getattr(self, "fresh", False):
            self.fresh = False
            self.row += 3
        else:
            self.next_line(3)
        self.ensure(1)
        base = gy(self.row)
        self.page["draw"].append(("prompt", text, base - 1.72 * CELL))
        band = (base - 1.5 * CELL, base + 0.5 * CELL)
        self.page["items"].append({"id": sid, "part": "1", "kind": "sentence", "text": plain(text), "label": text,
                                   "name": "", "reps": 1, "baseline": round(base, 2),
                                   "band": [round(band[0], 2), round(band[1], 2)], "anchor": "baseline",
                                   "boxes": [[round(gx(COL0), 2), round(band[0], 2), round(PW, 2), round(band[1], 2)]],
                                   "label_box": None, "tall": False})
        self.col = COL0

    def calib(self, sid, x, y):
        self.page["draw"].append(("calib", x, y))
        self.page["items"].append({"id": sid, "part": "K", "kind": "calib", "text": "Kalibrierpunkt",
                                   "center": [round(x, 2), round(y, 2)],
                                   "boxes": [[round(x - 12, 2), round(y - 12, 2), round(x + 12, 2), round(y + 12, 2)]],
                                   "label": "", "name": "", "reps": 1, "baseline": round(y, 2),
                                   "band": [round(y - 12, 2), round(y + 12, 2)], "anchor": "center",
                                   "label_box": None, "tall": False})


def build():
    L = Layout()
    pg = L.page
    pg["draw"].append(("title",))
    for k, t in enumerate(INSTRUCTIONS):
        pg["draw"].append(("instr", f"{k}. {t}" if k else f"0. {t}", 4 + k))
    L.calib("calib_p1", gx(33), gy(2) + 2)
    L.row = 4 + len(INSTRUCTIONS) - 1
    L.heading("Teil 1: Sätze", "einmal in normalem Tempo auf die Linie darunter abschreiben (mit Strich vorne, wo einer steht)", gap=3)
    for k, s in enumerate(SENTENCES):
        L.sentence(f"sent_{k}", s)
    L.heading("Kopfzeile und Überschrift", "so, wie du sie auf deinen Blättern schreibst", gap=3)
    for sid, lab, wc in SPECIAL:
        L.slot(f"special_{sid}", "1", "special", lab, write_cols=wc)
    L.heading("Teil 2: Buchstaben, Ziffern, Zeichen", "zwischen zwei gestrichelten Linien je 1 Zeichen, einzeln")
    for ch in UPPER:
        L.slot(f"upper_{ch}", "2", "letter", ch, 2)
    L.next_line(2)
    L.fresh = False
    for ch in LOWER:
        L.slot(f"lower_{ch}", "2", "letter", ch, 2)
    L.next_line(2)
    for ch in DIGITS:
        L.slot(f"digit_{ch}", "2", "digit", ch, 2)
    L.next_line(2)
    for ch, nm in PUNCT:
        L.slot(f"punct_U+{ord(ch):04X}", "2", "punct", ch, 2, name=nm, text=ch)
    L.heading("Zahlen", "genau so abschreiben")
    for k, t in enumerate(NUMBERS):
        L.slot(f"num_{k:02d}", "2", "number", t, write_cols=max(3, math.ceil(0.5 * len(t) + 1.5)))
    L.heading("Teil 3: Mathe-Zeichen", "zwischen zwei gestrichelten Linien je 1 Zeichen; nie benutzt → leer lassen")
    for ch, nm, reps in SYMBOLS:
        L.slot(f"sym_U+{ord(ch):04X}", "3", "symbol", ch, reps, name=nm, text=ch)
    L.heading("Mathe-Ausdrücke", "genau das abschreiben, was da steht – in deiner Klausur-Schrift")
    L.page["draw"].append(("note", "Hohe Felder: normaler Text (AC =, x =) auf die hellblaue Linie, Vektor und Bruch so hoch, wie du sie sonst setzt.", L.row + 1))
    L.row += 1
    for sid, m, wc in MATH_TALL:
        L.slot(f"math_{sid}", "3", "math", "§M" + m, write_cols=wc, tall=True, text=plain(m))
    L.next_line(5)
    for sid, m, wc in MATH_FLAT:
        L.slot(f"math_{sid}", "3", "math", "§M" + m, write_cols=wc, text=plain(m))
    words = json.load(open(HERE + "words_v2.json"))["items"]
    titles = {"de": ("Teil 4: Wörter", "jedes Wort einmal, genau wie du sonst schreibst (nichts extra verbinden oder trennen)"),
              "abbr": ("Abkürzungen", "mit Punkt, genau so"),
              "caps": ("Großbuchstaben-Wörter und Bindestriche", None),
              "en": ("Englisch", "jedes Wort einmal")}
    for grp in ("de", "abbr", "caps", "en"):
        L.heading(*titles[grp])
        for w in [i for i in words if i["group"] == grp]:
            wc = max(3, math.ceil(0.55 * len(w["text"]) + 1))
            if w["reps"] == 2:
                L.slot(f"word_{w['text']}", "4", "word", w["text"], 2, cell_cols=wc)
            else:
                L.slot(f"word_{w['text']}", "4", "word", w["text"], write_cols=wc)
    L.calib(f"calib_p{len(L.pages)}", gx(33), gy(50) + 2)
    return L.pages


# ----------------------------------------------------------------------------- Zeichnen
def draw_grid(c):
    c.setStrokeGray(0.80)
    c.setLineWidth(0.42)
    for k in range(0, (1414 - 37) // 38 + 1):
        x = (37 + k * 38) * SX
        c.line(x, 0, x, PH)
    for k in range(0, (2000 - 37) // 38 + 1):
        y = PH - (37 + k * 38) * SY
        c.line(0, y, PW, y)


def fiducials(c):
    c.setStrokeColorRGB(*BLUE)
    c.setLineWidth(0.8)
    for k, (x, y) in enumerate(((gx(0), gy(0)), (gx(35), gy(0)), (gx(0), gy(51)), (gx(35), gy(51)))):
        c.line(x - 5, Y(y), x + 5, Y(y))
        c.line(x, Y(y - 5), x, Y(y + 5))
        if k == 0:                       # oben links anders (Drehung erkennbar)
            c.circle(x, Y(y), 3.2, stroke=1, fill=0)


def text(c, s, x, y, size=LABEL_PT, font="DV", rgb=BLUE):
    c.setFillColorRGB(*rgb)
    c.setFont(font, size)
    c.drawString(x, Y(y), s)


def draw_page(c, pg, n_pages):
    draw_grid(c)
    fiducials(c)
    text(c, f"Schriftprobe Sang · {TEMPLATE_ID} · Seite {pg['index']}/{n_pages}", gx(COL0), gy(1) - 3, 7,
         rgb=(0.40, 0.40, 0.48))
    for d in pg["draw"]:
        if d[0] == "title":
            text(c, "Schriftprobe für deine Handschrift", gx(COL0), gy(3) - 2, 13, "DVB", DARK)
        elif d[0] == "instr":
            text(c, d[1], gx(COL0) + 3, gy(d[2]) - 3, 7.3, rgb=(0.13, 0.13, 0.18))
        elif d[0] == "heading":
            _, t, r, sub = d
            text(c, t, gx(COL0), gy(r) - 3, 10.5, "DVB", DARK)
            if sub:
                text(c, "– " + sub, gx(COL0) + tw(t, 10.5, "DVB") + 7, gy(r) - 3, 7.6, rgb=(0.33, 0.33, 0.43))
        elif d[0] == "note":
            text(c, d[1], gx(COL0) + 3, gy(d[2]) - 3, 7.4, rgb=(0.33, 0.33, 0.43))
        elif d[0] == "prompt":
            markup(c, d[1], gx(COL0) + 3, d[2], 8.6)
        elif d[0] == "calib":
            _, x, y = d
            c.setStrokeColorRGB(*BLUE)
            c.setLineWidth(0.6)
            c.circle(x, Y(y), 7, stroke=1, fill=0)
            c.line(x - 10, Y(y), x + 10, Y(y))
            c.line(x, Y(y - 10), x, Y(y + 10))
            c.setFillColorRGB(*NAME)
            c.setFont("DV", 6.8)
            c.drawRightString(x - 13, Y(y + 2.4), "Kalibrierpunkt: hier 1× genau in die Mitte tippen")
    for it in pg["items"]:
        if it["kind"] == "calib":
            continue
        c.setStrokeColorRGB(*LIGHT)
        c.setLineWidth(0.9)
        for b in it["boxes"]:
            c.line(b[0] + 1.5, Y(it["baseline"]), b[2] - 1.5, Y(it["baseline"]))
        if not it["label_box"]:
            continue
        lx0, by0, lx1, by1 = it["label_box"]
        c.setStrokeGray(SEP)
        c.setLineWidth(0.5)
        if len(it["boxes"]) > 1:
            c.setDash(1, 2)
            for b in it["boxes"][1:]:
                c.line(b[0], Y(b[1] + 3), b[0], Y(b[3] - 3))
            c.setDash()
        x_end = it["boxes"][-1][2]
        c.line(x_end, Y(by0 + 2), x_end, Y(by1 - 2))
        c.line(lx0, Y(by0 + 2), lx0, Y(by1 - 2))
        if it["label"].startswith("§M"):
            markup(c, it["label"][2:], lx0 + 3, it["baseline"] - 0.5)
        else:
            text(c, it["label"], lx0 + 3, it["baseline"] - 0.5)
            if it["name"]:
                text(c, it["name"], lx0 + 4 + tw(it["label"]), it["baseline"] - 0.5, 6.2, rgb=NAME)


def render(pages, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    n = len(pages)
    c = Canvas(out_dir + "Schriftprobe_Sang_Vorlage.pdf", pagesize=A4, invariant=1)
    c.setTitle("Schriftprobe für deine Handschrift")
    c.setAuthor("Sang Duc Do")
    single = []
    for pg in pages:
        draw_page(c, pg, n)
        c.showPage()
        buf = io.BytesIO()
        c1 = Canvas(buf, pagesize=A4, invariant=1)
        draw_page(c1, pg, n)
        c1.showPage()
        c1.save()
        single.append(buf.getvalue())
    c.save()
    layout = {
        "template_id": TEMPLATE_ID, "created": "2026-10-28",
        "page_size_pt": [PW, PH], "gn_scale": GN_SCALE, "page_size_gn": [PW * GN_SCALE, PH * GN_SCALE],
        "origin": "oben links, y nach unten, Einheit pt (PDF-Export 1:1, .goodnotes = pt * gn_scale)",
        "grid": {"cell_pt": CELL, "x0_pt": gx(0), "y0_pt": gy(0), "px_per_page": [1414, 2000]},
        "assignment_rule": ("Strich -> Feld: x-Überlappung >= 50 % mit label_box ∪ boxes und bogenlängen-gewichteter "
                            "Schwerpunkt im Band [band0, band1); hohe Felder zuerst; sonst nächste Grundlinie "
                            "(Abstand oberhalb x 0.5) innerhalb 1 Kästchen, sonst melden. Mehrere boxes: nach x-Lücken "
                            "in reps Gruppen teilen, kleine Striche (Punkte, Querstriche) zur Gruppe mit größter "
                            "x-Überlappung. Geometrie aus PDF-Export 'Bearbeitbar' (/Ink /InkList), .goodnotes nur für "
                            "Stiftart, Farbe, Reihenfolge. Stifte außer Kugelschreiber, Breite > 3 pt, Formen melden."),
        "pages": [{"index": p["index"], "header": f"Schriftprobe Sang · {TEMPLATE_ID} · Seite {p['index']}/{n}",
                   "bg_sha256": hashlib.sha256(single[k]).hexdigest(), "printed": p["printed"], "items": p["items"]}
                  for k, p in enumerate(pages)],
    }
    json.dump(layout, open(out_dir + "layout.json", "w"), ensure_ascii=False, indent=1)
    return single


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else HERE + "out/"
    pages = build()
    single = render(pages, out)
    import gn_writer  # noqa: E402
    from PIL import Image  # noqa: E402
    try:
        import fitz  # noqa: E402
        doc = fitz.open(out + "Schriftprobe_Sang_Vorlage.pdf")
        pix = doc[0].get_pixmap(dpi=40)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).resize((298, 421))
    except ImportError:
        doc, im = [], Image.new("RGB", (298, 421), "white")
    tb = io.BytesIO()
    im.save(tb, "JPEG", quality=85)
    gp = [(PW, PH, [], pdf) for pdf in single]
    res = gn_writer.write(out + "Schriftprobe_Sang_Vorlage.goodnotes", "Schriftprobe Sang", gp, None, tb.getvalue(),
                          1.05, (0.07, 0.07, 0.09))
    for k in range(len(doc)):
        doc[k].get_pixmap(dpi=110).save(out + f"preview_p{k + 1}.png")
    items = [i for p in pages for i in p["items"]]
    writes = sum(i["reps"] for i in items if i["kind"] != "calib")
    print(len(pages), "Seiten,", len(items), "Felder,", writes, "Schreibvorgänge", res)
