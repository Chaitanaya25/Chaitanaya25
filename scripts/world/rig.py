"""The character rig: a small hooded figure, about 44 units tall, built from separately pivoting parts.

Parts: scarf, far arm, far leg, near leg, cloak, hood/head, near arm. Facing right; flip mirrors it.
Pivots: arms at the shoulder, legs at the hip, scarf at the neck. Cycles are keyframe sets the plates
attach to those parts; characters that start and stop walking carry a walking limb set and a standing
limb set whose visibility is switched on the plate's clock.
"""
from .tokens import mix, shade


def cols(d, variant):
    p = d.pal
    night = p["night"]
    if variant == "terra":
        cloak, scarf, belt = p["terra"], shade(p["terra"], -.32), p["teal"]
    else:   # teal
        cloak, scarf, belt = p["teal"], p["cream"] if not night else p["sand"], p["terra"]
    return dict(cloak=cloak, dark=shade(cloak, -.2), light=shade(cloak, .1), scarf=scarf, belt=belt,
                skin=p["face"], leg="#3A3733" if not night else "#16202A", ink=p["ink"] if not night else "#1B2329")


def _limb(inner, x, y, style, extra=""):
    return f'<g transform="translate({x} {y})"><g style="{style}"{extra}>{inner}</g></g>'


def _arm(c, far):
    k = c["dark"] if far else c["cloak"]
    return (f'<rect x="-2.4" y="0" width="4.8" height="10.5" rx="2.3" fill="{k}"/>'
            f'<circle cx="0" cy="10.6" r="2.5" fill="{c["skin"]}"/>')


def _leg(c):
    return (f'<rect x="-2.3" y="0" width="4.6" height="12" rx="2.2" fill="{c["leg"]}"/>'
            f'<ellipse cx="1" cy="12" rx="3.6" ry="1.7" fill="{c["leg"]}"/>')


def character(d, x, y, variant="teal", s=1.0, flip=False, st=None, rest=None, moving=None, root="",
              wraps=(), carried="", lean="", scarf=True, shadow=True, cloak_op=None):
    """Return markup for one character standing at (x, y) (feet), scaled by s.

    st      styles for the animated parts: legN legF armN armF bob head scarf
    rest    styles for the standing pose, used when `moving` windows are given
    moving  list of (t0, t1) windows (seconds) when the walking limb set is shown
    root    style animating the whole figure (travel along a path)
    wraps   extra wrapper styles (e.g. fade-out for a fenced worker), applied outermost
    carried markup drawn in character space in front of the body (a block in the hands)
    lean    style leaning/tilting the whole figure around its feet
    """
    c = cols(d, variant)
    m = d.m
    st, rest = st or {}, rest or {}
    sx = -s if flip else s

    def back(styles):
        return (_limb(_arm(c, True), -5.5, -26, styles.get("armF", ""))
                + _limb(_leg(c), -2.7, -12, styles.get("legF", ""))
                + _limb(_leg(c), 2.7, -12, styles.get("legN", "")))

    def front(styles):
        return _limb(_arm(c, False), 5.5, -26, styles.get("armN", ""))

    if moving:
        wv = f'<g style="{m.windows(moving)}">{{}}</g>'
        sv = f'<g style="{m.windows(m.complement(moving))}">{{}}</g>'
        backs = wv.format(back(st)) + sv.format(back(rest))
        fronts = wv.format(front(st)) + sv.format(front(rest))
    else:
        backs, fronts = back(st), front(st)

    cloak = (f'<path d="M-7,-27 Q-11,-19 -10.5,-10.5 L10.5,-10.5 Q11,-19 7,-27 Q0,-30 -7,-27Z" fill="{c["cloak"]}"/>'
             f'<path d="M2,-28.5 Q8.5,-22 9.5,-10.5 L10.5,-10.5 Q11,-19 7,-27Z" fill="{c["dark"]}"/>'
             f'<rect x="-9.8" y="-19" width="19.6" height="2.2" fill="{c["belt"]}" opacity=".9"/>')
    head = (f'<g style="{st.get("head", "")}">'
            f'<path d="M-5,-41 L-11.5,-52 L-1,-42Z" fill="{c["light"]}"/>'
            f'<circle cx="0" cy="-33" r="10" fill="{c["light"]}"/>'
            f'<ellipse cx="3.6" cy="-32" rx="6" ry="5.5" fill="{c["skin"]}"/>'
            f'<circle cx="2.6" cy="-33.2" r="1" fill="{c["ink"]}"/><circle cx="6.6" cy="-33.2" r="1" fill="{c["ink"]}"/></g>')
    sc = (f'<g transform="translate(-2 -27)"><g style="{st.get("scarf", "")}">'
          f'<path d="M0,-.5 Q-6,-2 -12,2.5 Q-15,5 -13,8 Q-8,3 -2,3 Q3,2 4,0Z" fill="{c["scarf"]}"/></g></g>') if scarf else ""
    body = (f'<g style="{st.get("bob", "")}">{sc}{backs}{cloak}{head}{fronts}{carried}</g>')
    leanned = f'<g style="{lean}">{body}</g>' if lean else body
    sh = (f'<ellipse cx="0" cy="0" rx="10" ry="3" fill="{d.c("ink")}" opacity=".16"/>') if shadow else ""
    inner = f'<g transform="translate({x:.1f} {y:.1f}) scale({sx:.3f} {s:.3f})">{sh}{leanned}</g>'
    out = f'<g style="{root}">{inner}</g>' if root else inner
    for w in reversed(wraps):
        out = f'<g style="{w}">{out}</g>'
    return out


# ---- cycle builders ----------------------------------------------------------------------
def walk(m, p, amp=26, bob=1.4, delay=0.0, arms=22, carry=False):
    """Walk cycle styles (period p, must divide L). legs swing, arms counter-swing, body bobs."""
    def swing(a, ph):
        fr = [(0, f"transform:rotate({a}deg)"), (p / 2, f"transform:rotate({-a}deg)"), (p, f"transform:rotate({a}deg)")]
        return m.cycle(fr, p, delay=(delay + ph) % p, origin="50% 4%", base=f"transform:rotate({a}deg)")
    out = dict(
        legN=swing(amp, 0), legF=swing(amp, p / 2),
        bob=m.cycle([(0, "transform:translateY(0)"), (p / 4, f"transform:translateY({-bob}px)"), (p / 2, "transform:translateY(0)"),
                     (3 * p / 4, f"transform:translateY({-bob}px)"), (p, "transform:translateY(0)")], p, delay=delay,
                    base="transform:translateY(0)"),
        scarf=m.cycle([(0, "transform:rotate(-4deg)"), (p / 2, "transform:rotate(7deg)"), (p, "transform:rotate(-4deg)")], p,
                      delay=delay, origin="100% 10%", base="transform:rotate(-4deg)"),
    )
    if carry:
        out["armN"] = "transform-box:fill-box;transform-origin:50% 8%;transform:rotate(-78deg)"
        out["armF"] = "transform-box:fill-box;transform-origin:50% 8%;transform:rotate(-70deg)"
    else:
        out["armN"] = swing(-arms, p / 2)
        out["armF"] = swing(-arms, 0)
    return out


def idle(m, period=None, delay=0.0, arms=0):
    """Gentle breathing (1-2 % scale) with a slow scarf lift."""
    p = period or m.L / 4
    return dict(
        bob=m.cycle([(0, "transform:scaleY(1)"), (p / 2, "transform:scaleY(1.025)"), (p, "transform:scaleY(1)")], p,
                    delay=delay, origin="50% 100%", base="transform:scaleY(1)"),
        scarf=m.cycle([(0, "transform:rotate(-3deg)"), (p / 2, "transform:rotate(4deg)"), (p, "transform:rotate(-3deg)")], p,
                      delay=delay, origin="100% 10%", base="transform:rotate(-3deg)"),
        armN=f"transform-box:fill-box;transform-origin:50% 8%;transform:rotate({arms}deg)",
        armF=f"transform-box:fill-box;transform-origin:50% 8%;transform:rotate({-arms}deg)",
    )


def pose(armN=0, armF=0, legN=0, legF=0):
    def f(a):
        return f"transform-box:fill-box;transform-origin:50% 6%;transform:rotate({a}deg)"
    return dict(armN=f(armN), armF=f(armF), legN=f(legN), legF=f(legF))
