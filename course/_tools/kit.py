"""Building blocks for the Terminal Workflow course pages.

A page is plain data (see content/m*.py). This module turns that data into markup the
shared CSS and JS drive: copyable command boxes with a stated result, key tables and the search dialog.
"""
from html import escape as _esc

WHERE = {"shell": "Shell", "tmux": "tmux", "nvim": "Neovim", "lazygit": "LazyGit", "fzf": "fzf"}


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


def codebox(aid, kind, label, title, code, expect=None):
    """kind "cmd" shows a result line; kind "code" is a file or script with no result."""
    tail = ""
    if kind == "cmd":
        tail = f'<p class="tw-expect"><span class="tw-expect-label">You should see</span> {_rich(expect)}</p>'
    return (f'<figure class="tw-codebox tw-{kind}" id="{aid}">{_head(label, title)}'
            f'<pre class="sq-code"><code>{esc(code)}</code></pre>{tail}</figure>')


def cmd(aid, b):
    return codebox(aid, "cmd", WHERE[b["where"]], b["title"], b["code"], b["expect"])


def code(aid, b):
    return codebox(aid, "code", b["file"], b["title"], b["code"])


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


def worked(page_n, w):
    """w: h2, frame, given, steps [..], code (optional), meaning"""
    box = codebox(anchor(page_n, "worked", "code"), "code", "Example", w["h2"], w["code"]) if w.get("code") else ""
    steps = "".join(f"<li>{_rich(s)}</li>" for s in w["steps"])
    return (f'<section class="block" id="{anchor(page_n, "worked")}"><div class="section-label">Worked application</div><h2>{esc(w["h2"])}</h2>'
            f'<div class="word-problem"><span class="tag">The setup</span><p class="kitchen-frame">{_rich(w["frame"])}</p>'
            f'<p>{_rich(w["given"])}</p>{box}<ol class="worked-steps">{steps}</ol>'
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


def search_ui():
    return (
        '<button class="tw-search-btn" type="button" aria-haspopup="dialog" aria-controls="tw-search">Search <kbd>/</kbd></button>'
        '<div class="tw-search" id="tw-search" role="dialog" aria-modal="true" aria-label="Search the course" hidden><div class="tw-search-panel">'
        '<input id="tw-q" class="tw-q" type="search" role="combobox" aria-expanded="false" aria-controls="tw-results" '
        'aria-autocomplete="list" autocomplete="off" spellcheck="false" placeholder="Search commands, keys and pages" />'
        '<ul id="tw-results" class="tw-results" role="listbox" aria-label="Results"></ul>'
        '<p class="tw-search-foot">↑↓ move · Enter open · Esc close</p></div></div>'
    )
