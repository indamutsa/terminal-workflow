#!/usr/bin/env python3
"""Measure how well the site search answers real questions: the intent bank (intent_bank.py).

Usage: python3 course/_tools/intent_check.py [--top 3] [--show-fails] [--gaps] [--min PCT]

Runs the real site.js search in Node against the built _shared/search-index.js and cheatsheet.js, like
search_check.py. Rebuild first (python3 course/_tools/build.py) after changing content or the search.
A query with a target is a hit when a matching block is in the first --top results. Queries whose target is
None are content gaps and are counted, not scored. The cheat sheet drawer has no ranking, so a cheat row
counts as a hit when it is among the first CHEAT_VISIBLE rows the drawer lists for the query.
Exit 0 always (a measurement), except: 1 when the hit rate is below --min, 2 when the bank names a block
that does not exist.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import intent_bank  # noqa: E402

COURSE = Path(__file__).resolve().parent.parent
DEFAULT_TOP = 3
CHEAT_VISIBLE = 10
SHOWN_RESULTS = 5
NODE_TIMEOUT = 120
CHEAT = "cheat"

NODE_RUNNER = r"""
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { course, items, shown, cheatVisible } = JSON.parse(fs.readFileSync(0, "utf8"));
const core = require(path.join(course, "_shared/site.js"));
const context = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(course, "_shared/search-index.js"), "utf8"), context);
vm.runInNewContext(fs.readFileSync(path.join(course, "_shared/cheatsheet.js"), "utf8"), context);
const data = context.window.TW_SEARCH;
const sheets = context.window.TW_CHEAT;
const engine = core.createSearch(data);
const modN = (it) => data.mods[it[1]].n;
const describe = (it) => `M${modN(it)} ${it[3]} [${it[0]}] ${it[4]} | ${it[5]}`;

// Index by (module, anchor): the texts of each block, so identical copies on other pages count too.
const blockTexts = new Map();
const blockTitle = new Map();
data.items.forEach((it) => {
  const key = modN(it) + "|" + it[3];
  if (!blockTexts.has(key)) { blockTexts.set(key, new Set()); blockTitle.set(key, it[4]); }
  blockTexts.get(key).add(it[5]);
});
const depth = (anchor) => anchor.split("-").length;

function mainHit(it, targets) {
  return targets.some(([n, anchor]) => {
    if (modN(it) === n && it[3] === anchor) return true;
    // the drill section that holds the block
    if (modN(it) === n && depth(it[3]) >= 3 && anchor.startsWith(it[3] + "-")) return true;
    const texts = blockTexts.get(n + "|" + anchor);
    return Boolean(texts && texts.has(it[5]));
  });
}

const out = items.map((item) => {
  const { query, kind, targets, sheet, key } = item;
  const result = { query, kind };
  if (kind === "cheat") {
    const sheetData = sheets.find((s) => s.id === sheet);
    const row = sheetData && sheetData.rows.find((r) => r[0] === key);
    if (!row) { result.bad = true; result.expected = `cheat ${sheet} ${key}`; return result; }
    result.expected = `cheat ${sheet} | ${key}  ${row[1]}`;
    const tokens = engine.query(core.norm(query));
    const found = [];
    sheets.forEach((s) => s.rows.forEach((r) => {
      if (tokens.length && engine.match(core.norm(r[0] + " " + r[1]), tokens)) found.push([s.id, r]);
    }));
    result.total = found.length;
    const at = found.findIndex(([id, r]) => id === sheet && r[0] === key);
    result.rank = at < 0 ? null : at + 1;
    result.visible = cheatVisible;
    result.returned = found.slice(0, shown).map(([id, r]) => `cheat ${id} | ${r[0]}  ${r[1]}`);
    return result;
  }
  const found = engine.search(query, "");
  result.total = found.total;
  result.returned = found.items.slice(0, shown).map(describe);
  if (kind === "gap") return result;
  const missing = targets.filter(([n, anchor]) => !blockTexts.has(n + "|" + anchor));
  if (missing.length) { result.bad = true; result.expected = JSON.stringify(missing); return result; }
  result.expected = targets.map(([n, anchor]) => `M${n} ${anchor} ${blockTitle.get(n + "|" + anchor)}`).join("  OR  ");
  const at = found.items.findIndex((it) => mainHit(it, targets));
  result.rank = at < 0 ? null : at + 1;
  return result;
});
process.stdout.write(JSON.stringify(out));
"""


def normalize(query, target):
    """Turn one bank entry into the plain record the Node runner reads."""
    if target is None:
        return {"query": query, "kind": "gap"}
    if target[0] == CHEAT:
        return {"query": query, "kind": "cheat", "sheet": target[1], "key": target[2]}
    options = target if isinstance(target, list) else [target]
    return {"query": query, "kind": "main", "targets": [list(option) for option in options]}


def run():
    request = {
        "course": str(COURSE),
        "items": [normalize(q, t) for q, t in intent_bank.INTENTS],
        "shown": SHOWN_RESULTS,
        "cheatVisible": CHEAT_VISIBLE,
    }
    done = subprocess.run(
        ["node", "-e", NODE_RUNNER], input=json.dumps(request), text=True,
        capture_output=True, check=True, timeout=NODE_TIMEOUT,
    )
    return json.loads(done.stdout)


def area_of(query):
    for name, group in intent_bank.AREAS.items():
        if any(q == query for q, _ in group):
            return name
    return "?"


def is_hit(result, top):
    limit = result["visible"] if result["kind"] == "cheat" else top
    return result["rank"] is not None and result["rank"] <= limit


def pct(part, whole):
    return 100.0 * part / whole if whole else 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--top", type=int, default=DEFAULT_TOP, help="hit if the block is in the first N results")
    parser.add_argument("--show-fails", action="store_true", help="list each failing query and what it returned")
    parser.add_argument("--gaps", action="store_true", help="list the content gaps and what they returned")
    parser.add_argument("--min", type=float, default=None, metavar="PCT", help="exit 1 when the hit rate is below PCT")
    args = parser.parse_args()

    try:
        results = run()
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"intent_check: FAIL: {type(error).__name__}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stderr, file=sys.stderr)
        return 2

    bad = [r for r in results if r.get("bad")]
    for r in bad:
        print(f"BAD TARGET {r['query']!r}: no such block {r['expected']}", file=sys.stderr)
    if bad:
        print(f"intent_check: {len(bad)} bank targets do not exist in the built index", file=sys.stderr)
        return 2

    scored = [r for r in results if r["kind"] != "gap"]
    gaps = [r for r in results if r["kind"] == "gap"]
    hits = [r for r in scored if is_hit(r, args.top)]
    first = [r for r in scored if r["rank"] == 1]
    gap_hits = [r for r in gaps if r["total"]]

    if args.show_fails:
        for r in scored:
            if is_hit(r, args.top):
                continue
            where = f"rank {r['rank']}" if r["rank"] else "not returned"
            print(f"FAIL {r['query']!r} ({area_of(r['query'])}, {where}, {r['total']} results)")
            print(f"  wanted: {r['expected']}")
            for line in r["returned"]:
                print(f"  got:    {line}")
    if args.gaps:
        for r in gaps:
            print(f"GAP {r['query']!r} ({r['total']} results)")
            for line in r["returned"][:3]:
                print(f"  got:    {line}")

    print("by area (top-%d): " % args.top + ", ".join(
        f"{name} {sum(1 for r in scored if area_of(r['query']) == name and is_hit(r, args.top))}"
        f"/{sum(1 for r in scored if area_of(r['query']) == name)}"
        for name in intent_bank.AREAS if any(area_of(r["query"]) == name for r in scored)))
    rate = pct(len(hits), len(scored))
    print(f"intent_check: top-{args.top} {len(hits)}/{len(scored)} ({rate:.1f}%), "
          f"top-1 {len(first)}/{len(scored)} ({pct(len(first), len(scored)):.1f}%), "
          f"{len(gaps)} gaps ({len(gap_hits)} of them still return unrelated results), "
          f"{len(results)} queries")
    if args.min is not None and rate < args.min:
        print(f"intent_check: below --min {args.min:g}%", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
