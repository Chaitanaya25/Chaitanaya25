"""Helpers shared by the plates."""
from ..props import bird, cloud
from ..tokens import EASE


def travel(m, iso, pts, ease="linear"):
    """Root style moving a thing through iso points. pts: (t, x, y, z[, extra_css[, ease]]).
    Returns (style, (X0, Y0)): draw the thing at (X0, Y0); the style translates it."""
    X0, Y0 = iso.p(*pts[0][1:4])
    fr = []
    for pt in pts:
        t, x, y, z = pt[:4]
        extra = pt[4] if len(pt) > 4 and pt[4] else ""
        e = pt[5] if len(pt) > 5 else None
        X, Y = iso.p(x, y, z)
        css = f"transform:translate({X - X0:.1f}px,{Y - Y0:.1f}px)"
        if extra:
            css += ";" + extra
        if e:
            css += ";animation-timing-function:" + EASE.get(e, e)
        fr.append((t, css))
    return m.loop(fr, ease), (X0, Y0)


def sky(d, clouds, birds=()):
    out = ""
    for c in clouds:
        out += cloud(d, *c)
    for b in birds:
        out += bird(d, *b)
    return out


def complement(L, wins):
    out, t = [], 0.0
    for a, b in sorted(wins):
        if a > t + .001:
            out.append((t, a))
        t = max(t, b)
    if t < L - .001:
        out.append((t, float(L)))
    return out


def walker(d, iso, pts, variant="teal", scale=2.1, flip=False, carry=None, wp=.9, delay=0.0, lean=None, wraps=(), idle_arms=0,
           rest_pose=None):
    """A character that follows iso points. Walking limbs are shown while the position changes; the standing
    pose otherwise. pts: (t, x, y, z[, css[, ease]]). carry: markup drawn in the hands (None for empty)."""
    from ..rig import character, idle, pose, walk
    m = d.m
    L = m.L
    st, (X, Y) = travel(m, iso, pts)
    moving, prev = [], None
    for pt in pts:
        t, x, y, z = pt[:4]
        if prev is not None and (abs(x - prev[1]) > 1e-6 or abs(y - prev[2]) > 1e-6):
            if moving and abs(moving[-1][1] - prev[0]) < 1e-6:
                moving[-1] = (moving[-1][0], t)
            else:
                moving.append((prev[0], t))
        prev = pt
    rest = {**pose(idle_arms, -idle_arms, 0, 0), **idle(m, L / 4, delay % (L / 4))}
    if rest_pose:
        rest = {**rest, **rest_pose}
    return character(d, X, Y, variant, scale, flip, st=walk(m, wp, carry=carry is not None, delay=delay), rest=rest,
                     moving=moving or None, root=st, carried=carry or "", lean=lean or "", wraps=wraps)


def paper_plane(d, s=1.0):
    p = d.pal
    return (f'<g transform="scale({s})"><path d="M-13,2 L14,-5 L-2,8 Z" fill="{p["cloud"]}" stroke="{p["terra"]}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M-13,2 L14,-5 L-3,1 Z" fill="{p["sand"]}"/></g>')


def mailbox(d, x, y, s=1.0, lit_t=None):
    m, p = d.m, d.pal
    out = (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="1" rx="14" ry="4" fill="{p["ink"]}" opacity=".14"/>'
           f'<rect x="-2" y="-26" width="4" height="26" fill="{p["wood"]}"/><rect x="-14" y="-44" width="28" height="19" rx="9" fill="{p["teal"]}"/>'
           f'<rect x="9" y="-52" width="3" height="14" fill="{p["terra"]}"/>')
    if lit_t is not None:
        out += f'<path d="M12,-52 h10 v6 h-10z" fill="{p["terra"]}" style="{m.at(lit_t)}"/>'
    return out + "</g>"


def letter_bird(d, s=1.0, flap=True, env=True):
    """Letter-bird in profile facing right: round body, beak, flapping wing, an envelope below."""
    m, p = d.m, d.pal
    per = .6
    wing = m.cycle([(0, "transform:rotate(-28deg)"), (per / 2, "transform:rotate(34deg)"), (per, "transform:rotate(-28deg)")], per,
                   origin="30% 80%", base="transform:rotate(-28deg)") if flap else ""
    e = (f'<g transform="translate(-6 9)"><rect width="18" height="12" rx="2" fill="{p["cloud"]}" stroke="{p["terra"]}" stroke-width="1.5"/>'
         f'<path d="M0,1 L9,7.5 L18,1" fill="none" stroke="{p["terra"]}" stroke-width="1.5"/></g>') if env else ""
    return (f'<g transform="scale({s})"><path d="M-12,2 L-20,-2 L-17,5Z" fill="{p["teal"]}"/>{e}'
            f'<ellipse cx="0" cy="0" rx="12" ry="8" fill="{p["teal"]}"/><circle cx="10" cy="-5" r="6" fill="{p["teal"]}"/>'
            f'<path d="M15,-6 L22,-4 L15,-2Z" fill="{p["terra"]}"/><circle cx="11" cy="-6" r="1.1" fill="{p["cloud"]}"/>'
            f'<g style="{wing}"><path d="M-2,-2 Q-6,-16 6,-17 Q4,-8 4,-2Z" fill="{shade_(p["teal"])}"/></g></g>')


def shade_(h):
    from ..tokens import shade
    return shade(h, .18)


def crown(d, s=1.0):
    p = d.pal
    return (f'<g transform="scale({s})"><path d="M-11,0 L-13,-14 L-6,-7 L0,-17 L6,-7 L13,-14 L11,0Z" fill="{p["terra"]}" stroke="{p["ink"]}" stroke-width="1" stroke-linejoin="round" stroke-opacity=".5"/>'
            f'<circle cx="0" cy="-17" r="2" fill="{p["glow"]}"/></g>')
