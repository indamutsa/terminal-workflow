"""Build-time syntax colours for code blocks: small regex tokenizers, no JS and no dependencies.

highlight(code, lang) returns HTML-escaped code with <span class="hl-X"> tokens. Every tokenizer
emits each input character exactly once, and highlight() checks that stripping the tags gives the
original text back, so a bad tokenizer fails the build instead of changing what a visitor copies.
"""
import html
import re

CLS_COMMENT, CLS_STRING, CLS_KEYWORD, CLS_FLAG, CLS_NUMBER = "c", "s", "k", "f", "n"
CLS_CMD, CLS_VAR, CLS_FN, CLS_EX = "cmd", "v", "fn", "ex"


def _esc(text):
    return html.escape(text, quote=True)


def _span(cls, text):
    return f'<span class="hl-{cls}">{_esc(text)}</span>' if text else ""


# ---- shell

SHELL_KEYWORDS = {"if", "then", "else", "elif", "fi", "for", "while", "do", "done", "case", "esac", "in", "function", "alias", "export", "source"}
# After these a new command starts; after the other keywords (alias, export, for, ...) the next word is an argument.
SHELL_CMD_AFTER = {"if", "then", "else", "elif", "while", "do"}
SHELL_ALIAS = re.compile(r"""(\s*)(alias)(\s+)([\w.-]+)(=)(['"])""")
SHELL_VAR = re.compile(r"\$(?:\{[^}]*\}|\(|[A-Za-z_]\w*|[#?$!@*0-9-])")
SHELL_SINGLE = re.compile(r"'[^']*'?")
SHELL_DOUBLE = re.compile(r'"(?:\\.|[^"\\])*"?')
SHELL_QUOTES = {"'": SHELL_SINGLE, '"': SHELL_DOUBLE}
SHELL_SEP = re.compile(r"\|\|?|&&|;")
SHELL_WORD = re.compile(r"[\w./~:@%+=,*?\[\]!^-]+")
SHELL_FLAG = re.compile(r"--?[A-Za-z][\w-]*")
SHELL_NUMBER = re.compile(r"[+-]?\d+(?:\.\d+)?")
SHELL_ASSIGN = re.compile(r"\w+=")


def _shell_line(line, cmd_pos=True):
    out, i, n = [], 0, len(line)
    m = SHELL_ALIAS.match(line)
    if m and cmd_pos:
        quote = m.group(6)
        close = line.find(quote, m.end())
        inner_end = n if close < 0 else close
        out += [_esc(m.group(1)), _span(CLS_KEYWORD, m.group(2)), _esc(m.group(3)), _esc(m.group(4)), _esc(m.group(5)),
                _span(CLS_STRING, quote), _shell_line(line[m.end():inner_end]),
                _span(CLS_STRING, line[inner_end:inner_end + 1]), _esc(line[inner_end + 1:])]
        return "".join(out)
    while i < n:
        ch = line[i]
        if ch.isspace():
            j = i
            while j < n and line[j].isspace():
                j += 1
            out.append(_esc(line[i:j]))
            i = j
            continue
        if ch == "#" and (i == 0 or line[i - 1].isspace()):
            out.append(_span(CLS_COMMENT, line[i:]))
            break
        m = SHELL_VAR.match(line, i)
        if m:
            out.append(_span(CLS_VAR, m.group()))
            cmd_pos = m.group().endswith("(")
            i = m.end()
            continue
        m = SHELL_QUOTES[ch].match(line, i) if ch in SHELL_QUOTES else None
        if m:
            out.append(_span(CLS_STRING, m.group()))
            cmd_pos = False
            i = m.end()
            continue
        if ch == "\\" and i + 1 < n:
            out.append(_esc(line[i:i + 2]))
            i += 2
            continue
        m = SHELL_SEP.match(line, i)
        if m:
            out.append(_esc(m.group()))
            cmd_pos = True
            i = m.end()
            continue
        m = SHELL_WORD.match(line, i)
        if not m:
            out.append(_esc(ch))
            cmd_pos = cmd_pos and ch in "({"
            i += 1
            continue
        word = m.group()
        i = m.end()
        if word in SHELL_KEYWORDS:
            out.append(_span(CLS_KEYWORD, word))
            cmd_pos = word in SHELL_CMD_AFTER
        elif SHELL_ASSIGN.match(word):
            out.append(_esc(word))
        elif cmd_pos:
            out.append(_span(CLS_CMD, word))
            cmd_pos = False
        elif SHELL_FLAG.fullmatch(word):
            out.append(_span(CLS_FLAG, word))
        elif SHELL_NUMBER.fullmatch(word):
            out.append(_span(CLS_NUMBER, word))
        else:
            out.append(_esc(word))
    return "".join(out)


def _shell(code):
    return "\n".join(_shell_line(line) for line in code.split("\n"))


# ---- python and lua share one master regex each: strings and comments first so keywords never match inside them

PY_KEYWORDS = ("and as assert async await break class continue def del elif else except False finally for from global if import in is "
               "lambda None nonlocal not or pass raise return True try while with yield").split()
PY_BUILTINS = ("print len range int str float list dict set tuple sum min max abs sorted enumerate zip map filter open input type "
               "isinstance super self bool round any all").split()
LUA_KEYWORDS = ("and break do else elseif end false for function goto if in local nil not or repeat return then true until while").split()
NUMBER = r"\b\d+(?:\.\d+)?\b"


def _word_alt(words):
    return r"\b(?:" + "|".join(words) + r")\b"


PY_TOKEN = re.compile(
    r"(?P<c>#[^\n]*)"
    r"|(?P<s>[rRbBfFuU]{0,2}(?:\"\"\"[\s\S]*?(?:\"\"\"|\Z)|'''[\s\S]*?(?:'''|\Z)|\"(?:\\.|[^\"\\\n])*\"?|'(?:\\.|[^'\\\n])*'?))"
    r"|(?P<def>\b(?:def|class)\b)(?P<sp>[ \t]+)(?P<fn>[A-Za-z_]\w*)"
    rf"|(?P<k>{_word_alt(PY_KEYWORDS)})"
    rf"|(?P<b>{_word_alt(PY_BUILTINS)})"
    rf"|(?P<n>{NUMBER})")

LUA_TOKEN = re.compile(
    r"(?P<c>--\[(?P<eq>=*)\[[\s\S]*?(?:\](?P=eq)\]|\Z)|--[^\n]*)"
    r"|(?P<s>\[(?P<eq2>=*)\[[\s\S]*?(?:\](?P=eq2)\]|\Z)|\"(?:\\.|[^\"\\\n])*\"?|'(?:\\.|[^'\\\n])*'?)"
    rf"|(?P<k>{_word_alt(LUA_KEYWORDS)})"
    rf"|(?P<n>{NUMBER})")


def _scan(pattern, code):
    out, last = [], 0
    for m in pattern.finditer(code):
        out.append(_esc(code[last:m.start()]))
        kind = m.lastgroup
        if m.groupdict().get("def"):
            out += [_span(CLS_KEYWORD, m.group("def")), _esc(m.group("sp")), _span(CLS_FN, m.group("fn"))]
        elif kind == "b":
            out.append(_span(CLS_KEYWORD, m.group()))
        else:
            out.append(_span({"c": CLS_COMMENT, "s": CLS_STRING, "k": CLS_KEYWORD, "n": CLS_NUMBER}[kind], m.group()))
        last = m.end()
    out.append(_esc(code[last:]))
    return "".join(out)


# ---- vim: Neovim blocks mix keystrokes (left plain) with ex commands (lines that start with ":")

VIM_EX = re.compile(r"(:(?:[%.$]|\d+|'[<>a-z]|[,;+-])*)(!|[A-Za-z]+)")
VIM_SUBSTITUTE = {"s", "substitute"}
VIM_GLOBAL = {"g", "global", "v", "vglobal"}
VIM_NOT_DELIMITER = set(' \t"|\\')


def _unescaped(text, ch, start):
    """Index of the next unescaped ch at or after start, or -1."""
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == ch:
            return i
        i += 1
    return -1


def _vim_line(line):
    if re.match(r'"(\s|$)', line):
        return _span(CLS_COMMENT, line)
    m = VIM_EX.match(line)
    if not m:
        return _esc(line)
    name, rest = m.group(2), line[m.end():]
    out = [_esc(m.group(1)), _span(CLS_EX, name)]
    parts = 2 if name in VIM_SUBSTITUTE else 1 if name in VIM_GLOBAL else 0
    if parts and rest and not rest[0].isalnum() and rest[0] not in VIM_NOT_DELIMITER:
        end = 0
        for _ in range(parts):
            end = _unescaped(rest, rest[0], end + 1)
            if end < 0:
                end = len(rest) - 1
                break
        out += [_span(CLS_STRING, rest[:end + 1]), _esc(rest[end + 1:])]
    else:
        out.append(_esc(rest))
    return "".join(out)


def _vim(code):
    return "\n".join(_vim_line(line) for line in code.split("\n"))


# ---- xml (plist)

XML_TOKEN = re.compile(r"(?P<c><!--[\s\S]*?(?:-->|\Z))|(?P<t><[^<>]*>?)")
XML_HEAD = re.compile(r"<[?!/]?[\w:.-]*")
XML_VALUE = re.compile(r"\"[^\"]*\"?|'[^']*'?")


def _xml_tag(tag):
    head = XML_HEAD.match(tag).group()
    out, last = [_span(CLS_KEYWORD, head)], len(head)
    for m in XML_VALUE.finditer(tag, last):
        out += [_esc(tag[last:m.start()]), _span(CLS_STRING, m.group())]
        last = m.end()
    tail = tag[last:]
    close = re.search(r"[?/]?>$", tail)
    if close:
        out += [_esc(tail[:close.start()]), _span(CLS_KEYWORD, close.group())]
    else:
        out.append(_esc(tail))
    return "".join(out)


def _xml(code):
    out, last = [], 0
    for m in XML_TOKEN.finditer(code):
        out.append(_esc(code[last:m.start()]))
        out.append(_span(CLS_COMMENT, m.group()) if m.group("c") else _xml_tag(m.group()))
        last = m.end()
    out.append(_esc(code[last:]))
    return "".join(out)


TOKENIZERS = {
    "shell": _shell,
    "python": lambda code: _scan(PY_TOKEN, code),
    "lua": lambda code: _scan(LUA_TOKEN, code),
    "vim": _vim,
    "xml": _xml,
}


def highlight(code, lang):
    tokenizer = TOKENIZERS.get(lang)
    if tokenizer is None:
        return _esc(code)
    out = tokenizer(code)
    if html.unescape(re.sub(r"<[^>]+>", "", out)) != code:
        first = code.split("\n", 1)[0]
        raise SystemExit(f"highlight({lang}): output differs from the source block starting {first[:60]!r}")
    return out
