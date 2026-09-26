---
up:
  - "[[Learning Map]]"
related:
  - "[[Bash]]"
  - "[[fzf]]"
  - "[[Git Worktree]]"
created: 2026-06-27
in:
  - "[[Library Map]]"
tags:
  - terminal
  - neovim
  - tmux
  - workflow
  - library
---

# Lesson 1: tmux — Session Management

tmux keeps your terminal sessions alive. Close your laptop, reopen — everything is still running.

---

## Exercise 1.1: Start your first session

Open iTerm2 and type:

```bash
tmux new -s main
```

You're now inside tmux. Notice the green status bar at the bottom — that's tmux telling you you're in a session called "main".

---

## Exercise 1.2: The prefix key

tmux listens for commands after you press a **prefix key**. Your prefix is `Ctrl-a`.

Every tmux command follows this pattern:
1. Press `Ctrl+a` (hold Ctrl, tap a, release both)
2. Then press the command key

Try it now — create a new window:

```
Ctrl-a  then  c
```

Your status bar now shows two windows: `0:zsh` and `1:zsh`. You're on window 1.

---

## Exercise 1.3: Navigate between windows

```
Ctrl-a 0        Jump to window 0
Ctrl-a 1        Jump to window 1
Ctrl-a n        Next window
Ctrl-a p        Previous window
Ctrl-a w        Interactive window picker (preview + pick with j/k + Enter)
```

Go back and forth a few times. This is how you'll switch between editor, tests, and your AI agent.

Try `Ctrl-a w` — it shows all windows with a live preview. Fastest way to jump when you have many windows.

---

## Exercise 1.4: Detach and reattach

```
Ctrl-a d        Detach (you leave tmux but the session keeps running)
```

You're back to a bare terminal. Your session is alive in the background. Reattach:

```bash
tmux attach
```

Everything is exactly where you left it. Sessions survive crashes, reboots, SSH disconnects.

---

## Exercise 1.5: Split panes

```
Ctrl-a |        Split vertically (side by side)
Ctrl-a -        Split horizontally (top and bottom)
Ctrl-a h/j/k/l  Move between panes (vim-style)
Ctrl-a x        Close current pane (prompts y/n — press y to confirm)
```

Split your window, run `ls` in one pane and `htop` in the other. Navigate between them with `Ctrl-a h` and `Ctrl-a l`. Or just **click** on the pane you want (mouse is enabled).

---

## Exercise 1.6: Window and pane tricks

### Pane management

```
Ctrl-a z        Zoom current pane to full screen (press again to unzoom)
Ctrl-a Space    Cycle through pane layouts (even, tiled, etc.)
Ctrl-a !        Break pane into its own window
Ctrl-a q        Show pane numbers (press the number to jump to that pane)
Ctrl-a {        Swap pane with previous
Ctrl-a }        Swap pane with next
Ctrl-a o        Cycle to next pane
Ctrl-a ;        Jump to last active pane
:swap-pane -t 2  Swap current pane with pane 2 (tmux command)
```

### Pane resizing

```
Ctrl-a H        Resize pane left (5 cells)
Ctrl-a J        Resize pane down (5 cells)
Ctrl-a K        Resize pane up (5 cells)
Ctrl-a L        Resize pane right (5 cells)
```

(Capital H/J/K/L = resize, lowercase h/j/k/l = navigate)

### Window management

```
Ctrl-a c        Create new window
Ctrl-a ,        Rename current window
Ctrl-a &        Kill current window (confirms y/n)
Ctrl-a .        Move window to another index
Ctrl-a f        Find window by name
```

### Sending commands to other panes/windows

```bash
# Run a command in another window without switching to it:
tmux send-keys -t 1 "pytest tests/ -v" Enter

# Run in a specific named window:
tmux send-keys -t ml:tests "make build" Enter

# Capture output from another pane:
tmux capture-pane -t 1 -p | tail -10
```

`Ctrl-a z` — zoom a pane to fullscreen while reading output, press again to unzoom.

`Ctrl-a ,` — name windows so the status bar shows `editor`, `tests`, `agent` instead of `0:zsh`, `1:zsh`.

---

## Exercise 1.7: Copy mode

```
Ctrl-a [        Enter copy mode (cursor becomes free-moving)
                Navigate with h/j/k/l or Ctrl-d/Ctrl-u
v               Start selection (visual mode)
y               Yank (copy) selection, exits copy mode
Ctrl-a ]        Paste the copied text

EXIT:
q               Quit copy mode without copying
Esc             Also exits copy mode
```

---

## Exercise 1.8: Sessions

```bash
tmux new -s work          # create named session
tmux new -s personal      # another session
tmux ls                   # list all sessions
tmux switch -t work       # switch to session "work"
tmux kill-session -t old  # kill a session
```

Inside tmux:
```
Ctrl-a s        Session picker (like Ctrl-a w but for sessions)
Ctrl-a (        Previous session
Ctrl-a )        Next session
```

---

## Muscle memory (practice 10 times each)

| Command | What it does |
|---------|-------------|
| `Ctrl-a c` | New window |
| `Ctrl-a w` | Window picker (interactive list with preview) |
| `Ctrl-a 0-9` | Jump to window by number |
| `Ctrl-a n/p` | Next/previous window |
| `Ctrl-a ,` | Rename current window |
| `Ctrl-a d` | Detach |
| `Ctrl-a \|` | Vertical split |
| `Ctrl-a -` | Horizontal split |
| `Ctrl-a h/j/k/l` | Navigate panes |
| `Ctrl-a z` | Zoom/unzoom pane |
| `Ctrl-a q` | Show pane numbers (tap number to jump) |
| `Ctrl-a x` | Close pane (y to confirm) |
| `Ctrl-a [` | Enter copy mode |

---

## Auto-attach (already in your ~/.zshrc)

```bash
if [ -z "$TMUX" ]; then
  tmux attach || tmux new -s main
fi
```

Every new terminal automatically connects to tmux. No manual `tmux attach` needed.

---

## Terminal line editing (readline shortcuts)

Inside any terminal/shell prompt (works in tmux, zsh, bash):

```
Ctrl-u           Delete entire line (like Cmd+Delete)
Ctrl-w           Delete word backward (like Option+Delete)
Ctrl-k           Delete from cursor to end of line
Ctrl-a           Jump to start of line
Ctrl-e           Jump to end of line
Ctrl-h           Delete character backward (Backspace)
Alt-d            Delete word forward
Alt-b            Move back one word
Alt-f            Move forward one word
```

These are your Cmd+Delete and Option+Delete replacements in the terminal.

---

## Customizing tmux

Your config lives at `~/.config/tmux/tmux.conf`. After any change, reload with `Ctrl-a r`.

### Status bar styling

```bash
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
```

### Status bar variables

```
#S      Session name
#I      Window index
#W      Window name
#P      Pane index
#H      Hostname
#T      Pane title
%H:%M   Time (24h)
%d/%m   Date
```

### Status bar position

```bash
set -g status-position top       # bar at top instead of bottom
set -g status-justify centre     # center the window list
```

### Pane borders

```bash
set -g pane-border-style "fg=#565f89"
set -g pane-active-border-style "fg=#7aa2f7"
```

### Activity monitoring

```bash
# Highlight windows with activity
setw -g monitor-activity on
set -g visual-activity off       # don't show a message, just highlight

# Highlight style for windows with activity
set -g window-status-activity-style "fg=#e0af68"
```

### Useful options

```bash
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
```

### Plugins (TPM — tmux plugin manager)

Install TPM:
```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Add to bottom of tmux.conf:
```bash
# Plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'      # sane defaults
set -g @plugin 'tmux-plugins/tmux-resurrect'     # save/restore sessions across reboots
set -g @plugin 'tmux-plugins/tmux-continuum'     # auto-save sessions every 15 min
set -g @plugin 'tmux-plugins/tmux-yank'          # better copy to clipboard

# Initialize TPM (keep at bottom)
run '~/.tmux/plugins/tpm/tpm'
```

Install plugins: `Ctrl-a I` (capital I)

### tmux-resurrect (save/restore sessions)

```
Ctrl-a Ctrl-s    Save session (all windows, panes, layout)
Ctrl-a Ctrl-r    Restore session (after reboot)
```

Your entire tmux workspace survives reboots — all windows, pane layouts, even running commands.

### Auto-save every 10 minutes + auto-restore on boot

tmux-continuum auto-**saves** every N minutes. Restoring on a computer restart is trickier than it looks — see the warning below.

```bash
set -g @continuum-save-interval '10'          # auto-save every 10 minutes
set -g @continuum-restore 'off'               # OFF on purpose — see "the pileup trap"
set -g @resurrect-capture-pane-contents 'on'  # restore scrollback contents
set -g @resurrect-strategy-nvim 'session'     # restore nvim sessions too
```

**The reboot problem:** Quitting/reopening iTerm2 is fine — the tmux server keeps running in the background. But a **computer restart kills the server**, and nothing restarts it, so nothing restores.

**⚠️ The pileup trap (learned the hard way):** tmux-resurrect is **NOT idempotent** — every restore trigger *re-adds* panes instead of checking "already restored." If you have BOTH `@continuum-restore 'on'` AND a boot agent AND iTerm2 launching tmux, they race and each fires a restore. The result: the same panes stacked 3–6 times into useless slivers. The fix is to guarantee **exactly one restore**, lock-guarded.

**The fix — one idempotent restore path.** Two small scripts + one launch agent.

`~/.config/tmux/restore-once.sh` (lock-guarded — runs at most once per server lifetime):

```bash
#!/usr/bin/env bash
LOCK="/tmp/tmux-resurrect-restored-$(id -u)"
[ -f "$LOCK" ] && exit 0          # already restored this boot → do nothing
touch "$LOCK"
"$HOME/.tmux/plugins/tmux-resurrect/scripts/restore.sh"
```

`~/.config/tmux/boot-restore.sh` (runs at login):

```bash
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
```

Make both executable: `chmod +x ~/.config/tmux/{restore-once,boot-restore}.sh`

The launch agent `~/Library/LaunchAgents/com.indamutsa.tmux-restore.plist`:

```xml
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
```

Load it:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.indamutsa.tmux-restore.plist
```

**How it works on boot:**
1. Log in → launchd runs `boot-restore.sh` → starts server, restores `main` **once** (lock-guarded)
2. Open iTerm2 → `tmux new-session -A -s main` → **attaches** to the already-restored session (no new restore)
3. Continuum restore is OFF, lock blocks re-runs → **zero pileup**

Result: turn on the computer, open iTerm2, windows exactly where you left them — and never stacked into slivers.

**Gotchas that bit us:**
- launchd's PATH excludes `/opt/homebrew/bin` → resurrect's bare `tmux` calls silently fail. Export PATH in the boot script.
- `tmux start-server` alone can exit with no session attached → anchor with `new-session -d -s main`.
- Plist `Label` must NOT contain `.plist` and should be reverse-DNS (`com.you.name`), or `launchctl` rejects it.
- Don't run BOTH `@continuum-restore 'on'` and the boot agent — that's the pileup. Pick the lock-guarded path.

> **Why not `@continuum-boot 'on'`?** It auto-starts on boot but pops open **Terminal.app** on every login, and still races with iTerm2. The lock-guarded script restores silently and exactly once.

### Custom key bindings

```bash
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
```

### Color schemes

For tokyonight (matches nvim):
```bash
set -g status-style "bg=#1a1b26,fg=#a9b1d6"
set -g window-status-current-style "bg=#7aa2f7,fg=#1a1b26,bold"
```

For catppuccin:
```bash
set -g status-style "bg=#1e1e2e,fg=#cdd6f4"
set -g window-status-current-style "bg=#89b4fa,fg=#1e1e2e,bold"
```

For gruvbox:
```bash
set -g status-style "bg=#282828,fg=#ebdbb2"
set -g window-status-current-style "bg=#fabd2f,fg=#282828,bold"
```

---

Back to: [[Library Map]] | [[Learning Map]]
