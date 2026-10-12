"""Module 1: tmux and the shell. Sources: lessons 01 tmux.md, fzf.md and the quick-start guide."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


TMUX_CONF = "~/.config/tmux/tmux.conf"

STATUS_STYLE = C(r'''
# Colors (tokyonight theme)
set -g status-style "bg=#1a1b26,fg=#a9b1d6"
set -g window-status-current-style "bg=#7aa2f7,fg=#1a1b26,bold"
set -g window-status-style "bg=#1a1b26,fg=#565f89"

# Format: show index:name
set -g window-status-format " #I:#W "
set -g window-status-current-format " #I:#W "

# Left side: session name
set -g status-left "[#S] "

# Right side: time
set -g status-right "%H:%M"

# Right side with more info:
set -g status-right "#(whoami)@#H | %H:%M"
''')

STATUS_POSITION = C(r'''
set -g status-position top       # bar at top instead of bottom
set -g status-justify centre     # center the window list
''')

PANE_BORDERS = C(r'''
set -g pane-border-style "fg=#565f89"
set -g pane-active-border-style "fg=#7aa2f7"
''')

ACTIVITY = C(r'''
# Highlight windows with activity
setw -g monitor-activity on
set -g visual-activity off       # don't show a message, just highlight

# Highlight style for windows with activity
set -g window-status-activity-style "fg=#e0af68"
''')

USEFUL_OPTIONS = C(r'''
# Start window numbering at 1 (not 0)
set -g base-index 1
setw -g pane-base-index 1

# Renumber windows when one is closed
set -g renumber-windows on

# Bigger scrollback history
set -g history-limit 50000

# Mouse support (scroll, click to select pane, resize)
set -g mouse on

# No delay after pressing Esc (important for nvim)
set -sg escape-time 0

# Auto-rename windows based on running command
setw -g automatic-rename on
''')

PLUGINS = C(r'''
# Plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'      # sane defaults
set -g @plugin 'tmux-plugins/tmux-resurrect'     # save/restore sessions across reboots
set -g @plugin 'tmux-plugins/tmux-continuum'     # auto-save sessions every 15 min
set -g @plugin 'tmux-plugins/tmux-yank'          # better copy to clipboard

# Initialize TPM (keep at bottom)
run '~/.tmux/plugins/tpm/tpm'
''')

CONTINUUM = C(r'''
set -g @continuum-save-interval '10'          # auto-save every 10 minutes
set -g @continuum-restore 'off'               # OFF on purpose — see "the pileup trap"
set -g @resurrect-capture-pane-contents 'on'  # restore scrollback contents
set -g @resurrect-strategy-nvim 'session'     # restore nvim sessions too
''')

RESTORE_ONCE = C(r'''
#!/usr/bin/env bash
LOCK="/tmp/tmux-resurrect-restored-$(id -u)"
[ -f "$LOCK" ] && exit 0          # already restored this boot → do nothing
touch "$LOCK"
"$HOME/.tmux/plugins/tmux-resurrect/scripts/restore.sh"
''')

BOOT_RESTORE = C(r'''
#!/usr/bin/env bash
# launchd has a minimal PATH; resurrect's scripts call bare `tmux`, so add Homebrew.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
TMUX_BIN="/opt/homebrew/bin/tmux"
rm -f "/tmp/tmux-resurrect-restored-$(id -u)"   # fresh boot → clear stale lock
# Anchor the server with a session named to MATCH the save ("main") — a bare
# start-server with no session can exit immediately, and restore expects "main".
"$TMUX_BIN" has-session 2>/dev/null || "$TMUX_BIN" new-session -d -s main
sleep 1
"$HOME/.config/tmux/restore-once.sh"
''')

PLIST = C(r'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.indamutsa.tmux-restore</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOU/.config/tmux/boot-restore.sh</string>
    </array>
    <key>RunAtLoad</key><true/>
</dict>
</plist>
''')

BINDINGS = C(r'''
# Quick window swap
bind -r < swap-window -t -1\; select-window -t -1
bind -r > swap-window -t +1\; select-window -t +1

# Split and immediately open nvim
bind v split-window -h -c "#{pane_current_path}" \; send-keys "nvim ." Enter

# Kill pane without confirmation
bind X kill-pane

# Quick session switching
bind S choose-tree -s    # interactive session+window tree

# Toggle between last window
bind Tab last-window
''')

SCHEMES = C(r'''
# tokyonight (matches nvim)
set -g status-style "bg=#1a1b26,fg=#a9b1d6"
set -g window-status-current-style "bg=#7aa2f7,fg=#1a1b26,bold"

# catppuccin
set -g status-style "bg=#1e1e2e,fg=#cdd6f4"
set -g window-status-current-style "bg=#89b4fa,fg=#1e1e2e,bold"

# gruvbox
set -g status-style "bg=#282828,fg=#ebdbb2"
set -g window-status-current-style "bg=#fabd2f,fg=#282828,bold"
''')

FZF_ALIASES = C(r'''
# Find file and open in editor
alias ff='fzf --preview "bat --color=always {}" | xargs nvim'

# Find directory and cd
alias fd='cd $(find . -type d | fzf)'

# Search git commits
alias fgl='git log --oneline | fzf --preview "git show {1}"'

# Search running processes
alias fkill='ps aux | fzf | awk "{print \$2}" | xargs kill -9'
''')

MODULE = {
    "n": 1,
    "folder": "m1-tmux",
    "title": "tmux and the shell",
    "footer": "Sessions, windows and panes; copy mode and fzf; status bar, plugins and restore after reboot",
    "tagline": "Sessions that survive, panes that split, a config that restores.",
    "glossary": [],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Sessions that outlive the window",
            "subtitle": "Start a tmux session, detach, and come back to everything still running.",
            "idea": (
                "tmux keeps your terminal alive. Close the window and the work keeps running.",
                [
                    ("Start a session", "tmux new -s main", "Opens a session named main."),
                    ("Prefix", "Ctrl-a", "Tells tmux that the next key is a tmux command."),
                    ("Detach", "Ctrl-a d", "Leaves tmux. The session keeps running."),
                    ("Reattach", "tmux attach", "Brings back everything where you left it."),
                ],
                None,
            ),
            "problem": {
                "fail": "You close the terminal, or the laptop sleeps, and the running processes are gone.",
                "fix": "Run everything inside a tmux session. Detach with `Ctrl-a d`, and `tmux attach` brings it all back.",
            },
            "drills": [
                {
                    "h2": "Start your first session",
                    "intro": "Open iTerm2 and type this.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Start a session called main", "code": "tmux new -s main",
                         "expect": "A tmux status bar appears at the bottom with `[main]` on the left."},
                    ],
                },
                {
                    "h2": "The prefix key",
                    "intro": "tmux listens for commands after the prefix key. Yours is `Ctrl-a`: hold Ctrl, tap a, release both, then press the command key.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Create a window", "rows": [("Ctrl-a then c", "New window")],
                         "try": "Press `Ctrl-a`, let go, then press `c`.",
                         "expect": "A second window appears in the status bar and you are on it. Windows are numbered from 1 here (`base-index 1`)."},
                    ],
                },
                {
                    "h2": "Detach and reattach",
                    "intro": "Sessions survive crashes, reboots and SSH disconnects.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Detach", "rows": [("Ctrl-a d", "Detach: you leave tmux but the session keeps running")],
                         "try": "Press `Ctrl-a d`.",
                         "expect": "You are back at a bare terminal. The session is alive in the background."},
                        {"type": "cmd", "where": "shell", "title": "Reattach", "code": "tmux attach",
                         "expect": "Everything is exactly where you left it."},
                    ],
                },
                {
                    "h2": "Sessions",
                    "intro": "Run one session per project.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create, list, switch and kill sessions", "code": C('''
tmux new -s work          # create named session
tmux new -s personal      # another session
tmux ls                   # list all sessions
tmux switch -t work       # switch to session "work"
tmux kill-session -t old  # kill a session
'''),
                         "expect": "`tmux ls` lists every session by name, and `tmux switch -t work` moves you to work."},
                        {"type": "keys", "where": "tmux", "title": "Move between sessions", "rows": [
                            ("Ctrl-a s", "Session picker (like Ctrl-a w but for sessions)"),
                            ("Ctrl-a (", "Previous session"),
                            ("Ctrl-a )", "Next session"),
                        ], "try": "Press `Ctrl-a s`.", "expect": "A picker lists your sessions."},
                    ],
                },
                {
                    "h2": "Auto-attach",
                    "intro": "Already in your `~/.zshrc`: every new terminal connects to tmux. No manual `tmux attach`.",
                    "blocks": [
                        {"type": "code", "file": "~/.zshrc", "title": "Auto-attach", "code": C('''
if [ -z "$TMUX" ]; then
  tmux attach || tmux new -s main
fi
''')},
                        {"type": "code", "file": "~/.zshrc", "title": "Session aliases", "code": C('''
alias tl='tmux list-sessions'
alias tk='tmux kill-session -t'
''')},
                        {"type": "text", "body": "In the live config the kill alias is named `tkss`, not `tk`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Sessions at a glance",
                "cards": [
                    ("Session commands", "Run these in a shell.", ["Command", "Does"], [
                        ["`tmux new -s main`", "Start a named session"],
                        ["`tmux attach`", "Reattach"],
                        ["`tmux ls`", "List all sessions"],
                        ["`tmux switch -t work`", "Switch to session work"],
                        ["`tmux kill-session -t old`", "Kill a session"],
                    ]),
                    ("If the prefix does nothing", "Make sure you are inside tmux: the status bar is visible.", ["Step", "Command"], [
                        ["Not in tmux? Attach", "`tmux attach`"],
                        ["Reload the config", "`tmux source-file ~/.config/tmux/tmux.conf`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Park a session and come back",
                "frame": "You stop for the day and want your work to wait.",
                "given": "A session called `work` is running.",
                "code": "tmux ls\ntmux attach",
                "steps": [
                    "Press `Ctrl-a d` to detach.",
                    "Close the terminal. The session keeps running.",
                    "Open a new terminal and run `tmux ls`. The session is listed.",
                    "Run `tmux attach` to return to it.",
                ],
                "meaning": "Closing a window never ends the work. Only killing the session, or restarting the computer, does.",
            },
            "practice": {
                "h2": "Practice: sessions",
                "qs": [
                    ("Mechanism", "Why does a detached session keep running?",
                     "Who owns the processes: the window or tmux?",
                     ["tmux runs your shells, not the terminal window.", "Detach only closes your view of the session."],
                     "tmux keeps the processes alive; the window was only a view."),
                    ("Keystrokes", "Which keys detach from a session?",
                     "Prefix first, then one letter.",
                     ["Press `Ctrl-a`.", "Press `d`."],
                     "`Ctrl-a d`."),
                    ("Application", "You work on two projects. Create a named session for each.",
                     "Use `tmux new -s` with a name.",
                     ["Run `tmux new -s work`.", "Run `tmux new -s personal`.", "List them with `tmux ls`."],
                     "`tmux new -s work` and `tmux new -s personal`."),
                    ("Common mistake", "The prefix does nothing. What do you check first?",
                     "Where are you typing?",
                     ["Look for the tmux status bar.", "No bar means you are not inside tmux: run `tmux attach`."],
                     "Make sure you are inside tmux."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Windows and panes",
            "subtitle": "One window per job, split into panes when you need two views.",
            "idea": (
                "A session holds windows. A window holds panes.",
                [
                    ("New window", "Ctrl-a c", "One window per job: editor, tests, agent."),
                    ("Switch window", "Ctrl-a w", "A picker with a live preview."),
                    ("Split", "Ctrl-a |", "Two panes side by side."),
                    ("Zoom", "Ctrl-a z", "One pane fills the screen. Press again to unzoom."),
                ],
                None,
            ),
            "problem": {
                "fail": "One terminal, three jobs. The editor, the tests and your AI agent fight for the same screen.",
                "fix": "Give each job its own window, and split a window into panes to see two things at once.",
            },
            "drills": [
                {
                    "h2": "Navigate between windows",
                    "intro": "This is how you switch between editor, tests and your AI agent.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Switch windows", "rows": [
                            ("Ctrl-a 0", "Jump to window 0"),
                            ("Ctrl-a 1", "Jump to window 1"),
                            ("Ctrl-a n", "Next window"),
                            ("Ctrl-a p", "Previous window"),
                            ("Ctrl-a w", "Interactive window picker (preview + pick with j/k + Enter)"),
                        ], "try": "Press `Ctrl-a w`.",
                         "expect": "All windows are listed with a live preview. Press Enter to jump."},
                        {"type": "text", "body": "Windows start at 1 here (`base-index 1`), so `Ctrl-a 1` is your first window."},
                    ],
                },
                {
                    "h2": "Split panes",
                    "intro": "Split your window, run `ls` in one pane and `htop` in the other.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Split and move", "rows": [
                            ("Ctrl-a |", "Split vertically (side by side)"),
                            ("Ctrl-a -", "Split horizontally (top and bottom)"),
                            ("Ctrl-a h/j/k/l", "Move between panes (vim-style)"),
                            ("Ctrl-a x", "Close current pane (prompts y/n — press y to confirm)"),
                        ], "try": "Split, then move with `Ctrl-a h` and `Ctrl-a l`. Or click the pane you want: the mouse is on.",
                         "expect": "Two panes, each with its own shell."},
                        {"type": "text", "body": "Inside tmux, `Ctrl-h`, `Ctrl-j`, `Ctrl-k` and `Ctrl-l` also switch panes with no prefix."},
                    ],
                },
                {
                    "h2": "Window and pane tricks",
                    "intro": "Capital H/J/K/L resizes. Lowercase h/j/k/l navigates.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Pane management", "rows": [
                            ("Ctrl-a z", "Zoom current pane to full screen (press again to unzoom)"),
                            ("Ctrl-a Space", "Cycle through pane layouts (even, tiled, etc.)"),
                            ("Ctrl-a !", "Break pane into its own window"),
                            ("Ctrl-a q", "Show pane numbers (press the number to jump to that pane)"),
                            ("Ctrl-a {", "Swap pane with previous"),
                            ("Ctrl-a }", "Swap pane with next"),
                            ("Ctrl-a o", "Cycle to next pane"),
                            ("Ctrl-a ;", "Jump to last active pane"),
                            (":swap-pane -t 2", "Swap current pane with pane 2 (tmux command)"),
                        ], "try": "Press `Ctrl-a z` in a split window, then press it again.",
                         "expect": "One pane fills the screen. The second press brings the split back."},
                        {"type": "keys", "where": "tmux", "title": "Pane resizing", "rows": [
                            ("Ctrl-a H", "Resize pane left (5 cells)"),
                            ("Ctrl-a J", "Resize pane down (5 cells)"),
                            ("Ctrl-a K", "Resize pane up (5 cells)"),
                            ("Ctrl-a L", "Resize pane right (5 cells)"),
                        ]},
                        {"type": "keys", "where": "tmux", "title": "Window management", "rows": [
                            ("Ctrl-a c", "Create new window"),
                            ("Ctrl-a ,", "Rename current window"),
                            ("Ctrl-a &", "Kill current window (confirms y/n)"),
                            ("Ctrl-a .", "Move window to another index"),
                            ("Ctrl-a f", "Find window by name"),
                        ], "try": "Press `Ctrl-a ,` and type `editor`.",
                         "expect": "The status bar shows `editor` instead of `zsh`."},
                        {"type": "cmd", "where": "shell", "title": "Send commands to other windows", "code": C('''
# Run a command in another window without switching to it:
tmux send-keys -t 1 "pytest tests/ -v" Enter

# Run in a specific named window:
tmux send-keys -t ml:tests "make build" Enter

# Capture output from another pane:
tmux capture-pane -t 1 -p | tail -10
'''),
                         "expect": "The first two run in the other window while you stay put. The last prints that pane's last 10 lines here."},
                    ],
                },
            ],
            "rules": {
                "h2": "Muscle memory",
                "cards": [
                    ("Practice each 10 times", "These 13 keys carry most of your day.", ["Command", "What it does"], [
                        ["`Ctrl-a c`", "New window"],
                        ["`Ctrl-a w`", "Window picker (interactive list with preview)"],
                        ["`Ctrl-a 0-9`", "Jump to window by number"],
                        ["`Ctrl-a n/p`", "Next/previous window"],
                        ["`Ctrl-a ,`", "Rename current window"],
                        ["`Ctrl-a d`", "Detach"],
                        ["`Ctrl-a |`", "Vertical split"],
                        ["`Ctrl-a -`", "Horizontal split"],
                        ["`Ctrl-a h/j/k/l`", "Navigate panes"],
                        ["`Ctrl-a z`", "Zoom/unzoom pane"],
                        ["`Ctrl-a q`", "Show pane numbers (tap number to jump)"],
                        ["`Ctrl-a x`", "Close pane (y to confirm)"],
                        ["`Ctrl-a [`", "Enter copy mode"],
                    ]),
                    ("Lowercase or capital", "Same letters, two jobs.", ["Keys", "Does"], [
                        ["`Ctrl-a h/j/k/l`", "Navigate panes"],
                        ["`Ctrl-a H/J/K/L`", "Resize panes by 5 cells"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Editor, tests and agent in one session",
                "frame": "Three jobs, three windows, one session.",
                "given": "You are in the `main` session with one window.",
                "steps": [
                    "Press `Ctrl-a ,` and name this window `editor`.",
                    "Press `Ctrl-a c`, then `Ctrl-a ,` and name it `tests`.",
                    "Press `Ctrl-a c` again and name it `agent`.",
                    "Press `Ctrl-a w` to see all three with a preview.",
                ],
                "meaning": "The status bar now shows `editor`, `tests` and `agent`, so a jump is one keystroke away.",
            },
            "practice": {
                "h2": "Practice: windows and panes",
                "qs": [
                    ("Mechanism", "What is the difference between a window and a pane?",
                     "One lives inside the other.",
                     ["A window fills the screen.", "Panes divide one window into rectangles."],
                     "A window holds one or more panes."),
                    ("Keystrokes", "Split a window side by side, then close the new pane.",
                     "Split first, then close.",
                     ["Press `Ctrl-a |`.", "Press `Ctrl-a x`, then `y`."],
                     "`Ctrl-a |`, then `Ctrl-a x` and `y`."),
                    ("Application", "A test run is scrolling past. Read it without leaving the pane.",
                     "Fill the screen with one pane.",
                     ["Press `Ctrl-a z` to zoom.", "Press `Ctrl-a z` again to unzoom."],
                     "`Ctrl-a z` twice."),
                    ("Common mistake", "You pressed `Ctrl-a L` to move right, and the pane got bigger. Why?",
                     "Look at the letter case.",
                     ["Capital `H/J/K/L` resizes.", "Lowercase `h/j/k/l` navigates."],
                     "Use lowercase `l` to move, capital `L` to resize."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Copy mode, the command line and fzf",
            "subtitle": "Copy from scrollback, edit the prompt fast, and fuzzy-find anything.",
            "idea": (
                "Three tools remove most mouse work: copy mode, readline keys and fzf.",
                [
                    ("Copy mode", "Ctrl-a [", "Move through scrollback with vim keys."),
                    ("Clear the line", "Ctrl-u", "Deletes the whole line."),
                    ("Fuzzy find", "fzf", "A filterable list of files."),
                    ("History", "Ctrl+R", "Search your command history."),
                ],
                None,
            ),
            "problem": {
                "fail": "You copy output with the mouse and grab half a border, or retype a long path from history.",
                "fix": "Copy with copy mode, edit the prompt with readline keys, and find files, history and branches with fzf.",
            },
            "drills": [
                {
                    "h2": "Copy mode",
                    "intro": "Copy mode gives you a free-moving cursor in the scrollback.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Copy and paste", "rows": [
                            ("Ctrl-a [", "Enter copy mode (cursor becomes free-moving)"),
                            ("h/j/k/l or Ctrl-d/Ctrl-u", "Navigate"),
                            ("v", "Start selection (visual mode)"),
                            ("y", "Yank (copy) selection, exits copy mode"),
                            ("Ctrl-a ]", "Paste the copied text"),
                            ("q", "Quit copy mode without copying"),
                            ("Esc", "Also exits copy mode"),
                        ], "try": "Press `Ctrl-a [`, move with `j`, press `v`, move, press `y`, then `Ctrl-a ]`.",
                         "expect": "The copied text appears at the prompt."},
                    ],
                },
                {
                    "h2": "Terminal line editing",
                    "intro": "These readline keys work at any shell prompt, in tmux, zsh or bash. They replace Cmd+Delete and Option+Delete.",
                    "blocks": [
                        {"type": "keys", "where": "shell", "title": "Readline shortcuts", "rows": [
                            ("Ctrl-u", "Delete entire line (like Cmd+Delete)"),
                            ("Ctrl-w", "Delete word backward (like Option+Delete)"),
                            ("Ctrl-k", "Delete from cursor to end of line"),
                            ("Ctrl-a", "Jump to start of line"),
                            ("Ctrl-e", "Jump to end of line"),
                            ("Ctrl-h", "Delete character backward (Backspace)"),
                            ("Alt-d", "Delete word forward"),
                            ("Alt-b", "Move back one word"),
                            ("Alt-f", "Move forward one word"),
                        ], "try": "Type a few words, then press `Ctrl-w` and `Ctrl-u`.",
                         "expect": "`Ctrl-w` removes the last word. `Ctrl-u` clears the line."},
                        {"type": "text", "body": "Inside tmux, `Ctrl-a` is the prefix: press `Ctrl-a Ctrl-a` to reach the start of the line. In a pane that is not running vim, `Ctrl-h`, `Ctrl-j`, `Ctrl-k` and `Ctrl-l` switch panes instead."},
                    ],
                },
                {
                    "h2": "fzf basics",
                    "intro": "fzf is a fuzzy finder. Type to filter, Enter to pick.",
                    "blocks": [
                        {"type": "cmd", "where": "fzf", "title": "Basic usage", "code": C('''
# Search files in current directory
fzf

# Search command history
Ctrl+R

# Search and cd into directory
cd **<TAB>

# Search and open file
vim **<TAB>

# Kill process
kill -9 **<TAB>
'''),
                         "expect": "`fzf` lists the files under the current folder. `Ctrl+R` lists your history. `**<TAB>` opens a picker for the command."},
                        {"type": "keys", "where": "fzf", "title": "Keyboard shortcuts", "rows": [
                            ("Ctrl+J/K", "Navigate"),
                            ("↑/↓", "Navigate"),
                            ("Enter", "Select"),
                            ("Ctrl+C", "Cancel"),
                            ("Esc", "Cancel"),
                            ("Tab", "Multi-select"),
                            ("Ctrl+A", "Select all"),
                            ("Ctrl+D", "Deselect all"),
                        ]},
                        {"type": "text", "body": "In tmux, use the arrow keys: `Ctrl+J/K` switch panes there. In this setup `Ctrl+D` scrolls the preview and `Ctrl+A` is not bound to select all."},
                    ],
                },
                {
                    "h2": "Aliases, pipes and options",
                    "intro": "Add the aliases to `~/.zshrc`.",
                    "blocks": [
                        {"type": "code", "file": "~/.zshrc", "title": "fzf aliases", "code": FZF_ALIASES},
                        {"type": "text", "body": "The `fd` alias hides the `fd` program. Rename it if you use that program."},
                        {"type": "cmd", "where": "fzf", "title": "With pipes", "code": C('''
# Search history
history | fzf

# Search docker containers
docker ps -a | fzf

# Search git branches
git branch | fzf | xargs git checkout
'''),
                         "expect": "Each command opens its output as a filterable list. Enter on a branch checks it out."},
                        {"type": "cmd", "where": "fzf", "title": "Advanced options", "code": C('''
# Preview files
fzf --preview 'cat {}'

# Multi-select files
fzf -m

# Case-insensitive
fzf -i

# Exact match
fzf -e
'''),
                         "expect": "`--preview` shows the file beside the list, `-m` lets you pick several with Tab, `-i` ignores case and `-e` matches exactly."},
                        {"type": "cmd", "where": "shell", "title": "Reload the shell and test", "code": C('''
source ~/.zshrc
fzf  # Should work now
'''),
                         "expect": "`fzf` opens its list. Press `Esc` to cancel."},
                    ],
                },
            ],
            "rules": {
                "h2": "fzf options",
                "cards": [
                    ("Flags", "Add them after `fzf`.", ["Flag", "Does"], [
                        ["`--preview`", "Show a command's output for the selected line"],
                        ["`-m`", "Multi-select files"],
                        ["`-i`", "Case-insensitive"],
                        ["`-e`", "Exact match"],
                    ]),
                    ("Clashes inside tmux", "Two keys mean something else in this setup.", ["Key", "In tmux"], [
                        ["`Ctrl-a`", "The prefix. Press it twice to reach the start of the line."],
                        ["`Ctrl-j/k`", "Switch panes, so use the arrows in fzf."],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find a file and open it",
                "frame": "You know part of a name, not the path.",
                "given": "The alias `ff` from the fzf aliases is loaded.",
                "code": "ff",
                "steps": [
                    "Run `ff`.",
                    "Type a few letters of the name. The list narrows and `bat` shows a preview.",
                    "Press Enter. `nvim` opens the file.",
                ],
                "meaning": "One alias replaces a find, a read and an open.",
            },
            "practice": {
                "h2": "Practice: copy mode and fzf",
                "qs": [
                    ("Mechanism", "Why does `y` in copy mode also leave copy mode?",
                     "Yank is the last step of copying.",
                     ["`v` starts the selection.", "`y` copies it and exits."],
                     "The copy is done, so tmux exits copy mode."),
                    ("Keystrokes", "Copy a line of output and paste it at the prompt.",
                     "Enter copy mode first.",
                     ["`Ctrl-a [`, move, `v`, move.", "`y` to copy.", "`Ctrl-a ]` to paste."],
                     "`Ctrl-a [`, `v`, `y`, `Ctrl-a ]`."),
                    ("Application", "Check out a git branch by picking it from a list.",
                     "Pipe the branch list into fzf.",
                     ["`git branch` lists the branches.", "`fzf` filters them.", "`xargs git checkout` switches."],
                     "`git branch | fzf | xargs git checkout`"),
                    ("Common mistake", "`Ctrl-a` at the prompt does not jump to the start of the line in tmux. Why?",
                     "Think of the prefix.",
                     ["tmux takes `Ctrl-a` as its prefix.", "Send it on by pressing it twice."],
                     "Press `Ctrl-a Ctrl-a`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Make tmux yours",
            "subtitle": "Style the status bar, add plugins, and restore your workspace after a reboot.",
            "idea": (
                "One file, `~/.config/tmux/tmux.conf`, controls how tmux looks and behaves.",
                [
                    ("Reload", "Ctrl-a r", "Applies your config changes."),
                    ("Install plugins", "Ctrl-a I", "Capital I, with TPM."),
                    ("Save", "Ctrl-a Ctrl-s", "Saves windows, panes and layout."),
                    ("Restore", "Ctrl-a Ctrl-r", "Brings the saved workspace back."),
                ],
                None,
            ),
            "problem": {
                "fail": "A computer restart kills the tmux server, and your windows are gone.",
                "fix": "Save with resurrect and continuum, then restore once at login with a lock-guarded script.",
            },
            "drills": [
                {
                    "h2": "Status bar styling",
                    "intro": "Your config lives at `~/.config/tmux/tmux.conf`. After any change, reload it.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Reload the config", "rows": [("Ctrl-a r", "Reload tmux.conf")],
                         "try": "Edit the file, save, then press `Ctrl-a r`.",
                         "expect": "The change applies to the running session."},
                        {"type": "code", "file": TMUX_CONF, "title": "Colours, format and status text", "code": STATUS_STYLE},
                        {"type": "text", "body": "With `status-left` set to `[#S] `, the left of the bar reads `[main]` in the session called main."},
                        {"type": "keys", "where": "tmux", "title": "Status bar variables", "rows": [
                            ("#S", "Session name"),
                            ("#I", "Window index"),
                            ("#W", "Window name"),
                            ("#P", "Pane index"),
                            ("#H", "Hostname"),
                            ("#T", "Pane title"),
                            ("%H:%M", "Time (24h)"),
                            ("%d/%m", "Date"),
                        ]},
                        {"type": "code", "file": TMUX_CONF, "title": "Status bar position", "code": STATUS_POSITION},
                        {"type": "code", "file": TMUX_CONF, "title": "Pane borders", "code": PANE_BORDERS},
                        {"type": "code", "file": TMUX_CONF, "title": "Activity monitoring", "code": ACTIVITY},
                        {"type": "code", "file": TMUX_CONF, "title": "Useful options", "code": USEFUL_OPTIONS},
                    ],
                },
                {
                    "h2": "Plugins (TPM — tmux plugin manager)",
                    "intro": "TPM installs the rest.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Install TPM", "code": "git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm",
                         "expect": "TPM is cloned into `~/.tmux/plugins/tpm`."},
                        {"type": "code", "file": TMUX_CONF, "title": "Add to the bottom of tmux.conf", "code": PLUGINS},
                        {"type": "keys", "where": "tmux", "title": "Install the plugins", "rows": [("Ctrl-a I", "Install plugins (capital I)")],
                         "try": "Reload with `Ctrl-a r`, then press `Ctrl-a I`.", "expect": "TPM fetches the listed plugins."},
                    ],
                },
                {
                    "h2": "tmux-resurrect (save/restore sessions)",
                    "intro": "Your entire workspace survives reboots: windows, pane layouts, even running commands.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Save and restore", "rows": [
                            ("Ctrl-a Ctrl-s", "Save session (all windows, panes, layout)"),
                            ("Ctrl-a Ctrl-r", "Restore session (after reboot)"),
                        ]},
                        {"type": "code", "file": TMUX_CONF, "title": "Auto-save every 10 minutes", "code": CONTINUUM},
                        {"type": "text", "body": "The reboot problem. Quitting and reopening iTerm2 is fine: the tmux server keeps running. A computer restart kills the server, and nothing restarts it, so nothing restores."},
                        {"type": "text", "body": "The pileup trap. resurrect is not idempotent: every restore trigger re-adds panes. With `@continuum-restore 'on'`, a boot agent and iTerm2 launching tmux, each fires a restore, and the same panes stack 3-6 times into slivers. The fix is exactly one restore, lock-guarded."},
                    ],
                },
                {
                    "h2": "Restore once at login",
                    "intro": "Two small scripts and one launch agent.",
                    "blocks": [
                        {"type": "code", "file": "~/.config/tmux/restore-once.sh", "title": "Lock-guarded: runs at most once per server lifetime", "code": RESTORE_ONCE},
                        {"type": "code", "file": "~/.config/tmux/boot-restore.sh", "title": "Runs at login", "code": BOOT_RESTORE},
                        {"type": "cmd", "where": "shell", "title": "Make both executable", "code": "chmod +x ~/.config/tmux/{restore-once,boot-restore}.sh",
                         "expect": "Both scripts are executable."},
                        {"type": "code", "file": "~/Library/LaunchAgents/com.indamutsa.tmux-restore.plist", "title": "The launch agent", "code": PLIST},
                        {"type": "cmd", "where": "shell", "title": "Load the launch agent", "code": "launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.indamutsa.tmux-restore.plist",
                         "expect": "The agent is loaded and runs `boot-restore.sh` at every login."},
                    ],
                },
                {
                    "h2": "Custom key bindings and colour schemes",
                    "intro": "Add these to `tmux.conf` and reload.",
                    "blocks": [
                        {"type": "code", "file": TMUX_CONF, "title": "Custom key bindings", "code": BINDINGS},
                        {"type": "code", "file": TMUX_CONF, "title": "Colour schemes", "code": SCHEMES},
                    ],
                },
            ],
            "rules": {
                "h2": "Restore after reboot",
                "cards": [
                    ("How it works on boot", "One path, zero pileup.", ["Step", "What happens"], [
                        ["1. Log in", "launchd runs `boot-restore.sh`: starts the server and restores `main` once, lock-guarded"],
                        ["2. Open iTerm2", "`tmux new-session -A -s main` attaches to the restored session"],
                        ["3. No re-runs", "Continuum restore is off and the lock blocks repeats"],
                    ]),
                    ("Gotchas", "Four things that bit.", ["Gotcha", "Fix"], [
                        ["launchd's PATH excludes `/opt/homebrew/bin`, so resurrect's bare `tmux` calls fail silently", "Export PATH in the boot script"],
                        ["`tmux start-server` alone can exit with no session attached", "Anchor it with `new-session -d -s main`"],
                        ["Plist `Label` contains `.plist` or is not reverse-DNS", "Use `com.you.name`"],
                        ["Both `@continuum-restore 'on'` and the boot agent", "That is the pileup. Pick the lock-guarded path"],
                    ]),
                    ("Why not continuum-boot?", "It starts on boot, but opens Terminal.app on every login and still races with iTerm2.", None,
                     "set -g @continuum-boot 'on'    # avoid: opens Terminal.app, races with iTerm2"),
                ],
            },
            "worked": {
                "h2": "Show the session name and the time",
                "frame": "You want the bar to say where you are and what time it is.",
                "given": "Open `~/.config/tmux/tmux.conf` and add two lines.",
                "code": 'set -g status-left "[#S] "\nset -g status-right "%H:%M"',
                "steps": [
                    "Save the file.",
                    "Press `Ctrl-a r` to reload.",
                    "Look at the bar: `[main]` on the left, the time on the right.",
                ],
                "meaning": "`#S` and `%H:%M` are filled in live, so the bar always shows the current session and time.",
            },
            "practice": {
                "h2": "Practice: your config",
                "qs": [
                    ("Mechanism", "Why does a computer restart lose your tmux workspace even when quitting iTerm2 does not?",
                     "Where does the tmux server live?",
                     ["The server runs in the background, outside iTerm2.", "A restart kills the server."],
                     "A restart kills the server, and nothing restarts it."),
                    ("Keystrokes", "Reload the config, then install new plugins.",
                     "Two prefix commands.",
                     ["`Ctrl-a r` reloads.", "`Ctrl-a I` installs, capital I."],
                     "`Ctrl-a r`, then `Ctrl-a I`."),
                    ("Application", "Make window numbering start at 1.",
                     "It is an option in `tmux.conf`.",
                     ["Add `set -g base-index 1`.", "Add `setw -g pane-base-index 1` for panes.", "Reload with `Ctrl-a r`."],
                     "`set -g base-index 1` and `setw -g pane-base-index 1`."),
                    ("Common mistake", "Your restored session shows the same panes stacked 3-6 times. What went wrong?",
                     "Count the restore triggers.",
                     ["resurrect is not idempotent.", "continuum restore, a boot agent and iTerm2 each restored."],
                     "More than one restore ran. Keep only the lock-guarded script."),
                ],
            },
        },
    ],
}
