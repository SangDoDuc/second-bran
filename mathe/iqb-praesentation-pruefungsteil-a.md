# Mathe – IQB-Aufgaben zum Vorstellen (erhöhtes Niveau, Prüfungsteil A, je 5 BE)

Stand 28.10.2026. Alle drei Aufgaben sind hilfsmittelfrei. Die Ergebnisse stimmen mit dem offiziellen IQB-Erwartungshorizont überein, außerdem wurden sie mit dem Computer nachgerechnet (Abzählen aller 1024 Würfe, Probe der Koordinaten).

Quellen:
- Analysis 2026: https://www.iqb.hu-berlin.de/media/exercise_files/Abituraufgaben_Mathematik/2026MerhoehtAAnalysis21_Aufgabe.pdf
- Stochastik 2023: https://www.iqb.hu-berlin.de/media/exercise_files/Abituraufgaben_Mathematik/2023MerhoehtAStochastik21_Aufgabe.pdf
- Geometrie 2024: https://www.iqb.hu-berlin.de/media/exercise_files/Abituraufgaben_Mathematik/2024MerhoehtAAGLAA221_Aufgabe.pdf

---

## Aufgabe 1 – Analysis 2026: Wertemenge

**Gegeben:** f ist auf ℝ definiert und hat die Wertemenge W_f = [−3; 2[. Der Wert −3 wird also angenommen, der Wert 2 nicht.

### a) Begründen, dass der Graph nicht punktsymmetrisch zum Ursprung ist (1 BE)

1. Punktsymmetrie zum Ursprung bedeutet: f(−x) = −f(x) für alle x.
2. Daraus folgt für die Wertemenge: Ist y = f(x₀) ein Funktionswert, dann ist auch f(−x₀) = −y einer. Die Wertemenge müsste also symmetrisch zu 0 liegen.
3. Hier gilt aber: −3 ∈ W_f, während 3 ∉ W_f (die Werte reichen nur bis unter 2). → Widerspruch, f ist **nicht** punktsymmetrisch.

### b) Wertemenge von h(x) = −2·f(x − 5) + 1 angeben und begründen (4 BE)

**Schritt für Schritt (von innen nach außen):**

| Schritt | Wirkung auf den Graphen | Wirkung auf die Wertemenge |
|---|---|---|
| f(x − 5) | Verschiebung um 5 nach rechts | **keine**: x − 5 durchläuft ganz ℝ, also kommen dieselben Werte vor → [−3; 2[ |
| −2·f(x − 5) | Streckung mit dem Faktor 2 in y-Richtung und Spiegelung an der x-Achse | ]−4; 6] (mal −2 dreht die Reihenfolge um) |
| −2·f(x − 5) + 1 | Verschiebung um 1 nach oben | ]−3; 7] |

**Rechnung als Ungleichungskette** (jeder Schritt umkehrbar, deshalb ⟺):
−3 ≤ y < 2 ⟺ 6 ≥ −2y > −4 ⟺ 7 ≥ −2y + 1 > −3   (bei Multiplikation mit −2 drehen sich die Zeichen um).

**Saubere Begründung beider Richtungen** (das will eine strenge Lehrkraft hören):
- **W_h ⊆ ]−3; 7]:** Für jedes x ist y = f(x − 5) ∈ [−3; 2[, also liegt h(x) nach der Kette in ]−3; 7].
- **]−3; 7] ⊆ W_h:** Sei z ∈ ]−3; 7] beliebig. Setze y = (1 − z)/2. Nach der Kette ist y ∈ [−3; 2[ = W_f, also gibt es ein x₀ mit f(x₀) = y. Dann gilt h(x₀ + 5) = −2·f(x₀) + 1 = z. Jeder Wert wird angenommen. Stetigkeit von f braucht man dafür nicht.
- **Ränder:**
  - 7 gehört dazu, weil −3 von f angenommen wird: −2·(−3) + 1 = 7.
  - −3 gehört nicht dazu: h(x) = −3 ⟺ f(x − 5) = 2, und 2 ∉ W_f.

**Ergebnis: W_h = ]−3; 7]** – die Klammern tauschen durch die Spiegelung die Seiten.

**Warum so / was bringt Punkte / typische Fehler**
- a) Punkte gibt es für das konkrete Gegenbeispiel aus der Wertemenge (−3 drin, 3 nicht).
- b) Punkte gibt es für:
  - die richtige Menge mit den richtigen Klammern,
  - die Begründung über die Transformationen,
  - die Aussage, dass die x-Verschiebung nichts ändert.
- Typische Fehler:
  - Zeichen bei ·(−2) nicht umdrehen → falsch ]−5; 5].
  - Klammern nicht tauschen → falsch [−3; 7[.
  - Reihenfolge vertauschen, also erst +1 und dann ·(−2) → falsch ]−6; 4].
  - Bei a) mit f(0) = 0 argumentieren. Das klappt nicht, weil 0 ∈ W_f liegt.

**Beispiel einer passenden Funktion (für Nachfragen):** f(x) = 2 − 5·e^(−x²). Dann ist f(0) = −3, und f nähert sich 2, ohne die 2 zu erreichen. Für diese Funktion gilt h(5) = 7.

**Klausurfertige Kurzversion**
- a) −3 ∈ W_f, aber 3 ∉ W_f → keine Punktsymmetrie.
- b) Die x-Verschiebung ändert nichts. −3 ≤ f < 2 ⟹ 7 ≥ −2f + 1 > −3 → **W_h = ]−3; 7]**.

---

## Aufgabe 2 – Stochastik 2023: Tetraeder, fünfmal geworfen

**Modell:** regelmäßiges Tetraeder → jede Zahl 1, 2, 3, 4 hat die Wahrscheinlichkeit 1/4. Die fünf Würfe sind unabhängig; es gibt 4⁵ = 1024 gleich wahrscheinliche Ergebnisse (5-Tupel).

### a) Ereignis zum Term (3/4)⁵ (2 BE)

- **Ereignis:** „Bei keinem der fünf Würfe wird die Zahl 1 erzielt.“ (Genauso richtig: keine 4, oder „bei jedem Wurf eine Zahl kleiner als 4“.)
- **Begründung:**
  - Pro Wurf ist P(keine 1) = 3/4, denn drei von vier gleich wahrscheinlichen Seiten passen.
  - Die fünf Würfe sind unabhängig, also wird nach der Pfadregel multipliziert: (3/4)·(3/4)·(3/4)·(3/4)·(3/4) = (3/4)⁵.
  - Mit Binomialverteilung gesagt: X = Anzahl der Einsen, X ~ B(5; 1/4), P(X = 0) = (3/4)⁵.

### b) Term für „jede Zahl mindestens einmal“ (3 BE)

**Schritt 1 – Struktur erkennen:** Jede der 4 Zahlen braucht mindestens einen Wurf. Damit sind 4 Würfe verbraucht und genau 1 bleibt übrig. Also kommt **genau eine Zahl zweimal** vor, die anderen genau einmal. Dreimal geht nicht, denn dann blieben nur 2 Würfe für 3 fehlende Zahlen.

**Schritt 2 – Wo liegt das Doppel?** Man wählt die 2 Würfe (Positionen), die dieselbe Zahl zeigen: (5 über 2) = 10 Möglichkeiten. Die Reihenfolge innerhalb des Paars ist egal, deshalb nicht 5·4 = 20.

**Schritt 3 – Wahrscheinlichkeit für eine feste Wahl der Positionen:**

| Wurf | Bedingung | Wahrscheinlichkeit |
|---|---|---|
| 1. Doppel-Wurf | beliebige Zahl | 4/4 = 1 |
| 2. Doppel-Wurf | dieselbe Zahl | 1/4 |
| nächster Wurf | eine der 3 fehlenden Zahlen | 3/4 |
| nächster Wurf | eine der 2 fehlenden Zahlen | 2/4 |
| letzter Wurf | die letzte fehlende Zahl | 1/4 |

Die Doppel-Würfe zuerst zu betrachten ist erlaubt, weil die Würfe unabhängig sind. Es ändert sich nur die Reihenfolge der Faktoren. Beispiel Doppel bei Wurf 3 und 5: 4/4 · 3/4 · 2/4 · 1/4 · 1/4, also dieselben Faktoren.

**Schritt 4 – Warum mal 10?** Jedes günstige Ergebnis hat genau ein Paar gleicher Würfe und gehört deshalb zu genau einer der 10 Positionswahlen. Die Fälle überschneiden sich also nicht und sind alle gleich wahrscheinlich. Darum darf man 10-mal dasselbe addieren, also mit 10 multiplizieren.

**Term (verlangt):** P = (5 über 2) · 1 · 1/4 · 3/4 · 2/4 · 1/4 = 10 · 6/256 = **15/64 ≈ 23,4 %**

**Kontrollen (nur zur Sicherheit):**
- Abzählen: (5 über 2) · 4! = 10 · 24 = 240 günstige von 4⁵ = 1024 Ergebnissen → 240/1024 = 15/64 ✓. Der Faktor 4! verteilt die 4 Zahlen auf das Doppel und die 3 Einzelwürfe.
- Nur falls jemand nach dem Gegenereignis fragt: 1 − 4·(3/4)⁵ allein ist **falsch** (≈ 5 %), weil sich „keine 1“, „keine 2“, … überschneiden. Richtig wäre die Siebformel: 1 − 4·(3/4)⁵ + 6·(2/4)⁵ − 4·(1/4)⁵ = 15/64.

**Warum so / was bringt Punkte / typische Fehler**
- a) Punkte gibt es für das Ereignis **im Sachzusammenhang** plus beide Begründungsteile (3/4 pro Wurf, Unabhängigkeit/Exponent 5).
- b) Punkte gibt es für den richtigen Term, also die Struktur „eine Zahl doppelt“, den Faktor (5 über 2) und die Faktorkette.
- Typische Fehler:
  - (5 über 2) vergessen → nur 6/256.
  - 5!/4⁵ rechnen, was die Doppelung falsch zählt.
  - Das Gegenereignis ohne Siebformel benutzen.
  - Bei a) nur „(3/4)⁵ = P(nicht 1)“ schreiben, ohne die fünf Würfe zu nennen.

**Klausurfertige Kurzversion**
- a) „Keine 1 in fünf Würfen“: pro Wurf 3/4, fünf unabhängige Würfe → (3/4)⁵.
- b) Genau eine Zahl doppelt → **(5 über 2) · 1 · 1/4 · 3/4 · 2/4 · 1/4** (= 15/64).

---

## Aufgabe 3 – Analytische Geometrie 2024: Oktaeder im Würfel

**Gegeben:**
- Die Flächenmittelpunkte eines Würfels sind die Ecken eines Oktaeders.
- A(1|2|1), B, C(−3|−6|9) und D liegen in H: 2x₁ + x₂ + 2x₃ = 6.
- Laut Abbildung ist ABCD ein Quadrat, A und C liegen sich gegenüber.
- Probe: 2·1 + 2 + 2·1 = 6 ✓ und 2·(−3) − 6 + 2·9 = 6 ✓.

### a) Nachweisen, dass die Kantenlänge des Würfels 12 ist (2 BE)

1. **Idee:** AC ist laut Abbildung eine Diagonale des Quadrats ABCD, also keine Oktaederkante. Zwei Oktaederecken ohne gemeinsame Kante sind Mittelpunkte **gegenüberliegender** Würfelflächen. Ihre Verbindungsstrecke geht durch den Würfelmittelpunkt und steht senkrecht auf beiden Flächen. Ihre Länge ist also der Abstand der beiden Flächen = Kantenlänge a.
2. **Rechnung:** AC = C − A = (−4 | −8 | 8), |AC| = √(16 + 64 + 64) = √144 = **12** ✓.

### b) Koordinaten einer Oktaederecke außerhalb von H (3 BE)

1. **Mittelpunkt von AC = Würfelmittelpunkt:** M = ½·(A + C) = (−1 | −2 | 5).
2. **Richtung:**
   - Die beiden fehlenden Ecken (E, F) sind die Mittelpunkte des dritten Paars gegenüberliegender Würfelflächen.
   - Die drei Achsen AC, BD und EF gehen durch M und stehen paarweise senkrecht aufeinander.
   - Weil AC und BD in H liegen, steht EF senkrecht auf H. Die Ecken liegen also auf der Geraden durch M in Richtung des Normalenvektors n = (2 | 1 | 2).
3. **Abstand:** Vom Würfelmittelpunkt bis zu einer Flächenmitte ist es die halbe Kantenlänge, also 12 : 2 = **6**.
4. **Länge von n:** |n| = √(4 + 1 + 4) = 3 → für den Abstand 6 braucht man **2·n** (oder 6·n/3).
5. **Ergebnis:** E = M + 2·n = (−1 + 4 | −2 + 2 | 5 + 4) = **(3 | 0 | 9)**. Die zweite Lösung ist M − 2·n = (−5 | −4 | 1); verlangt ist nur eine.

**Probe:**
- Abstand von E zu H: |2·3 + 0 + 2·9 − 6| / 3 = 18/3 = 6 ✓.
- Kante des Oktaeders: |EA| = |(−2 | 2 | −8)| = √72 = 6√2 = 12/√2 ✓ (Seite des Quadrats mit Diagonale 12).

**Warum so / was bringt Punkte / typische Fehler**
- a) Punkte gibt es für den Betrag von AC **mit** der Begründung, warum |AC| die Würfelkante ist.
- b) Punkte gibt es für den Mittelpunkt M, den Normalenvektor mit Länge 3 und den richtigen Vielfachen 2n.
- Typische Fehler:
  - M + 6·n statt M + 2·n, also |n| vergessen.
  - Den Abstand 12 statt 6 nehmen.
  - A und C für benachbart halten, dann käme a = 12√2 heraus.

**Klausurfertige Kurzversion**
- a) A, C gegenüberliegende Flächenmitten → |AC| = √144 = 12 = Kantenlänge.
- b) M = (−1|−2|5), Abstand a/2 = 6, |n| = 3 → **M + 2n = (3|0|9)**.

---

## Welche Aufgabe vorstellen?

| Aufgabe | Vorteil | Risiko |
|---|---|---|
| 1 Analysis | kurz, ein klarer Knackpunkt (Zeichen und Klammern drehen sich) | wirkt eventuell zu kurz; Nachfrage zur Gegenrichtung (jeder Wert wird angenommen) |
| 2 Stochastik | zeigt am meisten Verständnis | b) ist schwer zu erklären; viele mögliche Rückfragen (warum (5 über 2), warum mal 10, Gegenereignis) |
| 3 Geometrie | anschaulich mit Skizze, lineare Schritte, typische Abi-Werkzeuge (Betrag, Mittelpunkt, Normalenvektor) | Begründung „warum senkrecht zu H, warum Abstand 6“ muss sitzen |

**Empfehlung:** Aufgabe 3. Sicherste Alternative mit wenig Aufwand: Aufgabe 1.

## Wahrscheinliche Rückfragen (mit Antwort)

**Aufgabe 1 – Analysis**

| Frage | Antwort |
|---|---|
| Warum ändert die Verschiebung um 5 nichts? | x − 5 durchläuft ganz ℝ, also kommen genau dieselben y-Werte vor. |
| Warum tauschen die Klammern? | Mal −2 dreht die Reihenfolge um: Das angenommene −3 wird zu 7, die nicht erreichte 2 wird zur nicht erreichten −3. |
| f muss nicht stetig sein – wird trotzdem jeder Wert angenommen? | Ja: Zu z setzt man y = (1 − z)/2 ∈ W_f, dann gilt h(x₀ + 5) = z. |

**Aufgabe 2 – Stochastik**

| Frage | Antwort |
|---|---|
| Warum (5 über 2) und nicht 5·4? | Es zählen nur die Positionen des Paars, ohne Reihenfolge; 20 : 2 = 10. |
| Wofür steht die 1 im Term? | Die doppelte Zahl ist frei wählbar: 4/4 = 1. |
| Ist b) eine Binomialverteilung? | Nein, es geht um vier verschiedene Ausgänge, nicht nur Treffer/Niete. a) dagegen ja: B(5; 1/4), P(X = 0). |

**Aufgabe 3 – Geometrie**

| Frage | Antwort |
|---|---|
| Woher weißt du, dass A und C gegenüberliegen? | Aus der Abbildung (Quadratdiagonale). Wären sie benachbart, wäre a = 12√2. |
| Warum 2n und nicht 6n? | \|n\| = 3, also hat 2n die Länge 6. |
| Gibt es noch eine Lösung? | Ja, M − 2n = (−5 | −4 | 1). |

## Präsentationstipps (je ca. 5 Minuten)

**Aufgabe 1 – Analysis:**
1. Einen Zahlenstrahl für [−3; 2[ zeichnen (−3 als voller Punkt, 2 als offener Punkt).
2. Für a) an der 0 spiegeln: −3 landet bei 3, und 3 liegt nicht in der Menge.
3. Für b) drei Zahlenstrahlen untereinander zeichnen: [−3; 2[ → ·(−2) → ]−4; 6] → +1 → ]−3; 7]. Mit Pfeilen zeigen, wohin der volle und der offene Punkt wandern.

**Aufgabe 2 – Stochastik:**
1. Ein Beispielergebnis „2 3 2 1 4“ als fünf Kästchen anschreiben und das Doppel einkreisen.
2. Daran zuerst „genau eine Zahl doppelt“ erklären, dann (5 über 2), dann die Faktorkette.
3. Die Siebformel nur bringen, wenn jemand danach fragt.

**Aufgabe 3 – Geometrie:**
1. Würfel mit Oktaeder skizzieren und A, C, M markieren.
2. Daneben H als waagerechte Linie zeichnen, mit M darauf und einem Pfeil 2n nach oben („6 = a/2“).
3. Zum Schluss die Probe (Abstand 6, Kante 6√2) und die zweite Lösung zeigen.
