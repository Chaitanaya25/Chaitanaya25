"""Build every SVG in /assets from the isometric-world generator (scripts/world).

    python scripts/build_assets.py              # all plates, day + dusk
    python scripts/build_assets.py hero raft    # selected plates
    python scripts/build_assets.py activity     # contribution plates from the GitHub API (GITHUB_TOKEN or gh)

Deterministic: the same inputs give byte-identical files.
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

PLATES = ["hero", "chronicle", "inference", "raft", "assistant", "work", "footer"]
THEMES = ("day", "dusk")


def write(name, svg):
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"  {name:30s} {len(svg.encode()) / 1024:7.1f} KB")


def activity_main():
    from world import contributions
    from world.plates import activity
    weeks = contributions.fetch(os.environ.get("GH_LOGIN", "Chaitanaya25"))
    for th in THEMES:
        write(f"activity-{th}.svg", activity.build(th, weeks))


def main(argv):
    os.makedirs(ASSETS, exist_ok=True)
    if argv == ["activity"]:
        return activity_main()
    want = argv or PLATES + ["posts", "activity-placeholder"]
    for name in want:
        if name == "posts":
            posts = importlib.import_module("world.plates.posts")
            for th in THEMES:
                for k, svg in posts.build(th):
                    write(f"{k}-{th}.svg", svg)
        elif name == "activity-placeholder":
            act = importlib.import_module("world.plates.activity")
            for th in THEMES:
                path = os.path.join(ASSETS, f"activity-{th}.svg")
                if not os.path.exists(path):      # never overwrite the workflow's real output
                    write(f"activity-{th}.svg", act.build(th))
        else:
            mod = importlib.import_module(f"world.plates.{name}")
            for th in THEMES:
                write(f"{name}-{th}.svg", mod.build(th))


if __name__ == "__main__":
    main(sys.argv[1:])
