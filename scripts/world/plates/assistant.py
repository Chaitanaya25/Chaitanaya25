"""P5 AI business assistant: the harbour shop. 16 s loop; key frame at 12 s.

 0.1-3.0  the boat glides in from the left; a "..." bubble pops (a customer message)   (sign 1 message)
 3.4-5.8  two shelves light in parallel (meaning, spelling); their results meet on the counter (sign 2 hybrid search)
 6.0-7.4  a reply bubble flies from the shop to the boat                                (sign 3 instant reply)
 7.6-9.6  the stopwatch arc, long for 20 min, shrinks to a sliver: <30 s
 ambient  two more boats bob at the dock with their own lanterns; their bubbles light at different times
14.6-16   the first boat drifts off and a new one fades in at the left
"""
import math

from ..doc import Doc
from ..iso import Iso
from ..props import bush, house, ripples, tree
from ..rig import character, idle, pose
from ..signs import legend, marker, status_plaque
from ..tokens import LOOPS, shade
from .common import sky, travel

H = 810


def build(theme):
    L = LOOPS["assistant"]
    d = Doc("a", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    iso = Iso(d, 700, 250, 48)
    out = sky(d, [(1080, 90, 1.0, 50, 2), (210, 70, .8, 40, 9), (640, 50, .7, 55, 12), (120, 470, .9, 50, 5)],
              [(-150, 1450, 140, 3, 1.1), (-150, 1450, 230, 11, .9)])
    # ---- water ----------------------------------------------------------------------------------------------------------------------
    wz = -.5
    wpts = [(-3.4, 5.0), (7.2, 5.0), (7.2, 11.5), (-3.4, 11.5)]
    out += iso.poly([(x, y, wz) for x, y in wpts], p["water"])
    out += iso.box(-3.4, 11.5, wz - .35, 10.6, 0.01, .35, cols=(p["water"], shade(p["water"], -.12), shade(p["water"], -.2)), top=False)
    out += ripples(d, 110, 560, 4, 90, 0) + ripples(d, 360, 690, 3, 90, 1.5) + ripples(d, 620, 740, 3, 80, 2.5)
    # ---- island + shop -------------------------------------------------------------------------------------------------------------------
    out += iso.island(0, 0, 9.4, 5.0, "cream", layers=3)
    out += tree(d, 1150, 350, 1.2) + bush(d, 1110, 405, 1.0) + tree(d, 1060, 300, 1.0)
    out += shop(d, iso)
    # lamppost
    lx, ly = iso.p(5.9, 3.6, 0)
    out += (f'<g transform="translate({lx:.1f} {ly:.1f})"><ellipse cx="0" cy="1" rx="9" ry="3" fill="{p["ink"]}" opacity=".14"/>'
            f'<rect x="-2" y="-92" width="4" height="92" fill="{shade(p["wood"], -.35)}"/><path d="M-2,-90 Q-14,-98 -16,-84" fill="none" stroke="{shade(p["wood"], -.35)}" stroke-width="3"/>'
            f'<g transform="translate(-16 -80)"><circle r="15" fill="{p["glow"]}" style="{m.cycle([(0, "opacity:.18"), (1, "opacity:.42"), (2, "opacity:.18")], 2.0, base="opacity:.3")}"/>'
            f'<rect x="-5" y="-7" width="10" height="14" rx="2.5" fill="{shade(p["teal"], -.35)}"/><rect x="-3.2" y="-5" width="6.4" height="10" rx="1.6" fill="{p["glow"]}"/></g></g>')
    # dock
    out += iso.box(3.2, 5.0, wz + .2, 1.1, 3.2, .35, "wood")
    for j in range(4):
        out += iso.box(3.0, 5.4 + j * .8, wz - .2, .12, .12, 1.0, "wood")
    # stopwatch on a pedestal
    out += stopwatch(d, iso)
    # signposts
    for k, (x, y, t_on) in enumerate([(2.7, 4.6, 3.0), (5.3, 3.3, 3.6), (4.6, 4.6, 6.0), (8.6, 2.7, 7.6)]):
        out += marker(d, iso, x, y, k + 1, t_on)
    out += legend(d, 40, 70, [(1, "message arrives", 3.0), (2, "hybrid search", 3.6), (3, "instant reply", 6.0), (4, "20 min → <30 s", 7.6)])
    # ---- boats ---------------------------------------------------------------------------------------------------------------------------------------
    out += extra_boat(d, iso, 5.0, 8.4, .6, 3.0, "teal")
    out += extra_boat(d, iso, 2.0, 10.2, 1.6, 9.5, "terra")
    out += main_boat(d, iso)
    out += reply_bubble(d, iso)
    out += status_plaque(d, 1250, 24, "LIVE", "LIVE")
    return d.render(out, "AI business assistant: the harbour shop", DESC)


DESC = ("A small harbour with a dock, a shop with a striped awning and a sign reading AI ASSISTANT, a lamppost and a stopwatch on a "
        "pedestal. A boat arrives with a speech bubble: a customer message. In the shop window two shelves light up in parallel, meaning "
        "and spelling, and their results merge on the counter: hybrid search. A reply bubble flies back to the boat. The stopwatch arc "
        "shrinks from 20 minutes to under 30 seconds. Two more boats with lanterns bob at the dock: separate conversations kept apart.")


def shop(d, iso):
    m, t, p = d.m, d.t, d.pal
    x, y, w, dd, h = .5, .2, 4.8, 2.6, 2.4
    from ..props import arch_path
    out = house(d, iso, x, y, 0, w, dd, h, "terra", 1.2, "sand", windows=0, door=False, ov=.3)
    g, hp = iso.g, iso.h
    fw = w * g
    c = ""
    # shop window with two shelves
    win = (fw * .1, fw * .55)
    c += f'<rect x="{win[0]:.1f}" y="{-hp * 1.55:.1f}" width="{win[1] - win[0]:.1f}" height="{hp * 1.1:.1f}" rx="4" fill="{shade(d.c("sand"), -.5)}"/>'
    sw_ = win[1] - win[0]
    for r_, (vy, lab) in enumerate(((-hp * 1.1, "meaning"), (-hp * 1.34, "spelling"))):
        c += f'<rect x="{win[0] + 6:.1f}" y="{vy:.1f}" width="{sw_ - 12:.1f}" height="3" fill="{d.c("wood")}"/>'
        for j in range(4):
            tt = 3.8 + r_ * .15 + j * .22
            c += (f'<rect x="{win[0] + 12 + j * (sw_ - 24) / 4:.1f}" y="{vy - 15:.1f}" width="{(sw_ - 24) / 4 - 5:.1f}" height="14" rx="2" fill="{shade(d.c("sand"), -.2)}"/>'
                  f'<rect x="{win[0] + 12 + j * (sw_ - 24) / 4:.1f}" y="{vy - 15:.1f}" width="{(sw_ - 24) / 4 - 5:.1f}" height="14" rx="2" fill="{d.c("terra") if r_ == 0 else d.c("glow")}" style="{m.windows([(tt, 6.0)], .25)}"/>')
    # counter blocks where results merge
    cx_ = win[0] + sw_ / 2
    c += f'<rect x="{win[0] + 4:.1f}" y="{-hp * .98:.1f}" width="{sw_ - 8:.1f}" height="9" fill="{d.c("wood")}"/>'
    c += (f'<rect x="{cx_ - 12:.1f}" y="{-hp * .98 - 17:.1f}" width="24" height="17" rx="3" fill="{d.c("terra")}" style="{m.windows([(5.4, 7.4)], .3, "land")}"/>')
    # door
    c += f'<path d="{arch_path(fw * .66, 0, g * .8, hp * 1.5)}" fill="{shade(d.c("wood"), -.35)}"/>'
    # awning stripes
    aw_y = -hp * 1.7
    stripes = ""
    n = 8
    uw = fw * .5 / n
    for j in range(n):
        stripes += f'<path d="M{win[0] - 6 + j * uw * 1.1:.1f},{aw_y:.1f} h{uw * 1.1:.1f} l{3:.1f},{hp * .55:.1f} h{-uw * 1.1:.1f}z" fill="{d.c("terra") if j % 2 == 0 else d.c("cloud")}"/>'
    c += stripes
    # sign above the door: AI ASSISTANT
    sg = (f'<rect x="{fw * .6:.1f}" y="{-hp * 2.12:.1f}" width="{fw * .37:.1f}" height="{hp * .46:.1f}" rx="5" fill="{d.c("board")}" stroke="{d.c("wood")}" stroke-width="2"/>'
          + t.text("AI ASSISTANT", fw * .6 + fw * .37 / 2, -hp * 2.12 + hp * .31, 15, "label", d.c("ink"), .1, "middle"))
    return out + iso.on_face(x, y, 0, w, dd, "L", c + sg)


def stopwatch(d, iso):
    m, t, p = d.m, d.t, d.pal
    out = iso.box(6.9, 1.2, 0, 1.6, 1.4, .6, "sand")
    X, Y = iso.p(7.7, 1.9, .6)
    r = 38
    dash = m.loop([(0, "stroke-dashoffset:0"), (7.6, "stroke-dashoffset:0"), (9.4, "stroke-dashoffset:97"), (14.4, "stroke-dashoffset:97"),
                   (14.9, "stroke-dashoffset:0"), (L := m.L, "stroke-dashoffset:0")], "travel")
    ring = (f'<circle r="{r}" fill="{p["cloud"]}" stroke="{shade(p["wood"], -.25)}" stroke-width="6"/>'
            f'<rect x="-6" y="{-r - 14}" width="12" height="10" rx="3" fill="{shade(p["wood"], -.25)}"/>'
            f'<circle r="{r - 11}" fill="none" stroke="{p["sand"]}" stroke-width="5" opacity=".7"/>'
            f'<circle r="{r - 11}" fill="none" stroke="{p["terra"]}" stroke-width="6" stroke-linecap="round" pathLength="100" stroke-dasharray="100" '
            f'transform="rotate(-90)" style="{dash}"/>')
    lab_a = t.text("20 min", 0, 8, 22, "label", p["ink"], .04, "middle", attrs=f'style="{m.windows([(0, 8.4)], .3)}"')
    lab_b = t.text("<30 s", 0, 8, 22, "label", shade(p["terra"], -.4) if not p["night"] else p["glow"], .04, "middle", attrs=f'style="{m.windows([(9.1, 14.4)], .3)}"')
    return out + f'<g transform="translate({X:.1f} {Y - r - 16:.1f})">{ring}{lab_a}{lab_b}</g>'


def hull(d, w=150, h=34):
    p = d.pal
    return (f'<path d="M{-w / 2},-8 Q{-w / 2 + 14},{h} {-w / 2 + 40},{h} H{w / 2 - 40} Q{w / 2 - 14},{h} {w / 2},-14 Z" fill="{p["wood"]}"/>'
            f'<path d="M{-w / 2},-8 L{w / 2},-14" stroke="{shade(p["wood"], -.3)}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M{-w / 2 + 20},10 H{w / 2 - 20}" stroke="{shade(p["wood"], -.2)}" stroke-width="2" opacity=".6"/>')


def bob(m, per=2.0, amp=3.0, delay=0.0):
    return m.cycle([(0, f"transform:translateY({amp}px)"), (per / 2, f"transform:translateY({-amp}px)"), (per, f"transform:translateY({amp}px)")],
                   per, delay=delay % per, base="transform:translateY(0)")


def bubble(d, x, y, t0, t1, s=1.3, dots=True):
    m, p = d.m, d.pal
    st = m.windows([(t0, t1)], .3, "land")
    pts = "".join(f'<circle cx="{-12 + 12 * i}" cy="-14" r="3.4" fill="{p["ink"]}"/>' for i in range(3))
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s})"><g style="{st};transform-box:fill-box;transform-origin:20% 100%">'
            f'<path d="M-26,-30 h52 a10,10 0 0 1 10,10 v10 a10,10 0 0 1 -10,10 h-34 l-10,12 v-12 h-8 a10,10 0 0 1 -10,-10 v-10 a10,10 0 0 1 10,-10z" '
            f'transform="translate(0 4)" fill="{p["board"]}" stroke="{p["ink"]}" stroke-width="2" stroke-opacity=".6"/>{pts}</g></g>')


def main_boat(d, iso):
    m, p = d.m, d.pal
    L = m.L
    pts = [(0, -3.0, 7.3, 0, "opacity:0"), (.1, -3.0, 7.3, 0, "opacity:1"), (2.9, 1.9, 7.3, 0, "opacity:1", "settle"),
           (14.5, 1.9, 7.3, 0, "opacity:1"), (15.5, 4.2, 6.4, 0, "opacity:0"), (L, -3.0, 7.3, 0, "opacity:0")]
    st, (X, Y) = travel(m, iso, pts)
    man = character(d, 4, 4, "teal", 1.8, False, st=idle(m, L / 4), scarf=True, shadow=False)
    crate = f'<rect x="-34" y="-34" width="22" height="20" rx="2" fill="{p["sand"]}"/><rect x="-34" y="-34" width="22" height="7" rx="2" fill="{shade(p["sand"], .15)}"/>'
    inner = f'<g style="{bob(m, 2.0, 3.0)}">{hull(d)}{crate}{man}<path d="M-40,2 Q0,26 40,-4 L40,-10 Q0,12 -40,-4Z" fill="{shade(p["wood"], .12)}"/></g>'
    return f'<g style="{st}"><g transform="translate({X:.1f} {Y:.1f})">{inner}{bubble(d, 40, -78, 3.0, 8.6)}</g></g>'


def extra_boat(d, iso, x, y, delay, t_bubble, variant):
    m, p = d.m, d.pal
    X, Y = iso.p(x, y, 0)
    lan = (f'<g transform="translate(-52 -50)"><rect x="-1.4" y="0" width="2.8" height="48" fill="{shade(p["wood"], -.3)}"/>'
           f'<circle cy="-4" r="12" fill="{p["glow"]}" style="{m.cycle([(0, "opacity:.2"), (1.0, "opacity:.45"), (2.0, "opacity:.2")], 2.0, delay=delay, base="opacity:.35")}"/>'
           f'<rect x="-4" y="-10" width="8" height="12" rx="2" fill="{shade(p["teal"], -.35)}"/><rect x="-2.6" y="-8" width="5.2" height="8" rx="1.3" fill="{p["glow"]}"/></g>')
    man = character(d, 6, 4, variant, 1.7, True, st=idle(m, d.m.L / 4, delay), scarf=True, shadow=False)
    return (f'<g transform="translate({X:.1f} {Y:.1f})"><g style="{bob(m, 2.0, 3.0, delay)}">{hull(d, 140, 32)}{lan}{man}'
            f'<path d="M-36,2 Q0,24 36,-4 L36,-10 Q0,10 -36,-4Z" fill="{shade(p["wood"], .12)}"/></g>{bubble(d, -30, -78, t_bubble, t_bubble + 2.6, .8)}</g>')


def reply_bubble(d, iso):
    m, p = d.m, d.pal
    L = m.L
    sx, sy = iso.p(2.0, 2.8, 1.7)
    bx, by = iso.p(1.9, 7.3, 0)
    pts = [(0, sx, sy), (6.0, sx, sy), (6.3, sx, sy), (7.2, bx + 40, by - 110), (7.6, bx + 40, by - 100), (L, bx + 40, by - 100)]
    fr = [(0, "opacity:0;transform:translate(0px,0px)"), (5.95, "opacity:0;transform:translate(0px,0px)"), (6.05, "opacity:1;transform:translate(0px,0px)"),
          (6.65, f"opacity:1;transform:translate({(bx + 40 - sx) * .55:.0f}px,{(by - 110 - sy) * .35 - 40:.0f}px);animation-timing-function:cubic-bezier(.22,1,.36,1)"),
          (7.3, f"opacity:1;transform:translate({bx + 40 - sx:.0f}px,{by - 110 - sy:.0f}px)"), (8.6, f"opacity:1;transform:translate({bx + 40 - sx:.0f}px,{by - 110 - sy:.0f}px)"),
          (8.9, f"opacity:0;transform:translate({bx + 40 - sx:.0f}px,{by - 110 - sy:.0f}px)"), (L, "opacity:0;transform:translate(0px,0px)")]
    st = m.loop(fr, "settle", base=f"opacity:0;transform:translate({bx + 40 - sx:.0f}px,{by - 110 - sy:.0f}px)")
    check = f'<path d="M-10,-14 L-3,-7 L10,-21" fill="none" stroke="{p["terra"]}" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
    bub = (f'<g transform="translate({sx:.1f} {sy:.1f})"><g style="{st}"><path d="M-24,-34 h48 a10,10 0 0 1 10,10 v22 a10,10 0 0 1 -10,10 h-34 l-10,12 v-12 h-4 a10,10 0 0 1 -10,-10 v-22 a10,10 0 0 1 10,-10z" '
           f'transform="translate(0 4)" fill="{p["board"]}" stroke="{p["terra"]}" stroke-width="2.4"/>{check}</g></g>')
    return bub
