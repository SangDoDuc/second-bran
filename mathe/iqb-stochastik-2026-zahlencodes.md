# Mathe – IQB 2026 Stochastik: Zahlencodes (Prüfungsteil A, 5 BE)

Aufgabe: IQB-Pool 2026, erhöhtes Niveau, Prüfungsteil A, Stochastik, Aufgabengruppe 2 (Datei 2026_M_erhoeht_A_Stochastik_2_2).
Quelle: https://www.iqb.hu-berlin.de/media/exercise_files/Abituraufgaben_Mathematik/2026MerhoehtAStochastik22_Aufgabe.pdf
Handschriftliche Fassung (GoodNotes): noch offen, wartet auf die neue Handschrift-Bibliothek (siehe `handschrift/README.md`). Das Skript dafür steht unten in Abschnitt 4.

---

## 0. Die Aufgabe in einfachen Worten

- Ein Zufallsgenerator erzeugt Zahlencodes.
- Jeder Code enthält eine bestimmte Ziffernfolge mit Wahrscheinlichkeit p (0 < p < 1), unabhängig von den anderen Codes.
- Treffer T = „Code enthält die Ziffernfolge“, P(T) = p
- Kein Treffer T̄ = „Code enthält sie nicht“, P(T̄) = 1 − p
- Es werden immer **zwei** Codes erzeugt → zweistufiges Zufallsexperiment, Baum mit 4 Pfaden:

| Pfad | Wahrscheinlichkeit | Bedeutung |
|---|---|---|
| T T | p · p = p² | beide enthalten die Folge |
| T T̄ | p · (1 − p) | nur der erste |
| T̄ T | (1 − p) · p | nur der zweite |
| T̄ T̄ | (1 − p)² | keiner |

- **a)** p = 0,1. Wahrscheinlichkeit, dass **genau einer** der beiden Codes die Folge enthält. (2 BE)
- **b)** Bekannt: **mindestens einer** enthält die Folge. Term in p für die Wahrscheinlichkeit, dass die Folge **nicht in beiden** enthalten ist. (3 BE)

## 1. Teilaufgabe a) – genau einer

**Lösungsweg**
- „Genau einer“ = zwei Pfade im Baum: T T̄ **oder** T̄ T.
- P = 0,1 · 0,9 + 0,9 · 0,1 = 2 · 0,1 · 0,9 = **0,18**

**Alternative (Binomialverteilung)**
- X = Anzahl der Codes mit der Folge, X ~ B(2; 0,1)
- P(X = 1) = (2 über 1) · 0,1¹ · 0,9¹ = 2 · 0,1 · 0,9 = 0,18

**Warum so**
- Beide Reihenfolgen zählen, deshalb der Faktor 2.
- Die Codes sind unabhängig → Pfadregel (Multiplikation), dann Summenregel (Addition der Pfade).

**Was Punkte bringt (2 BE)**
- Ansatz 2 · 0,1 · 0,9 (oder beide Pfade addiert) → 1 BE
- Ergebnis 0,18 → 1 BE

**Typische Fehler**
- Nur einen Pfad nehmen: 0,1 · 0,9 = 0,09 (halbe Lösung).
- „Genau einer“ mit „mindestens einer“ verwechseln (das wäre 1 − 0,9² = 0,19).

## 2. Teilaufgabe b) – bedingte Wahrscheinlichkeit

**Signal erkennen**
- Der Satz „Mindestens einer der beiden Zahlencodes enthält die Ziffernfolge.“ ist eine **Tatsache, die vorher feststeht** → Bedingung.
- Gesucht ist also P_A(B) mit
  - A = „mindestens einer enthält die Folge“ (Bedingung)
  - B = „nicht beide enthalten die Folge“ = „höchstens einer“ (gesucht)

**Schritt 1: P(A)**
- Gegenereignis von „mindestens einer“ ist „keiner“ = Pfad T̄ T̄.
- P(A) = 1 − (1 − p)²

**Schritt 2: P(A ∩ B)**
- „Mindestens einer“ **und** „nicht beide“ = **genau einer**.
- P(A ∩ B) = p · (1 − p) + (1 − p) · p = 2p(1 − p)

**Schritt 3: Quotient**
- P_A(B) = P(A ∩ B) / P(A) = [p(1 − p) + (1 − p)p] / [1 − (1 − p)²]

Das ist genau der Term im IQB-Erwartungshorizont. Vereinfachen ist **nicht** verlangt.

**Optionale Vereinfachung (nur wenn Zeit)**
- 1 − (1 − p)² = 1 − (1 − 2p + p²) = 2p − p² = p(2 − p)
- P_A(B) = 2p(1 − p) / (p(2 − p)) = **2(1 − p) / (2 − p)**
- Probe mit p = 0,1: 2 · 0,9 / 1,9 ≈ 0,947 und direkt 0,18 / 0,19 ≈ 0,947 ✓

**Warum so (Bild dazu)**
- Von den 4 Pfaden fällt T̄ T̄ weg, weil wir wissen, dass mindestens ein Treffer da ist.
- Es bleiben 3 Pfade mit Gesamtwahrscheinlichkeit 1 − (1 − p)². Das ist der neue „Nenner“ (das verkleinerte Universum).
- Davon sind die zwei Pfade „genau einer“ günstig. Das ist der Zähler.

**Was Punkte bringt (3 BE)**
- Erkennen, dass eine bedingte Wahrscheinlichkeit gefragt ist, und Ansatz P(A ∩ B)/P(A) → 1 BE
- Zähler p(1 − p) + (1 − p)p → 1 BE
- Nenner 1 − (1 − p)² → 1 BE

**Typische Fehler**
- Nicht durch P(A) teilen → man gibt nur 2p(1 − p) an. Das ist „genau einer“ ohne Bedingung, falsch.
- Nenner als 1 − p² schreiben. Das ist „nicht beide“, nicht „mindestens einer“. Gegenereignis von „mindestens einer“ ist immer „keiner“.
- „Nicht in beiden“ als „in keinem“ lesen. Unter der Bedingung „mindestens einer“ wäre das 0, ergibt keinen Sinn. Gemeint ist „nicht alle beide“.

## 3. Klausurfertige Kurzversion

**a)** p = 0,1
P(genau einer) = 2 · 0,1 · 0,9 = 0,18

**b)** A: mindestens einer enthält die Folge, B: nicht beide
P(A) = 1 − (1 − p)²
P(A ∩ B) = P(genau einer) = p(1 − p) + (1 − p)p
P_A(B) = [p(1 − p) + (1 − p)p] / [1 − (1 − p)²]

## 4. Skript für die Handschrift-Fassung (GoodNotes, A4 Karo, 1 Seite)

Zeile für Zeile so schreiben:

```
IQB 2026  Stochastik 2.2        Zahlencodes

T = Code enthält Folge   P(T) = p
T̄ = enthält sie nicht    P(T̄) = 1 − p
2 Codes, unabhängig  →  Baum:
   T T  p²      T T̄  p(1−p)      T̄ T  (1−p)p      T̄ T̄  (1−p)²

a)  p = 0,1
    P(genau einer) = 0,1 · 0,9 + 0,9 · 0,1
                   = 2 · 0,1 · 0,9 = 0,18

b)  Bedingung A: mind. einer enthält Folge
    gesucht B: nicht beide (= höchstens einer)

    P(A) = 1 − P(keiner) = 1 − (1−p)²
    A ∩ B = genau einer
    P(A ∩ B) = p(1−p) + (1−p)p

    P_A(B) = P(A ∩ B) / P(A)
           = [p(1−p) + (1−p)p] / [1 − (1−p)²]

    (Probe p = 0,1: 0,18 / 0,19 ≈ 0,947)
```

Kleiner Baum rechts neben den Pfaden skizzieren: Wurzel, zwei Äste p / 1−p, je zwei Äste p / 1−p, Pfad T̄ T̄ durchstreichen (fällt durch die Bedingung weg).
