# Mathe LK – Übungs-Analysisteil 2 (nach Vorbild Vor-Abi 2025) – NUR LÖSUNGEN (Aufgaben als PDF)

f_t(x) = (4 − t·x²)·e^(−x), t ≥ 0. Erstellt 15.11.2026, alle Werte numerisch geprüft.

| Teil | Lösung |
|---|---|
| a i | f_t(0) = 4 → S(0\|4) |
| a ii | e^(−x) ≠ 0 → 4 − tx² = 0 → x = ±2/√t (t > 0); t = 0: keine NS |
| a iii | Abstand 4/√t = 2√2 → √t = √2 → t = 2 |
| b | x → ∞: e^(−x) → 0 dominiert → f_t → 0 (unabh. von t); x → −∞: t > 0 → −∞, t = 0 → +∞ |
| c | f' = −2tx·e^(−x) − (4 − tx²)e^(−x) = e^(−x)(tx² − 2tx − 4) ✓ |
| d | f₀,₅' = e^(−x)(0,5x² − x − 4) = 0 → x² − 2x − 8 = 0 → x = −2, x = 4; f''(−2) = −3e² < 0 → HP; f''(4) = 3e^(−4) > 0 → TP; H(−2\|2e² ≈ 14,78), T(4\|−4e^(−4) ≈ −0,07) |
| e | f₀ = 4e^(−x), B(1\|4/e), m = −4/e ≈ −1,47, α ≈ 55,8°, y = −(4/e)x + 8/e |
| f | h = f_t − f_(t+1) = x²e^(−x); H' = −(2x + 2)e^(−x) + (x² + 2x + 2)e^(−x) = x²e^(−x) ✓ |
| g | A = lim H(b) − H(0) = 0 − (−2) = 2 FE |
