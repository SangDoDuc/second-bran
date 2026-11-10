# Mathe LK – Lernplan Vor-Abi-Klausur Di 17.11.2026

Erstellt 10.11.2026. Fokus: **Analysis + Analytische Geometrie**, Stochastik nur auffrischen.
Rahmen: ca. 30 Std./Woche Arbeit, So-Abend Minijob, Mo Schule bis 17:00 → kurze Wochentags-Blöcke, Samstag lang.

| Tag | Zeit | Thema | Ziel (am Ende kann ich …) |
|---|---|---|---|
| **Di 10.11** | 45 min | Ableitungsregeln + e/ln-Gleichungen | Ketten-, Produkt-, Quotientenregel fehlerfrei; e^x = a und ln-Gleichungen lösen |
| **Mi 11.11** | 60–75 min | Kurvendiskussion (mit e-Funktion) | Nullstellen, Extrem- und Wendepunkte mit hinreichender Bedingung, Monotonie, Krümmung, Verhalten im Unendlichen |
| **Do 12.11** | 60 min | Tangente/Normale, Steckbriefaufgaben, Funktionsscharen | Tangentengleichung, Funktion aus Bedingungen bestimmen, Extrempunkte einer Schar + Ortskurve |
| **Fr 13.11** | 60–75 min | Integralrechnung | Stammfunktionen, Fläche unter/zwischen Graphen, Integralfunktion, Bestand aus Änderungsrate, Mittelwert |
| **Sa 14.11** | 2 × 75 min | Geometrie 1 + 2 | Geraden/Ebenen in allen Formen, Lagebeziehungen, Schnittpunkte/-geraden; Abstände, Winkel, Spiegelung, Dreiecksfläche, Pyramidenvolumen |
| **So 15.11** | 90 min (vor dem Job) | Probeklausur gemischt + 20 min Stochastik | unter Zeitdruck rechnen; Binomial/Normalverteilung, Test, Prognose/Konfidenz, Vierfeldertafel |
| **Mo 16.11** | 45 min | Fehler der Probeklausur + Spickzettel | jede Fehlerart einmal richtig gerechnet; früh schlafen |
| **Di 17.11** | 10 min morgens | Spickzettel lesen | – |

## Ablauf pro Lerntag
1. 10 min Theorie (Spickzettel unten / Erklärung im Chat)
2. 3–5 Übungsaufgaben ohne Lösung → Antworten an Claude → Korrekturtabelle mit Fehlermuster
3. 5 min: neue Fehler in `uebungen/mathe-vorabi.md` notieren

## Meine Fehlermuster (höchste Priorität, jeden Tag 1 Aufgabe dazu)
- Kettenregel: Exponent der Klammer nicht um 1 reduziert
- Produktregel: nur einen Term geschrieben (u'v **+** uv')
- ln angewendet, bevor der e-Term allein stand

## Spickzettel – Muss sitzen
**Analysis**
- (u·v)' = u'v + uv' · (u/v)' = (u'v − uv')/v² · f(g(x))' = f'(g(x))·g'(x) · (e^{g(x)})' = g'(x)·e^{g(x)} · (ln x)' = 1/x
- Extrempunkt: f'(x) = 0 **und** f''(x) ≠ 0 (< 0 Hochpunkt, > 0 Tiefpunkt) · Wendepunkt: f''(x) = 0 und f'''(x) ≠ 0
- Tangente in x₀: y = f'(x₀)·(x − x₀) + f(x₀) · Normale: Steigung −1/f'(x₀)
- e-Gleichung: erst e-Term isolieren, dann ln · Satz vom Nullprodukt: e^x ≠ 0
- Fläche zwischen f und g: ∫ |f − g| dx, Schnittstellen als Grenzen, bei Vorzeichenwechsel aufteilen
- Bestand: B(t) = B(0) + ∫₀ᵗ r(s) ds · Mittelwert: 1/(b−a)·∫ₐᵇ f(x) dx
- Schar: Extrempunkt in Abhängigkeit von a → Ortskurve: x nach a auflösen, in y einsetzen

**Analytische Geometrie**
- Gerade: x = p + r·u · Ebene: x = p + r·u + s·v · Koordinatenform: ax + by + cz = d, n = (a, b, c)
- Normalenvektor: Kreuzprodukt u × v
- Lage Gerade–Ebene: Gerade in Koordinatenform einsetzen → eine Lösung (Schnittpunkt), keine (parallel), immer wahr (liegt drin)
- Lage Gerade–Gerade: Richtungen parallel? → identisch/parallel; sonst gleichsetzen → Schnittpunkt oder windschief
- Abstand Punkt–Ebene: d = |a·x₀ + b·y₀ + c·z₀ − d| / |n|
- Abstand Punkt–Gerade: Lotfußpunkt über Hilfsebene oder (P − F)·u = 0
- Winkel: cos α = |u·v|/(|u|·|v|) · Gerade–Ebene: **sin** α = |u·n|/(|u|·|n|)
- Dreiecksfläche: ½|AB × AC| · Pyramide: V = ⅓·G·h

**Stochastik (Auffrischen)**
- Binomial: P(X = k) = (n über k)·p^k·(1−p)^{n−k}, μ = np, σ = √(np(1−p))
- Normalverteilung nur bei σ > 3, Stetigkeitskorrektur ±0,5
- Prognose: μ ± 1,96σ (nach innen runden) · Konfidenz: |h − p| ≤ 1,96·√(p(1−p)/n)
- bedingte W.: P_B(A) = P(A ∩ B)/P(B), Vierfeldertafel
- Hypothesentest: Ablehnungsbereich so, dass P(Fehler 1. Art) ≤ α
