"""Validate assets and README.   python scripts/validate.py [--rebuild]"""
import glob
import hashlib
import os
import re
import subprocess
import sys
import xml.dom.minidom as minidom

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from world.tokens import PALETTES, contrast  # noqa: E402

ALLOWED = {"https://chronicle.hypertos.in", "https://hypertos.in", "https://www.linkedin.com/in/chaitanaya052006",
           "https://leetcode.com/u/Chaitanaya_25/", "mailto:Chaitanyasrivastava63@gmail.com"}
BANNED = ["capsule-render", "readme-typing", "github-readme-stats", "streak", "shields.io", "trophy", "visitor",
          "lakm", "salon,", "👋", "passionate", "galgotias", "2024", "2028", "third-year", "third year", "b.tech"]
FACT_NUMBERS = set("""0 1 2 3 4 5 8 11 12 16 19 20 24 25 28 29 30 38 40 50 81 95 100 144 200 1,112 1,818 2026
3.027 3.459 3.865 3.12 3.8 4.1 481.5 2.8 99.19 87,000 052006 63 6 7 180 215 6v2 L6""".split())
errors = []


def err(msg):
    errors.append(msg)
    print("  FAIL", msg)


def check_svgs():
    print("SVG checks")
    tot = {"day": 0, "dusk": 0}
    for f in sorted(glob.glob(os.path.join(ROOT, "assets", "*.svg"))):
        name = os.path.basename(f)
        s = open(f, encoding="utf-8").read()
        size = len(s.encode())
        theme = "dusk" if "-dusk" in name else "day"
        tot[theme] += size
        try:
            minidom.parseString(s)
        except Exception as e:  # noqa: BLE001
            err(f"{name}: not well-formed XML ({e})")
            continue
        for bad in ("<script", "<foreignObject", "@import", "@font-face", "<image", "data:"):
            if bad in s:
                err(f"{name}: contains {bad}")
        for h in re.findall(r'href="([^"]+)"', s):
            if not h.startswith("#"):
                err(f"{name}: external href {h[:50]}")
        for u in re.findall(r"url\((?!#)([^)]+)\)", s):
            err(f"{name}: external url() {u[:50]}")
        if size > 140 * 1024:
            err(f"{name}: {size / 1024:.1f} KB > 140 KB")
        if "prefers-reduced-motion" not in s:
            err(f"{name}: no reduced-motion rule")
        ids = re.findall(r'\sid="([^"]+)"', s)
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            err(f"{name}: duplicate ids {sorted(dup)[:5]}")
        refs = set(re.findall(r"url\(#([^)]+)\)", s)) | {h[1:] for h in re.findall(r'href="(#[^"]+)"', s)}
        miss = refs - set(ids)
        if miss:
            err(f"{name}: unresolved refs {sorted(miss)[:5]}")
        print(f"  ok {name:30s} {size / 1024:7.1f} KB")
    for th, v in tot.items():
        print(f"  total {th}: {v / 1024:.0f} KB")
        if v > 1.6 * 1024 * 1024:
            err(f"total {th} over 1.6 MB")


def check_contrast():
    print("Contrast")
    for name, p in PALETTES.items():
        for fg, bgk in (("ink", "bg"), ("ink", "board"), ("ink", "sand"), ("ink", "cloud")):
            if name == "dusk" and bgk == "sand":
                continue
            r = contrast(p[fg], p[bgk])
            print(f"  {name}: {fg} on {bgk} {r:.1f}")
            if r < 4.5:
                err(f"{name}: {fg} on {bgk} {r:.2f} < 4.5")


def check_readme():
    print("README checks")
    r = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    links = set(re.findall(r'href="([^"]+)"', r)) | set(re.findall(r"\]\((https?://[^)]+|mailto:[^)]+)\)", r))
    if links - ALLOWED:
        err(f"disallowed links {links - ALLOWED}")
    print("  links:", sorted(links))
    srcs = {re.sub("#.*", "", x) for x in re.findall(r'(?:src|srcset)="([^"]+)"', r)}
    for s in srcs:
        if not os.path.exists(os.path.join(ROOT, s)):
            err(f"missing image {s}")
    disk = {os.path.relpath(f, ROOT).replace("\\", "/") for f in glob.glob(os.path.join(ROOT, "assets", "*"))}
    if disk - srcs:
        err(f"unreferenced assets: {sorted(disk - srcs)}")
    if re.search(r"<img(?![^>]*alt=)", r):
        err("<img> without alt")
    per_theme = len([x for x in re.findall(r'<img src="([^"]+)"', r) if "-day" not in x])
    print(f"  images per theme: {per_theme} (<= 24)")
    if per_theme > 24:
        err("too many images")
    alltext = r
    for f in glob.glob(os.path.join(ROOT, "assets", "*.svg")):
        alltext += " ".join(re.findall(r"<(?:title|desc)[^>]*>([^<]*)<", open(f, encoding="utf-8").read()))
    for b in BANNED:
        if b.lower() in alltext.lower():
            err(f"banned term {b!r}")
    vis = re.sub(r'(src|srcset|href|width|height)="[^"]+"|\]\([^)]+\)', "", alltext)
    nums = {n.rstrip(",") for n in re.findall(r"(?<![\w.#])\d[\d,]*(?:\.\d+)?", vis)}
    odd = sorted(n for n in nums if n not in FACT_NUMBERS)
    print("  numbers:", sorted(nums))
    if odd:
        err(f"numbers not in the facts list: {odd}")
    for st in ("LIVE", "IN PROGRESS", "PLANNED"):
        if st not in r:
            err(f"status {st} missing")


def check_determinism():
    print("Determinism")
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "assets", "*.svg")) if "activity" not in f)
    before = {f: hashlib.sha256(open(f, "rb").read()).hexdigest() for f in files}
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_assets.py")], check=True, capture_output=True)
    diff = [os.path.basename(f) for f in files if hashlib.sha256(open(f, "rb").read()).hexdigest() != before[f]]
    if diff:
        err(f"rebuild changed: {diff}")
    else:
        print(f"  {len(files)} files byte-identical after rebuild")


if __name__ == "__main__":
    check_svgs()
    check_contrast()
    check_readme()
    if "--rebuild" in sys.argv:
        check_determinism()
    print("RESULT:", "PASS" if not errors else f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)
