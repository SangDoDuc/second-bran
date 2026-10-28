# Mathe – IQB 2024 Geometrie: Oktaeder im Würfel (ganz ausführlich, zum Vorstellen)

Aufgabe: IQB-Pool 2024, erhöhtes Niveau, Prüfungsteil A, AG/LA (A2), Aufgabengruppe 2 (5 BE).
Quelle: https://www.iqb.hu-berlin.de/media/exercise_files/Abituraufgaben_Mathematik/2024MerhoehtAAGLAA221_Aufgabe.pdf
Kurzfassung aller drei Aufgaben: [`iqb-praesentation-pruefungsteil-a.md`](iqb-praesentation-pruefungsteil-a.md).
Handschriftliche Fassung mit 3 Skizzen: GoodNotes-Datei *Mathe_IQB2024_Oktaeder_im_Wuerfel_A4* (6 Seiten, Vorstellung am 29.10.2026).

---

## 0. Die Aufgabe in einfachen Worten

- Man setzt auf jede der 6 Flächen eines Würfels genau in die Mitte einen Punkt.
- Verbindet man die 6 Punkte, entsteht ein **Oktaeder**: zwei Pyramiden, Boden an Boden (8 Dreiecke).
- Gegeben:
  - A(1|2|1) und C(−3|−6|9)
  - Die Ecken A, B, C, D liegen in der Ebene **H: 2x₁ + x₂ + 2x₃ = 6**.
- Gesucht:
  - **a)** Zeige: Die Würfelkante ist 12 lang.
  - **b)** Berechne eine Ecke, die **nicht** in H liegt. Die Namen E (oben) und F (unten) vergeben wir selbst, die Aufgabe nennt sie nicht.

**Skizze 1 (Würfel mit Oktaeder):**

| Ecke | Lage (nur in der Skizze) |
|---|---|
| A | vorne |
| C | hinten |
| B | rechts |
| D | links |
| E | oben |
| F | unten |
| M | Würfelmittelpunkt |

- ABCD ist das „Gürtel-Quadrat“ in H.

## 1. Grundwissen Würfel

- Alle 12 Kanten sind gleich lang (Kantenlänge **a**). Alle Winkel sind rechte Winkel.
- **Nachbarflächen** sind zwei Flächen mit einer gemeinsamen Kante.
  - Jede Fläche hat 4 Nachbarn und genau 1 Gegenüber.
  - Eine dritte Möglichkeit gibt es nicht.
- Gegenüberliegende Flächen sind parallel, ihr Abstand ist a.
- **M = Würfelmittelpunkt**: Er liegt genau in der Mitte und ist von jeder Fläche gleich weit weg, nämlich **a/2**.
- ⚠️ Der Würfel liegt im Koordinatensystem **schief**. „Oben“ und „unten“ gelten nur in der Skizze.

## 2. Warum liegen A und C gegenüber?

| Verbindung | Wo verläuft sie? | Folge |
|---|---|---|
| Mitte → Mitte einer **Nachbarfläche** | außen am Oktaeder entlang | **Kante** des Oktaeders |
| Mitte → Mitte der **Gegenüber-Fläche** | mitten durchs Innere, durch M | **keine** Kante |

1. In der Abbildung gehen von A Linien zu B, zu D, nach oben und nach unten, aber **keine zu C**.
2. Also ist AC eine **Diagonale des Gürtel-Quadrats ABCD**, nicht die Raumdiagonale des Würfels.
3. Keine Kante → keine Nachbarn → A und C sind die Mitten **gegenüberliegender** Flächen (vorne und hinten).
4. Längen darf man in der Abbildung nicht abmessen. Welche Ecken verbunden sind, gehört aber zur Aufgabe.

**Skizze 2 (Draufsicht, von oben):**
- „Vorne“ ist auf dem Blatt unten.
- AB ist eine Kante (Nachbarn, außen).
- AC ist eine Diagonale (gegenüber, durch M).
- |AC| = a/2 + a/2 = a.

## 3. Teil a: Warum ist |AC| die Würfelkante?

**Die Idee:**
1. Der Abstand zweier paralleler Wände ist die Länge einer Strecke, die **auf beiden Wänden senkrecht** steht. Schräge Strecken sind länger.
2. So eine senkrechte Strecke kennen wir schon: eine Würfelkante von vorne nach hinten. Sie ist a lang.
3. A ist genau die Mitte der Vorderwand, C genau die Mitte der Rückwand.
   - Beide sind also gleich hoch und gleich weit links.
   - Deshalb liegt C **genau hinter** A.
4. AC läuft deshalb parallel zu dieser Würfelkante, steht senkrecht auf beiden Wänden und ist genauso lang: **|AC| = a**.
5. Vergleich: Im Zimmer ist der Weg von der Mitte einer Wand zur Mitte der Wand gegenüber genau die Zimmerlänge.
6. Dabei geht AC durch M: von A bis M sind es a/2, von M bis C noch einmal a/2, zusammen a.

**Die Rechnung:**
- Vektor von A nach C = **Spitze minus Fuß**:
  AC = C − A = (−3 − 1 | −6 − 2 | 9 − 1) = **(−4 | −8 | 8)**
- Länge berechnen: alle Einträge quadrieren, addieren, Wurzel ziehen (Pythagoras im Raum):
  |AC| = √((−4)² + (−8)² + 8²) = √(16 + 64 + 64) = √144 = **12**
- Also gilt a = 12. Das war zu zeigen. ✓

**Warum die Idee wichtig ist:**
- Eine Oktaederkante, z. B. AB, geht von A erst a/2 nach hinten bis auf die Höhe von M und dann a/2 nach rechts bis B (Skizze 2).
- |AB| = √((a/2)² + (a/2)²) = **a/√2**
- Wäre 12 eine Oktaederkante, dann wäre der Würfel größer: a = 12·√2 ≈ 17.
- Deshalb muss man begründen, dass AC eine **Diagonale** ist.

## 4. Teil b: eine Ecke außerhalb von H

**Schritt 1: Mittelpunkt M**
- Aus Teil a wissen wir: AC geht mitten durch M, je a/2 → M ist genau die Mitte der Strecke AC.
- Mittelpunkt = Durchschnitt der Koordinaten. OA ist der Pfeil vom Ursprung zu A und hat dieselben Zahlen wie A.
  - OM = ½·(OA + OC)
  - OM = ½·(1 − 3 | 2 − 6 | 1 + 9) = ½·(−2 | −4 | 10) = (−1 | −2 | 5) → **M(−1|−2|5)**
- Probe: 2·(−1) + (−2) + 2·5 = 6 → M liegt in H. Das passt, denn H geht mitten durch den Würfel.

**Schritt 2: In welche Richtung?**
1. Eine **Achse** ist die Verbindung zweier gegenüberliegender Flächenmitten: AC, BD und EF.
2. Jede Achse läuft parallel zu einer Sorte Würfelkanten (wie in Teil a). Die Würfelkanten stehen senkrecht aufeinander, also auch die Achsen.
3. EF steht senkrecht auf AC und auf BD. Das sind zwei verschiedene Richtungen in H → EF steht **senkrecht auf ganz H**.
4. Vergleich: Ein Tischbein steht senkrecht auf Länge und Breite der Platte, also senkrecht auf der Platte.
5. Senkrecht auf H zeigt der **Normalenvektor** (wie ein Fahnenmast auf dem Boden). Man liest ihn ab: Es sind die Zahlen vor x₁, x₂, x₃.
   2x₁ + 1x₂ + 2x₃ = 6 → **n = (2 | 1 | 2)**

**Schritt 3: Wie weit?**
- EF verbindet wie AC zwei gegenüberliegende Flächenmitten → |EF| = a = 12. M ist die Mitte von EF.
- |ME| = 12 : 2 = **6**

**Schritt 4: Wie oft n?**
- |n| = √(2² + 1² + 2²) = √9 = **3**
- Ein n ist 3 lang, wir brauchen 6 → **zweimal n**: 2·n = (4 | 2 | 4), Länge 6.

**Skizze 3 (Seitenansicht):**
- H erscheint von der Seite als Linie durch M.
- n steht senkrecht auf H.
- Der Pfeil 2·n geht von M bis E, Länge 6. Nach unten (gestrichelt) liegt F, ebenfalls 6 entfernt.

**Schritt 5: E ausrechnen**
- OE = OM + 2·n = (−1 | −2 | 5) + (4 | 2 | 4) = (3 | 0 | 9) → **E(3|0|9)**
- In die andere Richtung: F = M − 2·n → **F(−5|−4|1)**. Beide sind richtig, verlangt ist nur eine.

**Probe:**
1. Abstand Punkt–Ebene (Hessesche Normalform): E links in H einsetzen, die rechte Seite abziehen, durch |n| teilen:
   (2·3 + 0 + 2·9 − 6) : 3 = (24 − 6) : 3 = **6** ✓
2. Echte Gegenprobe:
   - EA = (−2 | 2 | −8)
   - |EA| = √72 = 6·√2 = 12/√2, das ist genau die Oktaederkante a/√2 ✓

## 5. Kurzfassung für die Tafel (klausurfertig)

- **a)** AC ist eine Diagonale → A und C sind Mitten gegenüberliegender Flächen → |AC| = a = √144 = **12**.
- **b)**
  - M(−1|−2|5)
  - Richtung n = (2|1|2) mit |n| = 3
  - Abstand a/2 = 6 → 2·n → **E(3|0|9)** (oder F(−5|−4|1))

## 6. Mögliche Fragen beim Vorstellen

| Frage | Antwort |
|---|---|
| Warum 2·n und nicht 6·n? | n ist schon 3 lang, 2·3 = 6. |
| Warum Abstand 6 und nicht 12? | M liegt in der Mitte, bis zur Fläche ist es nur die halbe Kante. |
| Warum ist M die Würfelmitte? | AC geht durch M, M ist von A und C je a/2 entfernt. |
| Woher weißt du, dass A und C gegenüberliegen? | In der Abbildung sind A und C nicht verbunden, AC ist die Diagonale von ABCD. |
| Warum nicht einfach 6 zur x₃-Koordinate addieren? | Der Würfel liegt schief. „Oben“ heißt hier senkrecht zu H, also in Richtung n. |
| Gibt es noch eine Lösung? | Ja, F(−5|−4|1). |

## 7. Was bringt Punkte, typische Fehler

| Was bringt Punkte | Typischer Fehler |
|---|---|
| Begründung, **warum** \|AC\| = a ist (gegenüberliegende Flächenmitten, Diagonale) | nur rechnen \|AC\| = 12 ohne Begründung → in a) fehlt dann der Kern |
| M als Mittelpunkt von AC **begründen** | M einfach hinschreiben |
| Richtung n begründen (EF ⊥ H) | 6 zur x₃-Koordinate addieren |
| Länge von n beachten: 2·n | 6·n nehmen (das wäre 18 lang) |
| Abstand a/2 = 6 | Abstand 12 nehmen (ganze Kante statt halbe) |
