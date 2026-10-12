#!/usr/bin/env python3
"""Static checks for the built course. Prints one line per failure, then "verify: PASS" or "verify: FAIL n".

Usage: python3 _tools/verify.py [--queries-optional]
--queries-optional turns a search query with no hit into a warning. Use it only while some modules are not built yet.
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote

TOOLS = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
from content.common import PRACTICE_DIR, PRACTICE_FILES  # noqa: E402

QUERIES = ["split pane", "<C-w>v", "fzf --preview", "git worktree add"]
NEGATIVE = [r"pglite", r"sql-console", r"sqc-", r"SQL_GLOSSARY", r"Northgate", r"course-quest-premium", r"_vendor",
            r"(?i)nothing to type", r"(?i)claude|anthropic|codex|openai|generated with|co-authored"]
EXTERNAL = r"(src|href)\s*=\s*[\"']https?:|url\(\s*[\"']?https?:|@import"
INDEX_REL = os.path.join("_shared", "search-index.js")
MAX_RESULTS = 40
KIND_WEIGHT = {"c": 30, "k": 30, "h": 20, "p": 15, "t": 0}
PHRASE_BONUS, START_BONUS, SAME_FILE_BONUS = 100, 50, 5
TEXT_LEN_CAP, TEXT_LEN_DIVISOR = 200, 50


def norm(s):
    """Port of site.js norm: vim and tmux spellings of one key meet."""
    s = str(s).lower()
    s = re.sub(r"<c-([^>]+)>", r" ctrl-\1 ", s)
    s = s.replace("<leader>", "<space>")
    s = re.sub(r"\bctrl\+", "ctrl-", s)
    return re.sub(r"\s+", " ", s).strip()


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links = [], []
        self.lessons = {}          # lesson id -> [expect texts of its tw-cmd figures]
        self.boxes = []            # copy-button count per tw-codebox
        self._lesson = None
        self._box = None
        self._cmd = False
        self._expect = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if a.get("id"):
            self.ids.append(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        if tag == "section" and "lesson" in cls:
            self._lesson = a.get("id")
            self.lessons[self._lesson] = []
        if tag == "figure" and "tw-codebox" in cls:
            self._box = 0
            self._cmd = "tw-cmd" in cls
        if tag == "button" and "tw-copy" in cls and self._box is not None:
            self._box += 1
        if tag == "p" and "tw-expect" in cls and self._cmd and self._lesson:
            self._expect = []

    def handle_endtag(self, tag):
        if tag == "p" and self._expect is not None:
            text = re.sub(r"\s+", " ", "".join(self._expect)).strip()
            label = "You should see"
            body = text[len(label):].strip() if text.startswith(label) else text
            self.lessons[self._lesson].append(body)
            self._expect = None
        if tag == "figure" and self._box is not None:
            self.boxes.append(self._box)
            self._box, self._cmd = None, False

    def handle_data(self, data):
        if self._expect is not None:
            self._expect.append(data)


def parse(path):
    p = Page()
    with open(path, encoding="utf-8") as f:
        p.feed(f.read())
    return p


def load_index():
    path = os.path.join(COURSE, INDEX_REL)
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    return json.loads(raw[len("window.TW_SEARCH = "):].rstrip().rstrip(";"))


def run_query(data, q, here=""):
    q = norm(q)
    tokens = q.split(" ")
    hits = []
    for i, it in enumerate(data["items"]):
        hay = norm(it[4] + " " + it[5])
        if not all(t in hay for t in tokens):
            continue
        score = KIND_WEIGHT.get(it[0], 0)
        if q in hay:
            score += PHRASE_BONUS
        if norm(it[5]).startswith(q):
            score += START_BONUS
        if data["files"][it[1]] == here:
            score += SAME_FILE_BONUS
        score -= min(len(it[5]), TEXT_LEN_CAP) / TEXT_LEN_DIVISOR
        hits.append((-score, i))
    hits.sort()
    return [data["items"][i] for _s, i in hits[:MAX_RESULTS]]


def scan_files():
    for path in glob.glob(os.path.join(COURSE, "**", "*"), recursive=True):
        rel = os.path.relpath(path, COURSE)
        if not os.path.isfile(path) or "__pycache__" in rel or rel.endswith((".woff2", ".pyc")):
            continue
        if os.path.basename(path).startswith("LICENSE-") or rel == os.path.join("_tools", "verify.py"):
            continue
        yield path, rel


def main():
    optional = "--queries-optional" in sys.argv[1:]
    fails = []
    htmls = sorted(glob.glob(os.path.join(COURSE, "**", "*.html"), recursive=True))
    pages = {p: parse(p) for p in htmls}

    for path, pg in pages.items():
        rel = os.path.relpath(path, COURSE)
        for lesson, expects in pg.lessons.items():
            if not any(expects):
                fails.append(f"{rel}#{lesson}: no .tw-cmd with a non-empty .tw-expect")
        for n, count in enumerate(pg.boxes, 1):
            if count != 1:
                fails.append(f"{rel}: codebox {n} has {count} .tw-copy buttons")
        dup = sorted({i for i in pg.ids if pg.ids.count(i) > 1})
        if dup:
            fails.append(f"{rel}: repeated ids {dup[:5]}")
        for link in pg.links:
            if re.match(r"^(https?:|mailto:|data:|javascript:)", link):
                continue
            target, _, frag = link.partition("#")
            target = unquote(target.split("?")[0])
            dest = os.path.normpath(os.path.join(os.path.dirname(path), target)) if target else path
            if not os.path.exists(dest):
                fails.append(f"{rel}: broken link {link}")
            elif frag and dest.endswith(".html"):
                other = pages.get(dest) or parse(dest)
                if unquote(frag) not in other.ids:
                    fails.append(f"{rel}: missing anchor {link}")

    index_path = os.path.join(COURSE, INDEX_REL)
    if not os.path.exists(index_path):
        fails.append("missing _shared/search-index.js")
    else:
        data = load_index()
        for it in data["items"]:
            dest = os.path.join(COURSE, data["files"][it[1]])
            pg = pages.get(dest) or (parse(dest) if os.path.exists(dest) else None)
            if pg is None or it[3] not in pg.ids:
                fails.append(f"search anchor {data['files'][it[1]]}#{it[3]} not found")
        for q in QUERIES:
            hits = run_query(data, q)
            if hits:
                print(f"query {q!r}: {data['files'][hits[0][1]]}#{hits[0][3]}")
            elif optional:
                print(f"warning: query {q!r} has no hit yet")
            else:
                fails.append(f"query {q!r} has no hit")

    for path, rel in scan_files():
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        for pat in NEGATIVE:
            m = re.search(pat, text)
            if m:
                fails.append(f"{rel}: forbidden text {m.group(0)!r}")
        m = re.search(EXTERNAL, text)
        if m and not rel.startswith(os.path.join("_shared", "fonts")):
            fails.append(f"{rel}: external reference {m.group(0)!r}")

    for name, body in PRACTICE_FILES.items():
        path = os.path.join(COURSE, PRACTICE_DIR, name)
        if not os.path.exists(path):
            fails.append(f"{PRACTICE_DIR}/{name}: missing")
        elif open(path, "rb").read() != body.encode("utf-8"):
            fails.append(f"{PRACTICE_DIR}/{name}: differs from PRACTICE_FILES")

    for line in fails:
        print(line)
    print("verify: PASS" if not fails else f"verify: FAIL {len(fails)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
