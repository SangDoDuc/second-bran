"""Schriftprobe SP-k1 (Bild 1414x2000) -> Tinten-Alpha je Feld (Ausschnitte + Metadaten) + Kontrollbild."""
import json, os, pickle, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
os.chdir(HERE)
IMG = HERE + "schriftprobe_SP-k1.jpg"               # Sangs ausgefüllte Kurzfassung (28.10.2026), 1414 x 2000 px
LAY = HERE + "../vorlage/layout_kompakt.json"
rgb = np.asarray(Image.open(IMG).convert("RGB")).astype(np.float32)
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
lum = (R + G + B) / 3
blueish = (B - R) > 45                      # Vorlagen-Blau, hellblaue Linie
alpha = np.clip((215 - lum) / 150, 0, 1)
alpha[blueish & (lum > 60)] = 0
alpha[lum > 190] = 0                         # Karo-Raster (grau ~204) und Papier
lay = json.load(open(LAY))
sx = 1414 / lay["page_size_pt"][0]; sy = 2000 / lay["page_size_pt"][1]
items = lay["pages"][0]["items"]
out = {}
dbg = Image.fromarray(np.uint8(255 - 255 * np.clip(alpha, 0, 1))).convert("RGB")
d = ImageDraw.Draw(dbg)
for it in items:
    if it["kind"] == "calib":
        continue
    x0 = int(min(b[0] for b in it["boxes"]) * sx); x1 = int(max(b[2] for b in it["boxes"]) * sx)
    y0 = int(it["band"][0] * sy); y1 = int(it["band"][1] * sy)
    if it["kind"] == "sentence":
        x1 = 1414
    if it.get("tall"):
        y0 -= 12; y1 += 12
    x0 += 2; x1 -= 2
    sub = alpha[y0:y1, x0:x1].copy()
    L = lum[y0:y1, x0:x1]
    lab, n = ndi.label(sub > 0.2, structure=np.ones((3, 3)))
    keep = np.zeros_like(sub, bool)
    for k in range(1, n + 1):
        m = lab == k
        if m.sum() >= 3 and L[m].min() < 100:      # nur echte schwarze Tinte (Raster/Trennlinien sind heller)
            keep |= m
    sub = sub * ndi.binary_dilation(keep, iterations=1)
    ys, xs = np.where(sub > 0.25)
    rec = {"id": it["id"], "kind": it["kind"], "text": it["text"], "baseline": it["baseline"] * sy - y0,
           "origin": [x0, y0], "alpha": sub}
    if len(xs):
        rec["bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        d.rectangle((x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()), outline=(230, 0, 0))
    else:
        rec["bbox"] = None
    out[it["id"]] = rec
pickle.dump(out, open("sample_fields.pkl", "wb"))
dbg.save("debug_fields.png")
empty = [k for k, v in out.items() if v["bbox"] is None]
print(len(out), "Felder, leer:", empty)
