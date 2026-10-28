"""Wortauswahl für die Schriftprobe: häufige ganze Wörter + gierige Abdeckung der Buchstabenpaare
(Wortanfang ^x, Paare xy, Wortende x$) aus Sangs Schultexten, dazu jeder Großbuchstabe am Wortanfang."""
import collections, json, math, re
C = json.load(open("corpus.json"))
de = collections.Counter(dict(C["de"])); en = collections.Counter(dict(C["en"]))
# allgemeine Häufigkeitslisten (Grundwortschatz), damit Fach-Zufälle wie "Rechner" nicht dominieren
DE_COMMON = ("der die das und ist nicht mit von zu auf für ein eine sich auch wird werden sind den dem des im in als "
             "bei nach oder wie aus es an so dass wenn aber noch man kann muss hat haben war wir ich du sie er "
             "zum zur über durch hier also weil sehr mehr gibt immer schon nur").split()
EN_COMMON = ("the and of to is in that it for as with are this be on by which not or have because would they "
             "their there however although should could while people").split()
CAP_FORCE = {"Q": ["Quadrat"], "X": ["Xenon"], "Y": ["York"], "J": ["Januar"], "C": ["China"], "Ä": ["Änderung"],
             "Ö": ["Ökologie"], "Ü": ["Übung"], "V": ["Vektor"], "Ä2": []}
def units(w):
    s = w[0] if w[0].isupper() else w[0]
    low = w.lower()
    u = [("^" + w[0])] + [low[i:i + 2] for i in range(len(low) - 1)] + [low[-1] + "$"]
    return u
# Gewichte der Einheiten: Deutsch + Englisch (Englisch x2, kleinerer Korpus, aber Prüfungsfach)
W = collections.Counter()
for cnt, f in ((de, 1.0), (en, 2.0)):
    for w, n in cnt.items():
        if len(w) < 2 or not re.fullmatch(r"[A-Za-zÄÖÜäöüß]+", w): continue
        for u in units(w): W[u] += n * f
total = sum(W.values())
ranked = [u for u, _ in W.most_common()]
mass, need = 0, {}
for i, u in enumerate(ranked):
    if mass / total > 0.97: break
    need[u] = 3 if i < 40 else (2 if i < 150 else 1)
    mass += W[u]
print("Einheiten mit Bedarf:", len(need), "von", len(W))
chosen, have = [], collections.Counter()
def take(w):
    if w in chosen: return
    chosen.append(w)
    for u in units(w): have[u] += 1
SUBJECT = ("Funktion Ableitung Integral Gleichung Ebene Gerade Wahrscheinlichkeit Feldlinien Ladung Spannung "
           "Kraft Energie Physik Fläche Stärke Migration Klimawandel Begründung Ergebnis Lösung Frequenz Hafen Rheinland").split()
EXCLUDE = set("Mio vgl seq bzw ca Pings Step Filius Hormus Diagnose Abschnitt Acqua ttl Aufg Abb Ping Fix Pro Trump Switch Autorentext Rechner Lliuya RWE alta inf rwe Lido Kosovo Fallback Gondeln Dampfschiff Nga rect Nov ping pro switch".split())
for w in DE_COMMON + EN_COMMON + SUBJECT: take(w)
for cap, ws in CAP_FORCE.items():
    for w in ws: take(w)
# jeder Großbuchstabe am Wortanfang mindestens einmal (häufigstes Korpuswort)
for cap in "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ":
    if have["^" + cap]: continue
    cands = [(n, w) for w, n in de.items() if w[0] == cap and len(w) >= 3 and w[1:].islower() and re.fullmatch(r"[A-Za-zÄÖÜäöüß]+", w) and w not in EXCLUDE]
    if cands: take(max(cands)[1])
# Kandidaten für gierige Abdeckung
cand = {}
for cnt, lang in ((de, "de"), (en, "en")):
    for w, n in cnt.items():
        if 3 <= len(w) <= 13 and re.fullmatch(r"[A-Za-zÄÖÜäöüß]+", w) and (w[1:].islower()) and n >= 2 and w not in EXCLUDE:
            cand[w] = lang
letters_mid = "abcdefghijklmnopqrstuvwxyzäöüß"
def mid_count(ch): return sum(w[1:].lower().count(ch) for w in chosen)
MAX = 200
while len(chosen) < MAX:
    best, bw = 0, None
    for w in cand:
        if w in chosen: continue
        g = sum(W[u] ** 0.5 for u in set(units(w)) if have[u] < need.get(u, 0))
        g += sum(30 for ch in set(w[1:].lower()) if ch in letters_mid and mid_count(ch) < 2)
        score = g / (len(w) + 2) ** 0.8
        if score > best: best, bw = score, w
    if bw is None or best < 1.0: break
    take(bw)
missing = [u for u in need if have[u] < need[u]]
print("gewählt", len(chosen), "Wörter,", sum(len(w) for w in chosen), "Buchstaben")
print("noch offen (Bedarf nicht erfüllt):", len(missing), missing[:40])
print("Mitte-Buchstaben < 2:", [ch for ch in letters_mid if mid_count(ch) < 2])
def lang(w):
    if w in EN_COMMON: return "en"
    if w in DE_COMMON or w in SUBJECT or any(w in v for v in CAP_FORCE.values()): return "de"
    return "en" if en[w] > de[w] else "de"
json.dump({"words": chosen, "lang": {w: lang(w) for w in chosen}},
          open("words.json", "w"), ensure_ascii=False, indent=0)
print(chosen)
