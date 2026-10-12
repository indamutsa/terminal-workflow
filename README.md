<div align="center">

# Terminal Workflow

**A hands-on course that turns the terminal into a full IDE, one muscle memory at a time.**

tmux for sessions, Neovim for editing, git worktrees for parallel branches, and an AI coding agent
working beside you. Every lesson is a set of drills on a real, deliberately broken project.

**[Open the course →](https://nvim-workflow.vercel.app)** · press `/` on any page to search every command and key

![tmux](https://img.shields.io/badge/tmux-prefix_Ctrl--a-8FC9A8?style=flat-square&logo=tmux&logoColor=8FC9A8&labelColor=1C2B24)
![Neovim](https://img.shields.io/badge/Neovim-0.12+_·_LazyVim-8FC9A8?style=flat-square&logo=neovim&logoColor=8FC9A8&labelColor=1C2B24)
![Git](https://img.shields.io/badge/git-worktrees-E8C468?style=flat-square&logo=git&logoColor=E8C468&labelColor=1C2B24)
![Python](https://img.shields.io/badge/drills-Python_·_pytest_·_ruff-7FA8C9?style=flat-square&logo=python&logoColor=7FA8C9&labelColor=1C2B24)
![iTerm2](https://img.shields.io/badge/terminal-iTerm2-EDE6D6?style=flat-square&logo=iterm2&logoColor=EDE6D6&labelColor=1C2B24)

[Lessons](#lessons) · [Tour](#a-tour) · [Getting started](#getting-started) · [Drills](#the-drill-projects) · [Layout](#project-layout) · [Aliases](#shell-aliases) · [Finding things](#finding-things) · [Troubleshooting](#troubleshooting)

</div>

> Start with the [20-minute quick start](practice/lessons/neovim-tmux-iterm-guide.md). It gets you
> productive before you open a single lesson.

## Lessons

| | Lesson | What you practise | Time |
|:-:|--------|-------------------|:-:|
| 🪟 | [**01 · tmux**](practice/lessons/01%20tmux.md) | Sessions, the prefix key, windows, panes, detach and reattach, copy mode | 5 min |
| ✏️ | [**02 · Neovim essentials**](practice/lessons/02%20Neovim%20Essentials.md) | Opening a project, moving without a mouse, search, insert modes, delete/yank/paste, buffers | 10 min |
| ⚡ | [**03 · Neovim power editing**](practice/lessons/03%20Neovim%20Power%20Editing.md) | Operator + motion, text objects, visual mode, macros, registers, marks, search and replace | 15 min |
| 🌳 | [**04 · Git worktree**](practice/lessons/04%20Git%20Worktree.md) | Several branches checked out at once: no stashing, no switching | 10 min |
| 🤝 | [**05 · Agent worktree workflow**](practice/lessons/05%20Agent%20Worktree%20Workflow.md) | The three-window pattern: you in Neovim, an AI agent on the same branch, `main` untouched | 15 min |
| 🔭 | [**06 · Neovim LSP & Git**](practice/lessons/06%20Neovim%20LSP%20%26%20Git.md) | Go-to-definition, diagnostics, gitsigns, LazyGit, file explorers, grug-far, flash, harpoon | reference |
| 🥷 | [**07 · Neovim expert**](practice/lessons/07%20Neovim%20Expert.md) | The dot formula, expert macros, `:global`, quickfix, the command-line window, advanced substitution | mastery |
| 🔎 | [**fzf crash course**](practice/lessons/fzf.md) | Fuzzy-find files, history, directories, processes and commits | 5 min |

**Suggested pace:** week 1, lessons 1–2 · week 2, lesson 3 · week 3, lessons 4–5 · week 4 on, lessons 6–7.

## A tour

<table>
<tr>
<td width="50%" valign="top">

**One session, three windows**<br>
`main` stays clean in window 0. You write tests in window 1 while an agent writes the
implementation in window 2, both on the same feature worktree.

```
┌──────────┬──────────────────┬──────────────────┐
│ 0: main  │ 1: editor        │ 2: agent         │
│ reviews  │ nvim .           │ <agent>          │
│ rebases  │ write tests      │ generates code   │
└──────────┴──────────────────┴──────────────────┘
```

</td>
<td width="50%" valign="top">

**Operators times motions**<br>
Learn a handful of verbs and nouns, and every combination works.
Lesson 3 drills the grammar until you stop thinking about it.

```
ci"    change inside quotes
da(    delete around parentheses
yiw    yank inner word
>ap    indent a paragraph
.      repeat the last change
```

</td>
</tr>
<tr>
<td width="50%" valign="top">

**Branches side by side**<br>
A worktree is a second checkout of the same repo, so a hotfix never interrupts a feature.

```bash
git worktree add ../app-payments -b feature/payments main
git worktree list
git worktree remove ../app-payments
```

</td>
<td width="50%" valign="top">

**Bugs that are there on purpose**<br>
The drill project ships with an off-by-one, an unused import, bad names and failing tests,
so every exercise has something real to fix.

```bash
pytest               # two tests fail on purpose
ruff check .         # two lint findings on purpose
./scripts/reset-dirty.sh
```

</td>
</tr>
</table>

## Requirements

- macOS with [iTerm2](https://iterm2.com) (any terminal works; the lessons assume iTerm2 key bindings)
- [tmux](https://github.com/tmux/tmux) with the prefix set to `Ctrl-a`
- [Neovim](https://neovim.io) 0.12+ with [LazyVim](https://www.lazyvim.org); leader is `<Space>`
- A [Nerd Font](https://www.nerdfonts.com), such as JetBrainsMono Nerd Font Mono, so icons render
- Git 2.5+ for worktrees, and the [GitHub CLI](https://cli.github.com) for the PR steps
- Python 3.10+ for the drill projects
- `fzf`, `rg` and `fd` (optional but used throughout)
- Any terminal-based AI coding agent for Lesson 5; the lessons call its command `<agent>`

```bash
brew install tmux neovim git gh fzf ripgrep fd
```

## Getting started

```bash
git clone https://github.com/indamutsa/terminal-workflow.git
cd terminal-workflow
tmux new -s main
```

Then open [the quick start](practice/lessons/neovim-tmux-iterm-guide.md) and work through it in
the session you just started. Each lesson assumes the previous one.

## The drill projects

**`practice/nvim-drills/`**: the main playground for lessons 2, 3, 6 and 7. A small order-processing
app with a calculator, a report and tests, full of intentional imperfections.

```bash
cd practice/nvim-drills
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
nvim .                        # then <Space>cv to select .venv
```

| Command | Does |
|---------|------|
| `pytest` | Runs the tests; two fail on purpose (Lesson 6: neotest and DAP) |
| `python -m src.report` | Prints the order report |
| `ruff check .` | Lints; two findings on purpose (Lesson 6: diagnostics) |
| `./scripts/reset-dirty.sh` | Discards your edits and reapplies a fixed set of unstaged hunks plus an untracked file, for the git drills |

**`demo-project/`**: a smaller calculator (`src/calculator.py`, `src/app.py`, one test file) for the
quick start and first Neovim exercises.

```bash
cd demo-project
python3 src/app.py
pytest
```

## Project layout

```
practice/lessons/                   The course: one Markdown file per lesson
practice/lessons/neovim-tmux-iterm-guide.md   Quick start, learning path, reference card
practice/nvim-drills/src/           Drill app: calculator, orders, report, messy.py for reformat drills
practice/nvim-drills/tests/         Tests, two failing by design
practice/nvim-drills/scripts/       reset-dirty.sh, the patch it applies, and the scratch template
practice/nvim-drills/data/          Sample log for search and macro drills
demo-project/                       Minimal calculator for the quick start
```

## Shell aliases

The worktree lessons use these. Add them to `~/.zshrc`:

```bash
alias tl='tmux list-sessions'
alias tk='tmux kill-session -t'
alias gwl='git worktree list'

# New worktree for a branch, opened in its own tmux window
gwa() {
  local branch="$1"; local base="${2:-HEAD}"
  local dir="../$(basename $(pwd))-$(echo $branch | tr '/' '-')"
  git worktree add "$dir" -b "$branch" "$base" && \
  tmux new-window -n "$(echo $branch | sed 's/.*\///')" -c "$dir"
}
gwr() { git worktree remove "$1" && echo "Removed: $1"; }

vp() { cd "$1" && nvim . ; }
```

**The daily loop**

```
gwa feature/new-thing        worktree + tmux window
Ctrl-a c → <agent>           agent window on the same branch
Ctrl-a 1 → nvim .            you code in parallel
Ctrl-a 0/1/2                 switch between main, editor, agent
git push && gh pr create     ship it
gwr ../app-new-thing         clean up after merge
```

## Finding things

`rg` (ripgrep) searches file contents and `fd` finds files by name. Both are faster than `grep -rn`
and `find`, and both are drilled in the lessons.

**In the lessons**

```bash
fd . practice/lessons                                # every lesson file
rg -n "^## Exercise" practice/lessons                # every exercise, with line numbers
rg -n "text object" -i practice/lessons              # where a concept is taught
rg -n "<Space>g" practice/lessons                    # every git keymap mentioned
rg -c "^## " practice/lessons                        # sections per lesson
```

**In the drills**

```bash
rg -n "def " practice/nvim-drills/src                # every function
rg -n "import" practice/nvim-drills/src              # hunt the unused import
fd -e py . practice/nvim-drills                      # every Python file
git log --oneline -- practice/nvim-drills            # the drill project's history
```

**Useful flags:** `-i` ignore case · `-l` file names only · `-c` count per file · `-w` whole word ·
`-g '*.md'` limit to a glob · `-A3 -B3` lines of context · `--hidden` include dotfiles.

## Troubleshooting

Each entry: what you see, why, and the commands that fix it.

<details>
<summary><code>Ctrl-a</code> does nothing</summary>

You are not inside tmux, or the prefix is still the default `Ctrl-b`. Check for a status bar, then:

```bash
tmux attach || tmux new -s main
tmux show -g prefix                         # expect C-a
tmux source-file ~/.config/tmux/tmux.conf   # reload after editing the config
```

</details>

<details>
<summary>Icons show as boxes or question marks</summary>

The terminal font is not a Nerd Font. In iTerm2: Settings → Profiles → Text → Font →
JetBrainsMono Nerd Font Mono.

</details>

<details>
<summary>No completions, hover or go-to-definition in Neovim</summary>

The language server is missing or not attached to the buffer.

```vim
:checkhealth lsp
:Mason
:LspInfo
```

For the Python drills, make sure `.venv` exists and is selected with `<Space>cv`.

</details>

<details>
<summary><code>reset-dirty.sh</code> fails with <code>patch does not apply</code></summary>

A tracked file changed in a way the patch does not expect. Restore the drill files and run it again:

```bash
cd practice/nvim-drills
git checkout -- src/
./scripts/reset-dirty.sh
```

</details>

<details>
<summary><code>fatal: '&lt;branch&gt;' is already checked out</code> when adding a worktree</summary>

A branch can be checked out in only one worktree at a time.

```bash
git worktree list                          # find where it is checked out
git worktree add ../app-fix -b fix/other   # or use a new branch name
```

</details>

<details>
<summary>How do I exit everything?</summary>

```
Neovim   :qa        (or :qa! to discard changes)
tmux     Ctrl-a d   to detach and keep the session, or `exit` in every pane to end it
```

</details>
