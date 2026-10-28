"""Independent GoodNotes archive decoder / verifier.

Written from the public format notes only (inkterop_goodnotes.md, ni_format.md).
Does not import or read the writer code.
"""
import struct
import sys
import zipfile
import json
import math
import re
from collections import Counter, defaultdict


class DecodeError(Exception):
    pass


# ---------------------------------------------------------------- protobuf
def read_varint(buf, pos, limit=None):
    """Strict varint reader: max 10 bytes, rejects truncation and
    non-minimal (overlong) encodings are flagged via the returned flag."""
    if limit is None:
        limit = len(buf)
    result = 0
    shift = 0
    start = pos
    while True:
        if pos >= limit:
            raise DecodeError("truncated varint at %d" % start)
        b = buf[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
        if shift >= 70:
            raise DecodeError("varint too long at %d" % start)
    n = pos - start
    overlong = n > 1 and buf[pos - 1] == 0
    if result >= (1 << 64):
        raise DecodeError("varint > 64 bit at %d" % start)
    return result, pos, overlong


def parse_message(buf, start=0, end=None, issues=None, ctx=""):
    """Parse a protobuf message into list of (field, wiretype, value, (s,e)).
    Raises on malformed data. value: int for varint, bytes for LEN,
    int for fixed32/fixed64 (raw)."""
    if end is None:
        end = len(buf)
    pos = start
    out = []
    while pos < end:
        key, pos, ol = read_varint(buf, pos, end)
        if ol and issues is not None:
            issues.append("%s: overlong key varint" % ctx)
        field = key >> 3
        wt = key & 7
        if field == 0:
            raise DecodeError("%s: field number 0 at %d" % (ctx, pos))
        if wt == 0:
            v, pos, ol = read_varint(buf, pos, end)
            if ol and issues is not None:
                issues.append("%s: overlong varint field %d" % (ctx, field))
            out.append((field, wt, v))
        elif wt == 1:
            if pos + 8 > end:
                raise DecodeError("%s: truncated fixed64" % ctx)
            out.append((field, wt, bytes(buf[pos:pos + 8])))
            pos += 8
        elif wt == 2:
            ln, pos, ol = read_varint(buf, pos, end)
            if ol and issues is not None:
                issues.append("%s: overlong len varint field %d" % (ctx, field))
            if pos + ln > end:
                raise DecodeError("%s: LEN field %d overruns (%d+%d>%d)" % (ctx, field, pos, ln, end))
            out.append((field, wt, bytes(buf[pos:pos + ln])))
            pos += ln
        elif wt == 5:
            if pos + 4 > end:
                raise DecodeError("%s: truncated fixed32" % ctx)
            out.append((field, wt, bytes(buf[pos:pos + 4])))
            pos += 4
        else:
            raise DecodeError("%s: bad wiretype %d field %d at %d" % (ctx, wt, field, pos))
    if pos != end:
        raise DecodeError("%s: message overran end" % ctx)
    return out


def try_parse(b):
    try:
        return parse_message(b)
    except DecodeError:
        return None


def delimited_records(buf, issues=None, ctx=""):
    pos = 0
    recs = []
    while pos < len(buf):
        ln, p2, ol = read_varint(buf, pos)
        if ol and issues is not None:
            issues.append("%s: overlong record-length varint at %d" % (ctx, pos))
        if p2 + ln > len(buf):
            raise DecodeError("%s: record at %d length %d overruns stream (%d)" % (ctx, pos, ln, len(buf)))
        recs.append(bytes(buf[p2:p2 + ln]))
        pos = p2 + ln
    return recs


def fields(msg, num):
    return [v for (f, wt, v) in msg if f == num]


def one(msg, num, default=None):
    v = fields(msg, num)
    return v[0] if v else default


def dump(b, depth=0, maxdepth=6, maxlen=60):
    """Best-effort recursive pretty printer for exploration."""
    msg = try_parse(b) if depth < maxdepth else None
    lines = []
    if msg is None:
        return None
    ind = "  " * depth
    for f, wt, v in msg:
        if wt == 0:
            lines.append("%s%d: varint %d" % (ind, f, v))
        elif wt == 5:
            lines.append("%s%d: f32 %r (u32 %d)" % (ind, f, struct.unpack('<f', v)[0], struct.unpack('<I', v)[0]))
        elif wt == 1:
            lines.append("%s%d: f64 %r (u64 %d)" % (ind, f, struct.unpack('<d', v)[0], struct.unpack('<Q', v)[0]))
        else:
            printable = all(32 <= c < 127 for c in v) and len(v) > 0
            sub = None if printable or len(v) == 0 else dump(v, depth + 1, maxdepth, maxlen)
            if sub:
                lines.append("%s%d: msg (%d B)" % (ind, f, len(v)))
                lines.append(sub)
            elif printable:
                lines.append("%s%d: str %r" % (ind, f, v.decode()[:maxlen]))
            else:
                lines.append("%s%d: bytes(%d) %s" % (ind, f, len(v), v[:maxlen // 2].hex()))
    return "\n".join(lines)


# ---------------------------------------------------------------- LZ4
def lz4_block_decompress(src, raw_size):
    """Own LZ4 block decoder (no frame), per LZ4 block format spec."""
    dst = bytearray()
    i = 0
    n = len(src)
    while i < n:
        token = src[i]
        i += 1
        lit = token >> 4
        if lit == 15:
            while True:
                if i >= n:
                    raise DecodeError("lz4: truncated literal length")
                b = src[i]
                i += 1
                lit += b
                if b != 255:
                    break
        if i + lit > n:
            raise DecodeError("lz4: literal overrun")
        dst += src[i:i + lit]
        i += lit
        if i >= n:
            break  # last sequence: literals only
        if i + 2 > n:
            raise DecodeError("lz4: truncated offset")
        off = src[i] | (src[i + 1] << 8)
        i += 2
        if off == 0 or off > len(dst):
            raise DecodeError("lz4: bad offset %d (have %d)" % (off, len(dst)))
        ml = token & 15
        if ml == 15:
            while True:
                if i >= n:
                    raise DecodeError("lz4: truncated match length")
                b = src[i]
                i += 1
                ml += b
                if b != 255:
                    break
        ml += 4
        s = len(dst) - off
        for k in range(ml):
            dst.append(dst[s + k])
    if len(dst) != raw_size:
        raise DecodeError("lz4: size mismatch %d != %d" % (len(dst), raw_size))
    return bytes(dst)


def apple_lz4_decode(b, stats=None):
    """Decode Apple libcompression LZ4 frame: bv41/bv4- blocks + bv4$."""
    pos = 0
    out = bytearray()
    blocks = []
    while True:
        if pos + 4 > len(b):
            raise DecodeError("apple-lz4: missing end marker")
        magic = b[pos:pos + 4]
        pos += 4
        if magic == b'bv4$':
            break
        if magic == b'bv41':
            if pos + 8 > len(b):
                raise DecodeError("apple-lz4: truncated bv41 header")
            raw, comp = struct.unpack_from('<II', b, pos)
            pos += 8
            if pos + comp > len(b):
                raise DecodeError("apple-lz4: block overruns (%d+%d>%d)" % (pos, comp, len(b)))
            blk = b[pos:pos + comp]
            pos += comp
            mine = lz4_block_decompress(blk, raw)
            # cross-check with the lz4 library
            try:
                import lz4.block as LB
                lib = LB.decompress(blk, uncompressed_size=raw)
                if lib != mine:
                    raise DecodeError("apple-lz4: own decoder disagrees with lz4 lib")
            except ImportError:
                pass
            out += mine
            blocks.append(('bv41', raw, comp))
        elif magic == b'bv4-':
            raw, = struct.unpack_from('<I', b, pos)
            pos += 4
            out += b[pos:pos + raw]
            pos += raw
            blocks.append(('bv4-', raw, raw))
        else:
            raise DecodeError("apple-lz4: bad magic %r at %d" % (magic, pos - 4))
    if pos != len(b):
        raise DecodeError("apple-lz4: %d trailing bytes after bv4$" % (len(b) - pos))
    if stats is not None:
        stats.extend(blocks)
    return bytes(out)


# ---------------------------------------------------------------- TPL
def tokenize_sig(sig):
    """Parse signature grammar into a list of nodes:
    ('v'|'u'|'f') scalars, ('A', elem) arrays, ('S', [scalars])."""
    i = 0

    def parse_elem():
        nonlocal i
        c = sig[i]
        if c in 'vuf':
            i += 1
            return c
        if c == 'S':
            assert sig[i + 1] == '(', sig
            i += 2
            sc = []
            while sig[i] != ')':
                assert sig[i] in 'vuf', sig
                sc.append(sig[i])
                i += 1
            i += 1
            return ('S', sc)
        if c == 'A':
            assert sig[i + 1] == '(', sig
            i += 2
            e = parse_elem()
            assert sig[i] == ')', sig
            i += 1
            return ('A', e)
        raise DecodeError("bad sig char %r in %r" % (c, sig))

    toks = []
    while i < len(sig):
        toks.append(parse_elem())
    return toks


SCALAR = {'v': ('<H', 2), 'u': ('<f', 4)}


def read_elem(blob, pos, e):
    if isinstance(e, str):
        if e == 'f':
            raise DecodeError("tpl: 'f' scalar with nonzero count (size unknown)")
        fmt, sz = SCALAR[e]
        return struct.unpack_from(fmt, blob, pos)[0], pos + sz
    if e[0] == 'S':
        vals = []
        for s in e[1]:
            v, pos = read_elem(blob, pos, s)
            vals.append(v)
        return tuple(vals), pos
    if e[0] == 'A':
        cnt, = struct.unpack_from('<I', blob, pos)
        pos += 4
        if cnt > 10_000_000:
            raise DecodeError("tpl: absurd count %d" % cnt)
        arr = []
        for _ in range(cnt):
            v, pos = read_elem(blob, pos, e[1])
            arr.append(v)
        return arr, pos
    raise DecodeError("bad elem %r" % (e,))


def decode_tpl(blob):
    if blob[:4] != b'tpl\0':
        raise DecodeError("tpl: bad magic %r" % blob[:4])
    total, = struct.unpack_from('<I', blob, 4)
    nul = blob.index(b'\0', 8)
    sig = blob[8:nul].decode('ascii')
    pos = nul + 1
    toks = tokenize_sig(sig)
    vals = []
    for t in toks:
        v, pos = read_elem(blob, pos, t)
        vals.append(v)
    return {'sig': sig, 'total_len_field': total, 'blob_len': len(blob),
            'consumed': pos, 'values': vals}


# ---------------------------------------------------------------- stroke
def f32(b):
    return struct.unpack('<f', b)[0]


def decode_color(cb):
    m = parse_message(cb)
    rgba = [0.0, 0.0, 0.0, 0.0]
    for f, wt, v in m:
        if 1 <= f <= 4 and wt == 5:
            rgba[f - 1] = f32(v)
    return tuple(rgba)
