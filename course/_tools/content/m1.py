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
    "title": "Keep your work running with tmux and fzf",
    "footer": "Keep sessions running, split panes, copy text, find files with fzf and restore tmux after a reboot",
    "tagline": "Keep work running, split the screen into panes, and restore it all after a reboot.",
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
        ("Ctrl-a 0", "lesson counts windows from 0; your tmux.conf sets base-index 1, so the first window is Ctrl-a 1"),
        ("Ctrl-a 0-9", "lesson counts windows from 0; your tmux.conf sets base-index 1, so the range is Ctrl-a 1-9"),
        ("alias tl='tmux list-sessions'", "definition replaced by usage; installed in user's config"),
        ("alias tk='tmux kill-session -t'", "definition replaced by usage; installed in user's config"),
        ('if [ -z "$TMUX" ]; then', "definition replaced by usage; installed in user's config"),
        ('tmux attach || tmux new -s main', "definition replaced by usage; installed in user's config"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Keep your work running after you close the terminal",
            "subtitle": "Start a tmux session, leave it running (detach), get it back, list your sessions, rename a session, kill a session",
            "idea": (
                "Keep your work running after you close the terminal window: run it inside tmux.",
                [
                    ("Start a named tmux session", "tmux new -s main", "Opens a session named main."),
                    ("Send a command to tmux (prefix key)", "Ctrl-a", "Press it first. The next key is a tmux command."),
                    ("Leave tmux but keep everything running (detach)", "Ctrl-a d", "The session keeps running."),
                    ("Get your session back (reattach)", "tmux attach", "Brings back everything where you left it."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why did my running processes die when I closed the terminal or the laptop went to sleep?",
                "fix": "Run everything inside a tmux session. Detach with `Ctrl-a d`, and `tmux attach` brings it all back.",
            },
            "drills": [
                {
                    "h2": "Start a tmux session",
                    "intro": "Open iTerm2 and type this to start a tmux session.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Start a tmux session with a name", "code": "tmux new -s main",
                         "expect": "A tmux status bar appears at the bottom with `[main]` on the left."},
                    ],
                },
                {
                    "h2": "Send a command to tmux (the prefix key)",
                    "intro": "Give tmux a command: press the prefix key first. Yours is `Ctrl-a`: hold Ctrl, tap a, release both, then press the command key.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Open a new window in tmux", "rows": [("Ctrl-a then c", "Open a new window")],
                         "try": "Press `Ctrl-a`, let go, then press `c`.",
                         "expect": "A second window appears in the status bar and you are on it. Windows are numbered from 1 here (`base-index 1`)."},
                    ],
                },
                {
                    "h2": "Leave tmux but keep everything running (detach)",
                    "intro": "Leave a session running and come back to it later. Sessions survive crashes, reboots and SSH disconnects.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Leave tmux but keep everything running (detach)", "rows": [("Ctrl-a d", "Leave tmux and keep the session running (detach)")],
                         "try": "Press `Ctrl-a d`.",
                         "expect": "You are back at a bare terminal. The session is alive in the background."},
                        {"type": "cmd", "where": "shell", "title": "Get your session back (reattach)", "code": "tmux attach",
                         "expect": "Everything is exactly where you left it."},
                    ],
                },
                {
                    "h2": "Create, list, switch to and kill sessions",
                    "intro": "Keep one session per project.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create, list, switch to and kill a session", "code": C('''
tmux new -s work          # create named session
tmux new -s personal      # another session
tmux ls                   # list all sessions
tmux switch -t work       # switch to session "work"
tmux kill-session -t old  # kill a session
'''),
                         "expect": "`tmux ls` lists every session by name, and `tmux switch -t work` moves you to work."},
                        {"type": "keys", "where": "tmux", "title": "Switch to another session without leaving tmux", "rows": [
                            ("Ctrl-a s", "Pick a session from a list (like Ctrl-a w but for sessions)"),
                            ("Ctrl-a (", "Go to the previous session"),
                            ("Ctrl-a )", "Go to the next session"),
                        ], "try": "Press `Ctrl-a s`.", "expect": "A picker lists your sessions."},
                        {"type": "keys", "where": "tmux", "title": "Rename the session you are in", "rows": [
                            ("Ctrl-a $", "Rename the session: type the new name and press Enter"),
                        ], "try": "Press `Ctrl-a $`, replace the old name with `project` and press `Enter`.",
                         "expect": "The status bar left now reads `[project]`."},
                        {"type": "cmd", "where": "shell", "title": "Rename any session from the shell", "code": "tmux rename-session -t work project",
                         "expect": "`tmux ls` lists `project` where `work` was. Use `tmux rename-session project` with no `-t` to rename the session you are in."},
                    ],
                },
                {
                    "h2": "Start, attach to and kill a session with short aliases",
                    "intro": "Start tmux from a new terminal: it opens a plain shell, and nothing starts tmux for you. From that plain shell, start or attach with `to`, `ts`, `tds` or `ta`, list with `tl`, and kill with `tkss` or `tksv`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Check if you are inside tmux", "code": "tmux display -p '#S'",
                         "expect": "The name of your session prints, for example `main`. An error such as `no server running` means you are not inside tmux."},
                        {"type": "cmd", "where": "shell", "title": "List all tmux sessions", "code": "tl",
                         "expect": "One line per session, for example `main: 2 windows (created Mon Oct 12 09:00:00 2026)`."},
                        {"type": "cmd", "where": "shell", "title": "Attach to a session by name, or create it if it is missing", "code": "to work",
                         "expect": "The `work` session fills the terminal. If it did not exist, tmux creates it."},
                        {"type": "cmd", "where": "shell", "title": "Start a new named session", "code": "ts work",
                         "expect": "A fresh session called `work` opens. If `work` already exists tmux says so and does not attach: use `to work` instead."},
                        {"type": "cmd", "where": "shell", "title": "Start a session named after the current folder", "code": "cd ~/tw && tds",
                         "expect": "A new session called `tw` opens, named after the folder you were in."},
                        {"type": "cmd", "where": "shell", "title": "Attach to a session that already exists", "code": "ta work",
                         "expect": "The `work` session fills the terminal. If `work` does not exist tmux reports an error and nothing changes."},
                        {"type": "cmd", "where": "shell", "title": "Attach and disconnect every other terminal from the session", "code": "tad work",
                         "expect": "You are in `work`, and any other terminal that was attached to it is detached."},
                        {"type": "cmd", "where": "shell", "title": "Kill a session by name", "code": "tkss work",
                         "expect": "`work` is gone from `tl`. Your other sessions keep running."},
                        {"type": "cmd", "where": "shell", "title": "Kill every tmux session at once", "code": "tksv",
                         "expect": "The tmux server stops and every session ends with it. `tl` then reports that no server is running."},
                        {"type": "text", "body": "Inside tmux, `to`, `ts`, `tds`, `ta` and `tad` refuse to nest one session in another. Switch with `Ctrl-a s` or `ftm` instead."},
                    ],
                },
                {
                    "h2": "Look up what each session alias does",
                    "intro": "Forgot what an alias does? Print the reference.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Show every tmux alias and what it does", "code": "th",
                         "expect": "A table of aliases, the command each one runs and a one-line description: `ta`, `tad`, `to`, `ts`, `tl`, `tkss`, `tksv`, `tds` and `tmuxconf`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which command starts, lists, switches or kills a session?",
                "cards": [
                    ("Manage tmux sessions", "Run these in a shell.", ["Command", "Does"], [
                        ["`tmux new -s main`", "Start a named session"],
                        ["`tmux attach`", "Get the session back (reattach)"],
                        ["`tmux ls`", "List all sessions"],
                        ["`tmux switch -t work`", "Switch to session work"],
                        ["`tmux kill-session -t old`", "Kill a session"],
                        ["`Ctrl-a $`", "Rename the session"],
                    ]),
                    ("Shorter commands for the same jobs (aliases)", "Use these in place of the long commands.", ["Alias", "Does"], [
                        ["`to work`", "Attach to a session, or create it"],
                        ["`ts work`", "Start a new named session"],
                        ["`tds`", "Start a session named after this folder"],
                        ["`ta work` / `tad work`", "Attach / attach and detach other terminals"],
                        ["`tl`", "List sessions"],
                        ["`tkss work` / `tksv`", "Kill one session / kill every session"],
                        ["`th`", "Show this table in the terminal"],
                    ]),
                    ("Why does the prefix key do nothing?", "Make sure you are inside tmux: the status bar is visible.", ["Step", "Command"], [
                        ["Not in tmux? Attach", "`tmux attach`"],
                        ["Reload the config", "`tmux source-file ~/.config/tmux/tmux.conf`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Close the terminal and come back to your session later",
                "frame": "Stop for the day and keep your work waiting.",
                "open": "tmux new -s work",
                "steps": [
                    (None, "`Ctrl-a d`", "Leave tmux (detach). You are back at the shell; close the terminal if you like."),
                    (None, "`tmux ls`", "In a new terminal, lists `work` as still running."),
                    (None, "`tmux attach`", "Get the session back."),
                ],
                "after": "work: 1 windows (created Mon Oct 12 09:00:00 2026)",
                "meaning": "Does closing the terminal stop my work? No: only killing the session or restarting does.",
            },
            "practice": {
                "h2": "Check yourself: keep work running in tmux sessions",
                "qs": [
                    ("Mechanism", "Why does my session keep running after I detach?",
                     "Who owns the processes: the window or tmux?",
                     ["tmux runs your shells, not the terminal window.", "Detach only closes your view of the session."],
                     "tmux keeps the processes alive; the window was only a view."),
                    ("Keystrokes", "How do I leave a session without stopping it?",
                     "Prefix first, then one letter.",
                     ["Press `Ctrl-a`.", "Press `d`."],
                     "`Ctrl-a d`."),
                    ("Application", "How do I make a separate named session for each of two projects?",
                     "Use `tmux new -s` with a name.",
                     ["Run `tmux new -s work`.", "Run `tmux new -s personal`.", "List them with `tmux ls`."],
                     "`tmux new -s work` and `tmux new -s personal`."),
                    ("Common mistake", "Why does the prefix key do nothing? What do I check first?",
                     "Where are you typing?",
                     ["Look for the tmux status bar.", "No bar means you are not inside tmux: run `tmux attach`."],
                     "Make sure you are inside tmux."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Split your terminal into windows and panes",
            "subtitle": "Open a new window, switch windows, split the screen side by side or top and bottom, zoom one pane, resize panes",
            "idea": (
                "Run several jobs in one terminal: a session holds windows, and a window holds panes.",
                [
                    ("Open a window for each job", "Ctrl-a c", "One window per job: editor, tests, agent."),
                    ("Switch to another window", "Ctrl-a w", "A picker with a live preview."),
                    ("Split the screen side by side", "Ctrl-a |", "Two panes side by side."),
                    ("Make one pane fill the screen (zoom)", "Ctrl-a z", "One pane fills the screen. Press again to unzoom."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I run an editor, tests and an AI agent in one terminal? They fight for the same screen.",
                "fix": "Give each job its own window, and split a window into panes to see two things at once.",
            },
            "drills": [
                {
                    "h2": "Switch between windows",
                    "intro": "Switch between editor, tests and your AI agent with these keys.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Jump to another window", "rows": [
                            ("Ctrl-a 1", "Jump to window 1, your first window"),
                            ("Ctrl-a 2", "Jump to window 2"),
                            ("Ctrl-a n", "Go to the next window"),
                            ("Ctrl-a p", "Go to the previous window"),
                            ("Ctrl-a w", "Pick a window from a list (preview, pick with j/k + Enter)"),
                        ], "try": "Press `Ctrl-a w`.",
                         "expect": "All windows are listed with a live preview. Press Enter to jump."},
                        {"type": "text", "body": "Which key is my first window? Windows start at 1 here (`base-index 1`), so `Ctrl-a 1` is your first window."},
                    ],
                },
                {
                    "h2": "Split a window into panes",
                    "intro": "See two things at once: split your window, run `ls` in one pane and `htop` in the other.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Split the screen and move between panes", "rows": [
                            ("Ctrl-a |", "Split the pane side by side (vertical split)"),
                            ("Ctrl-a -", "Split the pane top and bottom (horizontal split)"),
                            ("Ctrl-a h/j/k/l", "Move to the pane on the left / below / above / on the right (vim-style)"),
                            ("Ctrl-a x", "Close the pane (prompts y/n: press y to confirm)"),
                        ], "try": "Split, then move with `Ctrl-a h` and `Ctrl-a l`. Or click the pane you want: the mouse is on.",
                         "expect": "Two panes, each with its own shell."},
                        {"type": "text", "body": "Switch panes without the prefix: inside tmux, `Ctrl-h`, `Ctrl-j`, `Ctrl-k` and `Ctrl-l` also switch panes."},
                    ],
                },
                {
                    "h2": "Zoom, resize, swap and rename windows and panes",
                    "intro": "Resize with capital H/J/K/L. Move with lowercase h/j/k/l.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Zoom a pane, swap panes or move a pane to its own window", "rows": [
                            ("Ctrl-a z", "Make the pane fill the screen (press again to unzoom)"),
                            ("Ctrl-a Space", "Rearrange the panes: cycle through layouts (even, tiled, etc.)"),
                            ("Ctrl-a !", "Move the pane into its own window"),
                            ("Ctrl-a q", "Jump to a pane by number: numbers appear, press one"),
                            ("Ctrl-a {", "Swap the pane with the previous one"),
                            ("Ctrl-a }", "Swap the pane with the next one"),
                            ("Ctrl-a o", "Go to the next pane"),
                            ("Ctrl-a ;", "Go back to the last pane"),
                            (":swap-pane -t 2", "Swap current pane with pane 2 (tmux command)"),
                        ], "try": "Press `Ctrl-a z` in a split window, then press it again.",
                         "expect": "One pane fills the screen. The second press brings the split back."},
                        {"type": "keys", "where": "tmux", "title": "Make a pane bigger or smaller", "rows": [
                            ("Ctrl-a H", "Resize the pane left (5 cells)"),
                            ("Ctrl-a J", "Resize the pane down (5 cells)"),
                            ("Ctrl-a K", "Resize the pane up (5 cells)"),
                            ("Ctrl-a L", "Resize the pane right (5 cells)"),
                        ]},
                        {"type": "keys", "where": "tmux", "title": "Open a system monitor pane, or close every other pane", "rows": [
                            ("Ctrl-a m", "Open a 12-line pane below running htop (system monitor)"),
                            ("Ctrl-a M", "Close every other pane and keep this one (kill other panes), no confirmation"),
                        ], "try": "Press `Ctrl-a m`, then `q` inside htop.",
                         "expect": "A 12-line pane with htop opens under your pane. `q` quits htop and the pane closes."},
                        {"type": "keys", "where": "tmux", "title": "Open, rename, close and find windows", "rows": [
                            ("Ctrl-a c", "Open a new window"),
                            ("Ctrl-a ,", "Rename the window"),
                            ("Ctrl-a &", "Close (kill) the window (confirms y/n)"),
                            ("Ctrl-a .", "Move the window to another number (index)"),
                            ("Ctrl-a f", "Find a window by name"),
                        ], "try": "Press `Ctrl-a ,` and type `editor`.",
                         "expect": "The status bar shows `editor` instead of `zsh`."},
                        {"type": "cmd", "where": "shell", "title": "Run a command in another window without switching to it", "code": C('''
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
                "h2": "The 13 window and pane keys to practise",
                "cards": [
                    ("Practise each key 10 times", "These 13 keys carry most of your day.", ["Command", "What it does"], [
                        ["`Ctrl-a c`", "Open a new window"],
                        ["`Ctrl-a w`", "Pick a window from a list (preview)"],
                        ["`Ctrl-a 1-9`", "Jump to window by number (windows start at 1)"],
                        ["`Ctrl-a n/p`", "Go to the next/previous window"],
                        ["`Ctrl-a ,`", "Rename the current window"],
                        ["`Ctrl-a d`", "Leave tmux but keep it running (detach)"],
                        ["`Ctrl-a |`", "Split side by side (vertical split)"],
                        ["`Ctrl-a -`", "Split top and bottom (horizontal split)"],
                        ["`Ctrl-a h/j/k/l`", "Move to the pane left / down / up / right"],
                        ["`Ctrl-a z`", "Make the pane fill the screen, or undo it (zoom)"],
                        ["`Ctrl-a q`", "Jump to a pane by number (tap the number)"],
                        ["`Ctrl-a x`", "Close pane (y to confirm)"],
                        ["`Ctrl-a [`", "Start copying text (copy mode)"],
                    ]),
                    ("Move or resize a pane? Lowercase or capital", "Same letters, two jobs.", ["Keys", "Does"], [
                        ["`Ctrl-a h/j/k/l`", "Move to the pane left / down / up / right"],
                        ["`Ctrl-a H/J/K/L`", "Resize the pane by 5 cells"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Run an editor, tests and an agent in one tmux session",
                "frame": "Three jobs, three windows, one session.",
                "open": "tmux new -s main",
                "steps": [
                    (None, "`Ctrl-a ,` then `editor` then `Enter`", "Name this window."),
                    (None, "`Ctrl-a c` then `Ctrl-a ,` then `tests` then `Enter`", "Open a new window and name it."),
                    (None, "`Ctrl-a c` then `Ctrl-a ,` then `agent` then `Enter`", "Open a third window and name it."),
                    (None, "`Ctrl-a w`", "List all three windows with a preview."),
                ],
                "after": "[main]  1:editor   2:tests   3:agent",
                "meaning": "How do I jump between jobs? Each one is now one keystroke away.",
            },
            "practice": {
                "h2": "Check yourself: windows and panes",
                "qs": [
                    ("Mechanism", "What is the difference between a window and a pane in tmux?",
                     "One lives inside the other.",
                     ["A window fills the screen.", "Panes divide one window into rectangles."],
                     "A window holds one or more panes."),
                    ("Keystrokes", "How do I split a window side by side, then close the new pane?",
                     "Split first, then close.",
                     ["Press `Ctrl-a |`.", "Press `Ctrl-a x`, then `y`."],
                     "`Ctrl-a |`, then `Ctrl-a x` and `y`."),
                    ("Application", "How do I read a long test run without leaving the pane?",
                     "Fill the screen with one pane.",
                     ["Press `Ctrl-a z` to zoom.", "Press `Ctrl-a z` again to unzoom."],
                     "`Ctrl-a z` twice."),
                    ("Common mistake", "Why did `Ctrl-a L` make the pane bigger instead of moving right?",
                     "Look at the letter case.",
                     ["Capital `H/J/K/L` resizes.", "Lowercase `h/j/k/l` navigates."],
                     "Use lowercase `l` to move, capital `L` to resize."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Copy text, edit the command line fast and find files with fzf",
            "subtitle": "Copy text from the terminal, delete a word or line at the prompt, search your command history, find a file, switch a git branch, kill a process",
            "idea": (
                "Skip the mouse: copy text in copy mode, edit the prompt with readline keys, find things with fzf.",
                [
                    ("Copy text from the terminal (copy mode)", "Ctrl-a [", "Move through scrollback with vim keys."),
                    ("Clear the whole line", "Ctrl-u", "Deletes the whole line."),
                    ("Find a file by typing a few letters (fuzzy find)", "fzf", "A filterable list of files."),
                    ("Search your command history", "Ctrl+R", "Find a past command and paste it at the prompt."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I copy terminal output without grabbing half a border, or retyping a long path from history?",
                "fix": "Copy with copy mode, edit the prompt with readline keys, and find files, history and branches with fzf.",
            },
            "drills": [
                {
                    "h2": "Copy text from the terminal and paste it (copy mode)",
                    "intro": "Copy any text on screen or in the scrollback: copy mode gives you a free-moving cursor there.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Copy text with the keyboard and paste it", "rows": [
                            ("Ctrl-a [", "Start copying text: enter copy mode (cursor becomes free-moving)"),
                            ("h/j/k/l or Ctrl-d/Ctrl-u", "Move the cursor"),
                            ("Alt-f / Alt-b", "Jump to the end of the next word / the start of the previous word"),
                            ("v", "Start selecting text (visual mode)"),
                            ("y", "Copy the selection (yank) and exit copy mode"),
                            ("Ctrl-a ]", "Paste the copied text"),
                            ("q", "Quit copy mode without copying"),
                            ("Esc", "Leave copy mode too"),
                        ], "try": "Press `Ctrl-a [`, move with `j`, press `v`, move, press `y`, then `Ctrl-a ]`.",
                         "expect": "The copied text appears at the prompt."},
                        {"type": "keys", "where": "tmux", "title": "Copy text with the mouse", "rows": [
                            ("Mouse drag", "Copy text: drag over it and let go, it goes to the macOS clipboard and copy mode ends"),
                        ], "try": "Drag across a line of output and release the button.",
                         "expect": "The highlight clears at once and the text is on the clipboard: `Cmd-v` pastes it."},
                    ],
                },
                {
                    "h2": "Delete a word or jump around the command line",
                    "intro": "Edit the command you are typing: these readline keys work at any shell prompt, in tmux, zsh or bash. They replace Cmd+Delete and Option+Delete.",
                    "blocks": [
                        {"type": "keys", "where": "shell", "title": "Delete a line or word and jump to the start or end of the line", "rows": [
                            ("Ctrl-u", "Delete the whole line (like Cmd+Delete)"),
                            ("Ctrl-w", "Delete the word before the cursor (like Option+Delete)"),
                            ("Ctrl-k", "Erase everything from the cursor to the end of the line"),
                            ("Ctrl-a", "Jump to the start of the line"),
                            ("Ctrl-e", "Jump to the end of the line"),
                            ("Ctrl-h", "Delete the character before the cursor (Backspace)"),
                            ("Alt-d", "Delete the word after the cursor"),
                            ("Alt-b", "Jump back one word"),
                            ("Alt-f", "Jump forward one word"),
                        ], "try": "Type a few words, then press `Ctrl-w` and `Ctrl-u`.",
                         "expect": "`Ctrl-w` removes the last word. `Ctrl-u` clears the line."},
                        {"type": "text", "body": "Why does `Ctrl-a` not jump to the start of the line in tmux? Inside tmux, `Ctrl-a` is the prefix: press `Ctrl-a Ctrl-a` to reach the start of the line. In a pane that is not running vim, `Ctrl-h`, `Ctrl-j`, `Ctrl-k` and `Ctrl-l` switch panes instead."},
                        {"type": "keys", "where": "shell", "title": "Break a long command onto a new line without running it", "rows": [
                            ("Option-Enter", "Start a new line in the shell: break a long command onto the next line without running it"),
                            ("Shift-Enter", "Same, when your terminal sends it (iTerm needs the key mapped to CSI-u)"),
                        ], "try": "Type `python3 ~/tw/orders.py`, then press `Option-Enter`.",
                         "expect": "The cursor drops to a new line and the command does not run. `Enter` on the last line runs the whole thing."},
                        {"type": "keys", "where": "shell", "title": "Accept the grey command suggestion", "rows": [
                            ("Ctrl-Space", "Accept the suggestion: take the grey history text after the cursor"),
                        ], "try": "Type `python3 ~/tw/or` after you have run that command once, then press `Ctrl-Space`.",
                         "expect": "The grey rest of the command turns into real text. Press `Enter` to run it."},
                    ],
                },
                {
                    "h2": "Find a file or past command by typing a few letters (fzf)",
                    "intro": "Find anything in a list by typing part of it: type to filter, Enter to pick.",
                    "blocks": [
                        {"type": "cmd", "where": "fzf", "title": "Search files, command history and processes with fzf", "code": C('''
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
                        {"type": "keys", "where": "fzf", "title": "Move, pick, cancel and preview in the fzf list", "rows": [
                            ("Ctrl+J/K", "Move up or down the list"),
                            ("↑/↓", "Move up or down the list"),
                            ("Enter", "Pick the highlighted line"),
                            ("Ctrl+C", "Cancel and close the list"),
                            ("Esc", "Cancel and close the list"),
                            ("Tab", "Select several lines (multi-select)"),
                            ("Ctrl+/", "Change the preview layout: cycles preview right, below and hidden"),
                            ("Ctrl+U / Ctrl+D", "Scroll the preview up / down half a page"),
                            ("Ctrl+Y", "Copy the picked names to the clipboard and close the list"),
                        ], "try": "Run `fzf`, move to a file and press `Ctrl+Y`.",
                         "expect": "The list closes and nothing opens. The file name is on the clipboard: `Cmd-v` pastes it."},
                        {"type": "text", "body": "Why does `Ctrl+J/K` switch panes instead of moving in fzf? In tmux, use the arrow keys: `Ctrl+J/K` switch panes there. In this setup `Ctrl+D` scrolls the preview and no key selects all."},
                    ],
                },
                {
                    "h2": "List files with sizes and see which folder is biggest",
                    "intro": "List files, hidden files and folder sizes: `ls`, `ll`, `la` and `lt` all run eza with icons. The size helpers wrap `du`. Try them on the practice folder.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "List files with sizes and dates, hidden ones too", "code": "ll ~/tw",
                         "expect": "One line per entry: permissions, size, date and name, each name with an icon. `orders.py`, `notes.md` and `todo.txt` are listed."},
                        {"type": "cmd", "where": "shell", "title": "List files including hidden ones", "code": "la ~/tw",
                         "expect": "Just the names, with dotfiles included."},
                        {"type": "cmd", "where": "shell", "title": "List a folder as a tree", "code": "lt ~/tw",
                         "expect": "A tree with `orders.py`, `notes.md` and `todo.txt` under `tw`."},
                        {"type": "cmd", "where": "shell", "title": "Show the size of one file or folder", "code": "size ~/tw/orders.py",
                         "expect": "One line: the size, then the path."},
                        {"type": "cmd", "where": "shell", "title": "Show sizes of the non-hidden items in a folder, biggest first", "code": "sizes ~/tw",
                         "expect": "One line per non-hidden item in `tw`, sorted from largest to smallest."},
                        {"type": "cmd", "where": "shell", "title": "Show the size of the current folder", "code": "cd ~/tw && dirsize",
                         "expect": "One line: the total size, then `.`."},
                        {"type": "cmd", "where": "shell", "title": "Show the ten biggest non-hidden items here", "code": "cd ~/tw && big",
                         "expect": "At most ten lines, largest first."},
                        {"type": "text", "body": "Why is the output of `grep`, `egrep`, `fgrep`, `diff`, `less` and `tree` coloured? They are aliased to colour their output. Use them as usual."},
                    ],
                },
                {
                    "h2": "Find a file, a folder or a word in your project",
                    "intro": "Find a file, open it, search for a word in the project, jump to a folder or copy a path. Each helper opens a filterable list: type to narrow it, Enter to pick, Esc to cancel.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find a file by part of its name", "code": "cd ~/tw && ff",
                         "expect": "A list of files with a `bat` preview on the right. Type `ord` and press Enter: `nvim` opens `orders.py`. Press Tab on several files to open them all."},
                        {"type": "cmd", "where": "shell", "title": "Find a PDF anywhere in your home folder", "code": "ffh pdf",
                         "expect": "Every `.pdf` under `~` is listed with a preview. Enter opens the pick in your editor. `ffh` alone lists every file type."},
                        {"type": "cmd", "where": "shell", "title": "Open a file at once when one name matches", "code": "cd ~/tw && fe todo",
                         "expect": "`todo.txt` is the only match, so `nvim` opens it with no list. With several matches a list appears, pre-filtered to `todo`."},
                        {"type": "cmd", "where": "shell", "title": "Find a word in the project and jump to it", "code": "cd ~/tw && frg calc_totl",
                         "expect": "Matching lines list as you type, each with its file and line number. The preview highlights the line. Enter opens `nvim` on that line of `orders.py`."},
                        {"type": "cmd", "where": "shell", "title": "Find any file, hidden and ignored ones too", "code": "cd ~/tw && fa",
                         "expect": "Every file under the folder is listed, dotfiles and git-ignored files included, but not `.git`. Enter opens the pick in `nvim`."},
                        {"type": "cmd", "where": "shell", "title": "Open a single file from a list", "code": "cd ~/tw && fv",
                         "expect": "A list of files with a preview. Enter without marking files opens the highlighted file in `nvim`."},
                        {"type": "cmd", "where": "shell", "title": "Find a word and open the match in VS Code", "code": "cd ~/tw && frc TODO",
                         "expect": "The matching lines list as you type. Enter opens VS Code on that line of the file."},
                        {"type": "cmd", "where": "shell", "title": "Open files in VS Code", "code": "cd ~/tw && fcode",
                         "expect": "Pick `orders.py` and VS Code opens it. Tab picks several files."},
                        {"type": "cmd", "where": "shell", "title": "Jump to a folder", "code": "fdir",
                         "expect": "Folders are listed with a tree preview. Enter picks one, and `pwd` shows you are now inside it."},
                        {"type": "cmd", "where": "shell", "title": "Go up to a parent folder", "code": "fcd",
                         "expect": "Your current folder and every folder above it are listed. Enter changes to the one you pick."},
                        {"type": "cmd", "where": "shell", "title": "Open a file with its default app", "code": "cd ~/tw && fopen",
                         "expect": "Pick `notes.md` and macOS opens it in the app set for Markdown. Tab picks several files."},
                        {"type": "cmd", "where": "shell", "title": "Copy a file's path", "code": "cd ~/tw && fscp",
                         "expect": "Pick `orders.py` and the terminal prints `Path copied: ` followed by the full path. Paste it anywhere with `Cmd-v`."},
                        {"type": "cmd", "where": "shell", "title": "Copy a file's content", "code": "cd ~/tw && fsc",
                         "expect": "Pick `notes.md` and the terminal prints `Content of 'notes.md' copied to clipboard`. `Cmd-v` pastes the whole file."},
                        {"type": "text", "body": "Why does `Ctrl-T` do nothing? It is unbound in this setup (`bindkey -r '^T'`) because it clashes with paste in some terminals. Use `ff` instead."},
                    ],
                },
                {
                    "h2": "Switch a git branch, stage a file or switch a tmux session from a list",
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
                    "h2": "Delete files and folders you pick",
                    "intro": "Both helpers list what you picked and ask `y/N` before deleting. Answer `N` to practise safely.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Delete files you pick", "code": "cd ~/tw && fsd",
                         "expect": "Tab marks files and Enter lists `Delete: todo.txt`, then asks `Delete these files? (y/N)`. `N` prints `Cancelled` and nothing is removed."},
                        {"type": "cmd", "where": "shell", "title": "Delete folders you pick", "code": "cd ~ && fsdd",
                         "expect": "Pick a folder and Enter lists it after `Delete:`, then asks `Delete these directories? (y/N)`. `N` prints `Cancelled`. `y` removes the folder and everything in it."},
                    ],
                },
                {
                    "h2": "Kill a process, free a port and look up a command's help",
                    "intro": "Kill a process, free a port that is already in use, look up an environment variable or search a command's help.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Kill a process by name", "code": "fkill",
                         "expect": "Every process is listed under `[kill:process]`. Type `node` and press Enter to kill it with signal 9. `fkill 15` sends the gentler SIGTERM."},
                        {"type": "cmd", "where": "shell", "title": "Free a port that is already in use (kill what holds it)", "code": C('''
python3 -m http.server 8000 &
fport 8000
'''),
                         "expect": "The `python3` process holding port 8000 is listed under `[kill:port:8000]`. Press Enter and it stops. `fport` with no number asks you to type the port."},
                        {"type": "cmd", "where": "shell", "title": "Look up an environment variable", "code": "fenv",
                         "expect": "Every variable is listed. Type `PATH` and the matching variables show in full in the preview above the list."},
                        {"type": "cmd", "where": "shell", "title": "Search a command's man page or help text", "code": "fchelp",
                         "expect": "Pick a command such as `curl`, then `help` or `man`, then type to search the text. `Ctrl-b` goes back and `Ctrl-q` quits."},
                        {"type": "cmd", "where": "shell", "title": "Pick a docker container", "code": "fdocker",
                         "expect": "Every container, running or not, is listed with its last 100 log lines as a preview. Enter prints the container ID."},
                        {"type": "cmd", "where": "shell", "title": "Show every fzf helper with an example", "code": "fh",
                         "expect": "A boxed reference lists each helper in this lesson with an example."},
                        {"type": "cmd", "where": "shell", "title": "Show the dev command sheet", "code": "devh",
                         "expect": "A cheat sheet headed `devh - dev helper`, grouped by topic: availability, code exploration, Python, HTTP and more."},
                        {"type": "cmd", "where": "shell", "title": "Check which dev tools are installed", "code": "devh --check",
                         "expect": "One line per tool: its name and its path, or `MISSING` when it is not on your PATH."},
                        {"type": "cmd", "where": "shell", "title": "Find a dev command and put it on the prompt", "code": "devh --pick",
                         "expect": "The dev cheat sheet opens as a list. Enter puts the chosen command on your prompt without running it, so you can fill in placeholders such as `<path>`."},
                    ],
                },
                {
                    "h2": "Which fzf helper do I type? Pick the job, read the command",
                    "intro": "What you want on the left, what to type on the right.",
                    "blocks": [
                        {"type": "keys", "where": "fzf", "title": "Find the fzf helper to type for each job", "rows": FZF_HELPERS},
                    ],
                },
                {
                    "h2": "Turn the output of any command into a searchable list (fzf)",
                    "intro": "Pipe a command into `fzf`: its output becomes a filterable list.",
                    "blocks": [
                        {"type": "cmd", "where": "fzf", "title": "Search history, docker containers and git branches with a pipe", "code": C('''
# Search history
history | fzf

# Search docker containers
docker ps -a | fzf

# Search git branches
git branch | fzf | xargs git checkout
'''),
                         "expect": "Each command opens its output as a filterable list. Enter on a branch checks it out."},
                        {"type": "cmd", "where": "fzf", "title": "Preview files, pick several, ignore case or match exactly", "code": C('''
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
                "h2": "Preview, pick several, ignore case: the fzf flags",
                "cards": [
                    ("Change how fzf lists and picks", "Add them after `fzf`.", ["Flag", "Does"], [
                        ["`--preview`", "Show a command's output for the selected line"],
                        ["`-m`", "Pick several files"],
                        ["`-i`", "Ignore upper and lower case"],
                        ["`-e`", "Match exactly, not fuzzy"],
                    ]),
                    ("Which keys work in every fzf list?", "History toggles the preview instead; the branch picker disables multi-select.", ["Key", "Does"], [
                        ["`Ctrl+/`", "Change the preview layout"],
                        ["`Ctrl+U` / `Ctrl+D`", "Scroll the preview up / down"],
                        ["`Ctrl+Y`", "Copy the picked names and close"],
                        ["`Tab`", "Select several lines"],
                    ]),
                    ("Why do two keys act differently inside tmux?", "Two keys mean something else in this setup.", ["Key", "In tmux"], [
                        ["`Ctrl-a`", "The prefix. Press it twice to reach the start of the line."],
                        ["`Ctrl-j/k`", "Switch panes, so use the arrows in fzf."],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find a file by part of its name and open it",
                "frame": "Find a file when you know part of its name but not the path.",
                "open": "cd ~/tw && ff",
                "steps": [
                    (None, "`ord`", "The list narrows to one file and `bat` shows a preview."),
                    (None, "`Enter`", "`nvim` opens the file."),
                ],
                "after": "  orders.py\n  1/3\n> ord",
                "meaning": "Find, read and open a file with one alias.",
            },
            "practice": {
                "h2": "Check yourself: copy text and find with fzf",
                "qs": [
                    ("Mechanism", "Why does `y` in copy mode also leave copy mode?",
                     "Yank is the last step of copying.",
                     ["`v` starts the selection.", "`y` copies it and exits."],
                     "The copy is done, so tmux exits copy mode."),
                    ("Keystrokes", "How do I copy a line of output and paste it at the prompt?",
                     "Enter copy mode first.",
                     ["`Ctrl-a [`, move, `v`, move.", "`y` to copy.", "`Ctrl-a ]` to paste."],
                     "`Ctrl-a [`, `v`, `y`, `Ctrl-a ]`."),
                    ("Application", "How do I switch to a git branch by picking it from a list?",
                     "Pipe the branch list into fzf.",
                     ["`git branch` lists the branches.", "`fzf` filters them.", "`xargs git checkout` switches."],
                     "`git branch | fzf | xargs git checkout`"),
                    ("Common mistake", "Why does `Ctrl-a` not jump to the start of the line in tmux?",
                     "Think of the prefix.",
                     ["tmux takes `Ctrl-a` as its prefix.", "Send it on by pressing it twice."],
                     "Press `Ctrl-a Ctrl-a`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Change tmux colors and keys, add plugins and restore after a reboot",
            "subtitle": "Reload the tmux config, change the status bar, install plugins, save your windows, get them back after a restart, add your own key binding",
            "idea": (
                "Change how tmux looks and behaves: edit one file, `~/.config/tmux/tmux.conf`.",
                [
                    ("Reload the tmux config", "Ctrl-a r", "Applies your config changes."),
                    ("Install tmux plugins", "Ctrl-a I", "Capital I, with TPM."),
                    ("Save your windows and panes", "Ctrl-a Ctrl-s", "Saves windows, panes and layout."),
                    ("Get your saved workspace back (restore)", "Ctrl-a Ctrl-r", "Brings the saved workspace back."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why are my tmux windows gone after I restart my computer? The restart kills the tmux server.",
                "fix": "Save with resurrect and continuum, then restore once at login with a lock-guarded script.",
            },
            "drills": [
                {
                    "h2": "Reload the tmux config and check a setting",
                    "intro": "Apply an edit to the config: tmux reads `~/.config/tmux/tmux.conf`. After you edit it, reload, then ask tmux which values it is using.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Reload the tmux config after an edit", "rows": [("Ctrl-a r", "Reload the config (tmux.conf)")],
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
                        {"type": "keys", "where": "tmux", "title": "Show the session name, time or hostname in the status bar", "rows": [
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
                    "h2": "Open the tmux config and control a tmux inside tmux (nested)",
                    "intro": "Edit the config with `tmuxconf`, which opens it in your editor. Control a tmux running inside this one, such as a server you reached over SSH: `F12` hands every key to it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Open tmux.conf in your editor", "code": "tmuxconf",
                         "expect": "`~/.config/tmux/tmux.conf` opens in `nvim`. Save, quit, then press `Ctrl-a r` to apply it."},
                        {"type": "keys", "where": "tmux", "title": "Control a tmux inside tmux, then switch back (nested)", "rows": [
                            ("F12", "Nested tmux: pass every key through to the inner session, press again to take control back"),
                        ], "try": "Press `F12`, read the status bar, then press `F12` again.",
                         "expect": "A red `NESTED` appears at the right of the status bar. While it shows, this tmux's prefix is off and every key, `Ctrl-a` included, reaches the tmux running inside. After the second `F12` the label is gone and `Ctrl-a` controls this tmux again."},
                    ],
                },
                {
                    "h2": "Install tmux plugins and list the ones you have",
                    "intro": "Add a tmux plugin: TPM, the tmux plugin manager, is already installed. List what it holds, and install new plugins with one key.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "List your installed plugins", "code": "ls ~/.tmux/plugins",
                         "expect": "One folder per plugin: `tpm`, `tmux-sensible`, `tmux-resurrect`, `tmux-continuum`, `tmux-yank` and `tmux-sidebar`."},
                        {"type": "keys", "where": "tmux", "title": "Install the plugins listed in tmux.conf", "rows": [("Ctrl-a I", "Install the plugins (capital I)")],
                         "try": "Add a `set -g @plugin` line to `tmux.conf`, reload with `Ctrl-a r`, then press `Ctrl-a I`.", "expect": "TPM fetches the listed plugins."},
                    ],
                },
                {
                    "h2": "Save your workspace and get it back after a reboot",
                    "intro": "Keep your whole workspace across reboots: windows, pane layouts, even running commands.",
                    "blocks": [
                        {"type": "keys", "where": "tmux", "title": "Save your windows and panes, then restore them", "rows": [
                            ("Ctrl-a Ctrl-s", "Save the session (all windows, panes, layout)"),
                            ("Ctrl-a Ctrl-r", "Restore the session (after a reboot)"),
                        ]},
                        {"type": "cmd", "where": "shell", "title": "Check that tmux is saving your sessions", "code": C('''
ls ~/.local/share/tmux/resurrect | tail -3
tmux show -g @continuum-save-interval
'''),
                         "expect": "The newest saves are `tmux_resurrect_` files named with a date and time, no more than 10 minutes old while tmux runs. `@continuum-save-interval 10` is the save interval in minutes."},
                        {"type": "text", "body": "Why is my workspace gone after a restart? Quitting and reopening iTerm2 is fine: the tmux server keeps running. A computer restart kills the server, and nothing restarts it, so nothing restores."},
                        {"type": "text", "body": "Why do my restored panes stack up 3-6 times? resurrect is not idempotent: every restore trigger re-adds panes. With `@continuum-restore 'on'` (your setting), a boot agent and iTerm2 launching tmux can each fire a restore, and the same panes stack 3-6 times into slivers. The fix is exactly one restore, lock-guarded."},
                    ],
                },
                {
                    "h2": "Check that your workspace restored after a reboot",
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
                    "h2": "Add your own tmux key binding",
                    "intro": "Add a line to `tmux.conf`, reload, then ask tmux for the binding.",
                    "blocks": [
                        {"type": "code", "file": TMUX_CONF, "title": "Add custom key bindings (swap windows, split and open nvim, kill pane)", "code": BINDINGS},
                        {"type": "cmd", "where": "tmux", "title": "Check which command a key runs", "code": "tmux list-keys -T prefix r",
                         "expect": "One `bind-key` line for the `prefix` table and key `r`: the reload binding, `source-file` followed by your `tmux.conf` path."},
                    ],
                },
            ],
            "rules": {
                "h2": "How do I restore tmux after a reboot?",
                "cards": [
                    ("What happens at login after a reboot", "One path, zero pileup.", ["Step", "What happens"], [
                        ["1. Log in", "launchd runs `boot-restore.sh`: starts the server and restores `main` once, lock-guarded"],
                        ["2. Attach", "`to main` (`tmux new-session -A -s main`) attaches to the restored session"],
                        ["3. No re-runs", "Continuum restore is on and fires once per server start; the lock blocks repeats"],
                    ]),
                    ("Why does the restore fail after a reboot?", "Four things that bit.", ["Gotcha", "Fix"], [
                        ["launchd's PATH excludes `/opt/homebrew/bin`, so resurrect's bare `tmux` calls fail silently", "Export PATH in the boot script"],
                        ["`tmux start-server` alone can exit with no session attached", "Anchor it with `new-session -d -s main`"],
                        ["Plist `Label` contains `.plist` or is not reverse-DNS", "Use `com.you.name`"],
                        ["Several restores at once: continuum, the boot agent and iTerm2", "That is the pileup. Send every restore through the lock-guarded script"],
                    ]),
                    ("Why not use continuum-boot?", "It starts on boot, but opens Terminal.app on every login and still races with iTerm2.", None,
                     "set -g @continuum-boot 'on'    # avoid: opens Terminal.app, races with iTerm2"),
                ],
            },
            "worked": {
                "h2": "Show the session name and the time in the tmux status bar",
                "frame": "Make the bar show where you are and what time it is.",
                "open": "nvim ~/.config/tmux/tmux.conf",
                "steps": [
                    (None, "`G` `o` then `set -g status-left \"[#S] \"` then `Esc`", "Add the left side."),
                    (None, "`o` then `set -g status-right \"%H:%M\"` then `Esc`", "Add the right side."),
                    (None, "`:w`", "Save the file."),
                    (None, "`Ctrl-a r`", "Reload the config."),
                ],
                "after": "[main]                          09:41",
                "meaning": "`#S` and `%H:%M` fill in live, so the bar always shows the session and the time.",
            },
            "practice": {
                "h2": "Check yourself: tmux config and restore",
                "qs": [
                    ("Mechanism", "Why does a computer restart lose my tmux workspace when quitting iTerm2 does not?",
                     "Where does the tmux server live?",
                     ["The server runs in the background, outside iTerm2.", "A restart kills the server."],
                     "A restart kills the server, and nothing restarts it."),
                    ("Keystrokes", "How do I reload the config, then install new plugins?",
                     "Two prefix commands.",
                     ["`Ctrl-a r` reloads.", "`Ctrl-a I` installs, capital I."],
                     "`Ctrl-a r`, then `Ctrl-a I`."),
                    ("Application", "How do I make window numbering start at 1?",
                     "It is an option in `tmux.conf`.",
                     ["Add `set -g base-index 1`.", "Add `setw -g pane-base-index 1` for panes.", "Reload with `Ctrl-a r`."],
                     "`set -g base-index 1` and `setw -g pane-base-index 1`."),
                    ("Common mistake", "Why does my restored session show the same panes stacked 3-6 times?",
                     "Count the restore triggers.",
                     ["resurrect is not idempotent.", "continuum restore, a boot agent and iTerm2 each restored."],
                     "More than one restore ran. Keep only the lock-guarded script."),
                ],
            },
        },
    ],
}
