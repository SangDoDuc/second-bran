"""Komponenten eines Feldes (Rang nach x-Start, wie in cc_view), Koordinaten relativ zur Grundlinie."""
import os, pickle, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import ndimage as ndi
F = pickle.load(open("sample_fields.pkl", "rb"))

def comps(fid):
    r = F[fid]; a = r["alpha"]
    lab, n = ndi.label(a > 0.2, structure=np.ones((3, 3)))
    objs = ndi.find_objects(lab)
    order = sorted(range(n), key=lambda k: objs[k][1].start)
    out = []
    for k in order:
        sl = objs[k]
        out.append({"label": k + 1, "x0": sl[1].start, "x1": sl[1].stop, "y0": sl[0].start, "y1": sl[0].stop,
                    "px": int((lab[sl] == k + 1).sum())})
    return lab, out

if __name__ == "__main__":
    for fid in sys.argv[1:]:
        lab, cs = comps(fid); b = F[fid]["baseline"]
        print(fid, "baseline", round(b, 1))
        for i, c in enumerate(cs):
            print(f"  {i:2d}: x {c['x0']:3d}-{c['x1']:3d}  y {c['y0'] - b:6.1f}..{c['y1'] - b:6.1f}  px {c['px']}")
