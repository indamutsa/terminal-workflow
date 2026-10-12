# Terminal Workflow course: contents and writing rules

Build: `python3 _tools/build.py` (all modules, index and search index) or `python3 _tools/build.py 2 3` (only those module files).
Checks: `python3 _tools/verify.py`, `python3 _tools/coverage.py [--lesson NAME ...]`.
Content lives in `_tools/content/mN.py`. Never edit `kit.py`, `build.py`, `site.js`, `course.js` or `course.css` from a content file.

## Modules

| Module | Folder | Pages |
|---|---|---|
| 1 tmux and the shell | `m1-tmux` | Sessions that outlive the window; Windows and panes; Copy mode, the command line and fzf; Make tmux yours |
| 2 Neovim essentials | `m2-nvim-essentials` | Open, move, save, quit; Move fast and search; Delete, yank, paste, undo; Buffers, terminals, splits, tabs, leader |
| 3 Power editing | `m3-power-editing` | Operators, motions, text objects; Visual mode, macros, search and replace; Indent, registers, marks, many files |
| 4 Worktrees and the agent loop | `m4-worktrees` | Parallel branches without stashing; Worktrees in tmux; The three-window pattern; Test, ship, clean up |
| 5 Code intelligence and git | `m5-lsp-git` | Navigate code with LSP; Git inside Neovim; Refactor, files and project search; Tests and the debugger |
| 6 Plugins and the key map | `m6-plugins-keymaps` | Jump and select; Sessions, history and UI helpers; The g, [ ], and z maps; Ctrl, Space and : maps |
| 7 Expert Neovim | `m7-expert` | Motions and the dot formula; Expert macros and registers; Quickfix, marks, substitution, :g; Windows, insert, block, ranges, undo |

## Schema

```python
MODULE = {"n", "folder", "title", "footer", "tagline", "glossary", "coverage_allow", "pages"}
PAGE = {"h1", "subtitle", "idea", "problem", "drills", "rules", "worked", "practice"}
BLOCK = {"type": "cmd"}   # where, title, code, expect (required)
      | {"type": "keys"}  # where, title, rows [(key, action)], try and expect (optional, try needs expect)
      | {"type": "code"}  # file, title, code (config or script, no result)
      | {"type": "text"}  # body
```

- `where` is one of `shell`, `tmux`, `nvim`, `lazygit`, `fzf`.
- `footer` is at most 120 characters. `tagline` is at most 90.
- 2 to 4 pages per module. 2 to 4 rule cards per page. Exactly 4 practice questions: Mechanism, Keystrokes, Application, Common mistake.
- Every page has at least one `cmd` block with a non-empty `expect`.
- Write a literal backtick (vim marks) as a backslash followed by a backtick.

## Writing rules

- Short sentences, one job each. No filler.
- Keep every lesson command and key word for word.
- An `expect` comes only from a lesson's stated outcome, its "Check yourself" lines, the live config facts below, or `practice/nvim-drills/README.md`. Never invent terminal output.
- Name differences from the live config in one short `text` block. Do not claim a lesson key works when the config does not set it.
- A line the page must rewrite goes in `coverage_allow` with a reason. At most 15 per module.

## Live config facts

- Prefix is `Ctrl-a`; windows start at 1 (`base-index 1`); the status bar left reads `[main]` for session main.
- Inside tmux, `Ctrl-h/j/k/l` switch panes in a pane not running vim, so readline `Ctrl-h`/`Ctrl-k` and fzf `Ctrl+J/K` clash.
- fzf `ctrl-d` scrolls the preview; `Ctrl+A` select-all is not set.
- The live kill-session alias is `tkss`.
- The practice folder is `Terminal-Workflow/practice/nvim-drills`.
