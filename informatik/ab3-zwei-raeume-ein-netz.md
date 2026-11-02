# Informatik GK – Arbeitsblatt 3: Zwei Räume, ein Netz? (Lösungen)

Informatik · MSS 13 · Grundkurs · 02.11.2026 · Raum 1: 192.168.0.10 / .11 / .12 · Raum 2: 192.168.1.10 / .11 / .12 · Maske 255.255.255.0

> Terminal-Meldungen geprüft im Filius-Quellcode (Terminal.java, ICMP.java, deutsches Sprachpaket):
> ohne passende Route (kein Gateway, Ziel in fremdem Netz) → sofort **„Zieladresse nicht erreichbar“**, es wird kein Paket gesendet.
> Route vorhanden, aber keine Antwort → je Versuch **„-- Timeout!“**, am Ende „x Paket(e) gesendet, 0 Paket(e) empfangen, 100% Paketverlust“.

---

## Teil A

**A1 b)** Terminal: **Zieladresse nicht erreichbar.** Es wird gar kein Ping-Paket gesendet.

**A1 c) Vermutung:** Raum 2 hat andere Adressen (192.168.1.x statt 192.168.0.x) → anderes Netz. Ein Kabel zwischen zwei Switchen verbindet keine verschiedenen Netze.

## Teil B

**B1 a)**

| IP-Adresse | Netzanteil | Hostanteil |
|---|---|---|
| 192.168.0.10 | 192.168.0 | 10 |
| 192.168.1.12 | 192.168.1 | 12 |
| 10.0.4.37 | 10.0.4 | 37 |

**B1 b)**

| Gerätepaar | gleiches Netz? | Begründung |
|---|---|---|
| 192.168.0.10 und 192.168.0.200 | ja | beide Netzanteil 192.168.0 |
| 192.168.0.10 und 192.168.1.10 | nein | 192.168.0 ≠ 192.168.1 |
| 10.0.4.37 und 10.0.4.9 | ja | beide Netzanteil 10.0.4 |

**B1 c)** Raum 1 = Netz 192.168.0, Raum 2 = Netz 192.168.1. Ein Rechner schickt nur an Geräte mit gleichem Netzanteil direkt. Für ein fremdes Netz braucht er einen Router als Gateway – den gibt es noch nicht. Ein Switch verbindet nur innerhalb eines Netzes.

**B2 a)** 8 Bit, jedes 0 oder 1 → 2⁸ = **256** Werte (0 bis 255).

**B2 b)** 256 − 2 = **254** nutzbare Adressen (.0 = Netzadresse, .255 = Broadcast).

## Teil C

**C1 b)** 192.168.0.1 → Raum 1 (Switch 1, Netz 192.168.0) · 192.168.1.1 → Raum 2 (Switch 2, Netz 192.168.1)

**C1 c)** Gateways: Raum 1 → 192.168.0.1, Raum 2 → 192.168.1.1. Ping von 192.168.0.10 an 192.168.1.10 klappt: „From 192.168.1.10: icmp_seq=1 …“, 4 gesendet, 4 empfangen, 0 % Paketverlust.

**C1 d)** Gateway = Tür aus dem eigenen Netz: an diese Router-Adresse gehen alle Pakete für fremde Netze. Der Rechner vergleicht mit der Netzmaske den Netzanteil der Ziel-IP mit seinem eigenen: gleich → direkt über den Switch, verschieden → ans Gateway.

## Teil D

**D1 a)**

| Ping-Ziel | Ergebnis |
|---|---|
| Nachbar im selben Raum | klappt: 4 gesendet, 4 empfangen, 0 % Verlust |
| Rechner in Raum 2 | Zieladresse nicht erreichbar |

**D1 b)** Nachbar: gleicher Netzanteil → direkt über den Switch, kein Gateway nötig. Raum 2: fremdes Netz → ohne Gateway kennt der Rechner keinen Weg und schickt gar nichts los.

**D1 c)** Aus Raum 1: Timeout, 0 empfangen, 100 % Paketverlust. Aus Raum 2: ebenfalls Timeout, 100 % Paketverlust.

**D1 d)** 192.168.0.40 hat den Netzanteil von Raum 1, steckt aber an Switch 2. Raum 1 sucht ihn per ARP am eigenen Switch (Broadcast geht nicht durch den Router) und findet ihn nicht; der Router schickt Pakete für 192.168.0.x nur nach Raum 1. Fehler ist logisch (Adresse), nicht physisch (Kabel). **Ändern:** wieder Adresse aus Raum 2, z. B. 192.168.1.12, Maske 255.255.255.0, Gateway 192.168.1.1.

## Hausaufgabe

**HA 1)** Netzanteil von 172.16.8.5 = 172.16.8 → im selben Netz: **172.16.8.200** und **172.16.8.1**. Nicht: 172.16.9.5 (Netz 172.16.9), 172.17.8.5 (Netz 172.17.8).

**HA 2) Netzplan**

```
   Raum 1: Netz 192.168.0                                 Raum 2: Netz 192.168.1
                       192.168.0.1        192.168.1.1
        [Switch 1]-----------------( Router )-----------------[Switch 2]
        /    |    \                                            /    |    \
   PC .10  PC .11  PC .12                                PC .10  PC .11  PC .12
   Gateway aller Rechner: 192.168.0.1                    Gateway aller Rechner: 192.168.1.1
```

---

## Klausurfertige Kurzversion
- **Netzanteil** (Maske 255.255.255.0 → erste 3 Zahlen) entscheidet: gleich → direkt über Switch; verschieden → über Router/Gateway.
- **Switch** = innerhalb eines Netzes · **Router** = zwischen Netzen, eine Schnittstelle pro Netz.
- Kein Gateway + fremdes Netz → „Zieladresse nicht erreichbar“ (nichts wird gesendet).
- Falsche Adresse im falschen Raum → Timeout (Route da, aber niemand antwortet).
- Hostanteil 8 Bit → 256 Werte, 254 nutzbar (.0 Netz, .255 Broadcast).

**Typische Fehler:** Kabel zwischen Switchen für die Lösung halten · Gateway aus dem *fremden* Netz eintragen · 256 statt 254 · Netzanteil mit Hostanteil verwechseln.
