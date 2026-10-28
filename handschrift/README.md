# Handschrift (Sang) – Schriftprobe und Bibliothek

Stand: 28.10.2026

## Warum es diesen Ordner gibt

| Punkt | Inhalt |
|---|---|
| Problem | Die bisherige „Sang-Handschrift“ wirkt fremd (Sangs Feedback vom 28.10.2026). |
| Ursache | Die alte Bibliothek stammt aus **einem Foto** mit 170 englischen Wörtern (Climate-Assessment). Rund 22 Zeichen kamen darin nicht vor: fast alle Großbuchstaben, z, k, j, v, ß, viele Ziffern, Klammern und Mathe-Zeichen. Claude hat sie künstlich gezeichnet. Außerdem lag die alte Bibliothek nur im temporären Arbeitsordner einer Sitzung. |
| Lösung | Sang füllt die Schriftprobe **SP-v2** einmal in GoodNotes aus. Daraus entsteht eine neue Bibliothek aus Vektorstrichen. Sie wird **hier im Repo** gespeichert und ersetzt die alte für alle künftigen Handschrift-Dateien. |

## Aktueller Stand: Bibliothek aus der Kurzfassung SP-k1 (28.10.2026)

- Sang hat die Kurzfassung ausgefüllt und als **Bild** geschickt (1414 × 2000 px, also genau das Seitenraster), nicht als PDF/GoodNotes-Export. Das reicht: Die Felder werden über `vorlage/layout_kompakt.json` ausgeschnitten.
- Ordner `bibliothek/`:

| Datei | Zweck |
|---|---|
| `schriftprobe_SP-k1.jpg` | Sangs ausgefüllte Probe (Rohdaten) |
| `extract_sample.py` | schneidet die schwarze Tinte je Feld aus (blaue Vorlage und Raster fallen weg) |
| `split_words.py` | zerlegt die 3 Sätze in Wörter |
| `comps.py`, `cc_view.py` | Strichteile eines Feldes auflisten bzw. vergrößert mit Nummern anzeigen |
| `glyphs.py` | **die Bibliothek**: 79 Zeichen, 113 Varianten, 13 ganze Wörter |
| `render_loesung.py` | setzt Zeilen daraus zusammen (Spaltenvektor, Pfeil, Wurzelstrich, Bruch, Hoch-/Tiefzahlen) |
| `zeichenuebersicht.png` | Übersicht aller Zeichen |

- In der Bibliothek:
  - A–Z, 0–9 und Zeichen einzeln
  - Mathe-Teile aus Sangs Ausdrücken (Pfeil, große Klammern, Wurzel mit Strich, Bruchstrich, ½, ₁₂₃, ², Malpunkt)
  - Kleinbuchstaben a b d e i k m n o r t x, aus Wörtern geschnitten
  - ganze Wörter: und, gegenüber, Diagonale, der, Würfel, Vektor, Richtung, also, keine, Kante, durch, in, den
- Ablauf: `cd handschrift/bibliothek && python3 extract_sample.py && python3 split_words.py && python3 glyphs.py && python3 render_loesung.py`
  - Ergebnis: `loes_p1_alpha.npy`. Daraus macht die Kuli-Umwandlung (uniform/strokes, liegt noch im Arbeitsordner der Sitzung) GoodNotes und PDF.
- Grenzen:
  - Viele Kleinbuchstaben gibt es nur 1×.
  - Für fehlende Kleinbuchstaben (c f g h l p s u v w y z ä ö ü ß) einzeln ist noch kein Schnitt angelegt. Lange Fließtexte gehen deshalb noch nicht.
  - Mathe-Lösungswege gehen gut.
- Erfahrungen:
  - Helle Striche werden um den Faktor 1,35 verstärkt.
  - Bei „=“ werden die Striche auf mindestens 5 px Abstand gezogen. Sonst verschmelzen sie bei der Kuli-Umwandlung.

## Fließtext-Methode seit 28.10.2026 (`werkzeug/render_font.py`)

- Sangs Feedback zur ersten Englisch-Fassung:
  - Buchstaben und Wörter zu weit auseinander
  - nicht gerade auf der Linie
  - teilweise unleserlich
- Neue Methode: Statt Wortstücke aneinanderzuhängen, wird **jeder Buchstabe einzeln** gesetzt.
  - Der Buchstabenkörper sitzt genau auf der Grundlinie.
  - Maße: x-Höhe 13 px, Oberlänge und Großbuchstaben 19 px.
  - Abstände: zwischen Buchstaben 1 px, zwischen Wörtern ~15 px.
- `font.py` holt die Kandidaten:
  - Kleinbuchstaben aus der alten Foto-Bibliothek (mit Buchstabengrenzen)
  - Großbuchstaben, Ziffern und Zeichen sowie a b d e i k m n o r t x aus SP-k1
  - v und z aus V und Z auf x-Höhe; i bekommt einen Punkt, wo er fehlt
- `PICK` in `render_font.py` sind die Varianten, die **nach der Kuli-Umwandlung** noch lesbar sind (geprüft mit `conv_test.py`). Dicke Proben verlieren sonst Details: Das Auge im e läuft zu, der Bogen im h verschwindet.
- Abhängigkeit: `hw/lib2.pkl` (alte Bibliothek) liegt nur im Arbeitsordner der Sitzung. Für eine dauerhafte Fassung fehlt eine Probe mit a–z, ä, ö, ü, ß.

## Für Sang: Ablauf

1. Datei `Schriftprobe_Sang_Vorlage.goodnotes` in GoodNotes öffnen. Falls das nicht klappt: die PDF importieren.
2. Die Anleitung oben auf Seite 1 beachten:
   - Kugelschreiber, Farbe Schwarz
   - Rechtschreibprüfung für Handschrift aus
   - nicht am Strichende stehen bleiben
   - beim Verschreiben „Rückgängig“ oder den Radierer „Ganzer Strich“ benutzen
3. Exportieren am iPad, **alle Seiten**:
   - einmal als **PDF „Bearbeitbar“** (Anmerkungen an)
   - einmal als **GoodNotes**
   - beide Dateien an Claude schicken
4. Dauer ca. 25–30 Minuten. Du kannst nach jeder Seite aufhören, Seite 1–3 sind am wichtigsten.

## Dateien

| Datei | Zweck |
|---|---|
| `vorlage/make_vorlage.py` | erzeugt die Vorlage (PDF + .goodnotes + `layout.json`), reproduzierbar (byte-gleich) |
| `vorlage/layout.json` | **Schlüssel für die Auswertung**: jedes Schreibfeld in pt (Ursprung oben links), Grundlinie, Band, Bezug (`anchor`), Wiederholungen, Hash je Seitenhintergrund |
| `vorlage/corpus_stats.py`, `select_words.py`, `finalize_words.py` | Wortauswahl aus Sangs Schultexten im Repo (Buchstabenpaar-Abdeckung, danach Prüfung und Kürzung) |
| `vorlage/words.json`, `words_v2.json` | Wortlisten v1 / v2 (v2 ist in der Vorlage) |
| `werkzeug/gn_writer.py` | schreibt .goodnotes-Dateien (Striche + eigener Seitenhintergrund je Seite) |
| `werkzeug/gnverify.py` | liest und prüft .goodnotes-Dateien |

Erzeugen: `cd handschrift/vorlage && python3 make_vorlage.py AUSGABEORDNER/`

Benötigt werden reportlab und lz4, PyMuPDF nur für die Vorschaubilder.

## Kurzfassung SP-k1 (1 Seite, ca. 8 Minuten) – die verschickte Version

Sang hatte für die lange Fassung keine Zeit (28.10.2026). Deshalb gibt es die Kurzfassung:
- 3 Sätze (darunter ein Pangramm mit allen Buchstaben, ä ö ü ß)
- A–Z, 0–9 und 18 Zeichen je 1×
- 6 Mathe-Ausdrücke (Spaltenvektor, Bruch, Vektorpfeil, Wurzelstrich, Ebene, Punkt, e-Funktion)
- 11 Wörter

Insgesamt 74 Felder. Erzeugen mit `SP_KOMPAKT=1 python3 make_vorlage.py OUT/`, Schlüssel ist `vorlage/layout_kompakt.json`.

Grenze: Jedes Zeichen gibt es nur 1×, deshalb gibt es kaum Abwechslung, und viele Buchstabenverbindungen kommen nur aus den 3 Sätzen. Die lange Fassung SP-v2 kann später ergänzt werden.

## Inhalt der Vorlage SP-v2 (6 Seiten, 364 Felder, 488 Schreibvorgänge)

| Teil | Inhalt | Wozu |
|---|---|---|
| 1 Sätze | 7 natürliche Sätze, Kopfzeile „Mathe 29.10.26“, unterstrichene Überschrift | Wortabstände, Satzzeichen direkt nach Wörtern, Spiegelstrich, Unterstreichung, Neigung, Größe |
| 2 Zeichen | A–Z und a–z je 2×, Ziffern 2×, Satzzeichen 2×, 12 Zahlen (Datum, Jahre, Dezimalzahlen, Zehnerpotenz) | Einzelformen; Ziffern im Zusammenhang |
| 3 Mathe | 38 Zeichen (→ 4×), 20 Ausdrücke in Klausur-Form: Spaltenvektor, Bruch, Vektorpfeil, Wurzelstrich, Integral mit Grenzen, Binomialkoeffizient, Ebene, Punkte | alles, was der Mathe-Renderer bisher künstlich zeichnet |
| 4 Wörter | 208 Felder: deutsche Grundwörter (häufigste 2×), Fachwörter, Abkürzungen (ca., z.B., Abb. …), NATO/USA/CO₂, Bindestrich-Wörter, Englisch | Buchstabenverbindungen; gewichtete Paar-Abdeckung 95 % (≥ 1 Probe) bzw. 87 % (≥ 2 Proben) |

## Für Claude: Auswertung, wenn die ausgefüllte Datei kommt

Fakten laut Prüfung vom 28.10.2026 (GoodNotes-Support-Artikel und ein öffentlicher iPad-Export):
- **Geometrie aus dem PDF-Export „Bearbeitbar“ nehmen.**
  - Jeder Kugelschreiber-Strich ist dort eine `/Ink`-Annotation.
  - `/InkList` ist die Mittellinie in pt, 1:1 zur Seite.
  - Die Vorlage bleibt Seiteninhalt, Tinte und Vorlage sind also strukturell getrennt.
  - Eine Seite mit 0 `/Ink` heißt: falscher Exportmodus. Dann nachfragen.
- **Die .goodnotes-Datei nur für Zusatzdaten nutzen:** Stiftart, Farbe, Zeichenreihenfolge (für späte i-Punkte und t-Striche).
  - Koordinaten = pt × 132/72.
  - Echte Exporte haben Schema 35.
  - Datensätze mit Breite 0 oder ohne PDF-Gegenstück sind unsichtbar oder radiert, also verwerfen.
  - GoodNotes tastet jedes Segment zehnmal ab.
- **Problemstriche:** Bleistift wird im PDF zu einem Rasterbild (`/Stamp`). Breiten über 3 pt, Textmarker und perfekte Formen (Feld 9) melden.
- **Zuordnung Strich → Feld:** Die Regel steht in `layout.json` unter `assignment_rule`.
  - Hohe Felder zuerst zuordnen.
  - Felder mit mehreren Kästchen nach x-Lücken in `reps` Gruppen teilen.
- **Kalibrierpunkte** (Seite 1 oben rechts, letzte Seite unten rechts) prüfen die Koordinaten-Umrechnung.

**Ziel:**
- `handschrift/bibliothek/` mit den Vektorstrichen je Feld als JSON, dazu gemessene Grundlinie, x-Höhe und Neigung.
- Den Renderer auf diese Bibliothek umstellen.
- Die alte Foto-Bibliothek nicht mehr verwenden.
