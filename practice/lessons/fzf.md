

## FZF Crash Course

**Basic Usage:**

```bash
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
```

**Keyboard Shortcuts:**
- `Ctrl+J/K` or `↑/↓` - Navigate
- `Enter` - Select
- `Ctrl+C` or `Esc` - Cancel
- `Tab` - Multi-select
- `Ctrl+A` - Select all
- `Ctrl+D` - Deselect all

**Useful Aliases (add to ~/.zshrc):**

```bash
# Find file and open in editor
alias ff='fzf --preview "bat --color=always {}" | xargs nvim'

# Find directory and cd
alias fd='cd $(find . -type d | fzf)'

# Search git commits
alias fgl='git log --oneline | fzf --preview "git show {1}"'

# Search running processes
alias fkill='ps aux | fzf | awk "{print \$2}" | xargs kill -9'
```

**With Pipes:**

```bash
# Search history
history | fzf

# Search docker containers
docker ps -a | fzf

# Search git branches
git branch | fzf | xargs git checkout
```

**Advanced Options:**

```bash
# Preview files
fzf --preview 'cat {}'

# Multi-select files
fzf -m

# Case-insensitive
fzf -i

# Exact match
fzf -e
```

Reload shell and test:
```bash
source ~/.zshrc
fzf  # Should work now
```