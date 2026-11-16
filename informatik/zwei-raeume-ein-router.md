# Informatik GK – Zwei Räume, ein Router (Aufgaben 1–5)

16.11.2026, Handschrift-Fassung als GoodNotes/PDF. Meldungen geprüft im Filius-Quellcode (siehe `ab3-zwei-raeume-ein-netz.md`).

| Aufg. | Lösung |
|---|---|
| 1a | Nachbar: klappt (4 gesendet, 4 empfangen, 0 %) · Raum 2: „Zieladresse nicht erreichbar“ |
| 1b | Maske 255.255.255.0 → Netzanteil = erste 3 Zahlen; 192.168.0 = 192.168.0 → direkt über Switch; 192.168.1 ≠ → fremdes Netz, kein Gateway/Router → keine Route |
| 2a | weiterhin „Zieladresse nicht erreichbar“ |
| 2b | Kabel = nur physisch; Router ohne IP-Adressen gehört zu keinem Netz; Rechner ohne Gateway |
| 3a | jede Schnittstelle muss den Netzanteil „ihres“ Raums haben, sonst ist der Router dort nicht direkt erreichbar und kann nicht unterscheiden, wohin er weiterleitet |
| 3b | Reiter je Schnittstelle, Feld „Verbunden mit“ zeigt den angeschlossenen Switch |
| 4a | Ping klappt: „From 192.168.1.10: icmp_seq=…“, 4/4, 0 % Verlust |
| 4b | Gateway muss im eigenen Netz liegen → Raum 1: 192.168.0.1, Raum 2: 192.168.1.1 |
| 4c | Netzanteil der Ziel-IP mit eigenem vergleichen (Netzmaske): gleich → direkt, verschieden → Gateway |
| 5a | Nachbar klappt · Raum 2: „Zieladresse nicht erreichbar“ |
| 5b | Nachbar gleiches Netz → kein Gateway nötig; fremdes Netz braucht Gateway |
| 5c | andere Rechner in Raum 1 erreichen Raum 2 weiterhin; nach Wiedereintragen klappt es → nur Konfigurationsfehler von 192.168.0.10 |
