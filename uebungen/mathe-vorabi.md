# Mathe – Vor-Abi-Training (Klausur 2025)

## 14.11.2026 – Teil B Analysis, f_t(x) = (1 − tx²)·e^(−2x)
| Teil | meine Antwort | richtig? | Kern der Lösung |
|---|---|---|---|
| a i | leer | ✗ | f_t(0) = 1 → S(0\|1) ohne t |
| a ii | ausmultipliziert, dann ln | ✗ | Nullprodukt: e^(−2x) ≠ 0 → 1 − tx² = 0 → x = ±1/√t (t > 0); t = 0 keine NS |
| a iii | √8 als x eingesetzt, e^(2x) | ✗ | Abstand 2/√t = √8 → t = 1/2 |
| b | „t bestimmt Schnitt mit y-Achse“ | ✗ | x → ∞: e^(−2x) → 0 gewinnt → f_t → 0 für jedes t |
| c | Produktregel mit e^(2x) | ✗ (Struktur ✓) | f' = e^(−2x)(−2tx − 2 + 2tx²) = 2e^(−2x)(tx² − tx − 1) |
| d | f''(0) ohne f' = 0, e⁰ = e | ✗ | x² − x − 2 = 0 → x = −1 (HP, f'' = −3e² < 0), x = 2 (TP, f'' = 3e^(−4) > 0) |
| e | leer | ✗ | m = f_0'(0,5) = −2/e, α ≈ 36,3°, y = −(2/e)x + 2/e |
| f | nur h hingeschrieben | ✗ | h = 2x²e^(−2x); H' = e^(−2x)(2x²) ✓ |
| g | ∫ von 0 bis 4 | ✗ | A = lim H(b) − H(0) = 0 − (−0,5) = 0,5 FE |

**Fehlermuster:**
1. **Vorzeichen im Exponenten verloren:** e^(−2x) als e^(2x) abgeschrieben (a iii, c, d) → innere Ableitung −2 fehlt.
2. **e⁰ = 1** nicht genutzt (d: e^(2·0) als e gerechnet).
3. **Satz vom Nullprodukt** nicht genutzt, stattdessen ausmultipliziert und ln (a ii) – altes Muster „ln zu früh“.
4. **Notwendige Bedingung f' = 0** übersprungen (d).
5. „Unendlich erstreckende Fläche“ → **uneigentliches Integral** (Grenze → ∞), nicht feste Grenze.
✓ Positiv: Produktregel mit beiden Termen und u, u', v, v' sauber notiert.

## 15.11.2026 – Analysis Block 1 (Wiederholung)
| Nr. | meine Antwort | richtig? | Erklärung |
|---|---|---|---|
| 1a | x = ±√(1/t) mit e^(−2x) ≠ 0 | ✓ | Nullprodukt sitzt |
| 1b | √(1/t) + √(1/t) = √(2/t) → t = 0,125 | ✗ | √a + √a = 2√a → 2√(1/t) = 4 → t = 1/4 |
| 2a | u' = −2·0,5x², falsch ausgeklammert | ✗ | u' = −x (Exponent −1!); f' = e^(−2x)(x² − x − 2) |
Fortschritt: v' = −2e^(−2x) mit Minus ✓, e^(−2x) ≠ 0 ✓.

## 15.11.2026 – Teil B Geometrie a–c
| Nr. | meine Antwort | richtig? | Erklärung |
|---|---|---|---|
| a | zwei Geraden schneiden sich in C₂ | ~ | genauer: Gerade durch B₂ mit Richtung A₂D₂ und Gerade durch D₂ mit Richtung A₂B₂ (Parallelogramm ergänzen), Schnitt r = s = 1 → C₂ |
| b | ja, Quader | ✗ | A₂B₂·A₂D₂ = (5\|15\|0)·(−5\|2\|0) = 5 ≠ 0 → kein rechter Winkel → kein Quader |
| c | Ortsvektoren B₁, F₁ als Richtungen, F₁(5\|15\|7) | ✗ | F₁(5\|15\|8) (Höhe 5 über x₃ = 3); Richtungen = Differenzen: E: x = (5\|0\|3) + r(0\|15\|0) + s(0\|15\|5) → E: x₁ = 5 |
**Muster:** Richtungsvektor = Spitze − Fuß (nicht Ortsvektor); „Quader“ immer mit Skalarprodukt = 0 prüfen.

## 15.11.2026 – Übungs-Analysis 2 (f_t = (4 − tx²)e^(−x)), a–d
| Nr. | meine Antwort | richtig? | Erklärung |
|---|---|---|---|
| a i | f_t(0) = 4·1 = 4, S(0\|4) | ✓ | e⁰ = 1 sitzt |
| a ii | x = ±√(4/t) | ✓ | Nullprodukt sitzt |
| a iii | quadriert: 4/t + 4/t = 8 → t = 1 | ✗ | (√a + √a)² ≠ a + a; erst 2√(4/t) = 2√2 → 4/t = 2 → t = 2 |
| b | „weil x → ∞ von e^(−x) kommt“ | ~ | e^(−x) → 0 dominiert → f_t → 0 für alle t; x → −∞ fehlt |
| c | u' = 4 − tx²·2, v' = e^(−x) | ✗ | u' = −2tx (Konstante → 0, Exponent −1), v' = −e^(−x) |
| d | f'(0) eingesetzt, f'' = 0 gelöst, pq falsch | ✗ | f' = 0: x² − 2x − 8 = 0 → x = −2 (HP), 4 (TP); f'' = 0 wären Wendestellen |
**Muster (bleibt):** Grundableitungen (Konstante → 0, x² → 2x, e^(−x) → −e^(−x)); Extremstellen-Schema (erst f' = 0); √a + √a = 2√a. pq-Formel: p, q sind Zahlen.

## 16.11.2026 – Session 1, Block 1: Ableitungs-Drill
| Nr. | meine Antwort | richtig? | Erklärung |
|---|---|---|---|
| 1 | f' = −6x | ✓ | Konstante → 0, x² → 2x sitzt |
| 2 | f' = −e^(−x) | ✓ | innere Ableitung −1 dabei |
| 3 | f' = −3e^(−3x) | ✓ | innere Ableitung −3 dabei |
| 4 | Ansatz ✓, vereinfacht zu e^(−x)(2x − 2 − x²) | ✗ | (2 − x²)·(−1) = −2 + x² → f' = e^(−x)(x² − 2x − 2) |
| 5 | Ansatz ✓, vereinfacht zu e^(2x)(x² + x + 1) | ✗ | (x² + 1)·2 = 2x² + 2 → f' = e^(2x)(2x² + 2x + 2) = 2e^(2x)(x² + x + 1) |
**Muster (neu):** Ableiten selbst sitzt jetzt (u, u', v, v', beide Terme). Punkte gehen beim **Ausklammern** verloren: Minus vor der Klammer nicht in jedes Glied gezogen (4), Faktor 2 beim Ausklammern verloren (5).

## 16.11.2026 – Abend: Ausklammern + Tangente
| Nr. | meine Antwort | richtig? | Erklärung |
|---|---|---|---|
| A1 | e^(−x)(−x² − 2x + 3) | ✗ | (3 − x²)·(−1) = −3 + x² → e^(−x)(x² − 2x − 3) |
| A2 | 2e^(2x)(x² + x + 3) | ✓ | Faktor 2 diesmal korrekt ausgeklammert |
| B1 | e^(−0) = −1 → P(0\|−2) | ✗ | −0 = 0 → e⁰ = 1 → P(0\|2); e^(…) ist nie negativ |
| B2 | f' = −e^(−x), m = 1 | ✗ | Faktor 2 bleibt: f' = −2e^(−x); −e⁰ = −1 → m = −2 |
| B3 | tan α = 1 | ✗ (Folgefehler) | tan α = \|−2\| = 2 → α ≈ 63,4° |
| B4 | offen | – | y = −2(x − 0) + 2 = −2x + 2 |
**Muster:** Minus vor Klammer (2. Mal!), e^(−0) = 1, konstanter Faktor beim Ableiten bleibt stehen.
