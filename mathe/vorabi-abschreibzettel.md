---
pagetitle: Abschreib-Zettel Mathe
---

# Abschreib-Zettel Mathe Vor-Abi (zum Abschreiben, ca. 30 min)

*Tipp: langsam abschreiben, die Beispiele mitrechnen, dabei laut im Kopf sagen, was du tust.*

## 1. Ableiten
| Ausdruck | Ableitung |
|---|---|
| Zahl (z. B. 4) | **0** |
| x² | **2x** (Exponent nach vorne, dann −1) |
| a·xⁿ | a·n·xⁿ⁻¹ |
| e^x | e^x |
| e^(−x) | **−e^(−x)** |
| e^(−2x) | **−2·e^(−2x)** (innere Ableitung!) |
| ln(x) | 1/x |

**Produktregel:** (u·v)' = u'·v **+** u·v' → immer **beide** Terme, u, u', v, v' vorher aufschreiben.
**Kettenregel:** äußere Ableitung · innere Ableitung.

**Beispiel:** f(x) = (4 − x²)·e^(−x)
u = 4 − x², u' = −2x · v = e^(−x), v' = −e^(−x)
f'(x) = −2x·e^(−x) + (4 − x²)·(−e^(−x)) = e^(−x)·(x² − 2x − 4)

## 2. Gleichungen mit e
- (Klammer)·e^(…) = 0 → **e^(…) ≠ 0** → Klammer = 0 (Satz vom Nullprodukt)
- e^(…) = Zahl → **erst e-Term allein**, dann ln
- **e⁰ = 1** · ln(e^a) = a · ln(1) = 0
- **√a + √a = 2·√a** (nicht √(2a))

## 3. Kurvendiskussion
| Gesucht | Bedingung |
|---|---|
| Nullstelle | f(x) = 0 |
| y-Achse | f(0) |
| Extremstelle | **1. f'(x) = 0**, 2. in f'' einsetzen: f'' < 0 → HP, f'' > 0 → TP |
| Wendestelle | f''(x) = 0 und f''' ≠ 0 |
| y-Wert | x in **f** einsetzen (nicht in f') |
| x → +∞ bei e^(−x) | e^(−x) → 0 gewinnt → f → 0 |

**pq-Formel:** x² + px + q = 0 → x = −p/2 ± √((p/2)² − q) → p, q sind **Zahlen**.

## 4. Tangente, Winkel, Fläche
- Tangente in x₀: **y = f'(x₀)·(x − x₀) + f(x₀)**
- Schnittwinkel mit x-Achse: **tan α = m** → α = tan⁻¹(|m|)
- Stammfunktion nachweisen: **H ableiten** → muss h ergeben
- Fläche bis ∞: **A = lim (b→∞) [H(b) − H(0)]**

## 5. Analytische Geometrie
- **Richtungsvektor = Spitze − Fuß** (B − A), nie den Ortsvektor nehmen
- Gerade: x = A + k·(B − A) · Ebene: x = A + r·(B − A) + s·(C − A)
- **Skalarprodukt:** u·v = u₁v₁ + u₂v₂ + u₃v₃ → **= 0 heißt senkrecht**
- Winkel: **cos α = |u·v| / (|u|·|v|)**, Länge |u| = √(u₁² + u₂² + u₃²)
- Normalenvektor: **Kreuzprodukt** u × v → Koordinatenform n₁x₁ + n₂x₂ + n₃x₃ = d (Punkt einsetzen)
- Schnitt Gerade–Ebene: Gerade in Koordinatenform einsetzen → k → Punkt; **Strecke: 0 ≤ k ≤ 1**
- Dreiecksfläche: **A = ½·|AB × AC|** (oder ½·g·h)
- Quader/Rechteck prüfen: Kanten an einer Ecke, **Skalarprodukt = 0?**
- Dachpunkt eines Prismas: x₃ = **Boden + Höhe**

## 6. Stochastik
| Formulierung | Rechnung |
|---|---|
| genau k | P(X = k) = (n über k)·p^k·(1−p)^(n−k) |
| höchstens k | Tabelle P(X ≤ k) |
| mehr als k | 1 − P(X ≤ k) |
| mindestens k | 1 − P(X ≤ k − 1) |

- **Mindestens eins in n Versuchen:** 1 − qⁿ ≥ 0,9 → qⁿ ≤ 0,1 → n ≥ ln 0,1 / ln q → **Zeichen dreht sich** (ln q < 0) → **aufrunden**
- **Baum:** „unter der Voraussetzung“ = **Ast** · „und“ = **Pfad** (multiplizieren) · fehlender Ast = Pfad ÷ Ast · Summe aller Pfade = 1
- **Test:** H₀: p = p₀ · H₁: p > p₀ (Verbesserung) · Ablehnungsbereich angeben · **α = P(Ablehnungsbereich) mit p₀**
- **Fehler 1. Art:** H₀ abgelehnt, obwohl wahr (falscher Alarm)
- **Fehler 2. Art:** H₀ behalten, obwohl falsch (echte Veränderung übersehen)

## 7. Klausurtaktik
- „Zeigen Sie“: Weg zählt, **Schlusssatz** schreiben
- Ergebnis aus a) falsch? → mit dem **gegebenen** Wert weiterrechnen
- Am Ende: **Probe** wo möglich (Nullstellen einsetzen, Abstand prüfen)
