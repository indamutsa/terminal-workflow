"""The course map: course/index.html. Lists every module and page, the learning path and the first command."""
import os

import kit
from content.common import MODULE_META, module_href

TIERS = {
    1: "Beginner", 2: "Beginner", 3: "Intermediate", 4: "Intermediate", 5: "Advanced", 6: "Advanced", 7: "Expert", 8: "Reference",
    9: "Beginner → Advanced", 10: "Beginner", 11: "Expert",
}

HERO_SUBTITLE = "Find files, shape text, automate Bash, and work faster in tmux & Neovim."

# (stage, module numbers, outcome) — one route through both parts of the toolkit.
LEARNING_PATH = [
    ("Shell basics", (10,), "Variables, decisions, loops and script input."),
    ("Everyday tasks", (9,), "Find files, search logs and turn text into answers."),
    ("Your workspace", (1, 2, 3), "Keep sessions running and edit without reaching for the mouse."),
    ("Automation", (11, 4), "Build reliable scripts and work across parallel branches."),
    ("Expert workflow", (5, 6, 7), "Navigate code, tune your tools and make every edit count."),
]

GROUP_INTROS = {
    "Linux & Bash": "Find it. Transform it. Automate it.",
    "tmux & Neovim": "A lasting workspace. An editor that keeps up.",
}

START = {
    "where": "shell",
    "title": "Start your first session",
    "code": "tmux new -s main",
    "expect": "The tmux status bar appears at the bottom with `[main]` on the left.",
}

def write(course, mods, version, cheat):
    css = open(os.path.join(course, "_shared", "course.css"), encoding="utf-8").read().replace("../_shared/fonts/", "_shared/fonts/")
    site_js = open(os.path.join(course, "_shared", "site.js"), encoding="utf-8").read()
    metadata = {m["n"]: m for m in MODULE_META}
    by_number = {m["n"]: m for m in mods}
    groups = {}
    for m in mods:
        href = module_href(m["folder"])
        pages = "".join(f'<li><a href="{href}#module-{i}">{kit.esc(p["h1"])}</a></li>' for i, p in enumerate(m["pages"], 1))
        group = metadata[m["n"]]["group"]
        groups.setdefault(group, []).append(
            f'<article class="cm-card"><span class="cm-num">Module {m["n"]} · {TIERS[m["n"]]}</span>'
            f'<h3><a href="{href}">{kit.esc(m["title"])}</a></h3><p>{kit.esc(m["tagline"])}</p><ol>{pages}</ol>'
            f'<a class="cm-open" href="{href}">{len(m["pages"])} pages · open →</a></article>')
    sections = []
    jumps = []
    for group, cards in sorted(groups.items()):
        group_id = "group-" + group.lower().replace(" & ", "-").replace(" ", "-")
        jumps.append(f'<a href="#{group_id}">{kit.esc(group)}</a>')
        sections.append(
            f'<section class="cm-group" id="{group_id}" aria-labelledby="{group_id}-title">'
            f'<div class="cm-group-head"><div><h2 id="{group_id}-title">{kit.esc(group)}</h2>'
            f'<p>{kit.esc(GROUP_INTROS.get(group, ""))}</p></div><span>{len(cards)} modules</span></div>'
            f'<div class="cm-grid">{"".join(cards)}</div></section>')
    path = []
    for stage, numbers, outcome in LEARNING_PATH:
        links = " · ".join(
            f'<a href="{module_href(by_number[n]["folder"])}">Module {n}</a>'
            for n in numbers if n in by_number)
        if links:
            path.append(f'<li><strong>{kit.esc(stage)}</strong><div>{links}<p>{kit.esc(outcome)}</p></div></li>')
    total = sum(len(m["pages"]) for m in mods)
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="description" content="Become a Linux power user. Find files, transform text, automate Bash, and work faster with tmux and Neovim. Search any task for commands and examples." />
    <title>Terminal Workflow — Course Map</title>
    <script>document.documentElement.classList.add("js");</script>
    <style>
{css}
    </style>
  </head>
  <body class="course-map" data-root="" data-file="index.html">
    {kit.topbar("", home=True)}
    {kit.sidebar(mods)}
    {kit.search_dialog()}
    {kit.cheat_drawer()}
    <main>
      <header class="cm-hero">
        <div class="eyebrow">{len(mods)} modules · {total} pages</div>
        <h1>Become a Linux power user.</h1>
        <p class="subtitle">{kit.esc(HERO_SUBTITLE)}</p>
        <button class="cm-search" type="button" data-tw-search aria-haspopup="dialog" aria-controls="tw-search">Search a task or command <kbd>/</kbd></button>
        <p class="cm-search-hint">Try “find big files”, “loop over files”, or “script flags”.</p>
        <nav class="cm-jumps" aria-label="Browse the toolkit">{"".join(jumps)}<a href="#learning-path">Learning path</a></nav>
      </header>
      {"".join(sections)}
      <section class="cm-learning" id="learning-path" aria-labelledby="path-title">
        <div><h2 id="path-title">From basics to expert</h2><p class="section-intro">Follow the path once. Come back for any command.</p></div>
        <div><ol class="cm-path">{"".join(path)}</ol>
        <p class="cm-reference">Coming from VS Code? <a href="{module_href(by_number[8]['folder'])}">Keep module 8 beside you.</a></p></div>
      </section>
      <section class="cm-start" aria-labelledby="start-title">
        <h2 id="start-title">Make it hands-on</h2>
        <p class="section-intro">Start Bash lessons with <code>bash</code>. For tmux lessons, start a session below.</p>
        {kit.cmd("start", START)}
        {kit.practice_setup("setup")}
      </section>
    </main>
    <footer><strong>Terminal Workflow</strong><br />Press / on any page to search every command and key.</footer>
    <script src="_shared/search-index.js?v={version}"></script>
    <script src="_shared/cheatsheet.js?v={cheat}"></script>
    <script>
{site_js}
    </script>
  </body>
</html>
"""
    with open(os.path.join(course, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote index.html")
