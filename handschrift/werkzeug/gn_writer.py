"""Eigener .goodnotes-Schreiber (experimentell) für Kugelschreiber-Striche.

Nachgebaut nach der Formatbeschreibung und dem Exporter von natural-ink
(https://github.com/LambertAlpha/natural-ink, MIT-Lizenz, Stand 2026-10-15, Commit 07188c7):
ZIP mit schema.pb (24), index.notes.pb, index.attachments.pb, index.events.pb, notes/<UUID>
(Strich-Datensätze: Protobuf + Apple-LZ4-Rahmen „bv41…bv4$“ um einen TPL-Block mit
Startpunkt + Liniensegmenten), attachments/<UUID> (Papier-PDF) und thumbnail.jpg.
Das Format ist NICHT offiziell dokumentiert; Import in GoodNotes ist nicht garantiert.
"""
import hashlib
import io
import struct
import uuid
import zipfile

import lz4.block

SCHEMA = 24
# GoodNotes rechnet Seite und Striche in iPad-Pixeln (132 ppi), PDF-Anhänge aber in Punkten (72 dpi).
# Ohne Umrechnung wird eine A4-Seite (595 x 842 pt) als 324 x 459 angelegt und der Hintergrund 1,83-fach
# vergrößert (Rückmeldung vom 27.10.2026). Daher: Seitengröße, Koordinaten und Strichbreite x 132/72.
UNIT = 132 / 72
TPL_FORMAT = b"vuA(v)A(S(uu))A(S(uuuu))vA(f)\0"


# --------------------------------------------------------------------------- Protobuf-Bausteine
def varint(v):
    out = bytearray()
    while v > 127:
        out.append((v & 127) | 128)
        v >>= 7
    out.append(v)
    return bytes(out)


def field(n, value):
    if isinstance(value, int):
        return varint(n << 3) + varint(value)
    raw = value.encode() if isinstance(value, str) else value
    return varint((n << 3) | 2) + varint(len(raw)) + raw


def ffield(n, value):
    return varint((n << 3) | 5) + struct.pack("<f", value)


def record(payload):
    return varint(len(payload)) + payload


def clock(counter):
    return field(1, 1) + field(2, counter)


def wrapped(value, counter=1):
    return field(1, value) + field(2, clock(counter))


# --------------------------------------------------------------------------- Strich
def encode_stroke(points, width, rgb, identifier, counter):
    """points: [(x, y), ...] in pt, Ursprung oben links; Kugelschreiber-Form mit einer Breite."""
    coords = list(points)
    if len(coords) == 1:                                   # Punkt als winziges Segment
        coords.append((coords[0][0] + 0.001, coords[0][1]))
    segs = list(zip(coords, coords[1:]))
    v = struct.pack("<HfI", 2, width, len(segs) + 1)
    v += struct.pack("<" + "H" * (len(segs) + 1), 0, *([1] * len(segs)))
    v += struct.pack("<Iff", 1, coords[0][0], coords[0][1])
    v += struct.pack("<I", len(segs))
    for a, b in segs:
        v += struct.pack("<ffff", a[0], a[1], b[0], b[1])
    v += struct.pack("<HI", 1, 0)
    tpl = b"tpl\0" + struct.pack("<I", 8 + len(TPL_FORMAT) + len(v)) + TPL_FORMAT + v
    comp = lz4.block.compress(tpl, store_size=False)
    framed = b"bv41" + struct.pack("<II", len(tpl), len(comp)) + comp + b"bv4$"
    rgba = b"".join(ffield(i + 1, c) for i, c in enumerate(rgb)) + ffield(4, 1.0)
    meta = (field(1, identifier) + field(2, clock(counter)) + field(8, 1) + field(9, counter)
            + field(14, 1) + field(16, SCHEMA))
    ink = (field(1, identifier) + field(2, framed) + field(4, rgba) + field(6, b"")
           + field(7, field(1, clock(counter))) + field(9, b"") + field(15, clock(counter))
           + field(20, b"") + field(21, SCHEMA))
    return record(meta) + record(field(7, ink))


# --------------------------------------------------------------------------- Dokument
def write(path, title, pages, paper_pdf, thumbnail_jpg, width_pt, rgb, schema_file=SCHEMA, page_links=False,
          salt=""):
    """pages: Liste von (breite_pt, hoehe_pt, [Strich als [(x, y), ...]]).

    Varianten für den Fall, dass GoodNotes die Standarddatei ablehnt (je nur EINE Änderung):
      schema_file=25  -> nur schema.pb auf 25 (Felder in den Datensätzen bleiben 24, wie in echten Exporten)
      page_links=True -> zusätzliche Seiten-Verknüpfung (Ereignis 105) je Seite
    """
    # IDs aus dem GESAMTEN Inhalt ableiten (sonst gleiche IDs für verschiedene Dateien)
    digest = hashlib.sha256(repr((title, width_pt, rgb, [p[:3] for p in pages], schema_file, page_links, salt)).encode()
                            + b"".join(hashlib.sha256(p[3]).digest() for p in pages if len(p) > 3)).hexdigest()

    def ident(label):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"sang-hw:{digest}:{label}")).upper()

    doc_id = ident("document")
    doc_event = (field(1, doc_id) + field(2, wrapped(title)) + field(6, wrapped("P")) + field(9, "auto")
                 + field(11, ident("document-event")) + field(13, 1) + field(14, 1) + field(20, SCHEMA))
    events = record(field(1, doc_id) + field(30, doc_event))
    notes_index, att_index = b"", b""
    members = {"schema.pb": field(1, schema_file), "document.info.pb": b"", "index.search.pb": b""}
    for pi, page in enumerate(pages):
        w, h, strokes = page[:3]
        page_id = ident(f"page-{pi}")
        page_id = str(uuid.UUID(int=uuid.UUID(page_id).int & ~1)).upper()   # Seiten-ID gerade,
        note_id = str(uuid.UUID(int=uuid.UUID(page_id).int + 1)).upper()    # Notiz-ID = +1 (beobachtet)
        att_id, tmpl_id = ident(f"background-{pi}"), ident(f"template-{pi}")
        paper = page[3] if len(page) > 3 else paper_pdf(w, h)   # eigener Seitenhintergrund (z. B. Foto) möglich
        members[f"attachments/{att_id}"] = paper
        att_index += record(field(1, att_id) + field(2, f"attachments/{att_id}"))
        notes_index += record(field(1, note_id) + field(2, f"notes/{note_id}"))
        attachment = (field(1, att_id) + field(2, att_id) + field(5, len(paper)) + field(6, doc_id)
                      + field(11, ident(f"attach-event-{pi}")) + field(12, clock(1)) + field(14, 1)
                      + field(15, 1) + field(16, SCHEMA))
        template = (field(1, doc_id) + field(2, tmpl_id) + field(4, att_id) + field(5, 1) + field(6, 1)
                    + field(8, ffield(1, w * UNIT) + ffield(2, h * UNIT)) + field(9, "Karo")
                    + field(11, ident(f"template-event-{pi}")) + field(15, 1) + field(16, 1) + field(21, SCHEMA))
        page_event = (field(1, doc_id) + field(2, page_id) + field(3, wrapped(tmpl_id))
                      + field(4, wrapped(f"A{pi:06d}")) + field(11, ident(f"page-event-{pi}"))
                      + field(13, 1) + field(14, 1) + field(15, SCHEMA))
        for identifier, tag, ev in ((att_id, 6, attachment), (tmpl_id, 2, template), (page_id, 54, page_event)):
            events += record(field(1, identifier) + field(tag, ev))
        if page_links:
            events += record(field(1, note_id) + field(105, field(1, pi + 1) + field(2, doc_id) + field(4, note_id)
                                                     + field(6, "auto") + field(13, 1) + field(14, 1) + field(15, SCHEMA)))
        members[f"notes/{note_id}"] = b"".join(
            encode_stroke([(x * UNIT, y * UNIT) for x, y in s], width_pt * UNIT, rgb, ident(f"stroke-{pi}-{si}"), si + 1)
            for si, s in enumerate(strokes))
    members["index.notes.pb"] = notes_index
    members["index.attachments.pb"] = att_index
    members["index.events.pb"] = events
    members["thumbnail.jpg"] = thumbnail_jpg
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 26, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    open(path, "wb").write(buf.getvalue())
    return {"pages": len(pages), "strokes": sum(len(p[2]) for p in pages),
            "bytes": len(buf.getvalue()), "sha256": hashlib.sha256(buf.getvalue()).hexdigest()}
