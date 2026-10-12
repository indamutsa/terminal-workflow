#!/usr/bin/env python3
"""Check that every command and key in the lessons appears in the built course.

Usage: python3 _tools/coverage.py [--lesson NAME ...] [--list]
A needle is one command, key or code span taken from a lesson (rules below). It must appear in the built HTML.
Lines a page rewrites on purpose go in that module's MODULE["coverage_allow"] with a reason.
Prints "coverage: N needles, M missing" and exits 1 when M > 0.
"""
import glob
import html as htmllib
import os
import re
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

LESSONS_DIR = os.path.join(os.path.dirname(COURSE), "practice", "lessons")
LESSON_FILES = ["01 tmux.md", "02 Neovim Essentials.md", "03 Neovim Power Editing.md", "04 Git Worktree.md",
                "05 Agent Worktree Workflow.md", "06 Neovim LSP & Git.md", "07 Neovim Expert.md", "fzf.md",
                "neovim-tmux-iterm-guide.md"]
BULLET_KEY_FILES = {"fzf.md"}
BOX_DRAWING = re.compile(r"[─-╿]")
LABEL_LINE = re.compile(r"^[A-Z][A-Z ]+:$")
FENCE = re.compile(r"^\s*```(\w*)\s*$")
CODE_SPAN = re.compile(r"`([^`]+)`")
CELL_SPLIT = re.compile(r"(?<!\\)\|")
DEEP_INDENT = 8
MIN_SPAN = 2


def norm(s):
    """Fold key spellings together: Ctrl+X and <C-x> become Ctrl-x, <leader> becomes <Space>, whitespace collapses."""
    s = re.sub(r"<C-([^>]+)>", lambda m: "Ctrl-" + m.group(1), s)
    s = re.sub(r"Ctrl[-+](.)", lambda m: "Ctrl-" + m.group(1).lower(), s)
    s = s.replace("<leader>", "<Space>")
    return re.sub(r"\s+", " ", s).strip()


def needles(md_text, name):
    """[(line number, needle)] for one lesson file."""
    out = []
    lines = md_text.split("\n")
    in_fence, lang = False, ""
    for no, raw in enumerate(lines, 1):
        m = FENCE.match(raw)
        if m:
            in_fence = not in_fence
            lang = m.group(1) if in_fence else ""
            continue
        if in_fence:
            s = raw.strip()
            if not s or s.startswith("#") or BOX_DRAWING.search(raw) or LABEL_LINE.match(s):
                continue
            if not lang and len(raw) - len(raw.lstrip(" ")) >= DEEP_INDENT:
                continue
            first = re.split(r"\s{2,}", s, maxsplit=1)[0]
            if first:
                out.append((no, first))
            continue
        if raw.lstrip().startswith("|"):
            cells = [c.strip() for c in CELL_SPLIT.split(raw.strip().strip("|"))]
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c) or no < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[no] if no < len(lines) else ""):
                continue
            for span in CODE_SPAN.findall(raw):
                span = span.replace("\\|", "|")
                if len(span) >= MIN_SPAN:
                    out.append((no, span))
            continue
        if name in BULLET_KEY_FILES and re.match(r"^\s*[-*] ", raw):
            out.extend((no, s) for s in CODE_SPAN.findall(raw))
    return out


def haystack():
    parts = []
    for path in sorted(glob.glob(os.path.join(COURSE, "**", "*.html"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            text = re.sub(r"<[^>]+>", " ", f.read())
        parts.append(htmllib.unescape(text))
    return norm(" ".join(parts))


def allowed():
    import build
    out = []
    for mod in build.present():
        out.extend(mod.get("coverage_allow", []))
    return [norm(n) for n, _reason in out]


def main():
    args = sys.argv[1:]
    chosen = [args[i + 1] for i, a in enumerate(args) if a == "--lesson" and i + 1 < len(args)]
    names = chosen or LESSON_FILES
    unknown = [n for n in names if n not in LESSON_FILES]
    if unknown:
        raise SystemExit(f"unknown lesson {unknown[0]!r}")
    hay = haystack()
    allow = allowed()
    total, missing = 0, []
    for name in names:
        with open(os.path.join(LESSONS_DIR, name), encoding="utf-8") as f:
            found = needles(f.read(), name)
        for no, needle in found:
            total += 1
            n = norm(needle)
            if n not in hay and n not in allow:
                missing.append(f"{name}:{no}  {needle}")
    if "--list" in args:
        print(f"allowlist entries: {len(allow)}")
    for line in missing:
        print(line)
    print(f"coverage: {total} needles, {len(missing)} missing")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
