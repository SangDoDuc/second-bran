"""Alle Kandidaten je Buchstabe auf eine Seite setzen, wie für GoodNotes umwandeln und die Striche zeigen."""
import pickle, sys
import numpy as np
from PIL import Image, ImageDraw
SP = "/tmp/claude-0/-home-user-second-bran/77087009-95da-55ff-8987-fa95a510b3dd/scratchpad/"
sys.path[:0] = [SP + "gn"]
import smooth_outputs as SO
C = pickle.load(open("font_candidates.pkl", "rb"))
letters = sys.argv[2]
MX = 14
can = np.zeros((2000, 1414), np.float32)
labels = []
for r, ch in enumerate(letters):
    cands = C["old"].get(ch, []) + C["new"].get(ch, [])
    medw = np.median([c["w"] for c in cands])
    order = sorted(range(len(cands)), key=lambda i: (-cands[i]["clean"], abs(cands[i]["w"] - medw)))[:MX]
    yb = 75 + r * 76
    for j, i in enumerate(order):
        a = cands[i]["alpha"]; x = 60 + j * 95; y = int(round(yb + cands[i]["top"]))
        can[y:y + a.shape[0], x:x + a.shape[1]] = np.maximum(can[y:y + a.shape[0], x:x + a.shape[1]], a)
        labels.append((x, yb, f"{ch}{i}"))
np.save(SP + "eng/conv_tmp_alpha.npy", can)
strokes = SO.convert(SP + "eng/conv_tmp_alpha.npy")
S = 2.5; PT = 1414 / 595.2756
im = Image.new("RGB", (int(1414 * S / 1.0 / PT * PT), int((75 + len(letters) * 76) * S)), "white")
im = Image.new("RGB", (int(1414 * S), int((75 + len(letters) * 76) * S)), "white"); d = ImageDraw.Draw(im)
for s in strokes:
    pts = [(x * PT * S, y * PT * S) for x, y in s]
    if len(pts) > 1: d.line(pts, fill=(15, 15, 25), width=int(1.05 * PT * S * 0.42 * 2.4), joint="curve")
    else: d.ellipse((pts[0][0] - 3, pts[0][1] - 3, pts[0][0] + 3, pts[0][1] + 3), fill=(15, 15, 25))
for x, yb, t in labels:
    d.text((x * S, (yb - 34) * S), t, fill=(220, 0, 0))
im.save(sys.argv[1]); print(im.size, len(strokes))
