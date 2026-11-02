# Physik LK – Interferenz im Alltag (Ölfilm, Seifenblase, Morphofalter, CD) – Lösungen

Abiturvorbereitung, Arbeitsblatt 5 Seiten. Bearbeitet 02.11.2026. Handschriftlicher Lösungsweg als GoodNotes/PDF (5 Karo-Seiten).
**(FS)** = Formel steht in der Formelsammlung · **(Blatt)** = Formel steht im Hinweiskasten des Arbeitsblatts.
⚠️ Welche Formeln genau in *deiner* FS stehen, bitte einmal gegenprüfen – Standard sind Gitter (g·sin α = kλ) und Max/Min-Bedingungen (Δs = kλ bzw. (2k+1)λ/2).

## Grundidee (gilt für 1–3)
1. **Phasensprünge zählen:** Reflexion am optisch *dichteren* Medium → +λ/2.
2. **Gangunterschied:** Δs = 2·n·d (senkrecht) bzw. 2d·√(n² − sin²α) (Blatt), + λ/2 pro Phasensprung-*Differenz*.
3. **Genau ein Phasensprung** → Verstärkung bei 2nd = (k − ½)λ, Auslöschung bei 2nd = kλ.
   **Null oder zwei Phasensprünge** → umgekehrt (Verstärkung bei 2nd = kλ).

---

## 1 Ölfilm (n_Öl = 1,50 auf Wasser 1,33)
| | Lösung | Warum |
|---|---|---|
| 1a | Oben Luft → Öl: **Phasensprung λ/2**; unten Öl → Wasser: **keiner** (1,50 > 1,33) | nur Reflexion am dichteren Medium springt |
| 1b | Δs = 2nd + λ/2 · Verstärkung (Δs = kλ, FS): **d = (2k−1)λ/(4n)**, k = 1,2,… · Auslöschung (Δs = (2k+1)λ/2, FS): **d = kλ/(2n)**, k = 0,1,… | ein Phasensprung → λ/2 einbauen |
| 1c | d₁ = 520/(4·1,50) ≈ **86,7 nm**, d₂ = 3·86,7 = **260 nm** | „erscheint grün“ = Verstärkung |
| 1d | 2nd = 780 nm · verstärkt: 1560 (IR), **520 nm (grün)**, 312 (UV) · ausgelöscht: **780 nm, 390 nm** (Ränder) → grün | λ = 2nd/(k−½) bzw. 2nd/k, nur 380–780 nm zählen |
| 1e | Δs' = 2·260·√(2,25 − 0,5) ≈ 688 nm (+λ/2) · verstärkt: **459 nm (blau)** · ausgelöscht: 688 nm (rot) → **blau** · allgemein: Winkel ↑ → Δs ↓ → Farbe wandert Richtung **blau/violett** | √(n² − sin²α) wird kleiner |
| 1f | ohne Öl: nur **eine** Grenzfläche nahe der Oberfläche, Boden cm tief ≫ Kohärenzlänge → keine kohärente 2. Welle · dicker Film (3 µm): 2nd = 9000 nm → **13 verstärkte λ** (k = 12…24) übers ganze Spektrum → Mischung = **weiß**; außerdem Δs > Kohärenzlänge | AFB III: zwei Gründe nennen |

## 2 Seifenblase (n = 1,33, beidseitig Luft, d = 400 nm)
| | Lösung | Warum |
|---|---|---|
| 2a | oben Luft → Wasser: Sprung, unten Wasser → Luft: keiner → **wie Ölfilm genau ein Sprung**, gleiche Bedingungen · Auslöschung: **2nd = kλ** | Vergleich = Gemeinsamkeit *und* Unterschied (unten Luft statt Wasser, aber in beiden Fällen dünneres Medium) |
| 2b | 2nd = 1064 nm · ausgelöscht: **532 nm (grün)** · verstärkt: **709 nm (rot), 426 nm (violett)** → **Purpur/Magenta** | Farbe = Weiß minus ausgelöschte Farbe |
| 2c | Absorption = 0 → R + T = 1: was reflektiert fehlt, geht durch → Grün im Durchlicht → **Komplementärfarbe** · blass: R(Wasser/Luft) ≈ 2 % → im reflektierten Licht zwei fast gleich starke Wellen → fast vollständige Auslöschung; im Durchlicht direkte Welle (~96 %) + winzige 2× reflektierte Welle → kaum Kontrast, viel Weiß | R = ((n−1)/(n+1))² ≈ 0,02 (Zusatzwissen, nicht nötig) |

## 3 Morphofalter (n_C = 1,56, Luftschichten, λ = 470 nm)
| | Lösung | Warum |
|---|---|---|
| 3a | (1) Durchlicht braun statt blau, (2) Alkohol → grün, nach Verdunsten wieder blau → kein Farbstoff · Melanin **absorbiert** das nicht reflektierte Licht → kein weißer Rückstreu-Anteil → kräftiges Blau | „nennen“ + „erläutern“ |
| 3b | Lamelle: oben Sprung, unten keiner → 2n_C d_C + λ/2 = kλ → d_C = (2k−1)λ/(4n_C), k = 1 kleinstes (k = 0 → d < 0) → **d_C = λ/(4n_C) ≈ 75,3 nm** · Luftschicht: oben Chitin→Luft keiner, unten Luft→Chitin Sprung → **d_L = λ/4 = 117,5 nm** | λ/4-Schichten („optische Dicke“ n·d = λ/4) |
| 3c | beide Wellen an Luft → Chitin reflektiert → Sprünge heben sich auf · Δs = 2(n_C d_C + d_L) = 2(117,5 + 117,5) = **470 nm = λ** → Verstärkung · viele Schichten: jede Fläche nur ~5 %, aber viele gleichphasige Wellen addieren sich (kräftig); kleine λ-Abweichungen summieren sich über viele Schichten zu Auslöschung → schmaler Bereich (farbrein) | wie Gitter vs. Doppelspalt |
| 3d | Δs = 2(117,5 + 1,36·117,5) ≈ 554,6 nm → **λ ≈ 555 nm (grün)** · Sprünge gleich, da n_E < n_C · Modell erklärt Beobachtung (grün, nach Verdunsten blau); Einschränkung: kleinerer Brechzahlkontrast → schwächere Reflexion, idealisierte Schichten | „beurteilen“ = Urteil + Einschränkung |

## 4 CD (λ = 532 nm, e = 30,0 cm, a₁ = 10,6 cm, a₂ = 26,7 cm)
| | Lösung | Warum |
|---|---|---|
| 4a | Spuren = **Reflexionsgitter**; Maxima bei g·sin α = kλ (FS); α hängt von λ ab → Rot weiter außen als Blau; jede Ordnung ein Spektrum (innen violett, außen rot), 0. Ordnung weiß | Reihenfolge aus der Formel begründen |
| 4b | tan α = a/e → α₁ ≈ 19,5°, α₂ ≈ 41,7° · g = kλ/sin α → g₁ ≈ 1597 nm, g₂ ≈ 1600 nm → **g ≈ 1,60 µm** · keine Kleinwinkelnäherung: bei 41,7° sin 0,665 vs. tan 0,890 (≈ 34 %), Näherung gäbe 1,20 µm | Näherung nur bis ca. 5–10° |
| 4c | sin α ≤ 1 → k ≤ g/λ ≈ 3,0 → **k_max = 3** (α₃ ≈ 86°) · a₃ = 30 cm·tan 86° ≈ **4,2 m** → auf dem Schirm **nicht beobachtbar** (fast streifend, außerdem g/λ ≈ 3,0 ganz knapp) | Ergebnis immer physikalisch bewerten |
| 4d | sin α = k·532/740 → k = 1: **α ≈ 46,0°**, k = 2: 1,44 > 1 → keine · DVD: 1 Punkt je Seite bei ≈ 31 cm; CD: 2 Punkte je Seite (10,6 / 26,7 cm) → **Anzahl/Lage** der Punkte unterscheiden | |

Messunsicherheit (± 0,2 cm, zur Info): g₁ liegt zwischen ca. 1571 und 1624 nm, g₂ zwischen ca. 1594 und 1607 nm → a₂ liefert das genauere g.

---

## Was bringt Punkte – typische Fehler
| | Was Punkte bringt | Typische Fehler |
|---|---|---|
| dünne Schichten | Phasensprünge **an jeder Grenzfläche begründen** (n-Vergleich) | λ/2 vergessen oder an der falschen Fläche; Max/Min vertauschen |
| Wellenlängen ermitteln | alle k durchprobieren, nur 380–780 nm werten, **Farbe nennen** | nur k = 1 rechnen |
| Begründungen (1f, 2c, 3a, 4c) | zwei Argumente, Fachbegriffe (kohärent, Energieerhaltung, Absorption) | nur ein Satz ohne „weil“ |
| Gitter | tan α = a/e, dann sin α – **nicht** a/e direkt einsetzen | Kleinwinkelnäherung bei großen Winkeln |

## Klausurfertige Kurzversion
- Phasensprung nur am dichteren Medium. **Ein** Sprung → hell: 2nd = (k−½)λ, dunkel: 2nd = kλ.
- Ölfilm/Seifenblase: je ein Sprung. 1c: 86,7 nm / 260 nm · 1d: grün (520) · 1e: blau (459) · 2b: Purpur (532 fehlt) · Durchlicht: Komplementärfarbe, blass.
- Morpho: λ/4-Schichten (75,3 nm Chitin, 117,5 nm Luft) → viele gleichphasige Wellen; Ethanol → 555 nm grün.
- CD: Reflexionsgitter, g ≈ 1,60 µm, k_max = 3 (nicht sichtbar), DVD nur 1. Ordnung bei 46°.
