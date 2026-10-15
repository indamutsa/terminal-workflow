#!/usr/bin/env python3
"""Run the real site.js search in Node against built course content.

Usage: python3 course/_tools/search_check.py
Requires Node, uses only standard libraries, and leaves the build untouched.
"""
import json
from pathlib import Path
import subprocess
import sys

COURSE = Path(__file__).resolve().parent.parent
TOP_RESULTS = 3
BROAD_HITS = 30

# Expectations are verbatim snippets from content/m*.py, not invented answers.
QUERIES = [
    ("change pane", "Change pane left"),
    ("close pane", "Close pane (prompts"),
    ("split pane vertically", "Split pane side by side"),
    ("zoom pane", "Zoom pane to full screen"),
    ("new window", "Ctrl-a c New window"),
    ("detach", "Ctrl-a d"),
    ("reload tmux config", "Reload tmux.conf"),
    ("copy mode", "Enter copy mode"),
    ("find file", "Find file by part of its name"),
    ("search text in project", "Search text in the project"),
    ("rename variable", "Rename a function or variable"),
    ("go to definition", "Go to definition"),
    ("comment line", "gcc"),
    ("move selected lines", "move all the selected lines"),
    ("multi cursor", "Multi-cursor without multi-cursor"),
    ("replace word everywhere", "Replace word everywhere"),
    ("undo", {"key": "u", "description": "Undo"}),
    ("save file", ":w Save"),
    ("quit nvim", "Quit entirely"),
    ("open terminal", "Open terminal in"),
    ("file explorer", "File explorer"),
    ("kill port", "Kill whatever holds a port"),
    ("kill process", "Kill a process by name"),
    ("switch branch", "Switch to another git branch"),
    ("copy file path", "Copy a file's path"),
    ("command line history", "q: Open the command-line window"),
    ("command history", "Search your command history"),
    ("stage file", "Stage file: stage or unstage the highlighted file"),
    ("commit", {"key": "c", "description": "Commit the staged files"}),
    ("push", {"key": "P", "description": "Push commits to the remote"}),
    ("stash", {"key": "s", "description": "Stash all changes (in the files panel)"}),
    ("view diff", ":DiffviewOpen"),
    ("open lazygit", "Open LazyGit"),
    ("new worktree", "Create a worktree for a new feature"),
    ("remove worktree", "git worktree remove"),
    ("list worktrees", "git worktree list"),
    ("resize pane", "Resize pane"),
    ("next buffer", "Next buffer"),
    ("close buffer", ":bd Close buffer"),
    ("pull", {"key": "p", "description": "Pull commits from the remote"}),
    ("copy line", "Copy a line"),
    ("switching panes", "Change pane left"),
    ("fullscreen pane", "Zoom pane to full screen"),
    ("refresh tmux config", "Reload tmux.conf"),
    ("yank file path", "Copy a file's path"),
    ("toggle comment line", "Toggle comment on current line"),
    ("rename session", "Rename session"),
    ("undo last commit", "Undo last commit"),
    ("kill other panes", "Kill other panes"),
    ("accept suggestion", "Accept suggestion"),
    ("new line in shell", "New line in shell"),
    ("stash changes", "Stash changes"),
    ("amend commit", "Amend commit"),
    ("copy file content", "Copy file content"),
    ("delete file", "Delete files you pick"),
    ("folder size", "Folder size"),
    ("list files", "List files"),
    ("nested tmux", "Nested tmux"),
    ("find big files", {"module": 9, "snippet": "Find files bigger than 100 MB"}),
    ("locate large files", {"module": 9, "snippet": "Find files bigger than 100 MB"}),
    ("look for hidden files", {"module": 9, "snippet": "Find hidden files"}),
    ("search ignoring case", {"module": 9, "snippet": "Search for a word ignoring upper and lower case"}),
    ("count lines", {"module": 9, "snippet": "Count lines"}),
    ("how many lines", {"module": 9, "snippet": "Count lines"}),
    ("print a column", {"module": 9, "snippet": "Get selected columns from a log or CSV file"}),
    ("top ips in log", {"module": 9, "snippet": "Find the 5 IP addresses with the most requests in a log"}),
    ("replace text in file", {"module": 9, "snippet": "Replace"}),
    ("read json field", {"module": 9, "snippet": "Get names from JSON with or without quotes"}),
    ("run on every file", {"module": 9, "snippet": "Run a command on every file"}),
    ("loop over files", {"module": 10, "snippet": "Loop over every .txt file"}),
    ("read script arguments", {"module": 10, "snippet": "Read the arguments"}),
    ("script flags", {"module": 10, "snippet": "Read a script's flags with getopts"}),
    ("argument default", {"module": 10, "snippet": "Give an argument a default value"}),
    ("read file line by line", {"module": 10, "snippet": "Read a file line by line"}),
    ("test file exists", {"module": 10, "snippet": "Test if a file or folder exists"}),
    ("count array values", {"module": 11, "snippet": "Create an array, add an element and count or slice its values"}),
    ("replace every match in string", {"module": 11, "snippet": "Count characters, slice text and replace one or every match"}),
    ("save error output", {"module": 11, "snippet": "Save stderr"}),
    ("trace script", {"module": 11, "snippet": "Trace a whole script with bash -x"}),
]

MISSING_CONTENT = []

NODE_RUNNER = r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { course, queries, missing, top } = JSON.parse(fs.readFileSync(0, "utf8"));
const core = require(path.join(course, "_shared/site.js"));
const context = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(course, "_shared/search-index.js"), "utf8"), context);
vm.runInNewContext(fs.readFileSync(path.join(course, "_shared/cheatsheet.js"), "utf8"), context);
const data = context.window.TW_SEARCH;
const engine = core.createSearch(data);
const matches = (q, text) => engine.match(core.norm(text), engine.query(q));
let checks = 0;
function check(value, label) { assert.ok(value, label); checks++; }
check(matches("change pane", "Switch panes"), "synonyms and plurals");
check(!matches("change pane", "Switch windows"), "AND across tokens");
check(matches("switching panes", "Switch pane"), "query stemming and synonym lookup");
check(matches("copied", "copied"), "original tokens remain available");
check(matches("renamed", "name"), "stemmed synonym lookup");
check(matches("saved", "write"), "save overlaps write");
check(matches("save", "commit"), "save overlaps commit");
check(!matches("write", "commit"), "overlap is not transitive");
check(matches("stage", "add"), "overlap includes stage/add");
check(!matches("stage", "open"), "stage does not expand through add/open");
check(matches("look for large files", "Find files bigger than 100 MB"), "multiword find phrase and size synonyms");
check(matches("how many lines", "Count lines"), "multiword count phrase");
check(!matches("look forest", "find trees"), "phrase matching keeps word boundaries");
check(matches("iterate over files", "Loop over every file"), "everyday loop words");
check(matches("script parameters", "Read script flags"), "argument synonyms");
check(!matches("left", "right"), "directions remain distinct");
check(!matches("right", "left"), "reverse directions remain distinct");
check(core.stem("sing") === "sing" && core.stem("up") === "up", "minimum stem length");
check(core.stem("ctrl-s") === "ctrl-s", "keys are not stemmed");
check(core.norm("<C-w>v") === core.norm("Ctrl+w v"), "key normalization");
check(matches("<C-w>v", "Ctrl-w v"), "key matching");
check(engine.search("  ").total === 0, "empty queries");
check(engine.search("how do i with this in the").total === 0, "stopword-only queries stay empty");
check(engine.query("why does my file break on spaces").map((token) => token.original).join(" ") === "file break spaces",
  "question scaffolding is ignored");
check(engine.query("not no every all").length === 4, "meaningful qualifiers remain searchable");
check(matches("stop process on port 49152", "Kill a process by port"), "literal numbers never exclude a match");
check(matches("find report.txt", "Find files"), "example filenames never exclude a match");
check(matches("files modified yesterday", "Find files with -mtime"), "time words find modification commands");
check(matches("files accessed recently", "Find files with -atime"), "time words find access commands");
check(matches("opened", "mdfind kMDItemLastUsedDate"), "access words find Spotlight dates");
check(matches("names spaces", "name space"), "plural nouns retain their final e");
const natural = core.createSearch({ syn: [], files: ["local"], items: [
  ["c", 0, 1, "partial", "Find files", "fd"],
  ["t", 0, 1, "full", "Find hidden files", "Show hidden files"],
  ["c", 0, 1, "number", "Find files", "fd 49152"],
] });
check(natural.search("find hidden files").items[0][3] === "full", "full coverage outranks partial actions");
check(natural.search("find unknown files").total > 0, "unknown words allow useful partial results");
check(natural.search("find files 49152").items[0][3] === "number", "matching literal arguments boost ranking");
check(natural.search("find files 59321").total > 0, "unmatched literal arguments allow results");
check(natural.match(core.norm("Find files"), natural.query("find unknown files"), true).variants.length > 0,
  "partial results provide safe highlight variants");
const fields = core.createSearch({ syn: [], files: ["local"], items: [
  ["c", 0, 1, "body", "Reference", "Detach session"],
  ["c", 0, 1, "title", "Detach session", "td"],
] });
check(fields.search("detach session").items[0][3] === "title", "task titles outrank body mentions");
const rarity = core.createSearch({ syn: [], files: ["local"], items: [
  ...Array.from({ length: 8 }, (_, i) => ["t", 0, 1, "common-" + i, "Reference", "common topic " + i]),
  ["t", 0, 1, "rare", "Reference", "zircon topic"],
] });
check(rarity.search("common zircon unknown").items[0][3] === "rare", "rare terms carry more weight in partial matches");
check(rarity.search("unlistedword").total === 0, "queries without any matching terms stay empty");
const synthetic = core.createSearch({ syn: data.syn, files: ["local"], items: [
  ["c", 0, 1, "syn", "Switch pane", "Switch pane"],
  ["t", 0, 1, "exact", "Change pane", "A change pane action with a longer description"],
] });
check(synthetic.search("change pane").items[0][3] === "exact", "literal match outranks synonym bonuses");
const ties = core.createSearch({ syn: [], files: ["local", "other"], items: [
  ["k", 0, 1, "first", "", "undo"], ["k", 1, 1, "second", "", "undo"],
] });
check(ties.search("undo").items[0][3] === "first", "stable index tie break");
check(ties.search("undo", "other").items[0][3] === "second", "same-file bonus");
check(ties.search("undo").items.length === 1 && ties.search("undo").total === 1,
  "identical rows from different pages collapse to one result");
const starts = core.createSearch({ syn: data.syn, files: ["local"], items: [
  ["k", 0, 1, "later", "", "x  An undo"],
  ["k", 0, 1, "synonym", "", "z  Reset undo"],
  ["k", 0, 1, "literal", "", "u  Undo the most recent change"],
] });
check(starts.search("undo").items.map((it) => it[3]).join(" ") === "literal synonym later",
  "literal description start outranks synonym start and later mentions");
check(starts.search("undo change").items[0][3] === "literal", "description starts support multiword queries");
const commandTitles = core.createSearch({ syn: data.syn, files: ["local"], items: [
  ["c", 0, 1, "command", "Undo and redo", "u"],
  ["k", 0, 1, "key", "", "u  Undo"],
] });
check(commandTitles.search("undo").items[0][3] === "key", "single-word command titles do not displace key actions");
const tasks = core.createSearch({ syn: data.syn, files: ["local"], items: [
  ["k", 0, 1, "key", "", "ff  Find file with a longer description"],
  ["c", 0, 1, "command", "Find file by name", "ff"],
] });
check(tasks.search("find file").items[0][3] === "command", "multiword command titles retain start credit");
const prose = core.createSearch({ syn: data.syn, files: ["local"], items: [
  ["t", 0, 1, "later", "", "x  Undo"],
  ["t", 0, 1, "start", "", "Undo a longer explanation"],
] });
check(prose.search("undo").items[0][3] === "start", "prose gets no description-start bonus");
const partial = core.createSearch({ syn: data.syn, files: ["local"], items: [
  ["k", 0, 1, "later", "", "x  An undo"],
  ["k", 0, 1, "partial", "", "z  Resettable undo"],
] });
check(partial.search("undo").items[0][3] === "later", "synonym starts require a whole first word");
const variants = matches("change pane", "Switch panes").variants;
check(variants.includes("switch") && variants.includes("pane"), "highlight matched variants");
// Run the browser's actual highlighter with a tiny text-only DOM.
global.document = { createElement: (tag) => ({ tag }), createTextNode: (text) => ({ text }) };
const pieces = [];
core.highlight({ append: (piece) => pieces.push(piece) }, "Switch panes", variants);
check(pieces.filter((piece) => piece.tag === "mark").map((piece) => piece.textContent).join(" ") === "Switch pane",
  "synonym highlights use text nodes");
for (const [query, text] of [["Ctrl-w v", "<C-w>v"], ["<leader>e", "<Space>e"], ["Ctrl+w", "Ctrl+w"]]) {
  const nodes = [];
  const found = matches(query, text);
  core.highlight({ append: (piece) => nodes.push(piece) }, text, found.variants);
  check(nodes.some((piece) => piece.tag === "mark"), "normalized key highlights: " + text);
}
delete global.document;
const cheatRows = context.window.TW_CHEAT.flatMap((sheet) => sheet.rows);
check(cheatRows.some((row) => row[1] === "Navigate panes" && matches("change pane", row.join(" "))),
  "cheat sheet uses the same matching rules");
check(cheatRows.some((row) => row[1] === "Reload tmux config" && matches("refresh tmux config", row.join(" "))),
  "cheat sheet synonym normalization");
for (const [query, key, description] of [
  ["undo", "u / Ctrl-r", "Undo, redo"],
  ["commit", "c (Files)", "Commit: type the message, then Enter"],
  ["push", "P", "Push to the remote"],
  ["stash", "s (Files)", "Stash changes: type a name, Enter"],
  ["pull", "p", "Pull from the remote"],
]) {
  check(cheatRows.some((row) => row[0] === key && row[1] === description && matches(query, row.join("  "))),
    "canonical cheat row matches: " + query);
}
const results = [...queries.map(([query, expected]) => {
  const result = engine.search(query, "", top);
  return { query, expected, total: result.total, ok: result.items.some((it) => {
    if (typeof expected === "string") return core.norm(it[4] + " " + it[5]).includes(core.norm(expected));
    if (expected.module) return data.files[it[1]].startsWith(`m${expected.module}-`) &&
      core.norm(it[4] + " " + it[5]).includes(core.norm(expected.snippet));
    const [key, description] = it[5].split(/ {2,}/, 2);
    return it[0] === "k" && key === expected.key && description && description.startsWith(expected.description);
  }),
    top: result.items.map((it) => it[4] + " | " + it[5]) };
}), ...missing.map((query) => ({ query, missing: true, total: engine.search(query).total }))];
process.stdout.write(JSON.stringify({ results, checks, synonyms: data.syn.length }));
"""


def main():
    request = {"course": str(COURSE), "queries": QUERIES, "missing": MISSING_CONTENT, "top": TOP_RESULTS}
    try:
        run = subprocess.run(
            ["node", "-e", NODE_RUNNER], input=json.dumps(request), text=True,
            capture_output=True, check=True, timeout=60,
        )
        report = json.loads(run.stdout)
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"search_check: FAIL: {type(error).__name__}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stderr, file=sys.stderr)
        return 1
    failures = [r for r in report["results"] if not r.get("missing") and not r["ok"]]
    for result in failures:
        print(f"FAIL {result['query']!r}: expected {result['expected']!r} in top {TOP_RESULTS}")
        for hit in result["top"]:
            print(f"  {hit}")
    print(f"MISSING_CONTENT ({len(MISSING_CONTENT)}):")
    for query in MISSING_CONTENT:
        print(f"  {query}")
    print(f"BROAD (more than {BROAD_HITS} hits, before result limit):")
    for result in report["results"]:
        if result["total"] > BROAD_HITS:
            print(f"  {result['query']}: {result['total']}")
    print(f"search_check: {len(QUERIES) - len(failures)} passed, {len(failures)} failed, "
          f"{len(MISSING_CONTENT)} missing; {report['checks']} core checks; "
          f"{report['synonyms']} synonym groups")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
