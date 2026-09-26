# Terminal IDE Tutorial: tmux + Neovim + Git Worktree + an AI Coding Agent

Learn by doing. After 20 minutes you'll have the core workflow. Detailed lessons are in the `lessons/` folder.

**Prerequisites**: iTerm2 installed, Neovim 0.12+ configured, an AI coding agent CLI installed (any terminal-based agent).

> **Neovim flavor**: These lessons target **LazyVim**. Plain `nvim` (and the aliases `v` / `vim` / `vi` / `v.` / `vp`) all open LazyVim. Leader = spacebar (`<Space>`).

---

## Lessons

| # | Topic | Time | File |
|---|-------|------|------|
| 1 | tmux — sessions, windows, panes, copy mode | 5 min | [01 tmux.md](01%20tmux.md) |
| 2 | Neovim essentials — navigation, editing, buffers | 10 min | [02 Neovim Essentials.md](02%20Neovim%20Essentials.md) |
| 3 | Neovim power — text objects, macros, registers, search/replace | 15 min | [03 Neovim Power Editing.md](03%20Neovim%20Power%20Editing.md) |
| 4 | Git worktree — parallel branches | 10 min | [04 Git Worktree.md](04%20Git%20Worktree.md) |
| 5 | Full workflow — AI agent + worktree + tmux | 15 min | [05 Agent Worktree Workflow.md](05%20Agent%20Worktree%20Workflow.md) |
| 6 | Neovim advanced — LSP, git, Oil, snacks picker, all prefix keys | reference | [06 Neovim LSP & Git.md](06%20Neovim%20LSP%20%26%20Git.md) |
| 7 | Neovim expert — dot formula, advanced macros, `:g`, undo tree, registers, ex commands | mastery | [07 Neovim Expert.md](07%20Neovim%20Expert.md) |

---

## Quick Start (20 minutes to productive)

### Minute 0-5: tmux

```bash
tmux new -s main                    # start session
```

```
Ctrl-a c        New window
Ctrl-a 0-9      Switch windows
Ctrl-a w        Window picker (interactive list)
Ctrl-a d        Detach (session stays alive)
Ctrl-a |        Vertical split
Ctrl-a -        Horizontal split
Ctrl-a z        Zoom/unzoom pane
```

Full lesson: [01 tmux.md](01%20tmux.md)

### Minute 5-15: Neovim

```bash
nvim .                              # open project
```

```
\                File tree (toggle)
<Space>sf        Search files (fuzzy)
<Space>sg        Search all file contents (grep)
i                Insert mode (type)
Esc              Normal mode (commands)
:w               Save
dd               Delete line
ci"              Change inside quotes
gg               Top of file
G                Bottom of file
u                Undo
.                Repeat last change
```

Full lesson: [02 Neovim Essentials.md](02%20Neovim%20Essentials.md)

### Minute 15-20: The combined workflow

```bash
# Window 0: Editor
nvim .

# Window 1: Tests
Ctrl-a c
pytest tests/ -v

# Window 2: AI agent
Ctrl-a c
<agent>                             # your agent's CLI command
```

The loop:
1. `Ctrl-a 0` — edit code
2. `:w` — save
3. `Ctrl-a 1` — run tests
4. `Ctrl-a 2` — ask the agent if stuck
5. Repeat

---

## Demo Project

A practice project is included at `demo-project/`:

```
demo-project/
├── pyproject.toml
├── src/
│   ├── calculator.py    ← edit this
│   └── app.py
└── tests/
    └── test_calculator.py
```

Set up:
```bash
cd demo-project
git init && git add -A && git commit -m "Initial commit"
```

Then follow the exercises in [02 Neovim Essentials.md](02%20Neovim%20Essentials.md) using these files.

---

## Learning Path

**Week 1**: Lessons 1-2. tmux windows + neovim basics + `<Space>sf` (find file). Enough to be productive.

**Week 2**: Lesson 3. Text objects (`ci"`, `da(`), macros, registers. This is where vim gets fast.

**Week 3**: Lesson 4-5. Git worktrees + an AI coding agent. The 3-window pattern becomes your default.

**Week 4+**: Lesson 6. LSP navigation, LazyGit, Oil, grug-far search & replace. Speed multipliers, not essentials.

---

## Reference Card

### tmux

| Keys | Action |
|------|--------|
| `Ctrl-a c` | New window |
| `Ctrl-a w` | Window picker |
| `Ctrl-a 0-9` | Switch to window N |
| `Ctrl-a n/p` | Next/prev window |
| `Ctrl-a ,` | Rename window |
| `Ctrl-a d` | Detach |
| `Ctrl-a \|` | Vertical split |
| `Ctrl-a -` | Horizontal split |
| `Ctrl-a h/j/k/l` | Navigate panes |
| `Ctrl-a z` | Zoom/unzoom pane |
| `Ctrl-a x` | Close pane (y to confirm) |
| `Ctrl-a [` | Copy mode |
| `Ctrl-a ]` | Paste |

### Neovim — movement

| Keys | Action |
|------|--------|
| `h/j/k/l` | Move cursor |
| `w/b/e` | Word forward/back/end |
| `0/$` | Start/end of line |
| `gg/G` | Top/bottom of file |
| `Ctrl-d/Ctrl-u` | Half-page down/up |
| `%` | Matching bracket |
| `/pattern` | Search (n=next, N=prev) |
| `*/#` | Search word under cursor |
| `f{c}/F{c}` | Jump to char on line |

### Neovim — editing

| Keys | Action |
|------|--------|
| `i/a/o/O` | Enter insert mode |
| `A/I` | Insert at end/start of line |
| `dd/D` | Delete line / to end |
| `cc/C` | Change line / to end |
| `yy/p` | Copy line / paste |
| `ci"/ci(/ci{` | Change inside quotes/parens/braces |
| `di"/da(` | Delete inside/around |
| `vi{/vip` | Select inside braces/paragraph |
| `u / Ctrl-r` | Undo / redo |
| `.` | Repeat last change |
| `>>  / <<` | Indent / unindent |
| `gg=G` | Auto-indent entire file |
| `<Space>cf` | Format file |
| `:%s/old/new/g` | Find and replace |

### Neovim — macros & registers

| Keys | Action |
|------|--------|
| `qa...q` | Record macro into 'a' |
| `@a / 5@a` | Play macro / 5 times |
| `"ayy/"ap` | Yank/paste register a |
| `"+y/"+p` | System clipboard |
| `"0p` | Paste last yank (survives deletes) |

### Neovim — files & search

| Keys | Action |
|------|--------|
| `<Space>sf` | Search files (fuzzy) |
| `<Space><Space>` | Find file (built-in alias) |
| `<Space>sg` | Grep project (search contents) |
| `<Space>,` | Switch buffers |
| `<Space>e` | Snacks explorer (sidebar) |
| `\` | Toggle file tree (neo-tree) |
| `Shift-H/L` | Prev/next buffer |
| `<Space>sr` | Search & replace (grug-far) |
| `<Space>1`-`9` | Jump to Harpoon file 1-9 |
| `<Space>H` | Add file to Harpoon; `<Space>h` menu |

### Neovim — LSP

| Keys | Action |
|------|--------|
| `gd` | Go to definition |
| `gr` / `grr` | Find references |
| `gri` | Go to implementation |
| `grn` | Rename |
| `gra` | Code action |
| `K` | Hover docs |
| `]d/[d` | Next/prev diagnostic |
| `<Space>xx` | Diagnostics panel (Trouble) |
| `<Space>cf` | Format buffer |

### Neovim — git

| Keys | Action |
|------|--------|
| `<Space>gg` | LazyGit |
| `<Space>gd` | Git Diff — hunks (snacks) |
| `<Space>gD` | Git Diff vs origin |
| `<Space>gs` | Git status |
| `]h/[h` | Next/prev hunk |
| `<Space>ghs` | Stage hunk |
| `<Space>ghb` | Blame line |

### Neovim — terminal (inside nvim)

| Keys | Action |
|------|--------|
| `Ctrl-\` | Toggle terminal (root dir) |
| `<Space>ft` | Terminal (toggle, root) |
| `<Space>Tf` | Terminal float |
| `<Space>Th` | Terminal horizontal (bottom) |
| `<Space>Tv` | Terminal vertical (right) |
| `Ctrl-\ Ctrl-n` | Exit terminal mode → normal |

### Git worktree

| Command | Action |
|---------|--------|
| `git worktree add ../dir -b branch` | Create |
| `git worktree list` | List |
| `git worktree remove ../dir` | Remove |
| `gwa feature/name` | Create + tmux window |
| `gwl` | List |
| `gwr ../dir` | Remove |

---

## How to Exit Everything

Stuck somewhere? Here's how to get out:

| Stuck in... | Exit with |
|-------------|-----------|
| Insert mode | `Esc` |
| Visual mode | `Esc` |
| Terminal mode (nvim) | `Ctrl-\ Ctrl-n` (then `q`/`<Space>ft` to close) |
| Picker / fuzzy finder (snacks) | `Esc` or `Ctrl-c` |
| LazyGit | `q` |
| Snacks explorer (`<Space>e`) | `<Space>e` or `q` |
| Neo-tree sidebar | `\` or `q` |
| grug-far (search/replace) | `q` or `:q` |
| tmux copy mode | `q` or `Esc` |
| tmux window picker (`Ctrl-a w`) | `Esc` or `q` |
| A command-line prompt (`:`) | `Esc` |
| Neovim entirely | `:q` (or `:q!` to force without saving) |
| Stuck and nothing works | `:qa!` (force quit everything) |

---

## Shell Aliases (in ~/.zshrc)

```bash
# tmux
alias tl='tmux list-sessions'
alias tk='tmux kill-session -t'

# git worktree
alias gwl='git worktree list'
gwa() {
  local branch="$1"; local base="${2:-HEAD}"
  local dir="../$(basename $(pwd))-$(echo $branch | tr '/' '-')"
  git worktree add "$dir" -b "$branch" "$base" && \
  tmux new-window -n "$(echo $branch | sed 's/.*\///')" -c "$dir"
}
gwr() { git worktree remove "$1" && echo "Removed: $1"; }

# neovim
vp() { cd "$1" && nvim . ; }

# auto-attach tmux
if [ -z "$TMUX" ]; then
  tmux attach || tmux new -s main
fi
```

---

## Troubleshooting

**tmux prefix not working** — make sure you're inside tmux (status bar visible). If not: `tmux attach`. Reload config: `tmux source-file ~/.config/tmux/tmux.conf`

**Icons look wrong** — set iTerm2 font to JetBrainsMono Nerd Font Mono (Settings → Profiles → Text → Font)

**LSP not working** — `:checkhealth lsp`, `:Mason`, `:LspInfo`

**Scala Metals broken** — `rm -rf .metals/ .bloop/ metals.sbt`, reopen file, accept "Import build"
