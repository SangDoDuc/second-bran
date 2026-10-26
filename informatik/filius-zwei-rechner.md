# Informatik GK – 1. Zwei Rechner sollen miteinander reden (Lösungen)

Informatik Grundkurs MSS 13 · Kommunikation in Rechnernetzen · Arbeitsblatt vom 19.10.2026 · Lösung: Sang Duc Do

**Leitfrage:** Was muss zwischen zwei Rechnern alles vereinbart sein, damit eine Nachricht ankommt?
**Kurzantwort:** eine physische Verbindung, eindeutige Adressen im selben Netz und gemeinsame Regeln (Protokolle) mit passender Software – Details in 1.7.

<div class="warn">
<b>⚠️ Wichtig für 1.4 – aktuelles Filius verhält sich anders als das Blatt erwartet.</b><br>
In der aktuellen Filius-Version (2.14) bekommt <b>jeder neue Rechner dieselbe Adresse 192.168.0.10</b> mit Netzmaske 255.255.255.0 (im Quellcode fest so eingestellt). Die Abbildungen auf dem Blatt (192.168.0.1 / .2 / .3) stammen aus älteren Unterrichtsfolien.<br>
Folge: In 1.4.2 sind beide Adressen <b>gleich</b>, und in 1.4.3 pingt Rechner 1 mit <code>ping 192.168.0.10</code> <b>sich selbst</b> an. Das Terminal meldet zwar Erfolg, Rechner 2 ist aber gar nicht beteiligt (das Kabel blinkt nicht). Ein echter Test ist erst nach 1.5 möglich, wenn die Adressen verschieden sind. Unten stehen deshalb für 1.4 zwei Varianten: <b>A</b> = gleiche Adressen (aktuelles Filius), <b>B</b> = verschiedene Adressen (wie in den Abbildungen).
</div>

---

## 1.1 Vermutung – vor dem Rechner

**Antwort (für die Linien):**
Nein, das Kabel allein reicht nicht. Zusätzlich braucht man: (1) in beiden Laptops eine Netzwerkkarte (Anschluss) für das Kabel, (2) für jeden Rechner eine eigene Adresse, damit klar ist, wer Sender und Empfänger ist, (3) gemeinsame Regeln (eine gemeinsame „Sprache“ = Protokoll), damit der Empfänger die Signale versteht, und (4) Software, die senden und empfangen kann.

*Warum:* Ein Kabel überträgt nur elektrische Signale. Was die Signale bedeuten und an wen sie gehen, muss vorher vereinbart sein – genau das untersucht das Arbeitsblatt.

---

## 1.2 Die Oberfläche von Filius

Keine schriftliche Antwort nötig.

- **Hammer** = Entwurfsmodus: Geräte platzieren, verkabeln, Adressen einstellen.
- **Grüner Pfeil** = Simulationsmodus: Rechner benutzen, Programme starten, testen.
- Der **Stift** in der Werkzeugleiste ist der Dokumentationsmodus (Beschriftungen, Rahmen) – für dieses Blatt nicht nötig.

---

## 1.3 Zwei Rechner verbinden

Keine schriftliche Antwort nötig. Ablauf und worauf man achten muss:

- **1.3.1:** Zwei **Rechner** (oder Notebooks) aus der linken Leiste auf die Arbeitsfläche ziehen. Kabel-Werkzeug anklicken, dann nacheinander Rechner 1 und Rechner 2 anklicken → eine Linie (Kabel) verbindet beide.
- **1.3.2:** Grüner Pfeil → Simulationsmodus. Doppelklick auf Rechner 1 → Desktop öffnet sich → **Software-Installation**. Rechts aus der Liste **„Befehlszeile“** auswählen (so heißt das Terminal im deutschen Filius), mit dem Pfeil nach links schieben, **„Änderungen annehmen“**. Auf dem Desktop erscheint das Symbol „Befehlszeile“. Dasselbe für Rechner 2.

---

## 1.4 Welche Adresse hat mein Rechner?

### 1.4.1 `ipconfig` auf Rechner 1

**Antwort:** IP-Adresse 192.168.0.10, Netzmaske 255.255.255.0 *(aktuelles Filius; bei dir evtl. andere Werte – dann die angezeigten eintragen)*

So sieht die Ausgabe aus:

```
root /> ipconfig
IP Adresse . . . : 192.168.0.10
Netzmaske. . . . : 255.255.255.0
Physische Adresse: (MAC-Adresse, bei jedem Rechner anders)
Standardgateway. :
DNS-Server . . . :
```

### 1.4.2 Vergleich mit Rechner 2

**Variante A (aktuelles Filius) – Antwort:** Beide Rechner haben genau dieselbe IP-Adresse (192.168.0.10) und dieselbe Netzmaske (255.255.255.0). Nur die physische Adresse (MAC-Adresse) unterscheidet sich. Das ist ein Problem: Eine IP-Adresse muss eindeutig sein, sonst weiß niemand, wer gemeint ist.

**Variante B (verschiedene Adressen wie 192.168.0.1 und 192.168.0.2) – Antwort:** Die ersten drei Zahlen (192.168.0) und die Netzmaske sind gleich → beide liegen im selben Netz. Nur die letzte Zahl ist verschieden → sie kennzeichnet den einzelnen Rechner.

### 1.4.3 Ping von Rechner 1 auf Rechner 2

**Variante A – Antwort:** `ping 192.168.0.10` meldet 4 gesendete und 4 empfangene Pakete, 0 % Paketverlust. Aber: Das ist Rechner 1 selbst, denn es ist seine eigene Adresse (das Kabel blinkt nicht). Rechner 2 ist so nicht gezielt erreichbar, solange beide dieselbe Adresse haben.

**Variante B – Antwort:** Wie in Abbildung 3: 4 Paket(e) gesendet, 4 Paket(e) empfangen, 0 % Paketverlust. Jede Zeile zeigt eine Antwort von Rechner 2 mit ttl=64 und der Laufzeit in ms. Die Verbindung funktioniert.

```
root /> ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2)
From 192.168.0.2: icmp_seq=1 ttl=64 time=...ms
From 192.168.0.2: icmp_seq=2 ttl=64 time=...ms
From 192.168.0.2: icmp_seq=3 ttl=64 time=...ms
From 192.168.0.2: icmp_seq=4 ttl=64 time=...ms
--- 192.168.0.2 Paketstatistik ---
4 Paket(e) gesendet, 4 Paket(e) empfangen, 0% Paketverlust
```

*Hintergrund:* `ping` schickt 4 „Echo-Anfragen“ (ungefähr eine pro Sekunde), der Zielrechner schickt jeweils eine „Echo-Antwort“ zurück. Ein Ping an die eigene Adresse verlässt den Rechner nicht, er wird intern beantwortet.

---

## 1.5 Adressen selbst vergeben

- **1.5.1:** Entwurfsmodus (Hammer) → Rechner 1 doppelklicken → unten im Konfigurationsfeld: IP-Adresse **192.168.0.10**, Netzmaske **255.255.255.0**. Rechner 2: **192.168.0.11**, Netzmaske **255.255.255.0**.
- **1.5.2:** Simulationsmodus, auf Rechner 1 `ping 192.168.0.11` → 4 gesendet, 4 empfangen, 0 % Paketverlust; das Kabel blinkt grün. Jetzt ist es ein echter Test über das Kabel.

### 1.5.3 Rechner 2 auf 192.168.5.11 geändert

**Antwort:** Der Ping scheitert, obwohl das Kabel steckt: Es kommt keine Antwort mehr (4× „Timeout!“, 4 gesendet, 0 empfangen, 100 % Paketverlust). Pingt man direkt die neue Adresse 192.168.5.11 an, meldet das Terminal sofort „Zieladresse nicht erreichbar“.

```
root /> ping 192.168.0.11
PING 192.168.0.11 (192.168.0.11)
From 192.168.0.11 (192.168.0.11): icmp_seq=1   -- Timeout!
   … (insgesamt 4×)
--- 192.168.0.11 Paketstatistik ---
4 Paket(e) gesendet, 0 Paket(e) empfangen, 100% Paketverlust

root /> ping 192.168.5.11
Zieladresse nicht erreichbar
```

### 1.5.4 Vermutung zur Ursache

**Antwort:** Die Netzmaske 255.255.255.0 legt fest, dass die ersten drei Zahlen das Netz angeben und nur die letzte Zahl den Rechner. 192.168.0.10 und 192.168.5.11 liegen deshalb in verschiedenen Netzen. Rechner 1 schickt Daten nur direkt an Rechner in seinem eigenen Netz; für ein anderes Netz bräuchte er einen Vermittler (Router/Gateway), den es hier nicht gibt. Unter der alten Adresse 192.168.0.11 meldet sich niemand mehr. → Das Kabel allein reicht nicht, die Adressen müssen zum selben Netz passen.

- **1.5.5:** Rechner 2 wieder auf **192.168.0.11** setzen (Entwurfsmodus), sonst funktioniert 1.6 nicht.

---

## 1.6 Ein dritter kommt dazu

### 1.6.1 Dritten Rechner direkt verbinden

**Antwort:** Es geht nicht. Filius lässt kein zweites Kabel an Rechner 1 bzw. Rechner 2 zu und zeigt die Meldung „Maximale Anzahl angeschlossener Geräte überschritten“. Rechner 3 lässt sich so mit keinem der beiden verbinden.

### 1.6.2 Ursache

**Antwort:** Ein Rechner hat in Filius nur **eine Netzwerkkarte** (in der Konfiguration gibt es nur eine IP-Adresse, eine Netzmaske und eine MAC-Adresse) und damit nur **einen Anschluss**. Ein Kabel verbindet immer genau zwei Anschlüsse. Ist der eine Anschluss belegt, passt kein weiteres Kabel.

*Begründung, warum ab drei Rechnern ein zusätzliches Gerät nötig ist (Lernziel):* Ohne Verteiler bräuchte jeder Rechner für jeden anderen eine eigene Netzwerkkarte und ein eigenes Kabel. Bei n Rechnern sind das n − 1 Netzwerkkarten pro Rechner und n·(n − 1)/2 Kabel – bei 3 Rechnern 3 Kabel, bei 5 Rechnern (Abb. 5) schon 10 Kabel und 4 Karten pro Rechner. Das ist teuer und unübersichtlich. Ein **Switch** löst das: Jeder Rechner braucht nur ein Kabel zum Switch, und der Switch leitet die Daten an den richtigen Anschluss weiter (Sterntopologie).

### 1.6.3 Switch einsetzen

Keine schriftliche Antwort nötig.

- Kabel entfernen: Rechtsklick auf das Kabel → „Verbindung entfernen“ (oder Rechtsklick auf einen Rechner → „Alle Verbindungen entfernen“).
- **Switch** aus der linken Leiste auf die Arbeitsfläche ziehen. Mit dem Kabel-Werkzeug nacheinander Rechner 1, 2 und 3 jeweils mit dem Switch verbinden.
- Rechner 3: IP-Adresse **192.168.0.12**, Netzmaske **255.255.255.0** (Befehlszeile auch auf Rechner 3 installieren).

### 1.6.4 Gegenseitig pingen

Alle sechs Pings funktionieren (jeweils 4 gesendet, 4 empfangen, 0 % Paketverlust):

| von \ nach | Rechner 1 (192.168.0.10) | Rechner 2 (192.168.0.11) | Rechner 3 (192.168.0.12) |
|---|---|---|---|
| Rechner 1 | – | ✅ `ping 192.168.0.11` | ✅ `ping 192.168.0.12` |
| Rechner 2 | ✅ `ping 192.168.0.10` | – | ✅ `ping 192.168.0.12` |
| Rechner 3 | ✅ `ping 192.168.0.10` | ✅ `ping 192.168.0.11` | – |

---

## 1.7 Zusammentragen

**Antwort (drei Voraussetzungen):**

1. **Eine physische Verbindung:** Netzwerkkarte und Kabel als Übertragungsmedium; ab drei Rechnern ein Verteiler (Switch).
2. **Eindeutige Adressen im selben Netz:** Jede IP-Adresse darf nur einmal vorkommen, und alle Rechner brauchen denselben Netzanteil (bei Netzmaske 255.255.255.0: die ersten drei Zahlen gleich).
3. **Gemeinsame Regeln (Protokolle) und passende Software:** Beide Rechner müssen dieselben Vereinbarungen zum Senden und Empfangen nutzen, und das Programm (hier die Befehlszeile mit `ping`) muss installiert sein.

*Vergleich mit 1.1:* Die Vermutung „Kabel allein reicht nicht“ stimmt. Neu dazugekommen ist, dass die Adressen nicht nur vorhanden, sondern **eindeutig** und **im selben Netz** sein müssen (1.4 und 1.5), und dass für mehr als zwei Rechner ein Switch nötig ist (1.6).

---

## Übungen

### Übung 1.1 – Ping von Rechner 1 auf Rechner 3 beobachten

**Antwort:** Während des Pings blinken die Kabel **grün**, sobald eine Nachricht darüber läuft. Hin und her gehen 4 Echo-Anfragen von Rechner 1 an Rechner 3 und 4 Echo-Antworten zurück, also **8 Nachrichten** (etwa eine Anfrage pro Sekunde). Sie laufen nur über die Kabel Rechner 1 – Switch – Rechner 3; das Kabel zu Rechner 2 bleibt dunkel. Kennt Rechner 1 die Hardware-Adresse (MAC) von Rechner 3 noch nicht, z. B. direkt nach dem Start der Simulation, kommen vorher **2 ARP-Nachrichten** dazu: eine Anfrage „Wer hat 192.168.0.12?“ an alle (dann blinken alle drei Kabel) und die Antwort von Rechner 3. Insgesamt sind es dann **10 Nachrichten**. Danach meldet das Terminal: 4 Paket(e) gesendet, 4 Paket(e) empfangen, 0 % Paketverlust.

*Tipp:* Rechtsklick auf Rechner 1 → **„Datenaustausch anzeigen“** listet alle Nachrichten einzeln auf (ARP, ICMP).

### Übung 1.2 – Netz aus 1.6 zeichnen

<div class="figure">
<svg viewBox="0 0 620 330" width="560" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">
  <g stroke="#333" stroke-width="2.5">
    <line x1="310" y1="190" x2="120" y2="80"/>
    <line x1="310" y1="190" x2="500" y2="80"/>
    <line x1="310" y1="190" x2="310" y2="290"/>
  </g>
  <rect x="255" y="170" width="110" height="40" rx="6" fill="#dbe8f7" stroke="#2b5c9e" stroke-width="2"/>
  <text x="310" y="196" text-anchor="middle" font-size="16" font-weight="bold" fill="#173a66">Switch</text>
  <g font-size="13" text-anchor="middle">
    <rect x="45" y="35" width="150" height="62" rx="6" fill="#fff" stroke="#333" stroke-width="2"/>
    <text x="120" y="57" font-weight="bold">Rechner 1</text>
    <text x="120" y="74">192.168.0.10</text>
    <text x="120" y="90" font-size="11" fill="#555">255.255.255.0</text>
    <rect x="425" y="35" width="150" height="62" rx="6" fill="#fff" stroke="#333" stroke-width="2"/>
    <text x="500" y="57" font-weight="bold">Rechner 2</text>
    <text x="500" y="74">192.168.0.11</text>
    <text x="500" y="90" font-size="11" fill="#555">255.255.255.0</text>
    <rect x="235" y="262" width="150" height="62" rx="6" fill="#fff" stroke="#333" stroke-width="2"/>
    <text x="310" y="284" font-weight="bold">Rechner 3</text>
    <text x="310" y="301">192.168.0.12</text>
    <text x="310" y="317" font-size="11" fill="#555">255.255.255.0</text>
  </g>
</svg>
<div class="caption">Sterntopologie: alle drei Rechner hängen mit je einem Kabel am Switch; Netzmaske überall 255.255.255.0.</div>
</div>

Für die eigene Zeichnung: Switch in die Mitte, drei Rechner außen, je **eine** Linie zum Switch (keine Linien zwischen den Rechnern), an jeden Rechner die IP-Adresse schreiben.

### Übung 1.3 – Hausaufgabe: „Ein Kabel über den Atlantik“ (inf-schule 10.1.1)

**Antwort:**

- **Physische Verbindung – ja:** Das Atlantikkabel zwischen Irland und Neufundland war das Übertragungsmedium. Ohne funktionierendes Kabel gab es keine Kommunikation; es fiel 1858 nach etwa drei Wochen aus, und die Verbindung war wieder weg.
- **Gemeinsame Regeln (Protokoll) – ja:** Sender und Empfänger mussten vereinbaren, wie Zeichen als Signale codiert werden (Morsecode: kurz, lang, Pause) und woran man Beginn und Ende einer Übertragung erkennt. Ohne diese Vereinbarungen hätte der Empfänger die Signale nicht deuten können.
- **Adressen – nur eingeschränkt:** Das Kabel verband genau zwei Stationen, wie unsere zwei Rechner mit einem Kabel. Auf dem Kabel selbst war daher klar, wer Empfänger ist. Wer die Nachricht am Ende bekommen sollte, stand im Telegramm selbst (z. B. Queen Victoria an Präsident Buchanan). Sobald mehr Stationen beteiligt sind, braucht man Adressen und Vermittlung – wie unseren Switch.

*Zusatzinfo:* Die erste offizielle Nachricht am 16. August 1858 (98 Wörter) brauchte rund 16 Stunden; per Dampfschiff dauerte eine Nachricht vorher mindestens eine Woche.

---

## Klausurfertige Kurzversion

| Begriff | Bedeutung |
|---|---|
| IP-Adresse | Eindeutige Adresse eines Rechners im Netz, z. B. 192.168.0.10 |
| Netzmaske | Legt fest, welcher Teil der IP-Adresse das Netz angibt; 255.255.255.0 → die ersten drei Zahlen = Netz, die letzte = Rechner |
| Gleiches Netz | Gleicher Netzanteil → direkte Kommunikation möglich; anderes Netz → Router/Gateway nötig |
| `ipconfig` | Zeigt IP-Adresse, Netzmaske, MAC-Adresse, Gateway und DNS-Server an |
| `ping` | Testet die Erreichbarkeit: 4 Echo-Anfragen, 4 Echo-Antworten; Ergebnis = Paketverlust in % |
| Netzwerkkarte | Anschluss eines Rechners ans Netz; ein Rechner hat in Filius genau eine |
| Switch | Verteiler: verbindet mehrere Rechner (Sterntopologie) und leitet Daten gezielt an den richtigen Anschluss weiter |
| Protokoll | Gesamtheit der Vereinbarungen für die Kommunikation (z. B. Morsecode 1858, heute IP/ICMP) |

**Typische Fehler:**

- In 1.4.3 die eigene Adresse anpingen und den Erfolg für eine Verbindung zu Rechner 2 halten.
- Zwei Rechnern dieselbe IP-Adresse geben.
- Annehmen, ein Kabel reiche aus, obwohl die Adressen in verschiedenen Netzen liegen (1.5.3).
- Switch und Router verwechseln: Ein Switch verbindet Rechner **im selben** Netz; für **verschiedene** Netze braucht man einen Router.

---

<div class="sources">
Quellen: Filius-Quellcode, Version 2.14.0 (gitlab.com/filius1/filius) – Standard-IP 192.168.0.10, Ping-Ausgaben, Meldung „Maximale Anzahl angeschlossener Geräte überschritten“ · inf-schule.de, Abschnitt 10.1.1 „Ein Kabel über den Atlantik“ (Problem, Sender-Empfänger-Modell, Kommunikationsprotokolle) · Wikipedia „Transatlantic telegraph cable“ (16.08.1858, 98 Wörter, ca. 16 Stunden, Ausfall nach ca. 3 Wochen)
</div>
