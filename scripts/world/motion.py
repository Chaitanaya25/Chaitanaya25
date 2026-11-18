"""Keyframe builder on one loop length L. The un-animated (reduced-motion) style is the key frame."""
from .tokens import EASE

KEY_T = .75   # fraction of L at which the key frame is read (inside the 60-92 % hold)


def _pct(t, L):
    return max(0.0, min(100.0, t / L * 100))


class Motion:
    def __init__(self, L, prefix):
        self.L, self.p, self.k, self.n, self.seen = L, prefix, [], 0, {}
        self.key = KEY_T

    def frames(self, fr, dur):
        body = "".join(f"{_pct(t, dur):.2f}%{{{c}}}" for t, c in fr)
        if body in self.seen:
            return self.seen[body]
        self.n += 1
        name = f"{self.p}k{self.n}"
        self.seen[body] = name
        self.k.append(f"@keyframes {name}{{{body}}}")
        return name

    @staticmethod
    def _strip(c):
        return ";".join(p for p in c.split(";") if p and not p.startswith("animation-timing-function"))

    def loop(self, fr, ease="settle", delay=0.0, origin=None, base=None, key_t=None):
        """Looping animation over L. Frames: [(seconds, css)]. The inline base style is the css of the
        last frame at or before the key-frame time, so reduced motion shows the designed key frame."""
        e = EASE.get(ease, ease)
        L = self.L
        kt = (key_t if key_t is not None else self.key) * L
        fr = sorted(fr, key=lambda f: f[0])
        keyc = [c for t, c in fr if t <= kt + 1e-6]
        b = self._strip(keyc[-1]) if keyc else self._strip(fr[0][1])
        if base is not None:
            b = base
        fr2 = [(t, c if "animation-timing-function" in c else f"{c};animation-timing-function:{e}") for t, c in fr]
        d = f"-{(L - delay) % L:.2f}s" if delay else "0s"
        org = f"transform-box:fill-box;transform-origin:{origin};" if origin else ""
        return f"{org}{b};animation:{self.frames(fr2, L)} {L}s linear {d} infinite both"

    def cycle(self, fr, period, ease="ease-in-out", delay=0.0, origin=None, base=""):
        """Short repeating cycle. The period must divide L so the loop stays seamless."""
        n = self.L / period
        assert abs(n - round(n)) < 1e-6, f"period {period} does not divide L={self.L}"
        org = f"transform-box:fill-box;transform-origin:{origin};" if origin else ""
        d = f"-{(period - delay) % period:.3f}s" if delay else "0s"
        b = f"{base};" if base else ""
        return f"{org}{b}animation:{self.frames(fr, period)} {period}s {ease} {d} infinite both"

    def at(self, t_on, t_off=None, fade=.35, ease="settle"):
        """Hidden until t_on, visible until t_off (default: reset window at 93 % of L)."""
        L = self.L
        t_off = t_off if t_off is not None else L * .93
        return self.loop([(0, "opacity:0"), (t_on, "opacity:0"), (t_on + fade, "opacity:1"),
                          (t_off, "opacity:1"), (min(t_off + fade, L), "opacity:0"), (L, "opacity:0")], ease)

    def windows(self, wins, fade=.3, ease="settle"):
        """Visible only inside the given [(t0, t1)] windows (sorted, non-overlapping)."""
        L = self.L
        wins = sorted(wins)
        pts = {}
        pts[0.0] = 1 if wins and wins[0][0] <= .001 else 0
        for a, b in wins:
            if a > .001:
                pts[a] = 0
                pts[min(a + fade, L)] = 1
            if b < L - .001:
                pts[b] = 1
                pts[min(b + fade, L)] = 0
        pts[float(L)] = 1 if wins and wins[-1][1] >= L - .001 else 0
        return self.loop([(t, f"opacity:{o}") for t, o in sorted(pts.items())], ease)

    def complement(self, wins):
        L, out, t = self.L, [], 0.0
        for a, b in sorted(wins):
            if a > t + .001:
                out.append((t, a))
            t = max(t, b)
        if t < L - .001:
            out.append((t, float(L)))
        return out

    def once(self, frm, to, dur, delay, ease="settle"):
        """One-shot intro: the un-animated style is the end state (to)."""
        name = self.frames([(0, frm), (dur, to)], dur)
        e = EASE.get(ease, ease)
        return f"{to};animation:{name} {dur}s {e} {delay:.3f}s 1 both"

    def css(self):
        return "".join(self.k)


def smil(attr, values, key_times, L, spline=None):
    kt = ";".join(f"{x:.4f}" for x in key_times)
    sp = ""
    if spline:
        sp = f' calcMode="spline" keySplines="{";".join([spline] * (len(key_times) - 1))}"'
    return (f'<animate attributeName="{attr}" dur="{L}s" repeatCount="indefinite" values="{values}" '
            f'keyTimes="{kt}"{sp}/>')
