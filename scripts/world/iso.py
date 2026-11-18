"""True 2:1 isometric helpers. x runs right-down, y runs left-down, z runs up.

Light comes from the top-left: top faces lightest, the +y face (left) mid, the +x face (right) darkest.
"""
import math

from .tokens import G


class Iso:
    def __init__(self, doc, ox, oy, g=G):
        self.d, self.ox, self.oy, self.g = doc, ox, oy, g
        self.h = g * 1.118          # z unit so an edge of every cube has the same length

    def p(self, x, y, z=0.0):
        return (self.ox + (x - y) * self.g, self.oy + (x + y) * self.g / 2 - z * self.h)

    def pts(self, *pp):
        return " ".join("%.1f,%.1f" % self.p(*q) for q in pp)

    def poly(self, pp, fill, extra=""):
        return f'<polygon points="{self.pts(*pp)}" fill="{fill}"{extra}/>'

    # -- solids ----------------------------------------------------------------------
    def box(self, x, y, z, w, d, h, role="sand", cols=None, extra="", top=True):
        t, l, r = cols or self.d.faces(role)
        out = (self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], r)
               + self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], l))
        if top:
            out += self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], t)
        return f"<g{extra}>{out}</g>" if extra else out

    def shadow(self, x, y, w, d, z=0.0, op=.16):
        cx, cy = self.p(x + w / 2, y + d / 2, z)
        return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{(w + d) * self.g * .52:.1f}" ry="{(w + d) * self.g * .27:.1f}" '
                f'fill="{self.d.c("ink")}" opacity="{op}"/>')

    def face(self, x, y, z, w, d, which):
        """Matrix mapping flat face space (u right in px, v down in px) onto a vertical face.
        'L' = the +y face (runs along x), 'R' = the +x face (runs along -y)."""
        if which == "L":
            X, Y = self.p(x, y + d, z)
            return f"matrix(1,.5,0,1,{X:.1f},{Y:.1f})"
        X, Y = self.p(x + w, y + d, z)
        return f"matrix(1,-.5,0,1,{X:.1f},{Y:.1f})"

    def on_face(self, x, y, z, w, d, which, content, extra=""):
        return f'<g transform="{self.face(x, y, z, w, d, which)}"{extra}>{content}</g>'

    def top_matrix(self, x, y, z):
        """Flat floor space (u along x, v along y, 1 unit = 1 grid unit) onto a horizontal plane."""
        X, Y = self.p(x, y, z)
        g = self.g
        return f"matrix({g},{g / 2},{-g},{g / 2},{X:.1f},{Y:.1f})"

    # -- islands ---------------------------------------------------------------------
    def island(self, x, y, w, d, top="cream", thick=.5, layers=3, side="sage"):
        out = ""
        for i in reversed(range(layers)):
            ins = min(.28 * (i + 1) + .08 * (i + 1) ** 1.3, w / 2 - .3, d / 2 - .3)
            zt = -thick - .62 * i
            role = "deep" if i % 2 else side
            out += self.box(x + ins, y + ins, zt - .62, w - 2 * ins, d - 2 * ins, .62, role, top=False)
        tt = self.d.faces(top)[0]
        sl, sr = self.d.faces(side)[1], self.d.faces(side)[2]
        out += self.box(x, y, -thick, w, d, thick, cols=(tt, sl, sr))
        return out

    def round_island(self, cx, cy, r, top="cream", thick=.5, layers=3):
        """Circular island of radius r (grid units) centred at (cx, cy)."""
        out = ""
        d = self.d
        for i in reversed(range(layers + 1)):
            rr = r - (0 if i == 0 else .32 * i)
            zt = -(thick if i == 0 else thick + .62 * (i - 1))
            hh = thick if i == 0 else .62
            role = "sage" if i % 2 == 0 else "deep"
            out += self._cyl(cx, cy, rr, zt - hh, hh, role, topcol=d.faces(top)[0] if i == 0 else None, sidecols=None)
        return out

    def _cyl(self, cx, cy, r, z, hgt, role, topcol=None, sidecols=None):
        X, Y = self.p(cx, cy, z + hgt)
        rx, ry = 1.414 * r * self.g, .707 * r * self.g
        H = hgt * self.h
        t, l, rr = self.d.faces(role)
        left = f"M{X - rx:.1f},{Y:.1f} L{X - rx:.1f},{Y + H:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {X:.1f},{Y + ry + H:.1f} L{X:.1f},{Y + ry:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {X - rx:.1f},{Y:.1f}Z"
        right = f"M{X + rx:.1f},{Y:.1f} L{X + rx:.1f},{Y + H:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {X:.1f},{Y + ry + H:.1f} L{X:.1f},{Y + ry:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {X + rx:.1f},{Y:.1f}Z"
        out = f'<path d="{left}" fill="{l}"/><path d="{right}" fill="{rr}"/>'
        out += f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{topcol or t}"/>'
        return out

    def cylinder(self, cx, cy, z, r, hgt, role="sand", topcol=None):
        return self._cyl(cx, cy, r, z, hgt, role, topcol)

    def stairs(self, x, y, z, n, axis="y", width=1.4, run=.5, rise=.36, role="sand", thick=.28):
        """Staircase descending toward +axis (first step top at z). Slabs are drawn far to near."""
        out = ""
        for i in range(n):
            zt = z - rise * i
            if axis == "y":
                out += self.box(x, y + i * run, zt - thick, width, run, thick, role)
            else:
                out += self.box(x + i * run, y, zt - thick, run, width, thick, role)
        return out

    def ground_diamond(self, x, y, w, d, z, fill, extra=""):
        return self.poly([(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z)], fill, extra)


def ellipse_pts(cx, cy, rx, ry, n=24, a0=0.0):
    return [(cx + rx * math.cos(a0 + 2 * math.pi * i / n), cy + ry * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]
