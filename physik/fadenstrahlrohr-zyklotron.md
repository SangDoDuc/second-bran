---
pagetitle: Fadenstrahlrohr und Zyklotron
---

# Physik LK – Fadenstrahlrohr und Zyklotron

Vorbereitung auf die Stunde am Di 24.11.2026. Beide Themen beruhen auf derselben Idee: **Lorentzkraft = Zentripetalkraft**.
Alle Beispielzahlen wurden nachgerechnet (e = 1,602·10⁻¹⁹ C, mₑ = 9,109·10⁻³¹ kg, mₚ = 1,673·10⁻²⁷ kg).

---

## 0. Grundlage: geladenes Teilchen im Magnetfeld

| Was | Formel | Bedeutung |
|---|---|---|
| Lorentzkraft (v ⊥ B) | **F<sub>L</sub> = q · v · B** | Kraft auf eine bewegte Ladung im Magnetfeld |
| Richtung | Drei-Finger-Regel | **rechte Hand** für positive Ladung, **linke Hand** für Elektronen. Daumen = Bewegung (Ursache), Zeigefinger = B (Vermittlung), Mittelfinger = F (Wirkung) |
| Zentripetalkraft | **F<sub>Z</sub> = m · v² / r** | Kraft, die nötig ist, damit sich etwas auf einem Kreis bewegt |
| Beschleunigung im E-Feld | **q · U = ½ · m · v²** | elektrische Energie wird zu Bewegungsenergie |

**Die wichtigste Begründung überhaupt:**
Die Lorentzkraft steht **immer senkrecht** zur Geschwindigkeit. Sie ändert deshalb nur die **Richtung**, nicht den **Betrag** der Geschwindigkeit. Sie verrichtet **keine Arbeit**, die Energie des Teilchens bleibt gleich. Weil v und B konstant bleiben, ist auch F<sub>L</sub> konstant und zeigt immer zur Mitte → **Kreisbahn**.

**Kreisbahn-Formel (gilt für beide Themen):**
F<sub>L</sub> = F<sub>Z</sub> → q·v·B = m·v²/r → **r = m·v / (q·B)**

---

## 1. Fadenstrahlrohr (Bestimmung der spezifischen Ladung e/m)

<svg viewBox="0 0 420 300" width="420" xmlns="http://www.w3.org/2000/svg" font-family="Arial" font-size="12">
  <circle cx="200" cy="150" r="130" fill="#f4f8ff" stroke="#555" stroke-width="2"/>
  <g fill="#999">
    <text x="110" y="80">⊙</text><text x="200" y="60">⊙</text><text x="290" y="80">⊙</text>
    <text x="90" y="170">⊙</text><text x="310" y="170">⊙</text><text x="200" y="150">⊙</text>
    <text x="140" y="250">⊙</text><text x="260" y="250">⊙</text>
  </g>
  <circle cx="200" cy="140" r="70" fill="none" stroke="#2a7" stroke-width="3" stroke-dasharray="6 3"/>
  <rect x="70" y="200" width="60" height="20" fill="#ccc" stroke="#555"/>
  <text x="62" y="236">Glühkathode + Anode</text>
  <line x1="130" y1="210" x2="200" y2="210" stroke="#2a7" stroke-width="3"/>
  <line x1="200" y1="210" x2="250" y2="210" stroke="#c33" stroke-width="2" marker-end="url(#a)"/>
  <text x="252" y="224" fill="#c33">v</text>
  <line x1="200" y1="210" x2="200" y2="170" stroke="#36c" stroke-width="2" marker-end="url(#b)"/>
  <text x="205" y="185" fill="#36c">F_L</text>
  <circle cx="200" cy="140" r="3" fill="#000"/><text x="206" y="137">M</text>
  <line x1="200" y1="140" x2="270" y2="140" stroke="#000" stroke-dasharray="3 2"/><text x="228" y="134">r</text>
  <text x="300" y="30" fill="#555">B aus der Ebene (⊙)</text>
  <text x="5" y="290" fill="#555">Gas (Wasserstoff) leuchtet entlang der Elektronenbahn</text>
  <defs>
    <marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#c33"/></marker>
    <marker id="b" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#36c"/></marker>
  </defs>
</svg>

### Aufbau

| Bauteil | Aufgabe |
|---|---|
| **Glaskolben** mit Wasserstoff (oder Neon) bei **sehr geringem Druck** | Elektronen stoßen Gasatome an, die dabei leuchten (Stoßanregung). So wird die Bahn **sichtbar**. Der Druck ist gering, damit die Elektronen kaum abgebremst werden |
| **Glühkathode** | Elektronen treten durch Erhitzen aus (glühelektrischer Effekt) |
| **Anode** mit Beschleunigungsspannung **U<sub>B</sub>** | beschleunigt die Elektronen auf die Geschwindigkeit v |
| **Helmholtz-Spulenpaar** (zwei Spulen im Abstand ihres Radius) | erzeugt ein **homogenes** Magnetfeld B senkrecht zur Bahn. Die Stärke von B wird über den Spulenstrom I eingestellt |

### Ablauf
1. Ohne Magnetfeld fliegen die Elektronen geradeaus.
2. Mit Magnetfeld werden sie durch die Lorentzkraft auf eine **Kreisbahn** gezwungen.
3. Man misst **U<sub>B</sub>**, **I** (daraus B) und den **Radius r**, meist über Markierungen im Kolben (Durchmesser ablesen).

### Herleitung e/m (Schritt für Schritt)
1. **Energie:** e·U<sub>B</sub> = ½·m·v² → v² = 2·e·U<sub>B</sub> / m
2. **Kreisbahn:** e·v·B = m·v²/r → v = e·B·r / m
3. Gleichung 2 quadrieren: v² = e²·B²·r² / m²
4. Beide v² gleichsetzen: 2·e·U<sub>B</sub> / m = e²·B²·r² / m²
5. Mit m² multiplizieren und durch e·B²·r² teilen:

**e/m = 2·U<sub>B</sub> / (B² · r²)**

Literaturwert: **e/m ≈ 1,76 · 10¹¹ C/kg**

**Magnetfeld der Helmholtz-Spulen** (steht in der Formelsammlung):
B = (4/5)<sup>3/2</sup> · μ₀ · n · I / R ≈ 0,716 · μ₀ · n · I / R (n = Windungszahl einer Spule, R = Spulenradius)

### Zusammenhänge (typische Begründungsaufgaben)
Aus r = √(2·U<sub>B</sub>·m/e) / B folgt:

| Änderung | Wirkung auf r | Begründung |
|---|---|---|
| U<sub>B</sub> größer | r **größer** (r ~ √U<sub>B</sub>) | Elektronen sind schneller, bei gleicher Kraft werden sie weniger stark „herumgebogen“ |
| B größer (mehr Spulenstrom) | r **kleiner** (r ~ 1/B) | größere Lorentzkraft, stärkere Ablenkung |
| U<sub>B</sub> vervierfacht | r **verdoppelt** | wegen der Wurzel |
| v nicht senkrecht zu B | **Schraubenbahn** (Helix) | nur der Anteil von v senkrecht zu B wird abgelenkt, der parallele Anteil bleibt |
| Magnetfeld umgepolt | Kreis in die **andere Richtung** | Lorentzkraft zeigt in die Gegenrichtung |

### Beispielrechnung
U<sub>B</sub> = 200 V, B = 1,0 mT:
- v = √(2 · 1,76·10¹¹ C/kg · 200 V) ≈ **8,4 · 10⁶ m/s** (ca. 2,8 % der Lichtgeschwindigkeit, also nicht relativistisch)
- r = v / ((e/m) · B) = 8,4·10⁶ / (1,76·10¹¹ · 1,0·10⁻³) m ≈ **4,8 cm**

### Bedeutung
- Mit e/m und der Elementarladung e aus dem **Millikan-Versuch** erhält man die **Elektronenmasse**: m = e / (e/m) ≈ 9,1·10⁻³¹ kg.

---

## 2. Zyklotron (Kreisbeschleuniger)

<svg viewBox="0 0 420 280" width="420" xmlns="http://www.w3.org/2000/svg" font-family="Arial" font-size="12">
  <path d="M195,30 A110,110 0 0,0 195,250 Z" fill="#eaf1fb" stroke="#555" stroke-width="2"/>
  <path d="M225,30 A110,110 0 0,1 225,250 Z" fill="#eaf1fb" stroke="#555" stroke-width="2"/>
  <text x="120" y="145" fill="#555">Duant 1</text><text x="255" y="145" fill="#555">Duant 2</text>
  <path d="M210,140 a10,10 0 0,1 0,20 a22,22 0 0,1 0,-44 a36,36 0 0,1 0,72 a52,52 0 0,1 0,-104 a70,70 0 0,1 0,140 a88,88 0 0,1 0,-176" fill="none" stroke="#c33" stroke-width="2"/>
  <circle cx="210" cy="150" r="4" fill="#000"/><text x="140" y="270" fill="#000">Ionenquelle in der Mitte</text>
  <line x1="210" y1="5" x2="210" y2="20" stroke="#000"/><text x="216" y="16">Spalt: Wechselspannung U~</text>
  <text x="320" y="40" fill="#555">B in die Ebene (⊗)</text>
  <line x1="210" y1="54" x2="380" y2="54" stroke="#c33" stroke-width="2"/><text x="330" y="70" fill="#c33">Austritt</text>
</svg>

### Aufbau
| Bauteil | Aufgabe |
|---|---|
| **zwei D-förmige, hohle Metallelektroden (Duanten)** | Im Inneren ist **kein elektrisches Feld** (wie im Faraday-Käfig). Dort fliegen die Teilchen nur unter dem Einfluss des Magnetfelds |
| **Spalt** zwischen den Duanten mit **hochfrequenter Wechselspannung U** | Hier werden die Teilchen jedes Mal **beschleunigt** |
| **großer Elektromagnet** | homogenes Magnetfeld B senkrecht zu den Duanten → **Halbkreise** |
| **Ionenquelle** in der Mitte | liefert die Teilchen (meist Protonen, Deuteronen oder α-Teilchen) |
| **Vakuum** | keine Zusammenstöße mit Gasteilchen |

### Funktionsweise (Schritt für Schritt)
1. Ein Teilchen startet in der Mitte und wird im Spalt zum Duanten hin **beschleunigt**.
2. Im Duanten beschreibt es wegen der Lorentzkraft einen **Halbkreis**.
3. Wenn es wieder am Spalt ankommt, hat die Wechselspannung **umgepolt**. Das Teilchen wird **erneut beschleunigt**.
4. Mit jeder Beschleunigung wird v größer, also auch der Radius r = m·v/(q·B) → Bahn ist eine **Spirale nach außen**.
5. Am Rand wird das Teilchen herausgelenkt.

### Der Trick: Die Umlaufzeit ist konstant
- Umlaufzeit: T = 2π·r / v. Einsetzen von r = m·v/(q·B):
- **T = 2π·m / (q·B)**, Frequenz **f = q·B / (2π·m)** (Zyklotronfrequenz)
- **T hängt weder von v noch von r ab.** Schnellere Teilchen fliegen einen größeren Kreis, brauchen dafür aber genauso lange.
- → Die Wechselspannung kann mit **fester Frequenz** arbeiten und bleibt immer im Takt mit dem Teilchen.

### Endenergie
- Am Rand (Radius R): v<sub>max</sub> = q·B·R / m
- **E<sub>kin</sub> = ½·m·v² = q²·B²·R² / (2·m)**
- Die Endenergie hängt **nicht von der Spannung U** ab. Eine größere Spannung bedeutet nur **weniger Umläufe**, bis der Rand erreicht ist.
- Energie pro Umlauf: 2·q·U (zweimal durch den Spalt). Anzahl der Umläufe: N = E<sub>kin</sub> / (2·q·U)

### Beispielrechnung (Protonen)
B = 1,0 T, R = 0,50 m, U = 10 kV:
- f = q·B / (2π·m) = 1,602·10⁻¹⁹ · 1,0 / (2π · 1,673·10⁻²⁷) Hz ≈ **15 MHz**
- E<sub>kin</sub> = q²·B²·R² / (2·m) ≈ 1,9·10⁻¹² J ≈ **12 MeV**
- Pro Umlauf 2 · 10 keV = 20 keV → N ≈ 12 MeV / 20 keV ≈ **600 Umläufe**
- v<sub>max</sub> ≈ 4,8·10⁷ m/s ≈ 16 % der Lichtgeschwindigkeit

### Grenze des Zyklotrons
- Bei hohen Geschwindigkeiten (nahe c) wird das Teilchen **relativistisch**: Seine Masse nimmt scheinbar zu.
- Dann wird T = 2π·m/(q·B) **größer**, das Teilchen kommt **zu spät** am Spalt an und gerät aus dem Takt.
- Lösungen: **Synchrozyklotron** (Frequenz wird angepasst) oder **Synchrotron** (B wird angepasst, Radius bleibt fest, z. B. am CERN).
- **Elektronen** eignen sich deshalb kaum: Sie sind so leicht, dass sie schon bei kleinen Energien relativistisch werden.

### Anwendungen
- Medizin: Herstellung radioaktiver Stoffe für die **PET-Untersuchung**, **Protonentherapie** gegen Tumore
- Forschung: Kernphysik
- Erfunden von Ernest Lawrence (1930er Jahre)

---

## 3. Vergleich

| | Fadenstrahlrohr | Zyklotron |
|---|---|---|
| Teilchen | Elektronen | meist Protonen, Deuteronen, α-Teilchen |
| Ziel | **messen**: e/m bestimmen | **beschleunigen**: hohe Energie |
| Beschleunigung | einmal (U<sub>B</sub>) | sehr oft im Spalt (Wechselspannung) |
| Bahn | ein Kreis mit festem Radius | Spirale nach außen |
| Gemeinsam | Lorentzkraft = Zentripetalkraft, r = m·v/(q·B), Magnetfeld ändert nur die Richtung, nicht die Energie |

---

## 4. Begründungsaufgaben: Musterformulierungen

Das ist dein wichtigster Hebel (CLAUDE.md: Punkte gehen bei Begründungen verloren).

| Frage | Musterantwort |
|---|---|
| Warum bewegen sich die Elektronen auf einer Kreisbahn? | Die Lorentzkraft wirkt stets senkrecht zur Geschwindigkeit. Sie ändert nur die Richtung, nicht den Betrag von v. Da v und B konstant sind, ist auch die Kraft konstant und zeigt immer zum Mittelpunkt. Sie wirkt als Zentripetalkraft → Kreisbahn. |
| Warum ist die Bahn sichtbar? | Die Elektronen stoßen Gasatome an und regen sie an. Beim Zurückfallen in den Grundzustand senden die Atome Licht aus. |
| Warum ist der Gasdruck gering? | Damit die Elektronen selten zusammenstoßen und kaum abgebremst werden. Sonst würde r kleiner werden und die Bahn wäre keine saubere Kreisbahn. |
| Warum Helmholtz-Spulen? | Sie erzeugen zwischen sich ein nahezu **homogenes** Magnetfeld. Nur dann ist B überall gleich und die Bahn ein Kreis. |
| Warum ändert das Magnetfeld die Energie nicht? | F<sub>L</sub> steht senkrecht auf v, deshalb verrichtet die Kraft keine Arbeit (W = F·s·cos 90° = 0). |
| Warum kann das Zyklotron mit fester Frequenz arbeiten? | Die Umlaufzeit T = 2π·m/(q·B) hängt nicht von v und r ab. Schnellere Teilchen laufen auf größeren Kreisen, brauchen aber gleich lang. |
| Warum werden die Teilchen nur im Spalt beschleunigt? | Im Inneren der hohlen Duanten ist kein elektrisches Feld (Abschirmung). Nur im Spalt liegt die Spannung an. |
| Warum hängt die Endenergie nicht von U ab? | Die Endenergie hängt nur vom maximalen Radius ab: E = q²B²R²/(2m). U bestimmt nur, wie viele Umläufe nötig sind. |
| Warum funktioniert das Zyklotron bei sehr hohen Energien nicht mehr? | Relativistische Massenzunahme → T wird größer → das Teilchen erreicht den Spalt zu spät und wird nicht mehr im Takt beschleunigt. |

---

## Warum so – was bringt Punkte – typische Fehler

| | |
|---|---|
| **Warum so** | Beide Geräte nutzen denselben Ansatz F<sub>L</sub> = F<sub>Z</sub>. Wer den sicher herleiten kann, kann beide Themen. |
| **Was bringt Punkte** | Ansatz hinschreiben (F<sub>L</sub> = F<sub>Z</sub>, Energiesatz), Herleitung Schritt für Schritt, Begründung mit „senkrecht → keine Arbeit“, Einheiten |
| **Typische Fehler** | Drei-Finger-Regel mit der falschen Hand (Elektronen = **links**) · r ~ U statt r ~ √U · e/m-Formel falsch umgestellt (Kreuzmultiplizieren vs. Teilen, dein Algebra-Muster) · beim Zyklotron behaupten, eine größere Spannung ergebe mehr Endenergie · vergessen, dass das Teilchen pro Umlauf **zweimal** beschleunigt wird · mT nicht in T umgerechnet |

---

## Klausurfertige Kurzversion

- **Grundidee:** F<sub>L</sub> = q·v·B steht senkrecht auf v → ändert nur die Richtung, keine Arbeit → Kreis. F<sub>L</sub> = F<sub>Z</sub> ergibt **r = m·v/(q·B)**.
- **Fadenstrahlrohr:** Elektronen aus der Glühkathode, mit U<sub>B</sub> beschleunigt, im homogenen Feld der Helmholtz-Spulen auf einer Kreisbahn, Gas macht die Bahn sichtbar. e·U<sub>B</sub> = ½mv² und e·v·B = mv²/r ergeben **e/m = 2U<sub>B</sub>/(B²r²) ≈ 1,76·10¹¹ C/kg**. r ~ √U<sub>B</sub>, r ~ 1/B.
- **Zyklotron:** zwei Duanten, Wechselspannung im Spalt beschleunigt, Magnetfeld biegt auf Halbkreise → Spirale. **T = 2πm/(qB)** unabhängig von v → feste Frequenz. **E<sub>max</sub> = q²B²R²/(2m)**, unabhängig von U. Grenze: relativistische Massenzunahme → Synchrotron.

---

## Übung (ohne Lösung, schick mir deine Antworten)

1. In einem Fadenstrahlrohr ist U<sub>B</sub> = 250 V und B = 1,2 mT. Der Bahndurchmesser beträgt 9,0 cm. Berechne e/m.
2. Wie ändert sich der Radius, wenn U<sub>B</sub> verdoppelt wird? Begründe.
3. Begründe, warum die Elektronen im Fadenstrahlrohr ihre Geschwindigkeit auf der Kreisbahn nicht ändern.
4. In einem Zyklotron mit B = 1,5 T werden Protonen beschleunigt. Berechne die Frequenz der Wechselspannung.
5. Erkläre, warum man im Zyklotron die Spannung erhöhen kann, ohne dass die Teilchen am Ende mehr Energie haben.
