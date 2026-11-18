"""Contact signposts: four small link-wrapped plates (wooden post, arrow sign, a tiny idle). 8 s loop."""
from ..doc import Doc
from ..tokens import LOOPS, shade

POSTS = [("post-demo", "Live demo", "chronicle.hypertos.in", True),
         ("post-portfolio", "Portfolio", "hypertos.in", False),
         ("post-linkedin", "LinkedIn", "chaitanaya052006", False),
         ("post-leetcode", "LeetCode", "Chaitanaya_25", False),
         ("post-email", "Email", "Chaitanyasrivastava63@gmail.com", False)]


def one(theme, key, label, sub, first, bird_on=False):
    L = LOOPS["post"]
    d = Doc(key[5:7], theme, L, 150, 380)
    m, t, p = d.m, d.t, d.pal
    wood = p["wood"]
    sw = max(t.width(label, 30, "display"), t.width(sub, 17, "body") * 1.12) + 74
    sw = min(sw, 350)
    sway = m.cycle([(0, "transform:rotate(-1.6deg)"), (L / 4, "transform:rotate(1.6deg)"), (L / 2, "transform:rotate(-1.6deg)")], L / 2,
                   origin="0% 50%", base="transform:rotate(-1.2deg)")
    fill = p["terra"] if first else p["board"]
    ink = (p["bg"] if p["night"] else "#FFF8EE") if first else p["ink"]
    sub_c = ink if first else shade(p["ink"], .25 if not p["night"] else -.15)
    out = (f'<ellipse cx="34" cy="140" rx="26" ry="6" fill="{p["ink"]}" opacity=".15"/>'
           f'<rect x="28" y="26" width="13" height="114" rx="3" fill="{wood}"/><rect x="28" y="26" width="5" height="114" rx="2" fill="{shade(wood, .15)}"/>'
           f'<g transform="translate(41 38)"><g style="{sway}">'
           f'<path d="M0,0 H{sw - 16:.0f} L{sw:.0f},24 L{sw - 16:.0f},48 H0Z" fill="{fill}" stroke="{shade(wood, -.15)}" stroke-width="2.4" stroke-linejoin="round"/>'
           f'{t.text(label, 16, 26, 28, "display", ink)}{t.text(sub, 16, 42, min(15, 15 * 250 / max(t.width(sub, 15, "body") * 1.12, 250)), "body", sub_c)}</g></g>')
    if bird_on:
        hop = m.cycle([(0, "transform:translateY(0)"), (.5, "transform:translateY(-4px)"), (1, "transform:translateY(0)")], 2.0, base="transform:translateY(0)")
        out += (f'<g transform="translate(34 24)"><g style="{hop}"><ellipse cx="0" cy="0" rx="11" ry="8" fill="{p["teal"]}"/><circle cx="9" cy="-5" r="5.5" fill="{p["teal"]}"/>'
                f'<path d="M13,-6 L19,-4 L13,-2Z" fill="{p["terra"]}"/><circle cx="10" cy="-6" r="1" fill="{p["cloud"]}"/><path d="M-10,1 L-18,-2 L-15,4Z" fill="{p["teal"]}"/></g></g>')
    return d.render(out, f"{label}: {sub}", f"Link: a wooden signpost with an arrow sign reading {label}, {sub}.", transparent=True)


def build(theme):
    return [(k, one(theme, k, lab, sub, first, k == "post-linkedin")) for k, lab, sub, first in POSTS]
