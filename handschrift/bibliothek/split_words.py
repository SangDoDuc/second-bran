"""Sätze in Wörter zerlegen (Spaltenlücken), als zusätzliche Felder sentK_wJ in sample_fields.pkl speichern."""
import os, pickle
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
F = pickle.load(open("sample_fields.pkl", "rb"))
for k in range(3):
    r = F[f"sent_{k}"]; a = r["alpha"]
    col = (a > 0.2).any(axis=0)
    xs = np.where(col)[0]
    groups, start, prev = [], xs[0], xs[0]
    for x in xs[1:]:
        if x - prev > 9:
            groups.append((start, prev + 1)); start = x
        prev = x
    groups.append((start, prev + 1))
    words = r["text"].split()
    print(k, len(groups), "Gruppen,", len(words), "Wörter:", [g[1] - g[0] for g in groups])
    for j, (g0, g1) in enumerate(groups):
        sub = np.zeros_like(a); sub[:, g0:g1] = a[:, g0:g1]
        ys = np.where((sub > 0.2).any(axis=1))[0]
        F[f"sent{k}_w{j:02d}"] = {"id": f"sent{k}_w{j:02d}", "kind": "sentword", "text": "?", "baseline": r["baseline"],
                                 "origin": r["origin"], "alpha": sub, "bbox": [int(g0), int(ys.min()), int(g1), int(ys.max()) + 1]}
pickle.dump(F, open("sample_fields.pkl", "wb"))
