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
