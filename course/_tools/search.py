"""The site-wide search index: _shared/search-index.js, built from the same module data as the pages."""
import hashlib
import json
import os
import re

from content.common import module_path
from kit import anchor

SNIPPET_MAX = 200
INDEX_REL = "_shared/search-index.js"
VERSION_LEN = 10
INDEX_VERSION = 1

# Overlapping groups expand one level only: save means commit or write, but write
# does not mean commit. Keep short navigation words out of unrelated groups.
SYNONYMS: list[list[str]] = [
    ["change", "switch", "move", "go", "jump", "navigate", "focus"],
    ["pane", "split"],
    ["window", "tab"],
    ["session", "workspace"],
    ["close", "kill", "delete", "remove", "quit", "exit"],
    ["create", "new", "add", "open", "make"],
    ["rename", "name"],
    ["find", "search", "grep", "look", "locate"],
    ["file", "files", "buffer"],
    ["copy", "yank"],
    ["paste", "put"],
    ["undo", "revert", "reset"],
    ["commit", "save"],
    ["write", "save"],
    ["resize", "size", "grow", "shrink"],
    ["zoom", "maximize", "fullscreen"],
    ["list", "show", "view", "see"],
    ["scroll", "page"],
    ["top", "start", "beginning"],
    ["bottom", "end"],
    ["up", "above", "previous", "prev", "back"],
    ["down", "below", "next", "forward"],
    ["select", "highlight", "mark", "visual"],
    ["replace", "substitute", "rename"],
    ["comment", "uncomment"],
    ["indent", "outdent", "unindent"],
    ["branch", "checkout"],
    ["stage", "add"],
    ["push", "upload"],
    ["pull", "fetch", "update"],
    ["diff", "changes", "compare"],
    ["history", "log"],
    ["terminal", "shell", "console"],
    ["reload", "refresh", "source"],
    ["help", "cheatsheet", "keys", "shortcut", "keymap"],
    ["process", "port", "pid"],
    ["line", "lines"],
    ["word", "words"],
    ["folder", "directory", "dir", "cd"],
    ["vertical", "vertically"],
    ["horizontal", "horizontally"],
    ["nvim", "neovim", "lazyvim"],
]


def clean(text, code=False, key_row=False):
    """Capped plain text; key rows retain the first two-space key/description separator."""
    s = str(text).replace("\\`", "\x00")
    if not code:
        s = s.replace("`", "")
    parts = re.split(r" {2,}", s.replace("\x00", "`"), maxsplit=1) if key_row else [s.replace("\x00", "`")]
    s = "  ".join(re.sub(r"\s+", " ", part).strip() for part in parts).strip()
    return s if len(s) <= SNIPPET_MAX else s[: SNIPPET_MAX - 1].rstrip() + "…"


def _lines(code):
    return [ln for ln in str(code).split("\n") if ln.strip()]


def entries(mods):
    out, seen = [], set()

    def add(kind, fi, n, aid, title, text, code=False):
        text = clean(text, code, key_row=kind == "k")
        if not text:
            return
        key = (fi, aid, text)
        if key in seen:
            return
        seen.add(key)
        out.append([kind, fi, n, aid, clean(title), text])

    for fi, mod in enumerate(mods):
        for n, page in enumerate(mod["pages"], 1):
            top = anchor(n)
            add("p", fi, n, top, page["h1"], page["subtitle"])
            lead, links, _defs = page["idea"]
            add("t", fi, n, top, page["h1"], lead)
            for plain, key, effect in links:
                add("t", fi, n, top, page["h1"], f"{plain} → {key}. {effect}")
            prob = page["problem"]
            pa = anchor(n, "problem")
            add("t", fi, n, pa, "The problem", prob["fail"])
            add("t", fi, n, pa, "The fix", prob["fix"])
            for k, d in enumerate(page["drills"], 1):
                da = anchor(n, f"d{k}")
                add("h", fi, n, da, d["h2"], d["intro"])
                for j, b in enumerate(d["blocks"], 1):
                    ba = anchor(n, f"d{k}", f"b{j}")
                    kind = b["type"]
                    if kind == "text":
                        add("t", fi, n, da, d["h2"], b["body"])
                    elif kind in ("cmd", "code"):
                        for ln in _lines(b["code"]):
                            add("c", fi, n, ba, b["title"], ln, code=True)
                        if kind == "cmd":
                            add("t", fi, n, ba, b["title"], b["expect"])
                    else:
                        for key, action in b["rows"]:
                            add("k", fi, n, ba, b["title"], f"{key}  {action}")
                        if b.get("try"):
                            add("t", fi, n, ba, b["title"], b["try"])
                        if b.get("expect"):
                            add("t", fi, n, ba, b["title"], b["expect"])
            for i, (title, intro, head, rows) in enumerate(page["rules"]["cards"], 1):
                ra = anchor(n, f"r{i}")
                add("h", fi, n, ra, title, intro)
                if head is None:
                    for ln in _lines(rows):
                        add("c", fi, n, ra, title, ln, code=True)
                else:
                    for row in rows:
                        first = str(row[0])
                        if first.startswith("`"):
                            add("k", fi, n, ra, title, "  ".join(row))
                        else:
                            add("t", fi, n, ra, title, " — ".join(row))
            w = page["worked"]
            wa = anchor(n, "worked")
            add("h", fi, n, wa, w["h2"], w["frame"])
            for ln in _lines(w["open"]):
                add("c", fi, n, wa, w["h2"], ln, code=True)
            for _cursor, keys, effect in w["steps"]:
                add("t", fi, n, wa, w["h2"], f"{keys} {effect}")
            add("t", fi, n, wa, w["h2"], w["meaning"])
            pr = page["practice"]
            add("h", fi, n, anchor(n, "practice"), pr["h2"], "Practice questions")
            for i, (kind, q, _hint, _steps, _final) in enumerate(pr["qs"], 1):
                add("t", fi, n, anchor(n, f"q{i}"), f"Q{i} · {kind}", q)
    return out


def payload(mods):
    return {
        "v": INDEX_VERSION,
        "syn": SYNONYMS,
        "files": [module_path(m["folder"]) for m in mods],
        "mods": [{"n": m["n"], "title": m["title"], "pages": [p["h1"] for p in m["pages"]]} for m in mods],
        "items": entries(mods),
    }


def write(course, mods):
    data_obj = payload(mods)
    body = "window.TW_SEARCH = " + json.dumps(data_obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";\n"
    data = body.encode("utf-8")
    path = os.path.join(course, INDEX_REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {INDEX_REL} ({len(data_obj['items'])} items, {len(data) / 1024:.0f} KB)")
    return hashlib.sha256(data).hexdigest()[:VERSION_LEN]


def version(course):
    path = os.path.join(course, INDEX_REL)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:VERSION_LEN]
