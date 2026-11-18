"""Contribution data: GraphQL fetch with sanity checks (never fabricates)."""
import json
import os
import subprocess
import urllib.request
from datetime import date

QUERY = ("query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{"
         "weeks{contributionDays{date contributionCount}}}}}}")


def fetch(login):
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req = urllib.request.Request("https://api.github.com/graphql",
                                     data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
                                     headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                                              "User-Agent": "profile-contributions"})
        data = json.load(urllib.request.urlopen(req, timeout=30))
    else:
        out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={login}"],
                             capture_output=True, text=True, check=True).stdout
        data = json.loads(out)
    if data.get("errors"):
        raise SystemExit(f"GraphQL error: {data['errors']}")
    try:
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    except (KeyError, TypeError):
        raise SystemExit(f"Unexpected response: {str(data)[:300]}")
    days = [(d["date"], int(d["contributionCount"])) for w in weeks for d in w["contributionDays"]]
    if not (50 <= len(weeks) <= 54) or not (350 <= len(days) <= 378):
        raise SystemExit(f"Odd calendar shape: {len(weeks)} weeks, {len(days)} days")
    if any(c < 0 for _, c in days) or [x for x, _ in days] != sorted(x for x, _ in days):
        raise SystemExit("Odd calendar data")
    return [[(d["date"], int(d["contributionCount"])) for d in w["contributionDays"]] for w in weeks]


def level_fn(weeks):
    counts = sorted(c for w in weeks for _, c in w if c > 0)
    if not counts:
        return lambda c: 0
    q = [counts[int(len(counts) * f)] for f in (.25, .5, .75)]
    return lambda c: 0 if c == 0 else 1 if c <= q[0] else 2 if c <= q[1] else 3 if c <= q[2] else 4


def weekday(ds):
    return (date.fromisoformat(ds).weekday() + 1) % 7   # Sunday = 0
