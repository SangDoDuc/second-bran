"""Wort- und Buchstabenpaar-Statistik aus Sangs Schultexten im Repo (Deutsch und Englisch getrennt)."""
import collections, glob, json, os, re
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) + "/"
EN_STOP = set("the and of to is in that it for as with are this be on by which not or have from can an but would their they has more will been was its".split())
DE_STOP = set("der die das und ist nicht mit von zu auf für ein eine sich auch wird werden sind den dem des im in als bei nach oder wie aus".split())
WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")
de, en = collections.Counter(), collections.Counter()
for f in glob.glob(REPO + "**/*.md", recursive=True):
    for line in open(f, encoding="utf-8"):
        line = re.sub(r"https?://\S+|`[^`]*`|\[[^\]]*\]\([^)]*\)", " ", line)
        ws = WORD.findall(line)
        if not ws: continue
        low = [w.lower() for w in ws]
        e = sum(w in EN_STOP for w in low); d = sum(w in DE_STOP for w in low)
        tgt = en if e > d else de
        for w in ws:
            if len(w) >= 1: tgt[w] += 1
json.dump({"de": de.most_common(), "en": en.most_common()}, open("corpus.json", "w"), ensure_ascii=False)
print("DE", sum(de.values()), len(de), "EN", sum(en.values()), len(en))
print("DE top:", [w for w, _ in de.most_common(40)])
print("EN top:", [w for w, _ in en.most_common(30)])
