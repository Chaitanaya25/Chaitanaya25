"""Outlined lettering. Glyphs defined once per SVG (<path> in <defs>) and reused with <use>."""
import os
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")
FILES = {"display": "Outfit-SemiBold.ttf", "label": "Outfit-SemiBold.ttf", "body": "Outfit-Medium.ttf"}
CODES = {"display": "D", "label": "L", "body": "B"}


def _n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Font:
    def __init__(self, key):
        self.key = key
        self.tt = TTFont(os.path.join(FONT_DIR, FILES[key]))
        self.gs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm
        self.hm = self.tt["hmtx"]
        self.kt = self._kern()
        self.kc, self.pc = {}, {}

    def _kern(self):
        out = []
        if "GPOS" not in self.tt:
            return out
        g = self.tt["GPOS"].table
        idx = set()
        for fr in g.FeatureList.FeatureRecord:
            if fr.FeatureTag == "kern":
                idx.update(fr.Feature.LookupListIndex)
        for i in sorted(idx):
            lk = g.LookupList.Lookup[i]
            for st in lk.SubTable:
                if lk.LookupType == 9:
                    st = st.ExtSubTable
                if getattr(st, "Format", None) in (1, 2) and hasattr(st, "Coverage"):
                    out.append(st)
        return out

    def kern(self, a, b):
        k = (a, b)
        if k in self.kc:
            return self.kc[k]
        val = 0
        for st in self.kt:
            cov = st.Coverage.glyphs
            if a not in cov:
                continue
            if st.Format == 1:
                ps = st.PairSet[cov.index(a)]
                hit = next((r for r in ps.PairValueRecord if r.SecondGlyph == b), None)
                if hit is not None and hit.Value1 is not None:
                    val = getattr(hit.Value1, "XAdvance", 0) or 0
                    break
            else:
                c1 = st.ClassDef1.classDefs.get(a, 0)
                c2 = st.ClassDef2.classDefs.get(b, 0)
                rec = st.Class1Record[c1].Class2Record[c2].Value1
                v = getattr(rec, "XAdvance", 0) if rec is not None else 0
                if v:
                    val = v
                    break
        self.kc[k] = val
        return val

    def glyph(self, ch):
        return self.cmap.get(ord(ch)) or self.cmap.get(ord("?"))

    def path(self, g):
        if g not in self.pc:
            pen = SVGPathPen(self.gs, ntos=_n)
            self.gs[g].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
            self.pc[g] = pen.getCommands()
        return self.pc[g]


_F = {}


def font(k):
    if k not in _F:
        _F[k] = Font(k)
    return _F[k]


class Type:
    def __init__(self, prefix):
        self.p, self.used = prefix, {}

    def _lay(self, s, f, tr):
        out, x, prev = [], 0, None
        for ch in s:
            g = f.glyph(ch)
            if prev is not None:
                x += f.kern(prev, g)
            out.append((g, x))
            x += f.hm[g][0] + tr
            prev = g
        return out, x - (tr if s else 0)

    def width(self, s, size, key="display", track=0.0):
        f = font(key)
        _, w = self._lay(s, f, track * f.upm)
        return w * size / f.upm

    def text(self, s, x, y, size, key="display", fill="#000", track=0.0, anchor="start", attrs="", gstyle=None):
        f = font(key)
        lay, w = self._lay(s, f, track * f.upm)
        sc = size / f.upm
        if anchor == "end":
            x -= w * sc
        elif anchor == "middle":
            x -= w * sc / 2
        uses = []
        for i, (g, gx) in enumerate(lay):
            if not f.path(g):
                continue
            gid = f"{self.p}{CODES[key]}{f.tt.getGlyphID(g)}"
            self.used[gid] = (f, g)
            st = f' style="{gstyle(i)}"' if gstyle else ""
            xs = f' x="{gx:.0f}"' if round(gx) else ""
            uses.append(f'<use href="#{gid}"{xs}{st}/>')
        a = f" {attrs}" if attrs else ""
        return f'<g transform="translate({x:.1f} {y:.1f}) scale({sc:.5f})" fill="{fill}"{a}>' + "".join(uses) + "</g>"

    def defs(self):
        return "".join(f'<path id="{i}" d="{f.path(g)}"/>' for i, (f, g) in sorted(self.used.items()))
