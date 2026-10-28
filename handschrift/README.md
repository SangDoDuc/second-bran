# Handschrift (Sang) – Schriftprobe und Bibliothek

Stand: 28.10.2026

## Warum es diesen Ordner gibt

| Punkt | Inhalt |
|---|---|
| Problem | Die bisherige „Sang-Handschrift“ wirkt fremd (Sangs Feedback vom 28.10.2026). |
| Ursache | Die alte Bibliothek stammt aus **einem Foto** mit 170 englischen Wörtern (Climate-Assessment). Rund 22 Zeichen kamen darin nicht vor: fast alle Großbuchstaben, z, k, j, v, ß, viele Ziffern, Klammern und Mathe-Zeichen. Claude hat sie künstlich gezeichnet. Außerdem lag die alte Bibliothek nur im temporären Arbeitsordner einer Sitzung. |
| Lösung | Sang füllt die Schriftprobe **SP-v2** einmal in GoodNotes aus. Daraus entsteht eine neue Bibliothek aus Vektorstrichen. Sie wird **hier im Repo** gespeichert und ersetzt die alte für alle künftigen Handschrift-Dateien. |

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
