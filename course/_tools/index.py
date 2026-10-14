"""The course map: course/index.html. Lists every module and page, the learning path and the first command."""
import os

import kit

TIERS = {
    1: "Beginner", 2: "Beginner", 3: "Intermediate", 4: "Intermediate", 5: "Advanced", 6: "Advanced", 7: "Expert", 8: "Reference",
}

HERO_SUBTITLE = "tmux for sessions, Neovim for editing, git worktrees for parallel branches, and an AI coding agent working beside you."

# (when, module numbers, what you get) — the guide's learning path, mapped to this course's modules.
LEARNING_PATH = [
    ("Week 1", "Modules 1–2", "tmux windows, Neovim basics and the file finder. Enough to be productive."),
    ("Week 2", "Module 3", "Text objects, macros and registers. This is where Neovim gets fast."),
    ("Week 3", "Module 4", "Git worktrees and an AI coding agent. The three-window pattern becomes your default."),
    ("Week 4+", "Modules 5–7", "Code navigation, LazyGit, project search and expert motions. Speed, not essentials."),
    ("Any time", "Module 8", "Coming from VS Code? Look up each shortcut you know and press the Neovim key for it."),
]

START = {
    "where": "shell",
    "title": "Start your first session",
    "code": "tmux new -s main",
    "expect": "The tmux status bar appears at the bottom with `[main]` on the left.",
}

STYLE = """
.cm-hero{padding:56px 0 18px;text-align:center}
.cm-hero h1{margin:10px 0 8px}
.cm-how{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:28px}
.cm-how div{padding:14px;border:1px solid var(--line);border-radius:var(--r);background:var(--alt)}
.cm-how strong{display:block;color:var(--gold);font:600 12px var(--mono);letter-spacing:.08em;text-transform:uppercase}
.cm-how p{margin:6px 0 0;color:var(--dim);font-size:14px}
.cm-path{margin:0;padding:0;list-style:none}
.cm-path li{display:grid;grid-template-columns:150px 1fr;gap:4px 14px;padding:10px 0;border-top:1px solid var(--soft)}
.cm-path li:first-child{border-top:0}
.cm-path strong{color:var(--gold);font:600 12px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.cm-path span{color:var(--dim)}
.cm-grid{display:grid;gap:14px;margin-top:18px}
.cm-card{padding:18px 20px;border:1px solid var(--line);border-radius:var(--r);background:var(--raised);color:var(--chalk);transition:border-color .18s,transform .18s}
.cm-card:hover,.cm-card:focus-within{border-color:var(--gold);transform:translateY(-2px)}
.cm-card h3{margin:4px 0 2px;font-size:24px}
.cm-card h3 a{color:var(--chalk);text-decoration:none}
.cm-card p{margin:0 0 8px;color:var(--dim)}
.cm-card ol{margin:0;padding-left:20px;font-size:14px}
.cm-card ol a{color:var(--chalk);text-decoration-color:var(--line)}
.cm-card ol a:hover{color:var(--gold)}
.cm-num{color:var(--blue);font:600 12px var(--mono);letter-spacing:.08em;text-transform:uppercase}
.cm-open{display:inline-block;margin-top:10px;color:var(--gold);font:600 12px var(--mono);text-decoration:none}
@media (max-width:650px){.cm-how{grid-template-columns:1fr}.cm-path li{grid-template-columns:1fr}}
"""


def write(course, mods, version, cheat):
    css = open(os.path.join(course, "_shared", "course.css"), encoding="utf-8").read().replace("../_shared/fonts/", "_shared/fonts/")
    site_js = open(os.path.join(course, "_shared", "site.js"), encoding="utf-8").read()
    cards = []
    for m in mods:
        href = f'{m["folder"]}/{m["folder"]}.html'
        pages = "".join(f'<li><a href="{href}#module-{i}">{kit.esc(p["h1"])}</a></li>' for i, p in enumerate(m["pages"], 1))
        cards.append(
            f'<article class="cm-card"><span class="cm-num">Module {m["n"]} · {TIERS[m["n"]]}</span>'
            f'<h3><a href="{href}">{kit.esc(m["title"])}</a></h3><p>{kit.esc(m["tagline"])}</p><ol>{pages}</ol>'
            f'<a class="cm-open" href="{href}">{len(m["pages"])} pages · open →</a></article>')
    path = "".join(f"<li><strong>{kit.esc(w)} · {kit.esc(mn)}</strong><span>{kit.esc(t)}</span></li>" for w, mn, t in LEARNING_PATH)
    total = sum(len(m["pages"]) for m in mods)
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="description" content="A hands-on course that turns the terminal into a full IDE: tmux, Neovim and git worktrees" />
    <title>Terminal Workflow — Course Map</title>
    <style>
{css}
{STYLE}
    </style>
  </head>
  <body data-root="" data-file="index.html">
    {kit.search_ui()}
    {kit.cheat_ui()}
    <main>
      <header class="cm-hero">
        <div class="eyebrow">Course map · {len(mods)} modules · {total} pages</div>
        <h1>The terminal as your whole IDE</h1>
        <p class="subtitle">{kit.esc(HERO_SUBTITLE)}</p>
        <div class="rule"></div>
      </header>
      <section class="cm-how">
        <div><strong>Problem first</strong><p>Each page opens with what goes wrong, then the fix.</p></div>
        <div><strong>Type it</strong><p>Every command has a copy button and the result you should see.</p></div>
        <div><strong>Find any key</strong><p>Press / to search every module.</p></div>
      </section>
      <section class="block">
        <div class="section-label">Start here</div>
        <h2>One command to begin</h2>
        <p class="section-intro">You need iTerm2, Neovim 0.12+ and an AI coding agent CLI. Open a terminal and type this.</p>
        {kit.cmd("start", START)}
        {kit.practice_setup("setup")}
      </section>
      <section class="block">
        <div class="section-label">Learning path</div>
        <h2>Four weeks, in order</h2>
        <ul class="cm-path">{path}</ul>
      </section>
      <section class="block">
        <div class="section-label">Modules</div>
        <h2>{len(mods)} modules</h2>
        <div class="cm-grid">{"".join(cards)}</div>
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
