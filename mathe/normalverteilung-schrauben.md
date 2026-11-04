# Mathe LK – Stochastik Aufgabe 3: Schrauben (Normalverteilung)

Ausschussquote p = 0,05. Gelöst 04.11.2026, Lösungsweg in Handschrift (GoodNotes/PDF, 1 Seite).

| Teil | Lösung |
|---|---|
| a) | Laplace-Bedingung σ > 3 ⇔ n·p·(1−p) > 9 ⇔ n·0,0475 > 9 ⇔ n > 189,5 → **n ≥ 190** |
| b) | n = 500: μ = 25, σ = √23,75 ≈ 4,87; P(X ≥ 30) = 1 − P(X ≤ 29) ≈ 1 − Φ((29,5 − 25)/4,87) = 1 − Φ(0,923) ≈ **17,8 %** |
| c) | P(X < 20) = P(X ≤ 19) ≈ Φ((19,5 − 25)/4,87) = Φ(−1,129) ≈ **13,0 %** |

Kontrolle mit exakter Binomialverteilung: b) 17,6 %, c) 12,7 % → Näherung passt.
Ohne Stetigkeitskorrektur (±0,5) käme b) 15,2 % und c) 15,2 % heraus – deutlich schlechter.
Mit Φ-Tabelle (z gerundet auf 0,92 / −1,13): b) 17,9 %, c) 12,9 %.

**Typische Fehler:** „mindestens 30“ als 1 − P(X ≤ 30) statt ≤ 29; „weniger als 20“ als ≤ 20; Stetigkeitskorrektur vergessen; σ² statt σ in die Bedingung einsetzen (σ > 3 heißt σ² > 9).
