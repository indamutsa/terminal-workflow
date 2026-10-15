"""Building blocks for the Terminal Workflow course pages.

A page is plain data (see content/m*.py). This module turns that data into markup the
shared CSS and JS drive: copyable command boxes with a stated result, key tables and the search dialog.
"""
from html import escape as _esc

from content.common import MODULE_META, PRACTICE_DIR, PRACTICE_FILES, PRACTICE_HOME, SITE_URL, module_href
from highlight import highlight

WHERE = {"shell": "Shell", "tmux": "tmux", "nvim": "Neovim", "lazygit": "LazyGit", "fzf": "fzf"}

# Highlighter language per command box (its "where") and per file label; anything unlisted stays plain.
CMD_LANG = {"shell": "shell", "tmux": "shell", "fzf": "shell", "lazygit": "shell", "nvim": "vim"}
CODE_LANG_SUFFIX = {".py": "python", ".lua": "lua", ".plist": "xml", ".sh": "shell", ".zshrc": "shell", ".bashrc": "shell"}
CODE_LANG_CONTAINS = {"tmux": "shell"}


def esc(text):
    return _esc(str(text), quote=True)


def anchor(page_n, *parts):
    """anchor(2) == "module-2"; anchor(2, "d1", "b3") == "module-2-d1-b3"."""
    return "-".join(["module", str(page_n), *map(str, parts)])


def _rich(text):
    """Escape, then turn `code` spans into <code>. A backslash-backtick is a literal backtick (vim marks)."""
    parts = str(text).replace("\\`", "\x00").split("`")
    out = "".join(esc(p) if i % 2 == 0 else f"<code>{esc(p)}</code>" for i, p in enumerate(parts))
    return out.replace("\x00", "`")


def _table(head, rows):
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    tb = "".join("<tr>" + "".join(f"<td>{_rich(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table>"


def header(mod_title, n, total, h1, subtitle):
    return (f'<header class="lesson-header"><div class="eyebrow">{esc(mod_title)} · Page {n} of {total}</div>'
            f'<h1>{esc(h1)}</h1><p class="subtitle">{esc(subtitle)}</p><div class="rule"></div></header>')


def one_idea(lead, links, defs=None):
    lis = "".join(f'<li><strong>{esc(a)} <span class="kl-nowrap">→ {esc(b)}.</span></strong> {esc(c)}</li>' for a, b, c in links)
    d = f'<div class="term-definition"><strong>Definitions before use:</strong> {_rich(defs)}</div>' if defs else ""
    return (f'<div class="block"><div class="one-idea"><span class="tag">The one idea</span><p>{esc(lead)}</p>'
            f'<ul class="kitchen-links">{lis}</ul>{d}</div></div>')


def problem(page_n, p):
    return (f'<div class="block" id="{anchor(page_n, "problem")}"><div class="word-problem"><span class="tag">The problem</span>'
            f'<p>{_rich(p["fail"])}</p><div class="result-box"><strong>The fix:</strong> {_rich(p["fix"])}</div></div></div>')


def copy_button(title):
    return f'<button class="tw-copy" type="button" aria-label="Copy: {esc(title)}">Copy</button>'


def _head(label, title):
    return (f'<figcaption class="tw-code-head"><span class="tw-where">{esc(label)}</span>'
            f'<span class="tw-code-title">{esc(title)}</span>{copy_button(title)}</figcaption>')


def code_lang(label):
    """Highlighter language for a file label such as "~/.zshrc"; None when the label says nothing."""
    for suffix, lang in CODE_LANG_SUFFIX.items():
        if label.endswith(suffix):
            return lang
    return next((lang for word, lang in CODE_LANG_CONTAINS.items() if word in label), None)


def codebox(aid, kind, label, title, code, expect=None, lang=None):
    """kind "cmd" shows a result line; kind "code" is a file or script with no result. lang picks the colours."""
    tail = ""
    if kind == "cmd" and expect:
        tail = f'<p class="tw-expect"><span class="tw-expect-label">You should see</span> {_rich(expect)}</p>'
    return (f'<figure class="tw-codebox tw-{kind}" id="{aid}">{_head(label, title)}'
            f'<pre class="sq-code"><code>{highlight(code, lang)}</code></pre>{tail}</figure>')


def cmd(aid, b):
    return codebox(aid, "cmd", WHERE[b["where"]], b["title"], b["code"], b["expect"], CMD_LANG[b["where"]])


def code(aid, b):
    return codebox(aid, "code", b["file"], b["title"], b["code"], lang=code_lang(b["file"]))


def keys(aid, b):
    rows = "".join(f'<tr><td><kbd class="tw-key">{esc(k)}</kbd></td><td>{_rich(a)}</td></tr>' for k, a in b["rows"])
    src = esc("\n".join(f"{k}  {a}" for k, a in b["rows"]))
    tail = ""
    if b.get("try"):
        tail += f'<p class="tw-try"><span class="tw-expect-label">Try it</span> {_rich(b["try"])}</p>'
    if b.get("expect"):
        tail += f'<p class="tw-expect"><span class="tw-expect-label">You should see</span> {_rich(b["expect"])}</p>'
    return (f'<figure class="tw-codebox tw-keys" id="{aid}">{_head(WHERE[b["where"]], b["title"])}'
            f'<div class="tw-scroll"><table class="tw-keytable"><tbody>{rows}</tbody></table></div>'
            f'<pre class="tw-copy-src" hidden><code>{src}</code></pre>{tail}</figure>')


def text(b):
    return f'<p class="tw-text">{_rich(b["body"])}</p>'


def block(aid, b):
    kind = b["type"]
    if kind == "text":
        return text(b)
    return {"cmd": cmd, "keys": keys, "code": code}[kind](aid, b)


def drills(page_n, ds):
    out = []
    for k, d in enumerate(ds, 1):
        blocks = "".join(block(anchor(page_n, f"d{k}", f"b{j}"), b) for j, b in enumerate(d["blocks"], 1))
        out.append(f'<section class="block" id="{anchor(page_n, f"d{k}")}"><div class="section-label">Type it</div>'
                   f'<h2>{esc(d["h2"])}</h2><p class="section-intro">{_rich(d["intro"])}</p>{blocks}</section>')
    return "".join(out)


def rules(page_n, r):
    """r: h2, cards [(title, intro, head, rows) or (title, intro, None, code)]"""
    out = [f'<section class="block"><div class="section-label">Rules and review depth</div><h2>{esc(r["h2"])}</h2>']
    for i, (title, intro, head, rows) in enumerate(r["cards"], 1):
        body = f'<p class="section-intro">{_rich(intro)}</p>'
        if head is None:
            body += codebox(anchor(page_n, f"r{i}", "code"), "code", "Example", title, rows)
        else:
            body += _table(head, rows)
        op = " open" if i == 1 else ""
        out.append(f'<details class="rule-card" id="{anchor(page_n, f"r{i}")}" name="rules-{page_n}"{op}><summary>'
                   f'<span><span class="num">{i:02d}</span>{esc(title)}</span><span class="chevron"></span></summary>'
                   f'<div class="rule-body">{body}</div></details>')
    out.append("</section>")
    return "".join(out)


def practice_setup(aid):
    """One command that downloads the shared practice files into PRACTICE_HOME."""
    urls = " -O ".join(f"{SITE_URL}/{PRACTICE_DIR}/{name}" for name in PRACTICE_FILES)
    code = f"mkdir -p {PRACTICE_HOME} && cd {PRACTICE_HOME} && curl -fsSO {urls}"
    expect = f"`ls` shows {', '.join(PRACTICE_FILES)}."
    return codebox(aid, "cmd", WHERE["shell"], "Get the practice files", code, expect, CMD_LANG["shell"])


def _step(cursor, keys, effect):
    parts = []
    if cursor:
        where, how = cursor if isinstance(cursor, tuple) else (cursor, "")
        via = f" ({_rich(how)})" if how else ""
        parts.append(f'<span><em>Cursor:</em> {_rich(where)}{via}</span>')
    parts.append(f'<span><em>Keys:</em> {_rich(keys)}</span>')
    parts.append(f'<span>{_rich(effect)}</span>')
    return "<li>" + " · ".join(parts) + "</li>"


def _pane(label, text):
    return f'<div class="ws-pane"><span class="ws-label">{label}</span><pre class="sq-code"><code>{esc(text)}</code></pre></div>'


def worked(page_n, w):
    """w: h2, frame, open, steps [(cursor_or_None, keys, effect)], before (optional), after, meaning"""
    where = w.get("where", "shell")
    box = codebox(anchor(page_n, "worked", "open"), "cmd", WHERE[where], "Open it", w["open"], lang=CMD_LANG[where])
    steps = "".join(_step(*s) for s in w["steps"])
    panes = (_pane("Before", w["before"]) if w.get("before") else "") + _pane("After" if w.get("before") else "You see", w["after"])
    one = "" if w.get("before") else " ws-one"
    return (f'<section class="block" id="{anchor(page_n, "worked")}"><div class="section-label">Worked application</div><h2>{esc(w["h2"])}</h2>'
            f'<div class="word-problem"><span class="tag">The setup</span><p class="kitchen-frame">{_rich(w["frame"])}</p>'
            f'{box}<ol class="worked-steps ws-steps">{steps}</ol><div class="ws-pair{one}">{panes}</div>'
            f'<div class="result-box"><strong>Why it matters:</strong> {_rich(w["meaning"])}</div></div></section>')


def practice(page_n, p):
    """p: h2, qs [(kind, question, hint, steps, final)]"""
    out = [f'<section class="block" id="{anchor(page_n, "practice")}"><div class="section-label">Your turn</div><h2>{esc(p["h2"])}</h2>']
    for i, (kind, q, hint, steps, final) in enumerate(p["qs"], 1):
        st = "".join(f"<li>{_rich(s)}</li>" for s in steps)
        out.append(f'<div class="practice-card" id="{anchor(page_n, f"q{i}")}"><span class="q-kind">{esc(kind)}</span><span class="q-num">Q{i}</span>'
                   f'<p class="q-text">{_rich(q)}</p><details class="hint"><summary>hint</summary><p>{_rich(hint)}</p></details>'
                   f'<details class="solution"><summary>step-by-step solution</summary><div class="solution-body">'
                   f'<ol class="solution-steps">{st}</ol><div class="solution-final"><strong>Final answer:</strong> {_rich(final)}</div>'
                   f'</div></details></div>')
    out.append("</section>")
    return "".join(out)


def search_button():
    return ('<button class="tw-search-btn" type="button" data-tw-search aria-haspopup="dialog" aria-controls="tw-search">'
            'Search <kbd>/</kbd></button>')


def search_dialog():
    return (
        '<div class="tw-search" id="tw-search" role="dialog" aria-modal="true" aria-label="Search the course" hidden><div class="tw-search-panel">'
        '<input id="tw-q" class="tw-q" type="search" role="combobox" aria-expanded="false" aria-controls="tw-results" '
        'aria-autocomplete="list" autocomplete="off" spellcheck="false" placeholder="Search commands, keys and pages" />'
        '<ul id="tw-results" class="tw-results" role="listbox" aria-label="Results"></ul>'
        '<p class="tw-search-foot">↑↓ move · Enter open · Esc close</p></div></div>'
    )


def cheat_button():
    return (
        '<button class="tw-cheat-btn" type="button" aria-controls="tw-cheat" aria-expanded="false">'
        '<span class="tw-cheat-long">Cheat sheet</span><span class="tw-cheat-short">Cheats</span> <kbd>?</kbd></button>'
    )


def cheat_drawer():
    return (
        '<aside id="tw-cheat" class="tw-cheat" hidden aria-label="Cheat sheet">'
        '<header class="tw-cheat-head"><h2 class="tw-cheat-title">Cheat sheet</h2>'
        '<button class="tw-cheat-close" type="button" aria-label="Close cheat sheet">×</button></header>'
        '<input id="tw-cheat-q" class="tw-q" type="search" autocomplete="off" spellcheck="false" aria-label="Filter the cheat sheet" placeholder="Filter keys and actions" />'
        '<div id="tw-cheat-tabs" class="tw-cheat-tabs" role="group" aria-label="Sheets"></div>'
        '<div id="tw-cheat-body" class="tw-cheat-body"></div></aside>'
    )


HOME_ICON = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
             '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/><path d="M10 19.5v-5h4v5"/></svg>')
MENU_ICON = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>')


def topbar(root, home=False):
    """Sticky bar on every page: Home, Menu (opens the course menu), then Search and Cheat sheet.

    root is the path from this page up to the site root ("" on the home page, "../" in a module).
    """
    current = ' aria-current="page"' if home else ""
    return (
        f'<header class="tw-topbar"><div class="tw-topbar-in">'
        f'<a class="tw-home" href="{root or "./"}" aria-label="Terminal Workflow home"{current}>{HOME_ICON}<span>Terminal Workflow</span></a>'
        f'<button class="tw-menu-btn" type="button" aria-controls="tw-side" aria-expanded="false" aria-label="Menu">'
        f'{MENU_ICON}<span class="tw-menu-label">Menu</span></button>'
        f'<div class="tw-topbar-end">{search_button()}{cheat_button()}</div>'
        f'</div></header>'
    )


def sidebar(mods, current=None, root=""):
    """The course menu: every group, its modules and their pages, built from MODULE_META and each module's pages.

    The current module is open and links its own pages with bare #module-N anchors (site.js marks the shown page).
    Groups sort by name, the same order as the course map.
    """
    meta = {m["n"]: m for m in MODULE_META}
    groups = {}
    for m in mods:
        groups.setdefault(meta[m["n"]]["group"], []).append(m)
    out = []
    for group in sorted(groups):
        items = []
        for m in groups[group]:
            here = m["n"] == current
            links = []
            for i, p in enumerate(m["pages"], 1):
                if here:
                    shown = ' aria-current="page"' if i == 1 else ""
                    links.append(f'<li><a href="#{anchor(i)}" data-page="{i}"{shown}>{esc(p["h1"])}</a></li>')
                else:
                    links.append(f'<li><a href="{root}{module_href(m["folder"])}#{anchor(i)}">{esc(p["h1"])}</a></li>')
            state = " open data-current" if here else ""
            items.append(
                f'<li><details class="tw-side-mod"{state}><summary><span class="tw-side-num">{m["n"]}</span>'
                f'<span class="tw-side-title">{esc(m["title"])}</span></summary>'
                f'<ol class="tw-side-pages">{"".join(links)}</ol></details></li>')
        out.append(f'<section class="tw-side-group"><h2>{esc(group)}</h2><ul>{"".join(items)}</ul></section>')
    return f'<nav class="tw-side" id="tw-side" aria-label="Course modules">{"".join(out)}</nav><div class="tw-backdrop" id="tw-backdrop"></div>'
