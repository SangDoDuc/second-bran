"""Vergrößerte Ansicht von Feldern mit nummerierten Zusammenhangskomponenten: python3 cc_view.py OUT.png ID [ID ...]"""
import pickle, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
F = pickle.load(open("sample_fields.pkl", "rb"))
S = 4
rows = []
for fid in sys.argv[2:]:
    r = F[fid]; a = r["alpha"]; x0, y0, x1, y1 = r["bbox"]
    a = a[max(0, y0 - 4):y1 + 4, max(0, x0 - 4):x1 + 4]
    lab, n = ndi.label(a > 0.2, structure=np.ones((3, 3)))
    im = Image.fromarray(np.uint8(255 - 230 * a)).resize((a.shape[1] * S, a.shape[0] * S), Image.NEAREST).convert("RGB")
    d = ImageDraw.Draw(im)
    objs = ndi.find_objects(lab)
    order = sorted(range(n), key=lambda k: objs[k][1].start)
    for rank, k in enumerate(order):
        sl = objs[k]
        d.rectangle((sl[1].start * S, sl[0].start * S, sl[1].stop * S, sl[0].stop * S), outline=(230, 0, 0))
        d.text((sl[1].start * S + 1, sl[0].start * S + 1), str(rank), fill=(0, 90, 220))
    for xx in range(0, a.shape[1], 10):
        d.line((xx * S, im.height - 6, xx * S, im.height), fill=(0, 160, 0))
    lab_im = Image.new("RGB", (im.width, im.height + 14), "white"); lab_im.paste(im, (0, 14))
    ImageDraw.Draw(lab_im).text((2, 1), f"{fid}  bbox={r['bbox']}  baseline={r['baseline']:.1f}", fill=(0, 0, 0))
    rows.append(lab_im)
W = max(r.width for r in rows); H = sum(r.height for r in rows)
sh = Image.new("RGB", (W, H), "white"); y = 0
for r in rows: sh.paste(r, (0, y)); y += r.height
sh.save(sys.argv[1]); print(sh.size)
