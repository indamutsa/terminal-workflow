#!/usr/bin/env python3
"""Build the Terminal Workflow course: one self-contained HTML file per module, the course index and the search index.

Usage: python3 _tools/build.py [module numbers...]   (run from the course folder or anywhere)
With no numbers every module is built and the index and search index are rewritten.
With numbers only those module files are written; the index and search index are left alone.
Content lives in _tools/content/m*.py; shared CSS and JS in _shared/ are inlined into each file.
Only the fonts (_shared/fonts) and the search index stay as separate local files.
"""
import hashlib
import importlib
import json
import os
import re
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import kit  # noqa: E402
import search  # noqa: E402
from content.cheatsheet import CHEATSHEET  # noqa: E402
from content.common import MODULE_FILE, MODULE_META, PRACTICE_DIR, PRACTICE_FILES, PRACTICE_HOME, PRACTICE_MAX_LINES, SITE_GLOSSARY, module_href, module_path  # noqa: E402

SITE_NAME = "Terminal Workflow"
PAGES_MIN, PAGES_MAX, PRACTICE_COUNT = 2, 4, 4
CARDS_MIN, CARDS_MAX = 2, 4
# Split in two so verify.py's scan of this folder does not match the definition itself.
BANNED_PHRASES = ("nothing to " + "type",)
BLOCK_TYPES = ("cmd", "keys", "code", "text")
CHEAT_REL = "_shared/cheatsheet.js"
CHEAT_VERSION_LEN = 10
LINE_REF = re.compile(r"\bline (\d+)")


def cheat_version():
    """Content hash of the written cheat sheet data, or "" when it has not been built yet."""
    path = os.path.join(COURSE, CHEAT_REL)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:CHEAT_VERSION_LEN]


def write_cheat():
    sheets = [{"id": s["id"], "title": s["title"], "task_first": s.get("task_first", False),
               "rows": [list(r) for r in s["rows"]]} for s in CHEATSHEET]
    body = "window.TW_CHEAT = " + json.dumps(sheets, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";\n"
    path = os.path.join(COURSE, CHEAT_REL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"wrote {CHEAT_REL} ({sum(len(s['rows']) for s in sheets)} rows in {len(sheets)} sheets)")
    return cheat_version()


def write_practice():
    """Write the shared practice files byte for byte so a visitor can download them."""
    for name, body in PRACTICE_FILES.items():
        if len(body.splitlines()) > PRACTICE_MAX_LINES:
            raise SystemExit(f"{name}: more than {PRACTICE_MAX_LINES} lines")
    folder = os.path.join(COURSE, PRACTICE_DIR)
    os.makedirs(folder, exist_ok=True)
    for name, body in PRACTICE_FILES.items():
        with open(os.path.join(folder, name), "w", encoding="utf-8", newline="") as f:
            f.write(body)
    print(f"wrote {PRACTICE_DIR}/ ({len(PRACTICE_FILES)} files)")


def opened_practice_file(command):
    """The PRACTICE_FILES name a command opens, or None."""
    for token in str(command).split():
        name = token[len(PRACTICE_HOME) + 1:] if token.startswith(PRACTICE_HOME + "/") else token
        if name in PRACTICE_FILES:
            return name
    return None


def validate_worked(where, w):
    for key in ("open", "steps", "after"):
        if not w.get(key):
            raise SystemExit(f"{where}: worked needs {key}")
    name = opened_practice_file(w["open"])
    if not name:
        return
    text = PRACTICE_FILES[name]
    if w.get("before") and w["before"].rstrip("\n") not in text:
        raise SystemExit(f"{where}: worked before is not verbatim in {name}")
    count = len(text.splitlines())
    for cursor, _keys, _effect in w["steps"]:
        if not cursor:
            continue
        for ln in LINE_REF.findall(cursor[0] if isinstance(cursor, tuple) else cursor):
            if int(ln) > count:
                raise SystemExit(f"{where}: worked cursor names line {ln}, {name} has {count}")


def read(rel):
    with open(os.path.join(COURSE, rel), encoding="utf-8") as f:
        return f.read()


def load(n):
    name = f"content.m{n}"
    try:
        return importlib.import_module(name).MODULE
    except ModuleNotFoundError as error:
        if error.name == name:
            return None
        raise


def present():
    """The MODULE_META entries whose content file exists, in order."""
    return [m for m in (load(meta["n"]) for meta in MODULE_META) if m]


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _strings(v)
    elif isinstance(node, (list, tuple)):
        for v in node:
            yield from _strings(v)


def validate(mod):
    meta = MODULE_META[mod["n"] - 1]
    tag = f"m{mod['n']}"
    if mod["folder"] != meta["folder"] or mod["title"] != meta["title"]:
        raise SystemExit(f"{tag}: folder/title differ from MODULE_META")
    if not PAGES_MIN <= len(mod["pages"]) <= PAGES_MAX:
        raise SystemExit(f"{tag}: {len(mod['pages'])} pages, need {PAGES_MIN}-{PAGES_MAX}")
    for s in _strings(mod):
        for phrase in BANNED_PHRASES:
            if phrase in s.lower():
                raise SystemExit(f"{tag}: banned phrase {phrase!r} in {s[:60]!r}")
    for k, page in enumerate(mod["pages"], 1):
        where = f"{tag} p{k}"
        has_expect = False
        for d in page["drills"]:
            for b in d["blocks"]:
                kind = b.get("type")
                if kind not in BLOCK_TYPES:
                    raise SystemExit(f"{where}: unknown block type {kind!r}")
                if kind in ("cmd", "keys") and b.get("where") not in kit.WHERE:
                    raise SystemExit(f"{where}: bad where {b.get('where')!r}")
                if kind == "cmd":
                    if not str(b.get("expect", "")).strip():
                        raise SystemExit(f"{where}: cmd {b.get('title')!r} has no expect")
                    has_expect = True
                if kind == "keys":
                    rows = b.get("rows")
                    if not rows or any(not isinstance(r, tuple) or len(r) != 2 for r in rows):
                        raise SystemExit(f"{where}: keys {b.get('title')!r} needs non-empty (key, action) rows")
                    if b.get("try") and not str(b.get("expect", "")).strip():
                        raise SystemExit(f"{where}: keys {b.get('title')!r} has try but no expect")
        validate_worked(where, page["worked"])
        if not has_expect:
            raise SystemExit(f"{where}: no cmd block with an expect")
        if len(page["practice"]["qs"]) != PRACTICE_COUNT:
            raise SystemExit(f"{where}: practice needs exactly {PRACTICE_COUNT} questions")
        if not CARDS_MIN <= len(page["rules"]["cards"]) <= CARDS_MAX:
            raise SystemExit(f"{where}: rules need {CARDS_MIN}-{CARDS_MAX} cards")


def check_ids(mod, html):
    ids = re.findall(r'\bid="([^"]+)"', html)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit(f"m{mod['n']}: repeated ids {dup[:5]}")


def page_html(mod, i, page):
    n = i + 1
    parts = [
        f'<section class="lesson sq-page{" active" if i == 0 else ""}" id="{kit.anchor(n)}" data-module="{n}" role="tabpanel" '
        f'aria-labelledby="tab-{n}" aria-hidden="{"false" if i == 0 else "true"}">',
        kit.header(mod["title"], n, len(mod["pages"]), page["h1"], page["subtitle"]),
        kit.one_idea(*page["idea"]),
        f'<div class="block">{kit.practice_setup(kit.anchor(n, "setup"))}</div>' if i == 0 else "",
        kit.problem(n, page["problem"]),
        kit.drills(n, page["drills"]),
        kit.rules(n, page["rules"]),
        kit.worked(n, page["worked"]),
        kit.practice(n, page["practice"]),
        "</section>",
    ]
    return "".join(parts)


def glossary(mod):
    """The module's own terms, then each site word whose id and forms the module does not already use."""
    own = mod["glossary"]
    ids = {g[0] for g in own}
    forms = {f.lower() for g in own for f in g[2]}
    return own + [g for g in SITE_GLOSSARY if g[0] not in ids and not any(f.lower() in forms for f in g[2])]


def module_html(mod, prev, nxt, version, cheat, mods):
    css = read("_shared/course.css")
    js = read("_shared/course.js")
    site_js = read("_shared/site.js")
    gloss = json.dumps([{"id": g[0], "label": g[1], "forms": g[2], "definition": g[3]} for g in glossary(mod)], ensure_ascii=False)
    pages = "".join(page_html(mod, i, p) for i, p in enumerate(mod["pages"]))
    nav_prev = f'<a rel="prev" href="../{module_href(prev["folder"])}">← {kit.esc(prev["title"])}</a>' if prev else '<a href="../index.html">← Course map</a>'
    nav_next = f'<a rel="next" href="../{module_href(nxt["folder"])}">{kit.esc(nxt["title"])} →</a>' if nxt else '<a href="../index.html">Course map →</a>'
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>{kit.esc(mod["title"])} — {SITE_NAME}</title>
    <script>document.documentElement.classList.add("js");</script>
    <style>
{css}
    </style>
  </head>
  <body class="has-side" data-root="../" data-file="{module_path(mod["folder"])}">
    {kit.topbar("../")}
    {kit.sidebar(mods, mod["n"], "../")}
    {kit.search_dialog()}
    {kit.cheat_drawer()}
    <div class="tw-page">
    <main id="lessonRoot">
{pages}
    </main>
    <nav class="tabbar" aria-label="Page navigation">
      <div class="tabbar-inner">
        <button id="prevBtn" class="nav-arrow" type="button" aria-label="Previous page">‹</button>
        <div id="tabs" class="tabs sq-tabs" role="tablist" aria-label="Pages"></div>
        <button id="nextBtn" class="nav-arrow" type="button" aria-label="Next page">›</button>
        <span id="progressMini" class="progress-mini" aria-live="polite">1/{len(mod["pages"])}</span>
      </div>
    </nav>
    <nav class="group-nav" aria-label="Course modules">
      {nav_prev}
      {nav_next}
    </nav>
    <footer>
      <strong>Module {mod["n"]} · {kit.esc(mod["title"])}</strong><br />{kit.esc(mod["footer"])}
    </footer>
    </div>
    <script>window.TW_GLOSSARY = {gloss};</script>
    <script src="../_shared/search-index.js?v={version}"></script>
    <script src="../_shared/cheatsheet.js?v={cheat}"></script>
    <script>
{js}
    </script>
    <script>
{site_js}
    </script>
  </body>
</html>
"""
    check_ids(mod, html)
    return html


def write_module(mod, prev, nxt, version, cheat, mods):
    folder = os.path.join(COURSE, mod["folder"])
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, MODULE_FILE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(module_html(mod, prev, nxt, version, cheat, mods))
    print(f"wrote {os.path.relpath(path, COURSE)} ({len(mod['pages'])} pages)")


def main():
    only = set(sys.argv[1:])
    mods = present()
    chosen = [m for m in mods if not only or str(m["n"]) in only]
    for m in chosen:
        validate(m)
    version = search.version(COURSE) if only else search.write(COURSE, mods)
    cheat = cheat_version() if only else write_cheat()
    if not only:
        write_practice()
    for k, mod in enumerate(mods):
        if mod not in chosen:
            continue
        write_module(mod, mods[k - 1] if k > 0 else None, mods[k + 1] if k + 1 < len(mods) else None, version, cheat, mods)
    if only:
        print("partial build: index and search index not rebuilt")
        return
    import index
    index.write(COURSE, mods, version, cheat)


if __name__ == "__main__":
    main()
