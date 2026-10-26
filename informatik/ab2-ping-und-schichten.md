# Informatik GK – Arbeitsblatt 2: Was bei einem Ping passiert (Lösungen)

Informatik · MSS 13 · Grundkurs · 26.10.2026 · Netz aus AB1: Rechner 1–3 = 192.168.0.10 / .11 / .12, Netzmaske 255.255.255.0, ein Switch.

> **Hinweis zu den Werten:** Die MAC-Adressen vergibt Filius bei jedem Rechner **zufällig** (Format `xx:xx:xx:xx:xx:xx`, Kleinbuchstaben). `4e:05:b2:6c:13:da` (Rechner 3) ist ein Beispiel – bei dir stehen andere Werte. IP-Adressen, Protokolle und Schichten stimmen.
> Geprüft im Filius-Quellcode (Version 2.14): Fenster „Datenaustausch“, ARP- und ICMP-Zeilen, Switch-Tabelle (SAT).

---

## Teil A

**A1** – keine schriftliche Antwort (Netz laden/bauen, `ping 192.168.0.12` von Rechner 1 → 4 gesendet, 4 empfangen, 0 % Verlust).

**A2 – drei Voraussetzungen (aus AB1, 1.7)**
1. Verbindung: Netzwerkkarte und Kabel, ab drei Rechnern ein Switch
2. eindeutige IP-Adressen im selben Netz, also mit passender Netzmaske
3. gleiche Protokolle und passende Software (hier das Terminal mit `ping`)

**A3 a) Spaltenüberschriften:** Nr. · Zeit · Quelle · Ziel · Protokoll · Schicht · Bemerkungen / Details

**A3 b) Die ersten sechs Zeilen** (Ping Rechner 1 → Rechner 3):

| Nr. | Quelle | Ziel | Protokoll | Schicht |
|---|---|---|---|---|
| 1 | 192.168.0.10 | 192.168.0.12 | ARP | Vermittlung |
| 2 | 192.168.0.12 | 192.168.0.10 | ARP | Vermittlung |
| 3 | 192.168.0.10 | 192.168.0.12 | ICMP | Vermittlung |
| 4 | 192.168.0.12 | 192.168.0.10 | ICMP | Vermittlung |
| 5 | 192.168.0.10 | 192.168.0.12 | ICMP | Vermittlung |
| 6 | 192.168.0.12 | 192.168.0.10 | ICMP | Vermittlung |

*Warum so:* Das Standard-Fenster in Filius zeigt **pro Paket eine Zeile** (die oberste beteiligte Schicht). Erst fragt Rechner 1 per ARP nach der MAC von .12 (1), Rechner 3 antwortet (2), dann laufen Echo-Anfrage und -Antwort hin und her (3–6).
*Falls bei dir die alte Ansicht eingestellt ist:* Dann steht jedes Paket in **zwei** Zeilen mit derselben Nr. – einmal „Netzzugang“ mit MAC-Adressen (Ziel der ARP-Anfrage: `FF:FF:FF:FF:FF:FF`) und einmal „Vermittlung“ mit IP-Adressen.
*Falls oben keine ARP-Zeilen stehen:* Rechner 1 kennt die MAC schon aus dem Ping in A1b. Einmal in den Entwurfsmodus und zurück wechseln, dann ist alles zurückgesetzt.

---

## Teil B

**B1 a)**
- 1. ARP-Zeile: Rechner 1 fragt alle Geräte: „Suche nach MAC für 192.168.0.12“ – also: Wer hat diese IP-Adresse?
- 2. ARP-Zeile: Rechner 3 antwortet: „MAC ist 4e:05:b2:6c:13:da“.

**B1 b)** `4e:05:b2:6c:13:da` ist die **MAC-Adresse**: sechs Blöcke aus je zwei Hexadezimalziffern (0–9, a–f), durch Doppelpunkte getrennt, zusammen 48 Bit. Sie ist fest in der Netzwerkkarte gespeichert.

**B1 c)** Im lokalen Netz werden Rahmen an **MAC-Adressen** zugestellt – Netzwerkkarte und Switch kennen keine IP-Adressen. Die IP-Adresse gehört zur Vermittlungsschicht, die MAC-Adresse zum Netzzugang. Deshalb muss Rechner 1 erst per **ARP** die passende MAC herausfinden; danach merkt er sie sich (ARP-Tabelle), beim nächsten Ping entfällt die Frage.

**B2 a)**

| | IP-Adresse | MAC-Adresse |
|---|---|---|
| Beispiel | 192.168.0.12 | 4e:05:b2:6c:13:da |
| Wer vergibt sie? | der Administrator (von Hand) oder ein DHCP-Server | der Hersteller der Netzwerkkarte |
| Ändert sie sich in einem anderen Netz? | ja – sie muss zum neuen Netz passen | nein – bleibt gleich, fest in der Karte |

**B2 b)** Der Switch lernt mit: In seiner Tabelle (SAT, *Source Address Table*) merkt er sich, an welchem Port welche **Absender-MAC** ankommt. Einen Rahmen an eine bekannte Ziel-MAC schickt er nur an diesen einen Port. Ist die Ziel-MAC unbekannt oder die Broadcast-Adresse `FF:FF:FF:FF:FF:FF` (wie bei der ARP-Anfrage), schickt er ihn an alle Ports. *(In Filius: Rechtsklick auf den Switch → „SAT Tabelle“.)*

---

## Teil C

**C1 a)**

| Nr. | Schicht | Aufgabe | Beispiel | Adressart |
|---|---|---|---|---|
| 4 | Anwendung | Dienste für Programme | HTTP, DNS | Domainname |
| 3 | Transport | Daten an das richtige Programm | TCP, UDP | Port |
| 2 | Vermittlung | Weg zum Zielrechner finden | IP, ICMP, ARP | IP-Adresse |
| 1 | Netzzugang | Rahmen im lokalen Netz senden | Ethernet, WLAN | MAC-Adresse |

**C1 b)** Beide gehören zur **Vermittlung** – so steht es auch in Filius in der Spalte „Schicht“. ICMP arbeitet mit IP-Adressen und meldet, ob ein Ziel erreichbar ist. ARP sucht zur IP-Adresse die MAC-Adresse und verbindet so Vermittlung und Netzzugang (liegt genau an der Grenze).

**C2 a)** Nur die unterste Schicht, der **Netzzugang** (Schicht 1): statt Ethernet-Kabel jetzt WLAN.

**C2 b)** Jede Schicht nutzt nur die **Dienste der Schicht darunter**, ohne zu wissen, wie diese arbeitet. Der Browser übergibt seine Daten an Transport und Vermittlung – die bleiben gleich. Nur ganz unten wird jetzt per Funk statt per Kabel übertragen. Davon merkt der Browser nichts.

**C2 c) – neue Voraussetzung:** Alle Geräte brauchen zusätzlich eine **eindeutige MAC-Adresse**, und der Sender muss die MAC des Ziels kennen – dafür gibt es ARP. Also zwei Adressen: die IP-Adresse für den Weg, die MAC-Adresse für die Zustellung im lokalen Netz.

---

## Hausaufgabe

1. inf-schule 10.1.3 mischt OSI- und TCP/IP-Modell. Ergänzt: **Jede Schicht fügt eigene Zusatzdaten mit Adressen hinzu** (Kapselung: die Daten werden Schicht für Schicht „eingepackt“). Die unterste Schicht überträgt die Bitfolgen über das Medium.
2. Paketversand: Ich gebe ein Paket mit Adresse in der Filiale ab (oben). Die Filiale nutzt das Logistiksystem der Post, das den Weg über Verteilzentren plant (Mitte). Dieses nutzt LKW, Bahn oder Flugzeug für den eigentlichen Transport (unten). Keine Ebene muss wissen, wie die Ebene darunter arbeitet.

---

## Warum so – was bringt Punkte

| Aufgabe | Worauf es ankommt | Typische Fehler |
|---|---|---|
| A3b | Erst ARP, dann ICMP; Quelle/Ziel wechseln bei jeder Antwort | Zeilen erfinden statt abschreiben; ARP fehlt, weil schon vorher gepingt wurde |
| B1c | Begründung über die **Schichten**: Rahmen im lokalen Netz → MAC | nur „weil es so ist“; IP und MAC verwechseln |
| B2b | Switch **lernt** aus der Absender-MAC; unbekannt/Broadcast → an alle | „Der Switch kennt die IP-Adressen“ (falsch – er arbeitet nur mit MAC) |
| C1 | Reihenfolge von **unten** (1 = Netzzugang) nach oben | Reihenfolge umgedreht; Port und IP-Adresse vertauscht |
| C2b | Begriff „Dienst der darunterliegenden Schicht“ benutzen | nur „WLAN ist auch Internet“ |

## Klausurfertige Kurzversion

| Begriff | Merksatz |
|---|---|
| MAC-Adresse | 48 Bit, 6 Hex-Blöcke, fest in der Netzwerkkarte, gilt im lokalen Netz (Schicht 1) |
| IP-Adresse | logische Adresse, passt zum Netz, ändert sich beim Netzwechsel (Schicht 2) |
| ARP | „Wer hat IP x?“ an alle (FF:FF:FF:FF:FF:FF) → Antwort mit MAC → Ergebnis wird gemerkt |
| ICMP | Ping: Echo Request / Echo Reply, Vermittlungsschicht |
| Switch | lernt Absender-MAC je Port (SAT); bekannte Ziel-MAC → ein Port, sonst alle |
| Schichtenmodell | 4 Anwendung · 3 Transport · 2 Vermittlung · 1 Netzzugang; jede Schicht nutzt nur die darunter |
