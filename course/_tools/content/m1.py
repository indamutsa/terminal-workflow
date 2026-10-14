"""Module 1: tmux and the shell. Sources: lessons 01 tmux.md, fzf.md and the quick-start guide."""
from content.common import FZF_HELPERS


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


TMUX_CONF = "~/.config/tmux/tmux.conf"

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

MODULE = {
    "n": 1,
    "folder": "m1-tmux",
    "title": "tmux and the shell",
    "footer": "Sessions, windows and panes; copy mode and fzf; status bar, plugins and restore after reboot",
    "tagline": "Sessions that survive, panes that split, a config that restores.",
    "glossary": [],
    "coverage_allow": [
        ('if [ -z "$TMUX" ]; then', "definition replaced by usage; installed in user's config"),
        ('tmux attach || tmux new -s main', "definition replaced by usage; installed in user's config"),
        ('set -g status-style "bg=#1a1b26,fg=#a9b1d6"', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-current-style "bg=#7aa2f7,fg=#1a1b26,bold"', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-style "bg=#1a1b26,fg=#565f89"', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-format " #I:#W "', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-current-format " #I:#W "', "definition replaced by usage; installed in user's config"),
        ('set -g status-right "#(whoami)@#H | %H:%M"', "definition replaced by usage; installed in user's config"),
        ('set -g status-position top', "definition replaced by usage; installed in user's config"),
        ('set -g status-justify centre', "definition replaced by usage; installed in user's config"),
        ('set -g pane-border-style "fg=#565f89"', "definition replaced by usage; installed in user's config"),
        ('set -g pane-active-border-style "fg=#7aa2f7"', "definition replaced by usage; installed in user's config"),
        ('setw -g monitor-activity on', "definition replaced by usage; installed in user's config"),
        ('set -g visual-activity off', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-activity-style "fg=#e0af68"', "definition replaced by usage; installed in user's config"),
        ('set -g renumber-windows on', "definition replaced by usage; installed in user's config"),
        ('set -g history-limit 50000', "definition replaced by usage; installed in user's config"),
        ('set -g mouse on', "definition replaced by usage; installed in user's config"),
        ('set -sg escape-time 0', "definition replaced by usage; installed in user's config"),
        ('setw -g automatic-rename on', "definition replaced by usage; installed in user's config"),
        ('git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm', "definition replaced by usage; installed in user's config"),
        ("set -g @plugin 'tmux-plugins/tpm'", "definition replaced by usage; installed in user's config"),
        ("set -g @plugin 'tmux-plugins/tmux-sensible'", "definition replaced by usage; installed in user's config"),
        ("set -g @plugin 'tmux-plugins/tmux-resurrect'", "definition replaced by usage; installed in user's config"),
        ("set -g @plugin 'tmux-plugins/tmux-continuum'", "definition replaced by usage; installed in user's config"),
        ("set -g @plugin 'tmux-plugins/tmux-yank'", "definition replaced by usage; installed in user's config"),
        ("run '~/.tmux/plugins/tpm/tpm'", "definition replaced by usage; installed in user's config"),
        ("set -g @continuum-save-interval '10'", "definition replaced by usage; installed in user's config"),
        ("set -g @continuum-restore 'off'", "definition replaced by usage; installed in user's config"),
        ("set -g @resurrect-capture-pane-contents 'on'", "definition replaced by usage; installed in user's config"),
        ("set -g @resurrect-strategy-nvim 'session'", "definition replaced by usage; installed in user's config"),
        ('LOCK="/tmp/tmux-resurrect-restored-$(id -u)"', "definition replaced by usage; installed in user's config"),
        ('[ -f "$LOCK" ] && exit 0', "definition replaced by usage; installed in user's config"),
        ('touch "$LOCK"', "definition replaced by usage; installed in user's config"),
        ('"$HOME/.tmux/plugins/tmux-resurrect/scripts/restore.sh"', "definition replaced by usage; installed in user's config"),
        ('export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"', "definition replaced by usage; installed in user's config"),
        ('TMUX_BIN="/opt/homebrew/bin/tmux"', "definition replaced by usage; installed in user's config"),
        ('rm -f "/tmp/tmux-resurrect-restored-$(id -u)"', "definition replaced by usage; installed in user's config"),
        ('"$TMUX_BIN" has-session 2>/dev/null || "$TMUX_BIN" new-session -d -s main', "definition replaced by usage; installed in user's config"),
        ('sleep 1', "definition replaced by usage; installed in user's config"),
        ('"$HOME/.config/tmux/restore-once.sh"', "definition replaced by usage; installed in user's config"),
        ('<?xml version="1.0" encoding="UTF-8"?>', "definition replaced by usage; installed in user's config"),
        ('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">', "definition replaced by usage; installed in user's config"),
        ('<plist version="1.0">', "definition replaced by usage; installed in user's config"),
        ('<dict>', "definition replaced by usage; installed in user's config"),
        ('<key>Label</key>', "definition replaced by usage; installed in user's config"),
        ('<string>com.indamutsa.tmux-restore</string>', "definition replaced by usage; installed in user's config"),
        ('<key>ProgramArguments</key>', "definition replaced by usage; installed in user's config"),
        ('<array>', "definition replaced by usage; installed in user's config"),
        ('<string>/Users/YOU/.config/tmux/boot-restore.sh</string>', "definition replaced by usage; installed in user's config"),
        ('</array>', "definition replaced by usage; installed in user's config"),
        ('<key>RunAtLoad</key><true/>', "definition replaced by usage; installed in user's config"),
        ('</dict>', "definition replaced by usage; installed in user's config"),
        ('</plist>', "definition replaced by usage; installed in user's config"),
        ('launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.indamutsa.tmux-restore.plist', "definition replaced by usage; installed in user's config"),
        ('set -g status-style "bg=#1a1b26,fg=#a9b1d6"', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-current-style "bg=#7aa2f7,fg=#1a1b26,bold"', "definition replaced by usage; installed in user's config"),
        ('set -g status-style "bg=#1e1e2e,fg=#cdd6f4"', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-current-style "bg=#89b4fa,fg=#1e1e2e,bold"', "definition replaced by usage; installed in user's config"),
        ('set -g status-style "bg=#282828,fg=#ebdbb2"', "definition replaced by usage; installed in user's config"),
        ('set -g window-status-current-style "bg=#fabd2f,fg=#282828,bold"', "definition replaced by usage; installed in user's config"),
        ('alias ff=\'fzf --preview "bat --color=always {}" | xargs nvim\'', "definition replaced by usage; installed in user's config"),
        ("alias fd='cd $(find . -type d | fzf)'", "definition replaced by usage; installed in user's config"),
        ('alias fgl=\'git log --oneline | fzf --preview "git show {1}"\'', "definition replaced by usage; installed in user's config"),
        ('alias fkill=\'ps aux | fzf | awk "{print \\$2}" | xargs kill -9\'', "definition replaced by usage; installed in user's config"),
        ('source ~/.zshrc', "definition replaced by usage; installed in user's config"),
        ("alias tl='tmux list-sessions'", "definition replaced by usage; installed in user's config"),
        ("alias tk='tmux kill-session -t'", "definition replaced by usage; installed in user's config"),
        ('if [ -z "$TMUX" ]; then', "definition replaced by usage; installed in user's config"),
        ('tmux attach || tmux new -s main', "definition replaced by usage; installed in user's config"),
    ],
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
                    "h2": "Start in tmux, list and kill sessions",
                    "intro": "Open a new terminal and it lands in tmux. These shortcuts check where you are, list your sessions, attach to one by name and kill one you are done with.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Check that you are inside tmux", "code": "tmux display -p '#S'",
                         "expect": "The name of your session prints, for example `main`. An error such as `no server running` means you are not inside tmux."},
                        {"type": "cmd", "where": "shell", "title": "List your sessions", "code": "tl",
                         "expect": "One line per session, for example `main: 2 windows (created Mon Oct 12 09:00:00 2026)`."},
                        {"type": "cmd", "where": "shell", "title": "Attach to a session by name, or create it", "code": "to work",
                         "expect": "The `work` session fills the terminal. If it did not exist, tmux creates it. `ta work` attaches only if it exists."},
                        {"type": "cmd", "where": "shell", "title": "Kill a session by name", "code": "tkss work",
                         "expect": "`work` is gone from `tl`. Your other sessions keep running."},
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
                "open": "tmux new -s work",
                "steps": [
                    (None, "`Ctrl-a d`", "Detaches. You are back at the shell; close the terminal if you like."),
                    (None, "`tmux ls`", "In a new terminal, lists `work` as still running."),
                    (None, "`tmux attach`", "Returns to the session."),
                ],
                "after": "work: 1 windows (created Mon Oct 12 09:00:00 2026)",
                "meaning": "Closing a window never ends the work; only killing the session or restarting does.",
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
                "open": "tmux new -s main",
                "steps": [
                    (None, "`Ctrl-a ,` then `editor` then `Enter`", "Names this window."),
                    (None, "`Ctrl-a c` then `Ctrl-a ,` then `tests` then `Enter`", "New window, named."),
                    (None, "`Ctrl-a c` then `Ctrl-a ,` then `agent` then `Enter`", "Third window, named."),
                    (None, "`Ctrl-a w`", "Lists all three with a preview."),
                ],
                "after": "[main]  1:editor   2:tests   3:agent",
                "meaning": "A jump is now one keystroke away.",
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
                    "h2": "Find files, folders and text",
                    "intro": "Find a file, open it, search for a word in the project, jump to a folder or copy a path. Each helper opens a filterable list: type to narrow it, Enter to pick, Esc to cancel.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Open a file by part of its name", "code": "cd ~/tw && ff",
                         "expect": "A list of files with a `bat` preview on the right. Type `ord` and press Enter: `nvim` opens `orders.py`. Press Tab on several files to open them all."},
                        {"type": "cmd", "where": "shell", "title": "Find a PDF anywhere in your home folder", "code": "ffh pdf",
                         "expect": "Every `.pdf` under `~` is listed with a preview. Enter opens the pick in your editor. `ffh` alone lists every file type."},
                        {"type": "cmd", "where": "shell", "title": "Open a file at once when one name matches", "code": "cd ~/tw && fe todo",
                         "expect": "`todo.txt` is the only match, so `nvim` opens it with no list. With several matches a list appears, pre-filtered to `todo`."},
                        {"type": "cmd", "where": "shell", "title": "Find a word in the project and jump to it", "code": "cd ~/tw && frg calc_totl",
                         "expect": "Matching lines list as you type, each with its file and line number. The preview highlights the line. Enter opens `nvim` on that line of `orders.py`."},
                        {"type": "cmd", "where": "shell", "title": "Jump to a folder", "code": "fdir",
                         "expect": "Folders are listed with a tree preview. Enter picks one, and `pwd` shows you are now inside it."},
                        {"type": "cmd", "where": "shell", "title": "Go up to a parent folder", "code": "fcd",
                         "expect": "Your current folder and every folder above it are listed. Enter changes to the one you pick."},
                        {"type": "cmd", "where": "shell", "title": "Open a file with its default app", "code": "cd ~/tw && fopen",
                         "expect": "Pick `notes.md` and macOS opens it in the app set for Markdown. Tab picks several files."},
                        {"type": "cmd", "where": "shell", "title": "Copy a file's path", "code": "cd ~/tw && fscp",
                         "expect": "Pick `orders.py` and the terminal prints `Path copied: ` followed by the full path. Paste it anywhere with `Cmd-v`."},
                        {"type": "text", "body": "`Ctrl-T` does nothing in this setup: it is unbound (`bindkey -r '^T'`) because it clashes with paste in some terminals. Use `ff` instead."},
                    ],
                },
                {
                    "h2": "Git and tmux with fzf",
                    "intro": "Switch a git branch, stage a changed file, browse commits, switch to another tmux session or kill one. Run the git helpers inside a repository.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Switch to another git branch", "code": "fgb",
                         "expect": "Local and remote branches are listed. Type part of a name and press Enter: `git checkout` switches to it."},
                        {"type": "cmd", "where": "shell", "title": "Stage or unstage a changed file", "code": "fgs",
                         "expect": "Changed files are listed with a diff preview. `Ctrl-a` stages the highlighted file and `Ctrl-r` unstages it. The list reloads each time. Esc leaves."},
                        {"type": "cmd", "where": "shell", "title": "Browse the commit history", "code": "fgl",
                         "expect": "A graph of commits with the commit's diff beside it. Enter opens the full diff in `less`; press `q` to come back. `fgl --all` includes every branch."},
                        {"type": "cmd", "where": "shell", "title": "Switch to another tmux session", "code": "ftm",
                         "expect": "Your sessions are listed with a preview of each one's pane. Enter moves you to the one you pick."},
                        {"type": "cmd", "where": "shell", "title": "Kill tmux sessions you pick", "code": "ftmk",
                         "expect": "Tab marks one or more sessions and Enter kills them at once, with no confirmation. `tl` no longer lists them."},
                    ],
                },
                {
                    "h2": "Processes, ports and help",
                    "intro": "Kill a process, free a port that is already in use, look up an environment variable or search a command's help.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Kill a process by name", "code": "fkill",
                         "expect": "Every process is listed under `[kill:process]`. Type `node` and press Enter to kill it with signal 9. `fkill 15` sends the gentler SIGTERM."},
                        {"type": "cmd", "where": "shell", "title": "Kill whatever holds a port", "code": C('''
python3 -m http.server 8000 &
fport 8000
'''),
                         "expect": "The `python3` process holding port 8000 is listed under `[kill:port:8000]`. Press Enter and it stops. `fport` with no number asks you to type the port."},
                        {"type": "cmd", "where": "shell", "title": "Look up an environment variable", "code": "fenv",
                         "expect": "Every variable is listed. Type `PATH` and the matching variables show in full in the preview above the list."},
                        {"type": "cmd", "where": "shell", "title": "Search a command's man page or help text", "code": "fchelp",
                         "expect": "Pick a command such as `curl`, then `help` or `man`, then type to search the text. `Ctrl-b` goes back and `Ctrl-q` quits."},
                        {"type": "cmd", "where": "shell", "title": "Show every helper with an example", "code": "fh",
                         "expect": "A boxed reference lists each helper in this lesson with an example."},
                        {"type": "cmd", "where": "shell", "title": "Find a dev command and put it on the prompt", "code": "devh --pick",
                         "expect": "The dev cheat sheet opens as a list. Enter puts the chosen command on your prompt without running it, so you can fill in placeholders such as `<path>`."},
                    ],
                },
                {
                    "h2": "Every fzf helper at a glance",
                    "intro": "What you want on the left, what to type on the right.",
                    "blocks": [
                        {"type": "keys", "where": "fzf", "title": "fzf helpers: what to type", "rows": FZF_HELPERS},
                    ],
                },
                {
                    "h2": "Pipe anything into fzf",
                    "intro": "Any command's output becomes a filterable list.",
                    "blocks": [
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
                "open": "cd ~/tw && ff",
                "steps": [
                    (None, "`ord`", "The list narrows to one file and `bat` shows a preview."),
                    (None, "`Enter`", "`nvim` opens the file."),
                ],
                "after": "  orders.py\n  1/3\n> ord",
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
                    "h2": "Reload tmux and check a setting",
                    "intro": "tmux reads `~/.config/tmux/tmux.conf`. After you edit it, reload, then ask tmux which values it is using.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Reload the config", "rows": [("Ctrl-a r", "Reload tmux.conf")],
                         "try": "Edit the file, save, then press `Ctrl-a r`.",
                         "expect": "`Config reloaded` flashes in the status bar and the change applies to the running session."},
                        {"type": "cmd", "where": "tmux", "title": "Check that a setting is active", "code": C('''
tmux show -g base-index
tmux show -g history-limit
tmux show -g mouse
'''),
                         "expect": "`base-index 1`, `history-limit 50000` and `mouse on` print, one per line."},
                        {"type": "cmd", "where": "tmux", "title": "Check what the status bar shows", "code": C('''
tmux show -g status-left
tmux show -g status-style
'''),
                         "expect": "`status-left \"[#S] \"` prints, so the left of the bar reads `[main]` in the session called main. `status-style bg=#1a1b26,fg=#a9b1d6` is the bar colour."},
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
                    ],
                },
                {
                    "h2": "Install and update plugins",
                    "intro": "TPM, the tmux plugin manager, is already installed. List what it holds, and install new plugins with one key.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "List your installed plugins", "code": "ls ~/.tmux/plugins",
                         "expect": "One folder per plugin: `tpm`, `tmux-sensible`, `tmux-resurrect`, `tmux-continuum`, `tmux-yank` and `tmux-sidebar`."},
                        {"type": "keys", "where": "tmux", "title": "Install the plugins", "rows": [("Ctrl-a I", "Install plugins (capital I)")],
                         "try": "Add a `set -g @plugin` line to `tmux.conf`, reload with `Ctrl-a r`, then press `Ctrl-a I`.", "expect": "TPM fetches the listed plugins."},
                    ],
                },
                {
                    "h2": "Save and restore your workspace",
                    "intro": "Your entire workspace survives reboots: windows, pane layouts, even running commands.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Save and restore", "rows": [
                            ("Ctrl-a Ctrl-s", "Save session (all windows, panes, layout)"),
                            ("Ctrl-a Ctrl-r", "Restore session (after reboot)"),
                        ]},
                        {"type": "cmd", "where": "shell", "title": "Check that tmux is saving your sessions", "code": C('''
ls ~/.local/share/tmux/resurrect | tail -3
tmux show -g @continuum-save-interval
'''),
                         "expect": "The newest saves are `tmux_resurrect_` files named with a date and time, no more than 10 minutes old while tmux runs. `@continuum-save-interval 10` is the save interval in minutes."},
                        {"type": "text", "body": "The reboot problem. Quitting and reopening iTerm2 is fine: the tmux server keeps running. A computer restart kills the server, and nothing restarts it, so nothing restores."},
                        {"type": "text", "body": "The pileup trap. resurrect is not idempotent: every restore trigger re-adds panes. With `@continuum-restore 'on'`, a boot agent and iTerm2 launching tmux, each fires a restore, and the same panes stack 3-6 times into slivers. The fix is exactly one restore, lock-guarded."},
                    ],
                },
                {
                    "h2": "Check the restore after a reboot",
                    "intro": "A launch agent runs two small scripts at login so the restore happens exactly once. Check that each part is in place.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Check that both restore scripts are executable", "code": "ls -l ~/.config/tmux/*.sh",
                         "expect": "`boot-restore.sh` and `restore-once.sh` are listed, each starting with `-rwxr-xr-x`."},
                        {"type": "cmd", "where": "shell", "title": "Check that the login launch agent is loaded", "code": "launchctl list | grep tmux-restore",
                         "expect": "One line ending in `com.indamutsa.tmux-restore`. A `0` before the name means the last run exited cleanly."},
                        {"type": "cmd", "where": "shell", "title": "Check that the restore ran once", "code": "ls /tmp/tmux-resurrect-restored-$(id -u)",
                         "expect": "After login the lock file is listed: the restore already ran for this boot and will not run again. `No such file` means no restore has run since login."},
                    ],
                },
                {
                    "h2": "Add your own key binding",
                    "intro": "Add a line to `tmux.conf`, reload, then ask tmux for the binding.",
                    "blocks": [
                        {"type": "code", "file": TMUX_CONF, "title": "Custom key bindings", "code": BINDINGS},
                        {"type": "cmd", "where": "tmux", "title": "Check a key binding", "code": "tmux list-keys -T prefix r",
                         "expect": "One `bind-key` line for the `prefix` table and key `r`: the reload binding, `source-file` followed by your `tmux.conf` path."},
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
                "open": "nvim ~/.config/tmux/tmux.conf",
                "steps": [
                    (None, "`G` `o` then `set -g status-left \"[#S] \"` then `Esc`", "Adds the left side."),
                    (None, "`o` then `set -g status-right \"%H:%M\"` then `Esc`", "Adds the right side."),
                    (None, "`:w`", "Saves the file."),
                    (None, "`Ctrl-a r`", "Reloads the config."),
                ],
                "after": "[main]                          09:41",
                "meaning": "`#S` and `%H:%M` fill in live, so the bar always shows the session and the time.",
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
