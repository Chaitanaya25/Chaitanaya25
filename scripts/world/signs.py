"""Signposts (numbered steps), engraved island names and status plaques."""
from .tokens import shade


def signpost(d, iso, x, y, num, text, t_on, z=0.0, wb=None, lit_to=None):
    """A little wooden post with a sign. Wide layout shows the numbered phrase; the narrow layout
    shows a large numeral badge only. The badge turns terracotta and a flag rises at t_on."""
    m, t, p = d.m, d.t, d.pal
    L = m.L
    wood = p["wood"]
    out = iso.box(x, y, z, .16, .16, 1.9, cols=d.faces(wood))
    size = 21
    wb = wb or (t.width(text, size, "body") + 62)
    hb = 38
    zb = z + 1.05
    board = (f'<rect x="0" y="{-hb}" width="{wb:.0f}" height="{hb}" rx="7" fill="{p["board"]}" stroke="{shade(wood, -.1)}" stroke-width="1.6"/>'
             f'<circle cx="19" cy="{-hb / 2}" r="14" fill="{p["sand"] if not p["night"] else p["deep"]}"/>')
    lit = m.at(t_on, lit_to)
    board += f'<circle cx="19" cy="{-hb / 2}" r="14" fill="{p["terra"]}" style="{lit}"/>'
    board += t.text(str(num), 19, -hb / 2 + 7.2, 19, "display", p["ink"] if not p["night"] else p["bg"], anchor="middle")
    board += t.text(text, 42, -hb / 2 + 7.4, size, "body", p["ink"])
    out += f'<g class="w">{iso.on_face(x, y, zb, .16, .16, "L", board, "")}</g>'
    # flag raised when lit
    fx, fy = iso.p(x + .08, y + .08, z + 1.9)
    rise = m.loop([(0, "transform:translateY(16px);opacity:0"), (t_on, "transform:translateY(16px);opacity:0"),
                   (t_on + .5, "transform:translateY(0);opacity:1;animation-timing-function:cubic-bezier(.34,1.56,.64,1)"),
                   ((lit_to or L * .93), "transform:translateY(0);opacity:1"), (min((lit_to or L * .93) + .4, L), "transform:translateY(0);opacity:0"),
                   (L, "transform:translateY(16px);opacity:0")], "settle")
    out += (f'<g transform="translate({fx:.1f} {fy:.1f})"><g style="{rise}"><path d="M0,-2 L16,3 L0,8Z" fill="{p["terra"]}"/></g></g>')
    # narrow: big numeral badge only
    bx, by = iso.p(x + .08, y + .08, z + 2.0)
    nb = (f'<circle cx="{bx:.1f}" cy="{by - 28:.1f}" r="26" fill="{p["board"]}" stroke="{shade(wood, -.1)}" stroke-width="3"/>'
          f'<circle cx="{bx:.1f}" cy="{by - 28:.1f}" r="19" fill="{p["terra"]}" style="{lit}"/>'
          + t.text(str(num), bx, by - 28 + 13, 38, "display", p["ink"] if not p["night"] else p["bg"], anchor="middle"))
    out += f'<g class="n">{nb}</g>'
    return out


def engraved(d, iso, x, y, z, w, dd, text, which="L", size=40, track=.18, col=None):
    """Spaced uppercase name engraved on an island face, following the isometric angle."""
    t, p = d.t, d.pal
    g = iso.g
    fw = (w if which == "L" else dd) * g
    tw = t.width(text, size, "label", track)
    return iso.on_face(x, y, z, w, dd, which, t.text(text, fw / 2, 0, size, "label", col or p["ink"], track, "middle"))


def status_plaque(d, x_right, y, text, kind):
    """Status sign, right-aligned at x_right: LIVE, IN PROGRESS, PLANNED, SCHEMATIC. Wide + large narrow versions."""
    t, p = d.t, d.pal
    on = kind in ("LIVE", "IN PROGRESS")
    col = p["terra"] if on else p["deep"]
    out = ""
    for cls, size, h in (("w", 21, 38), ("n", 36, 64)):
        w = t.width(text, size, "label", .2) + size * 2.1
        x = x_right - w
        r = h / 2
        dot = (f'<circle cx="{r:.0f}" cy="{r:.0f}" r="{size * .3:.1f}" fill="{col}"/>' if on else
               f'<circle cx="{r:.0f}" cy="{r:.0f}" r="{size * .26:.1f}" fill="none" stroke="{p["ink"]}" stroke-width="{size * .1:.1f}"/>')
        out += (f'<g class="{cls}" transform="translate({x:.0f} {y})"><rect width="{w:.0f}" height="{h}" rx="{r}" fill="{p["board"]}" '
                f'stroke="{col}" stroke-width="{2 if cls == "w" else 3}"/>{dot}'
                f'{t.text(text, size * 1.4 + r * .4, h / 2 + size * .36, size, "label", p["ink"], .2)}</g>')
    return out


def marker(d, iso, x, y, num, t_on, z=0.0, h=1.25):
    """Short post with a round numeral badge that turns terracotta (and a flag rises) at t_on."""
    m, t, p = d.m, d.t, d.pal
    wood = p["wood"]
    out = iso.box(x, y, z, .14, .14, h, cols=d.faces(wood))
    bx, by = iso.p(x + .07, y + .07, z + h)
    lit = m.at(t_on)
    out += (f'<g class="w"><circle cx="{bx:.1f}" cy="{by - 16:.1f}" r="17" fill="{p["board"]}" stroke="{shade(wood, -.1)}" stroke-width="2.4"/>'
            f'<circle cx="{bx:.1f}" cy="{by - 16:.1f}" r="12.5" fill="{p["terra"]}" style="{lit}"/>'
            + t.text(str(num), bx, by - 16 + 7.4, 21, "display", p["ink"] if not p["night"] else p["bg"], anchor="middle") + "</g>")
    out += (f'<g class="n"><circle cx="{bx:.1f}" cy="{by - 26:.1f}" r="27" fill="{p["board"]}" stroke="{shade(wood, -.1)}" stroke-width="3"/>'
            f'<circle cx="{bx:.1f}" cy="{by - 26:.1f}" r="20" fill="{p["terra"]}" style="{lit}"/>'
            + t.text(str(num), bx, by - 26 + 13, 38, "display", p["ink"] if not p["night"] else p["bg"], anchor="middle") + "</g>")
    return out


def legend(d, x, y, items):
    """Row of numbered step pills (wide layout only); each lights at its cue. items: [(num, text, t_on)]."""
    m, t, p = d.m, d.t, d.pal
    out, cx = "", x
    for num, text, t_on in items:
        w = t.width(text, 19, "body") + 52
        out += (f'<g transform="translate({cx:.0f} {y})"><rect width="{w:.0f}" height="36" rx="18" fill="{p["board"]}" stroke="{shade(p["wood"], -.1)}" stroke-width="1.6"/>'
                f'<circle cx="18" cy="18" r="12" fill="{p["sand"] if not p["night"] else p["deep"]}"/>'
                f'<circle cx="18" cy="18" r="12" fill="{p["terra"]}" style="{m.at(t_on)}"/>'
                + t.text(str(num), 18, 24.6, 17, "display", p["ink"] if not p["night"] else p["bg"], anchor="middle")
                + t.text(text, 38, 24.6, 19, "body", p["ink"]) + "</g>")
        cx += w + 10
    return f'<g class="w">{out}</g>'


def chip(d, x, y, text):
    t, p = d.t, d.pal
    w = t.width(text, 20, "label", .12) + 34
    return (f'<g class="w" transform="translate({x} {y})"><rect width="{w:.0f}" height="38" rx="19" fill="{p["board"]}" stroke="{p["deep"]}" stroke-width="2"/>'
            f'{t.text(text, w / 2, 26, 20, "label", p["ink"], .12, "middle")}</g>')
