"""Wortliste v2 nach der Prüfung (Usability/Extraktion/Abdeckung): Streichungen, Ergänzungen, Gruppen, Wiederholungen."""
import collections, json, re
v1 = json.load(open("words.json"))
C = json.load(open("corpus.json")); de = collections.Counter(dict(C["de"])); en = collections.Counter(dict(C["en"]))
CUT = set(("Xenon York Dominica Rechners Rechner Fonds Abs bold Social Switching Faktorkette uncle Tage Hafen Rheinland "
           "Gipfel verwechseln ihm Würfe sea area lost left run adjust requires outlook supply could Die in").split())
FREQ2 = "und die der ist mit nicht für".split()           # 2-mal (häufigste Wörter, Abwechslung)
FREQ2_EN = "to and of is".split()
ADD_DE = ("Der Das Es In Warum Koordinaten Kante Winkel Wendepunkt Schritt Seite Zeile Mitte Magnetfeld Menschen "
          "Parabel Graph Hochpunkt Hilfe Normalenvektor Einfluss Europa Ursache Sicherheit Beispiel gleich möglich "
          "Entwicklung einfach Punkt senkrecht Deutschland zusammen Angriff groß heißt Würfel Länge Richtung Abstand "
          "keine bis seit gegen genau zwischen Erdkunde Sozialkunde Englisch Deutsch Mathe").split()
ADD_EN = "The While was but more than what change causes technology energy something using only used pollution very".split()
ABBR = ["ca.", "(Z. 12–15)", "S. 260", "bzw.", "usw.", "Mio.", "Mrd.", "Nr. 7", "z.B.", "d.h."]
CAPS = ["NATO", "USA", "EU", "UN", "CO₂", "ABCD", "IQB"]
HYPH = ["x-Achse", "Push-Pull-Modell", "US-Dollar", "EU-Mission"]
EN_ALL = set("the and of to is that it for as with are this be on by which not or have because would they their there "
             "however although should could while people control extreme keep against difficulty expensive said habits "
             "approach impact new public government evidence may".split()) | set(ADD_EN)
words = [w for w in v1["words"] if w not in CUT]
for w in ADD_DE + ADD_EN:
    if w not in words: words.append(w)
de_w = [w for w in words if w not in EN_ALL]
en_w = [w for w in words if w in EN_ALL]
items = ([{"text": w, "reps": 2 if w in FREQ2 else 1, "group": "de"} for w in de_w]
         + [{"text": w, "reps": 1, "group": "abbr"} for w in ABBR]
         + [{"text": w, "reps": 1, "group": "caps"} for w in CAPS + HYPH]
         + [{"text": w, "reps": 2 if w in FREQ2_EN else 1, "group": "en"} for w in en_w])
# Abdeckung prüfen (Paare mit >= 2 Proben, gewichtet) – nur Information
def units(w):
    low = w.lower(); return ["^" + w[0]] + [low[i:i + 2] for i in range(len(low) - 1)] + [low[-1] + "$"]
W = collections.Counter()
for cnt, f in ((de, 1.0), (en, 2.0)):
    for w, n in cnt.items():
        if len(w) >= 2 and re.fullmatch(r"[A-Za-zÄÖÜäöüß]+", w):
            for u in units(w): W[u] += n * f
have = collections.Counter()
for it in items:
    for part in re.findall(r"[A-Za-zÄÖÜäöüß]+", it["text"]):
        for u in units(part): have[u] += it["reps"]
tot = sum(W.values())
cov1 = sum(v for u, v in W.items() if have[u] >= 1) / tot
cov2 = sum(v for u, v in W.items() if have[u] >= 2) / tot
json.dump({"items": items}, open("words_v2.json", "w"), ensure_ascii=False, indent=0)
print(len(items), "Felder,", sum(i["reps"] for i in items), "Schreibvorgänge,", sum(len(i["text"]) * i["reps"] for i in items), "Zeichen")
print(f"gewichtete Paar-Abdeckung: >=1 Probe {cov1:.3f}, >=2 Proben {cov2:.3f}")

# ---- Kürzen auf ein Zeitbudget: Wörter mit dem geringsten Abdeckungsverlust je Zeichen entfernen
PROTECT = set(FREQ2 + FREQ2_EN + ABBR + CAPS + HYPH + ["Der", "Das", "Es", "In", "Warum", "The", "While", "Mathe",
              "Erdkunde", "Sozialkunde", "Englisch", "Deutsch", "Physik", "Würfel", "Koordinaten", "Normalenvektor",
              "Quadrat", "Januar", "China", "Änderung", "Ökologie", "Übung", "Vektor", "groß", "heißt", "Kante", "Schritt",
              "Seite", "Winkel", "Europa", "Beispiel", "Länge", "Punkt", "senkrecht", "something", "using", "change"])
SUBJ_KEEP = set("Funktion Ableitung Integral Gleichung Ebene Gerade Wahrscheinlichkeit Feldlinien Ladung Spannung Kraft "
                "Energie Fläche Stärke Migration Klimawandel Begründung Ergebnis Lösung Frequenz".split())
PROTECT |= SUBJ_KEEP | set("der die das und ist nicht mit von zu auf für ein eine sich auch wird werden sind den dem des im als bei nach oder wie aus es an so dass wenn aber noch man kann muss hat haben war wir ich du sie er zum zur über durch hier also weil sehr mehr gibt immer schon nur the and of to is that it for as with are this be on by which not or have because would they their there however although should while people".split())
BUDGET = 1150
def score(items):
    have = collections.Counter()
    for it in items:
        for part in re.findall(r"[A-Za-zÄÖÜäöüß]+", it["text"]):
            for u in units(part): have[u] += it["reps"]
    return sum(v * (0.4 * (have[u] >= 1) + 0.6 * (have[u] >= 2)) for u, v in W.items()) / tot
cur = list(items)
removed = []
while sum(len(i["text"]) * i["reps"] for i in cur) > BUDGET:
    base = score(cur)
    best = None
    for k, it in enumerate(cur):
        if it["text"] in PROTECT: continue
        loss = (base - score(cur[:k] + cur[k + 1:])) / (len(it["text"]) + 2)
        if best is None or loss < best[0]: best = (loss, k)
    if best is None: break
    removed.append(cur.pop(best[1])["text"])
items = cur
have = collections.Counter()
for it in items:
    for part in re.findall(r"[A-Za-zÄÖÜäöüß]+", it["text"]):
        for u in units(part): have[u] += it["reps"]
cov1 = sum(v for u, v in W.items() if have[u] >= 1) / tot
cov2 = sum(v for u, v in W.items() if have[u] >= 2) / tot
json.dump({"items": items}, open("words_v2.json", "w"), ensure_ascii=False, indent=0)
print("gekürzt um:", removed)
print(len(items), "Felder,", sum(i["reps"] for i in items), "Schreibvorgänge,", sum(len(i["text"]) * i["reps"] for i in items), "Zeichen")
print(f"nach Kürzung: >=1 Probe {cov1:.3f}, >=2 Proben {cov2:.3f}")
