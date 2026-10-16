"""Module 11: Bash expert. Source: snippets run in /bin/bash 3.2 on macOS; no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


BASH_FIRST = "Start Bash first: type `bash`. Run this page's blocks in order in that shell. Type `exit` to go back to zsh."

MODULE = {
    "n": 11,
    "folder": "m11-bash-expert",
    "title": "Write safer Bash scripts and reuse functions",
    "footer": "Write Bash functions, edit strings, keep arrays, stop on errors, redirect output and copy ready scripts",
    "tagline": "Reuse code in functions, stop scripts on errors, save output and copy ready scripts.",
    "glossary": [
        ("tw-function", "Function", ["function", "functions"], "Run the same commands again by name. Call it like a command; its arguments become $1, $2 and $@ inside the function."),
        ("tw-array", "Indexed array", ["array", "arrays", "indexed array"], "Keep a list of values addressed by number, starting at 0. Quoted \"${a[@]}\" passes each element as its own argument."),
        ("tw-trap", "Trap", ["trap", "traps"], "Run a shell command when an event happens. EXIT runs when the shell exits; ERR runs on eligible command failures."),
        ("tw-process-substitution", "Process substitution", ["process substitution"], "Use a command's output as a file: <(command) gives another command a path from which it can read that output."),
        ("tw-here-doc", "Here-doc", ["here-doc", "heredoc", "here document"], "Feed lines of text to a command's standard input until a delimiter. Quote the delimiter to keep dollar signs literal."),
    ],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Write Bash functions, cut up strings and keep lists in arrays",
            "subtitle": "Reuse a command in a function, remove .txt from a file name, keep file names with spaces in a list, loop over every array item",
            "idea": (
                "Repeat a task: write a function. Cut up text: use an expansion. Keep a list: use an array.",
                [
                    ("Call a function with an argument", "greet Ada", "Inside the function, $1 is this call's first argument."),
                    ("Save a function's output in a variable", "value=$(fn)", "return sets a status; echo prints text."),
                    ("Remove .txt from a file name", "${f%.txt}", "It removes the shortest matching suffix."),
                    ("Pass every array item as its own argument", "\"${a[@]}\"", "Each value stays one argument."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does my helper function change a variable in the main script? Why does my list lose file names with spaces?",
                "fix": "Keep helper variables local. Store lists in arrays and expand them with `\"${a[@]}\"`.",
            },
            "drills": [
                {
                    "h2": "Reuse a command with a function",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create practice files for functions, strings and arrays", "code": C(r'''
mkdir -p /tmp/tw/m11-functions/samples && cd /tmp/tw/m11-functions
cat > names.txt <<'EOF'
samples/red apple.txt
samples/blue plum.txt
EOF
printf 'red\n' > 'samples/red apple.txt'
printf 'blue\n' > 'samples/blue plum.txt'
cat names.txt
'''), "expect": "`samples/red apple.txt`; then `samples/blue plum.txt`."},
                        {"type": "cmd", "where": "shell", "title": "Write a function and call it with arguments", "code": C(r'''
greet() { printf 'Hello, %s (%s arguments)\n' "$1" "$#"; }
greet Ada
greet 'Bo Lee' extra
'''), "expect": "`Hello, Ada (1 arguments)`; then `Hello, Bo Lee (2 arguments)`."},
                        {"type": "cmd", "where": "shell", "title": "Stop a function from changing a variable outside it (local)", "code": C(r'''
name=outside
show_name() { local name=$1; printf 'inside: %s\n' "$name"; }
show_name Ada
printf 'outside: %s\n' "$name"
'''), "expect": "`inside: Ada`; then `outside: outside`."},
                        {"type": "cmd", "where": "shell", "title": "Save a function's output and check if it worked (return code)", "code": C(r'''
label() { echo "report: $1"; return 0; }
value=$(label sales); status=$?
printf 'output=%s status=%s\n' "$value" "$status"
reject() { echo 'not ready' >&2; return 7; }
value=$(reject); status=$?
printf 'output=[%s] status=%s\n' "$value" "$status"
'''), "expect": "`output=report: sales status=0`; then `not ready`; then `output=[] status=7`."},
                        {"type": "text", "body": "Return text or a number from a function: `return` takes a status from 0 to 255, not a string. `echo` or `printf` sends data to stdout. `$(fn)` captures stdout and strips trailing newlines. It runs in a subshell, so variable changes there do not reach the caller. A function without `return` uses its last command's status."},
                    ],
                },
                {
                    "h2": "Cut, slice and replace text in a variable",
                    "intro": "Change a file name or text held in a variable. These expansions change the value you print. They do not rename a file.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Count characters, take part of a string, replace text in a string", "code": C(r'''
s=banana
printf 'length=%s first-three=%s\n' "${#s}" "${s:0:3}"
printf 'first=%s all=%s\n' "${s/a/A}" "${s//a/A}"
'''), "expect": "`length=6 first-three=ban`; then `first=bAnana all=bAnAnA`."},
                        {"type": "cmd", "where": "shell", "title": "Remove a file extension, get the file name, get the parent folder", "code": C(r'''
f=report.txt; p=reports/2026/report.txt
printf 'stem=%s\n' "${f%.txt}"
printf 'filename=%s parent=%s\n' "${p##*/}" "${p%/*}"
printf 'short-prefix=%s long-prefix=%s\n' "${p#*/}" "${p##*/}"
'''), "expect": "`stem=report`; then `filename=report.txt parent=reports/2026`; then `short-prefix=2026/report.txt long-prefix=report.txt`."},
                        {"type": "text", "body": "Remove the start or end of a value: `#` removes a matching prefix and `%` a matching suffix. Double them to remove the longest match. The pattern is a shell glob. `${p%/*}` stays unchanged if `p` has no slash; use `dirname` when you need that case handled."},
                        {"type": "cmd", "where": "shell", "title": "Change text to uppercase or lowercase (Bash 3.2 on a Mac)", "code": C(r'''
printf '%s\n' 'Hello Ada' | LC_ALL=C tr '[:lower:]' '[:upper:]'
printf '%s\n' 'Hello Ada' | LC_ALL=C tr '[:upper:]' '[:lower:]'
'''), "expect": "`HELLO ADA`; then `hello ada`."},
                        {"type": "text", "body": "Why does `${s^^}` fail on my Mac? macOS `/bin/bash` is 3.2 here. `${s^^}` for uppercase and `${s,,}` for lowercase are Bash 4+ only. Many GNU/Linux systems have a newer Bash; `tr` works on both. These `LC_ALL=C` examples convert ASCII letters."},
                    ],
                },
                {
                    "h2": "Keep a list of values in an array",
                    "intro": "Keep every value in a list whole: an indexed array starts at 0. Use `[@]` inside quotes to keep each value whole.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make an array, add an item, count the items, loop over them and take a slice", "code": C(r'''
a=(red 'green pear' blue)
a+=(gold)
printf 'count=%s first=%s\n' "${#a[@]}" "${a[0]}"
for item in "${a[@]}"; do printf '[%s]\n' "$item"; done
printf 'slice=[%s]\n' "${a[@]:1:2}"
'''), "expect": "`count=4 first=red`; then `[red]`; then `[green pear]`; then `[blue]`; then `[gold]`; then `slice=[green pear]`; then `slice=[blue]`."},
                        {"type": "cmd", "where": "shell", "title": "Read file names with spaces from a file into an array", "code": C(r'''
cd /tmp/tw/m11-functions
files=()
while IFS= read -r file || [[ -n $file ]]; do files+=("$file"); done < names.txt
printf 'files=%s\n' "${#files[@]}"
printf '[%s]\n' "${files[@]}"
'''), "expect": "`files=2`; then `[samples/red apple.txt]`; then `[samples/blue plum.txt]`."},
                        {"type": "cmd", "where": "shell", "title": "Read any file names, even with newlines, into an array (NUL separators)", "code": C(r'''
cd /tmp/tw/m11-functions
files=()
while IFS= read -r -d '' file; do files+=("$file"); done < <(find samples -type f -name '*.txt' -print0)
printf 'files=%s\n' "${#files[@]}"
printf '[%s]\n' "${files[@]}" | LC_ALL=C sort
'''), "expect": "`files=2`; then `[samples/blue plum.txt]`; then `[samples/red apple.txt]`."},
                        {"type": "text", "body": "Read file names safely: a line list keeps spaces and backslashes but cannot encode a newline inside a filename. `find -print0` and `read -d ''` use NUL separators, so the array preserves those names too. Sorting printed names here only makes these sample results stable. `mapfile` is Bash 4+ only. Page 3 explains `< <(command)`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Pick the syntax for a function, a string edit or a list",
                "cards": [
                    ("Reuse a command in a function", "Keep the output and the status separate.", ["What you want", "Type this"], [
                        ["Write and call a helper function", "`greet() { echo \"Hi $1\"; }; greet Ada`"],
                        ["Keep a helper's variable local", "`local name=$1` inside the function"],
                        ["Return a failure status", "`return 7`"],
                        ["Save what a function prints", "`value=$(fn); status=$?`"],
                    ]),
                    ("Change text in a string", "Patterns are globs, not regular expressions.", ["What you want", "Type this"], [
                        ["Count characters / take the first three", "`${#s}` / `${s:0:3}`"],
                        ["Remove .txt / get the file name", "`${f%.txt}` / `${f##*/}`"],
                        ["Get the parent folder of a path with a slash", "`${p%/*}`"],
                        ["Replace first / every a with b", "`${s/a/b}` / `${s//a/b}`"],
                        ["Make text uppercase on Bash 3.2", "`printf '%s\\n' \"$s\" | LC_ALL=C tr '[:lower:]' '[:upper:]'`"],
                    ]),
                    ("Keep a list of values whole", "Always quote the @ expansion.", ["What you want", "Type this"], [
                        ["Make a list / add an item", "`a=(one 'two words'); a+=(three)`"],
                        ["Count items / read the first item", "`${#a[@]}` / `${a[0]}`"],
                        ["Loop over every item", "`for x in \"${a[@]}\"; do ...; done`"],
                        ["Take two items starting at index 1", "`\"${a[@]:1:2}\"`"],
                        ["Read a list of lines into an array", "`while IFS= read -r f || [[ -n $f ]]; do a+=(\"$f\"); done < list`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Get a short label from a report path",
                "frame": "Get the file name without .txt from a path, and keep the original path.",
                "open": "cd /tmp/tw/m11-functions",
                "steps": [
                    (None, "`short_label() { local f=${1##*/}; echo \"${f%.txt}\"; }`", "Remove everything up to the last slash, then remove the suffix."),
                    (None, "`result=$(short_label 'reports/monthly sales.txt')`", "Save what the function prints in a variable."),
                    (None, "`printf '%s\\n' \"$result\"`", "Print the label."),
                ],
                "after": "monthly sales",
                "meaning": "Get a label from a path: the function takes one path, keeps its helper local and prints one value.",
            },
            "practice": {
                "h2": "Check how to use functions and lists",
                "qs": [
                    ("Mechanism", "Why does `value=$(reject)` capture no text when reject prints to stderr and returns 7?", "Which stream does command substitution capture?", ["It captures stdout only.", "The error text stays on stderr.", "Read the assignment's status immediately with `$?`."], "`value` is empty and the status is 7."),
                    ("Keystrokes", "How do I get report.txt from reports/2026/report.txt and then remove .txt?", "Strip a prefix, then a suffix.", ["Write `f=${p##*/}`.", "Write `echo \"${f%.txt}\"`."], "`${p##*/}` gives report.txt; `${f%.txt}` gives report."),
                    ("Application", "How do I print two array items starting at index 1?", "Use an array slice.", ["Start at 1 and take 2.", "Keep the expansion quoted."], "`printf '%s\\n' \"${a[@]:1:2}\"`."),
                    ("Common mistake", "Why does unquoted ${a[@]} split green pear?", "The quotes belong around the whole expansion.", ["Unquoted elements undergo word splitting and glob expansion.", "Quoted `\"${a[@]}\"` keeps one argument per element."], "Use `\"${a[@]}\"`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Make a Bash script stop on errors and clean up after itself",
            "subtitle": "Stop a script when a command fails, catch unset variables, clean up temp files on exit, show the line that failed, trace what ran",
            "idea": (
                "Make a script stop when something fails: turn on the failure checks, then handle expected failures explicitly.",
                [
                    ("Stop on a failed command, an unset variable or a broken pipe", "set -euo pipefail", "Failed commands, unset values and broken pipelines."),
                    ("Run cleanup when a script ends", "trap cleanup EXIT", "Keep the script's original exit status."),
                    ("Show which line failed", "trap ... ERR", "Use set -E to inherit ERR in functions."),
                    ("See every command a script runs", "bash -x trace.sh", "It prints each expanded command on stderr."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does my script keep going after a failed step, leave temp files in the working folder and still report success?",
                "fix": "Catch unexpected failure, keep an EXIT cleanup and use explicit checks for expected failure.",
            },
            "drills": [
                {
                    "h2": "Stop a script at the first error",
                    "intro": BASH_FIRST + " The options below run in child shells so your interactive shell stays open.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a script to practice error checks and tracing", "code": C(r'''
mkdir -p /tmp/tw/m11-safe/retained && cd /tmp/tw/m11-safe
cat > trace.sh <<'EOF'
#!/bin/bash
name=Ada
printf 'Hello %s\n' "$name"
EOF
cat trace.sh
'''), "expect": "`#!/bin/bash`; then `name=Ada`; then `printf 'Hello %s\\n' \"$name\"`."},
                        {"type": "cmd", "where": "shell", "title": "Stop a script after a failed command (set -e)", "code": C(r'''
bash -c 'false; echo "bug: continued"'
bash -c 'set -e; false; echo "unreachable"'
printf 'checked exit=%s\n' "$?"
'''), "expect": "`bug: continued`; then `checked exit=1`."},
                        {"type": "cmd", "where": "shell", "title": "Catch a variable that was never set (set -u)", "code": C(r'''
bash -c 'unset report_dir; printf "bug: empty=[%s]\n" "$report_dir"'
bash -c 'set -u; unset report_dir; printf "%s\n" "$report_dir"'
printf 'checked exit=%s\n' "$?"
'''), "expect": "`bug: empty=[]`; then `bash: report_dir: unbound variable`; then `checked exit=127`."},
                        {"type": "cmd", "where": "shell", "title": "Catch a failure in the middle of a pipe (pipefail)", "code": C(r'''
bash -c 'false | cat; printf "bug: pipeline exit=%s\n" "$?"'
bash -c 'set -euo pipefail; false | cat; echo "unreachable"'
printf 'checked exit=%s\n' "$?"
'''), "expect": "`bug: pipeline exit=0`; then `checked exit=1`."},
                        {"type": "text", "body": "Why did `set -e` not stop my script? `-e` stops on eligible failures; `-u` rejects unset values; `pipefail` makes a pipeline return the rightmost nonzero status. `-e` and ERR skip failures tested by `if`, `while`, `!` and most `&&` / `||` lists. A function called as a condition also runs without errexit protection. Check important steps explicitly there. `-u` still allows empty values, so validate required input too."},
                    ],
                },
                {
                    "h2": "Clean up temp files and show which line failed",
                    "intro": "Run cleanup whether the script works or fails: put it in EXIT. This exercise moves work to retained/ instead of deleting it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Clean up a temp folder when the script exits, without deleting its files", "code": C(r'''
cd /tmp/tw/m11-safe
cat > cleanup.sh <<'EOF'
#!/bin/bash
set -euo pipefail
work=$(mktemp -d "$PWD/work.XXXXXX")
cleanup() {
  local status=$?
  if mv "$work" retained/; then
    echo 'cleanup: work moved into retained/'
  else
    echo 'cleanup: move failed; work remains in place' >&2
    [[ $status -ne 0 ]] || status=1
  fi
  return "$status"
}
trap cleanup EXIT
printf 'draft\n' > "$work/report.txt"
echo 'work: draft written'
exit 7
EOF
bash cleanup.sh
printf 'script exit=%s\n' "$?"
'''), "expect": "`work: draft written`; then `cleanup: work moved into retained/`; then `script exit=7`."},
                        {"type": "text", "body": "Make a private temp folder and clean up on exit: `mktemp -d` creates a unique private directory. An EXIT trap runs on normal shell exit, including exit after `-e`; it cannot run after SIGKILL or a power loss. Capture `$?` before cleanup commands overwrite it. The retained files remain available for inspection."},
                        {"type": "cmd", "where": "shell", "title": "Show which line failed and its exit code (ERR trap)", "code": C(r'''
cd /tmp/tw/m11-safe
cat > fail.sh <<'EOF'
#!/bin/bash
set -Eeuo pipefail
trap 'status=$?; printf "error: line %s status %s\n" "$LINENO" "$status" >&2' ERR
echo 'starting'
false
echo 'unreachable'
EOF
bash fail.sh
printf 'script exit=%s\n' "$?"
'''), "expect": "`starting`; then `error: line 5 status 1`; then `script exit=1`."},
                        {"type": "cmd", "where": "shell", "title": "Check an exit code and run a fallback when a command fails", "code": C(r'''
if grep -q 'Nobody' trace.sh; then echo found; else status=$?; printf 'grep exit=%s\n' "$status"; fi
bash -c 'set -euo pipefail; false || echo "fallback: cached result"; echo "continuing"'
'''), "expect": "`grep exit=1`; then `fallback: cached result`; then `continuing`."},
                        {"type": "text", "body": "What do grep's exit codes mean? For grep, 0 means found, 1 means no match and 2 means an error. A fallback after `||` runs for any failure: distinguish statuses if they need different handling. Save `$?` before printing anything."},
                        {"type": "cmd", "where": "shell", "title": "Check if a command is installed before using it (command -v)", "code": C(r'''
if command -v tar >/dev/null 2>&1; then echo 'tar: available'; else echo 'tar: missing'; fi
if command -v tw_m11_missing_tool >/dev/null 2>&1; then echo available; else echo 'missing tool: use fallback'; fi
'''), "expect": "`tar: available`; then `missing tool: use fallback`."},
                    ],
                },
                {
                    "h2": "See which commands a script ran",
                    "intro": "Trace a whole script, or just the part you are checking.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "See every command a script runs (bash -x)", "code": C(r'''
cd /tmp/tw/m11-safe
PS4='+ ' bash -x trace.sh 2>&1
'''), "expect": "`+ name=Ada`; then `+ printf 'Hello %s\\n' Ada`; then `Hello Ada`."},
                        {"type": "cmd", "where": "shell", "title": "Trace just one part of a script (set -x, then set +x)", "code": C(r'''
bash -c 'PS4="+ "; set -x; printf "traced\n"; set +x; printf "quiet\n"' 2>&1
'''), "expect": "`+ printf 'traced\\n'`; then `traced`; then `+ set +x`; then `quiet`."},
                        {"type": "text", "body": "Why does a trace show my values? Tracing prints expanded arguments, so enable it only around values that are safe to display. `set +x` stops the trace."},
                        {"type": "cmd", "where": "shell", "title": "Check if ShellCheck is installed before linting (checking) a script", "code": C(r'''
cd /tmp/tw/m11-safe
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck trace.sh && echo 'ShellCheck: passed'
else
  echo 'ShellCheck: not installed'
fi
'''), "expect": "`ShellCheck: not installed`."},
                        {"type": "text", "body": "How do I install ShellCheck? On macOS use `brew install shellcheck`; on Debian/Ubuntu use `sudo apt install shellcheck`. Then run `shellcheck trace.sh`. Installation and lint results are not assumed here. Bash 3.2 supports all options and traps on this page."},
                    ],
                },
            ],
            "rules": {
                "h2": "Choose how to stop, clean up and debug a script",
                "cards": [
                    ("Stop a script when something fails", "Use these in scripts; handle expected failures explicitly.", ["What you want", "Type this"], [
                        ["Stop after a failed command (eligible failures)", "`set -e`"],
                        ["Catch a variable that is not set", "`set -u`"],
                        ["Catch a failed step inside a pipe", "`set -o pipefail`"],
                        ["Turn on all three", "`set -euo pipefail`"],
                    ]),
                    ("Clean up and show errors", "Save the exit status before doing other work.", ["What you want", "Type this"], [
                        ["Create a private temp folder", "`work=$(mktemp -d \"$PWD/work.XXXXXX\")`"],
                        ["Run cleanup when the shell exits", "`trap cleanup EXIT`"],
                        ["Show the line number when a command fails (eligible failures)", "`trap 'printf \"error: line %s\\n\" \"$LINENO\" >&2' ERR`"],
                        ["Make ERR work inside functions and subshells", "`set -E`"],
                        ["Run a fallback when a command fails", "`command || fallback`"],
                    ]),
                    ("Find out why a script fails", "Start with a small trace.", ["What you want", "Type this"], [
                        ["Check if a command is installed", "`command -v tar >/dev/null 2>&1`"],
                        ["Trace a whole script / one section", "`bash -x file.sh` / `set -x` then `set +x`"],
                        ["Check if ShellCheck is installed", "`command -v shellcheck`"],
                        ["Check a script with ShellCheck (lint)", "`shellcheck file.sh`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find which line failed and keep its exit code",
                "frame": "Why does fail.sh exit early? Find the line that failed and keep a nonzero exit code.",
                "open": "cd /tmp/tw/m11-safe",
                "steps": [
                    (None, "`bash fail.sh`", "See the line number: the ERR trap reports line 5."),
                    (None, "`printf 'script exit=%s\\n' \"$?\"`", "Read the exit status right away."),
                ],
                "after": "starting\nerror: line 5 status 1\nscript exit=1",
                "meaning": "See what failed: the trap prints a diagnostic; errexit ends the script with failure.",
            },
            "practice": {
                "h2": "Check how to stop on errors, clean up and trace",
                "qs": [
                    ("Mechanism", "Why can false | cat return success without pipefail?", "Which pipeline stage supplies the status by default?", ["The last command is cat.", "Cat succeeds even though false failed.", "Pipefail returns the rightmost failing stage's status."], "Enable `set -o pipefail`."),
                    ("Keystrokes", "How do I trace trace.sh and put the trace on stdout too?", "Use bash -x and a redirection.", ["Run `bash -x trace.sh`.", "Append `2>&1`."], "`bash -x trace.sh 2>&1`."),
                    ("Application", "How do I run cleanup whether a script succeeds or fails?", "Register an exit event.", ["Define a cleanup function.", "Save `$?` at its start.", "Register it with `trap cleanup EXIT`."], "Use an EXIT trap and preserve the status."),
                    ("Common mistake", "Does set -e guarantee a function called in an if stops at its first failure?", "Conditional calls suppress errexit in the function body.", ["The call's status is being tested.", "Commands inside that function need explicit checks."], "No. Check critical commands inside the function and return failure yourself."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Redirect output, type multi-line text and compare command output",
            "subtitle": "Save output and errors to a file, see output and save it, feed text to a command, compare the output of two commands",
            "idea": (
                "Send output to a file or the screen: redirections run left to right. Choose a stream, then choose its destination.",
                [
                    ("Save output and errors in one file", "cmd > run.log 2>&1", "Both streams reach the same file."),
                    ("See output on screen and save it to a file", "cmd | tee run.log", "tee copies stdin to the screen and a file."),
                    ("Type multi-line text with no $ expansion (here-doc)", "<<'EOF'", "No dollar or command expansion."),
                    ("Compare the output of two commands", "diff <(cmd1) <(cmd2)", "Two readable paths replace temporary files."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why do errors still print on the screen after I redirect output? Why does a piped loop lose its counter?",
                "fix": "Redirect stdout before copying stderr. Feed a loop with `< <(cmd)` to keep its state.",
            },
            "drills": [
                {
                    "h2": "Send output or errors to a file",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create practice output and lists for redirection", "code": C(r'''
mkdir -p /tmp/tw/m11-redirect && cd /tmp/tw/m11-redirect
cat > left.txt <<'EOF'
pear
apple
EOF
printf 'apple\npear\n' > right.txt
both() { printf 'OUT\n'; printf 'ERR\n' >&2; }
cat left.txt
'''), "expect": "`pear`; then `apple`."},
                        {"type": "cmd", "where": "shell", "title": "Save output to a file, or add to the end of it (> and >>)", "code": C(r'''
cd /tmp/tw/m11-redirect
printf 'first\n' > output.log
printf 'second\n' >> output.log
cat output.log
'''), "expect": "`first`; then `second`."},
                        {"type": "cmd", "where": "shell", "title": "Save errors to a file, or mix them with output (2> and 2>&1)", "code": C(r'''
cd /tmp/tw/m11-redirect
both > stdout.log 2> stderr.log
printf 'stdout: '; cat stdout.log
printf 'stderr: '; cat stderr.log
both > combined.log 2>&1
cat combined.log
'''), "expect": "`stdout: OUT`; then `stderr: ERR`; then `OUT`; then `ERR`."},
                        {"type": "cmd", "where": "shell", "title": "Save output and errors together (&>), or throw them away (/dev/null)", "code": C(r'''
cd /tmp/tw/m11-redirect
both &> short.log
cat short.log
both > /dev/null 2>&1
both &> /dev/null
echo 'quiet commands finished'
'''), "expect": "`OUT`; then `ERR`; then `quiet commands finished`."},
                        {"type": "cmd", "where": "shell", "title": "Why do errors still show on screen? Fix the order of 2>&1", "code": C(r'''
cd /tmp/tw/m11-redirect
both 2>&1 > order.log
printf 'file: '; cat order.log
both > order.log 2>&1
printf 'file after fix:\n'; cat order.log
'''), "expect": "`ERR`; then `file: OUT`; then `file after fix:`; then `OUT`; then `ERR`."},
                        {"type": "text", "body": "Does the order of redirections matter? With `2>&1 > file`, stderr copies the current stdout destination, then only stdout moves to the file. With `> file 2>&1`, both reach the file. `>` replaces existing contents; `>>` appends. `&>` is Bash syntax. The portable shell form is `> file 2>&1`."},
                        {"type": "cmd", "where": "shell", "title": "See output on screen and save a copy to a file (tee)", "code": C(r'''
cd /tmp/tw/m11-redirect
both 2>&1 | tee live.log
printf 'again\n' | tee -a live.log
printf 'saved:\n'; cat live.log
'''), "expect": "`OUT`; then `ERR`; then `again`; then `saved:`; then `OUT`; then `ERR`; then `again`."},
                    ],
                },
                {
                    "h2": "Type multi-line text into a command (here-doc)",
                    "intro": "Feed lines of text to a command: a here-doc ends at its delimiter on a line by itself. Quotes on the delimiter control expansion.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Print a $variable literally in a here-doc, or expand it (<<'EOF' or <<EOF)", "code": C(r'''
name=Ada
cat <<'EOF'
Hello $name
$(printf command)
EOF
cat <<EOF
Hello $name
$(printf command)
EOF
'''), "expect": "`Hello $name`; then `$(printf command)`; then `Hello Ada`; then `command`."},
                        {"type": "cmd", "where": "shell", "title": "Indent a here-doc with tabs (<<-)", "code": C('''
cat <<-'EOF'
	line indented with a tab
	EOF
'''), "expect": "`line indented with a tab`."},
                        {"type": "text", "body": "Why does my indented here-doc fail? The two indented lines above start with actual tabs. `<<-` strips leading tabs from the body and delimiter, but does not strip spaces. The copy button preserves those tabs."},
                        {"type": "cmd", "where": "shell", "title": "Feed one string to a command (here-string <<<)", "code": C(r'''
LC_ALL=C tr '[:lower:]' '[:upper:]' <<< 'hello ada'
wc -l <<< 'one line'
'''), "expect": "`HELLO ADA`; then `       1`."},
                        {"type": "text", "body": "Does <<< add a newline? A here-string adds a newline. Here-strings and process substitution work in Bash 3.2 on macOS and in Bash on GNU/Linux; they are not POSIX sh syntax."},
                    ],
                },
                {
                    "h2": "Use a command's output as a file, or log a whole script",
                    "intro": "Use one command's output as a file: `<(cmd)` supplies a readable path. The separate `<` before it redirects that path into a loop.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Compare the output of two commands with diff (process substitution)", "code": C(r'''
cd /tmp/tw/m11-redirect
diff <(LC_ALL=C sort left.txt) <(LC_ALL=C sort right.txt)
printf 'diff exit=%s\n' "$?"
diff <(printf 'apple\n') <(printf 'pear\n')
printf 'diff exit=%s\n' "$?"
'''), "expect": "`diff exit=0`; then `1c1`; then `< apple`; then `---`; then `> pear`; then `diff exit=1`."},
                        {"type": "text", "body": "What does diff's exit code mean? Diff returns 0 for equal inputs, 1 for differences and a larger status for trouble. Process substitution's producer status is not returned by diff and is not covered by pipefail; use checked intermediate files when producer failure must stop the job."},
                        {"type": "cmd", "where": "shell", "title": "Keep a counter in a while-read loop (while read ... < <(command))", "code": C(r'''
cd /tmp/tw/m11-redirect
count=0
while IFS= read -r line; do count=$((count + 1)); done < <(LC_ALL=C sort left.txt)
printf 'count=%s\n' "$count"
'''), "expect": "`count=2`."},
                        {"type": "cmd", "where": "shell", "title": "Send everything a script prints to a log file (exec > logfile)", "code": C(r'''
cd /tmp/tw/m11-redirect
cat > logall.sh <<'EOF'
#!/bin/bash
exec > whole.log 2>&1
echo 'job started'
echo 'diagnostic' >&2
echo 'job finished'
EOF
bash logall.sh
cat whole.log
'''), "expect": "`job started`; then `diagnostic`; then `job finished`."},
                        {"type": "text", "body": "Log everything a script prints. Use `exec > logfile 2>&1` inside a script: it changes that shell's streams for all later commands. Running logall.sh as a child keeps your interactive prompt attached to the terminal."},
                    ],
                },
            ],
            "rules": {
                "h2": "Choose a redirection to save, hide or feed output",
                "cards": [
                    ("Save or throw away output", "Streams: stdin 0, stdout 1, stderr 2.", ["What you want", "Type this"], [
                        ["Save output / add output to the end of a file", "`cmd > file` / `cmd >> file`"],
                        ["Save only the errors", "`cmd 2> errors.log`"],
                        ["Save output and errors together", "`cmd > file 2>&1` or Bash `cmd &> file`"],
                        ["Throw away output and errors", "`cmd > /dev/null 2>&1`"],
                        ["See output and save it / add it to a file", "`cmd | tee file` / `cmd | tee -a file`"],
                    ]),
                    ("Type text into a command", "Quote the delimiter for literal text.", ["What you want", "Type this"], [
                        ["Feed lines with no expansion", "`cmd <<'EOF'` then body and `EOF`"],
                        ["Feed lines and expand $variables and commands", "`cmd <<EOF` then body and `EOF`"],
                        ["Remove leading tabs", "`cmd <<-'EOF'`"],
                        ["Feed one value followed by a newline", "`cmd <<< \"$value\"`"],
                    ]),
                    ("Use a command's output as a file", "Keep the receiving loop in the current shell.", ["What you want", "Type this"], [
                        ["Compare the output of two commands", "`diff <(cmd1) <(cmd2)`"],
                        ["Feed a loop without losing its variables (no pipe subshell)", "`while IFS= read -r x; do ...; done < <(cmd)`"],
                        ["Log everything the script prints from here on", "`exec > logfile 2>&1`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Check if two lists match after sorting",
                "frame": "Check if left.txt and right.txt match: they have the same fruit in a different order.",
                "open": "cd /tmp/tw/m11-redirect",
                "steps": [
                    (None, "`diff <(LC_ALL=C sort left.txt) <(LC_ALL=C sort right.txt)`", "Sort each list and read it through a path."),
                    (None, "`printf 'diff exit=%s\\n' \"$?\"`", "Check the result: an equal comparison has no diff text and a zero status."),
                ],
                "after": "diff exit=0",
                "meaning": "Compare sorted lists without temp files: no named temporary files are needed for this comparison.",
            },
            "practice": {
                "h2": "Check how to redirect output and feed input",
                "qs": [
                    ("Mechanism", "Why does cmd 2>&1 > file leave errors on the screen?", "Follow destinations left to right.", ["Stderr first copies stdout's terminal destination.", "Then stdout changes to file.", "The earlier stderr copy stays attached to the terminal."], "Use `cmd > file 2>&1`."),
                    ("Keystrokes", "How do I save output and errors and still see them on screen?", "Combine before the pipe.", ["Redirect stderr to stdout.", "Pipe the combined stream to tee."], "`cmd 2>&1 | tee run.log`."),
                    ("Application", "How do I write a file containing a literal $HOME with a here-doc?", "Quote the opening delimiter.", ["Start with `cat > script.sh <<'EOF'`.", "Type the body.", "End with `EOF` alone."], "A quoted delimiter keeps `$HOME` literal in the file."),
                    ("Common mistake", "Why does my <<- here-doc keep reading when I put spaces before EOF?", "Which indentation does the dash strip?", ["The dash strips tabs only.", "Spaces remain part of the delimiter line."], "Use actual tabs or put EOF at column 1."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Copy ready-made Bash scripts for backup, rename, retry and confirm",
            "subtitle": "Back up a folder, rename many files at once, run a command on every file, read flags, retry a failed command, ask before continuing",
            "idea": (
                "Copy one small script per job. Preview changes and check failures before continuing.",
                [
                    ("Back up a folder", "bash backup.sh source", "It saves the files in a dated tar archive."),
                    ("Preview renaming many files", "bash rename.sh", "Apply only after reading the dry run."),
                    ("Retry a failed command", "bash retry.sh 3 1 cmd", "Limit attempts and pause between them."),
                    ("Ask yes or no before continuing", "bash confirm.sh", "Only yes or y proceeds."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why did my quick command overwrite a file, retry forever or keep going after I said no?",
                "fix": "Keep a dry-run default, reject collisions, cap retries and treat EOF as a declined confirmation.",
            },
            "drills": [
                {
                    "h2": "Back up a folder and preview a rename",
                    "intro": BASH_FIRST + " Each example creates its script with a quoted here-doc and runs it with bash.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create practice folders for the ready-made scripts", "code": C(r'''
mkdir -p /tmp/tw/m11-scripts/source /tmp/tw/m11-scripts/photos /tmp/tw/m11-scripts/text
cd /tmp/tw/m11-scripts
cat > source/note.txt <<'EOF'
keep this note
EOF
printf 'image\n' > 'photos/red apple.jpeg'
printf 'image\n' > photos/blue.jpeg
printf 'one\ntwo\n' > 'text/red apple.txt'
printf 'three\n' > text/blue.txt
cat source/note.txt
'''), "expect": "`keep this note`."},
                        {"type": "cmd", "where": "shell", "title": "Back up a folder into a dated tar archive", "code": C(r'''
cd /tmp/tw/m11-scripts
cat > backup.sh <<'EOF'
#!/bin/bash
set -euo pipefail
src=${1:?usage: backup.sh FOLDER}
[[ -d $src ]] || { echo 'not a folder' >&2; exit 1; }
mkdir -p backups
archive=$(mktemp "$PWD/backups/backup-$(date +%Y%m%d).XXXXXX")
tar -czf "$archive" -C "$src" .
printf 'saved: %s\n' "${archive##*/}"
tar -tzf "$archive" | LC_ALL=C sort
EOF
bash backup.sh source
'''), "expect": "`saved: backup-<date>.<random>` (for example `backup-20261014.yebYbB`); then `./`; then `./note.txt`."},
                        {"type": "text", "body": "Will a second backup overwrite the first? No. The archive name contains today's date and a unique suffix, so a second run cannot overwrite an older backup. `tar -tzf` lists its contents without extracting. The printed name varies per run. BSD tar can preserve macOS metadata; GNU tar on Linux may show different metadata entries for real folders."},
                        {"type": "cmd", "where": "shell", "title": "Rename every .jpeg file to .jpg, previewing first (dry run)", "code": C(r'''
cd /tmp/tw/m11-scripts
cat > rename.sh <<'EOF'
#!/bin/bash
set -euo pipefail
mode=${1:---dry-run}
[[ $mode == --dry-run || $mode == --apply ]] || { echo 'usage: rename.sh [--dry-run|--apply]' >&2; exit 2; }
for f in photos/*.jpeg; do
  [[ -e $f ]] || continue
  to=${f%.jpeg}.jpg
  [[ ! -e $to && ! -L $to ]] || { printf 'collision: %s\n' "$to" >&2; exit 1; }
  printf '%s -> %s\n' "$f" "$to"
  [[ $mode != --apply ]] || mv -n "$f" "$to"
done
EOF
bash rename.sh
bash rename.sh --apply
printf '%s\n' photos/*.jpg
'''), "expect": "`photos/blue.jpeg -> photos/blue.jpg`; then `photos/red apple.jpeg -> photos/red apple.jpg`; then `photos/blue.jpeg -> photos/blue.jpg`; then `photos/red apple.jpeg -> photos/red apple.jpg`; then `photos/blue.jpg`; then `photos/red apple.jpg`."},
                        {"type": "text", "body": "Check the rename before you apply it. Read the first two preview lines before running `bash rename.sh --apply`. The example then prints the applied renames and final names. A collision stops the script; earlier renames are not rolled back. `mv -n` also avoids overwriting if a destination appears after the check."},
                    ],
                },
                {
                    "h2": "Run a command on many files and read flags",
                    "intro": "Reuse a flag parser: the input parsing is the pattern from Bash basics, now packaged as a reusable script.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Run a command on every file of one type in a folder", "code": C(r'''
cd /tmp/tw/m11-scripts
cat > each.sh <<'EOF'
#!/bin/bash
set -euo pipefail
[[ $# -ge 3 ]] || { echo 'usage: each.sh FOLDER EXT COMMAND [ARG...]' >&2; exit 2; }
dir=$1; ext=$2; shift 2
[[ -d $dir ]] || { echo 'not a folder' >&2; exit 1; }
for f in "$dir"/*."$ext"; do
  [[ -f $f ]] || continue
  printf '%s: ' "${f##*/}"
  "$@" < "$f"
done
EOF
bash each.sh text txt awk 'END { print NR " lines" }'
'''), "expect": "`blue.txt: 1 lines`; then `red apple.txt: 2 lines`."},
                        {"type": "text", "body": "Which commands work with each.sh? Use one that reads stdin: this batch helper passes each file on stdin. It visits immediate children only. Use the NUL-separated find pattern on page 1 for recursive work."},
                        {"type": "cmd", "where": "shell", "title": "Make a script read its flags (-v, -o) with usage and defaults", "code": C(r'''
cd /tmp/tw/m11-scripts
cat > flags.sh <<'EOF'
#!/bin/bash
set -euo pipefail
usage() { echo 'usage: flags.sh [-v] [-o DIR] [FILE...]'; }
verbose=0; out=reports
while getopts ':hvo:' opt; do
  case $opt in
    h) usage; exit 0 ;;
    v) verbose=1 ;;
    o) out=$OPTARG ;;
    :) printf 'missing value: -%s\n' "$OPTARG" >&2; usage >&2; exit 2 ;;
    \?) printf 'unknown flag: -%s\n' "$OPTARG" >&2; usage >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))
printf 'verbose=%s out=%s files=%s\n' "$verbose" "$out" "$#"
EOF
bash flags.sh
bash flags.sh -v -o 'my reports' -- 'red apple.txt'
bash flags.sh -o
printf 'exit=%s\n' "$?"
'''), "expect": "`verbose=0 out=reports files=0`; then `verbose=1 out=my reports files=1`; then `missing value: -o`; then `usage: flags.sh [-v] [-o DIR] [FILE...]`; then `exit=2`."},
                    ],
                },
                {
                    "h2": "Retry a failed command and ask before continuing",
                    "intro": "Retry a command with an attempt limit and a pause. The confirmation is tested with supplied input so this page runs without waiting.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Retry a failed command N times, pausing between attempts", "code": C(r'''
cd /tmp/tw/m11-scripts
cat > retry.sh <<'EOF'
#!/bin/bash
set -euo pipefail
[[ $# -ge 3 ]] || { echo 'usage: retry.sh N SECONDS COMMAND [ARG...]' >&2; exit 2; }
limit=$1; delay=$2; shift 2
[[ $limit =~ ^[1-9][0-9]*$ && $delay =~ ^[0-9]+$ ]] || { echo 'N must be positive; SECONDS must be nonnegative' >&2; exit 2; }
for ((attempt=1; attempt<=limit; attempt++)); do
  if "$@"; then printf 'success: attempt %s\n' "$attempt"; exit 0; else status=$?; fi
  printf 'failed: attempt %s status %s\n' "$attempt" "$status" >&2
  [[ $attempt -lt $limit ]] || exit "$status"
  sleep "$delay"
done
EOF
bash retry.sh 3 1 false
printf 'exit=%s\n' "$?"
bash retry.sh 3 1 true
'''), "expect": "`failed: attempt 1 status 1`; then `failed: attempt 2 status 1`; then `failed: attempt 3 status 1`; then `exit=1`; then `success: attempt 1`."},
                        {"type": "text", "body": "How many times does retry.sh try? N counts total attempts, including the first. Only failed attempts with another attempt left sleep. The final failure returns the command's status. Use retries for commands that are safe to repeat. A command or function tested in `if` must handle its own internal failures."},
                        {"type": "cmd", "where": "shell", "title": "Ask yes or no before continuing, and cancel if there is no answer", "code": C(r'''
cd /tmp/tw/m11-scripts
cat > confirm.sh <<'EOF'
#!/bin/bash
set -euo pipefail
printf 'Continue? [y/N] '
IFS= read -r answer || { echo 'cancelled (no input)'; exit 1; }
case $answer in
  y|Y|yes|YES) echo 'continuing' ;;
  *) echo 'cancelled'; exit 1 ;;
esac
EOF
printf 'yes\n' | bash confirm.sh
printf 'no\n' | bash confirm.sh
printf 'exit=%s\n' "$?"
bash confirm.sh < /dev/null
printf 'exit=%s\n' "$?"
'''), "expect": "`Continue? [y/N] continuing`; then `Continue? [y/N] cancelled`; then `exit=1`; then `Continue? [y/N] cancelled (no input)`; then `exit=1`."},
                        {"type": "text", "body": "Answer the prompt by hand: run `bash confirm.sh` at the terminal. The prompt uses `printf`, so it also appears when input is piped. Empty input, EOF and answers outside the listed yes forms cancel."},
                    ],
                },
                {
                    "h2": "Download a file, unzip an archive and run a script every night",
                    "intro": "Three jobs people search for by name. The commands also run in zsh.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Download a file from a url (curl)", "code": C('''
mkdir -p /tmp/tw/dl && cd /tmp/tw/dl
curl -LO https://example.com/index.html
curl -L -o example.html https://example.com
command ls
head -c 40 index.html
'''),
                         "expect": "Each `curl` prints a progress table that ends with `100  577` bytes received; the byte count can change. Then `ls` lists `example.html` and `index.html`, and `head` prints `<!doctype html><html lang=en><head><meta`. `-O` keeps the name from the url, `-o name` picks your own name and `-L` follows redirects."},
                        {"type": "cmd", "where": "shell", "title": "Unzip a downloaded archive (unzip, tar)", "code": C('''
mkdir -p /tmp/tw/archive/src && cd /tmp/tw/archive
echo 'hello' > src/a.txt
echo 'world' > src/b.txt
zip -qr photos.zip src
tar -czf notes.tar.gz src
unzip -l photos.zip
unzip -qo photos.zip -d unzipped
command ls unzipped/src
mkdir -p untarred && tar -xzf notes.tar.gz -C untarred
command ls untarred/src
'''),
                         "expect": "`unzip -l` lists the archive without opening it: a table with `Length Date Time Name`, the rows `src/`, `src/a.txt` and `src/b.txt` (order can differ), and `3 files` at the bottom. Then `ls` prints `a.txt` and `b.txt` from `unzipped/src`, and again from `untarred/src`. `-d unzipped` and `-C untarred` choose the folder to open the archive into. Use `tar -xzf` for `.tar.gz` and `unzip` for `.zip`."},
                        {"type": "code", "file": "crontab", "title": "Run my script every night (cron)", "code": C('''
0 2 * * * /Users/you/bin/backup.sh >> /tmp/backup.log 2>&1
''')},
                        {"type": "text", "body": "Run my script every night at 02:00: type `crontab -e`, paste the line above, save and quit. The five fields are minute, hour, day of month, month and day of week; `*` means every. `crontab -l` lists your jobs, so it prints that line. Write full paths, because cron runs with a small environment, and send output to a log file so you can read what happened. `crontab -r` removes all your jobs."},
                    ],
                },
            ],
            "rules": {
                "h2": "Choose the script for a backup, rename, batch job, retry or confirm",
                "cards": [
                    ("Back up a folder and rename files", "Preview first and avoid collisions.", ["What you want", "Type this"], [
                        ["Back up a folder", "`bash backup.sh source`"],
                        ["List what is inside an archive", "`tar -tzf ARCHIVE`"],
                        ["Preview the .jpeg renames", "`bash rename.sh`"],
                        ["Apply the previewed renames", "`bash rename.sh --apply`"],
                    ]),
                    ("Run a command on many files and read flags", "Reuse the templates above.", ["What you want", "Type this"], [
                        ["Count lines in every .txt file", "`bash each.sh text txt awk 'END { print NR }'`"],
                        ["Show the script's usage message", "`bash flags.sh -h`"],
                        ["Set an output folder and pass a file", "`bash flags.sh -v -o reports -- file.txt`"],
                    ]),
                    ("Retry a command or ask first", "Cap the retries and make no the default answer.", ["What you want", "Type this"], [
                        ["Try at most three times, pausing a second", "`bash retry.sh 3 1 COMMAND`"],
                        ["Ask before continuing", "`bash confirm.sh`"],
                        ["Answer yes automatically to test the script", "`printf 'yes\\n' | bash confirm.sh`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "See a script's default settings, then override them",
                "frame": "See what the flag parser does by default and with flags: it starts quiet and writes to reports.",
                "open": "cd /tmp/tw/m11-scripts",
                "steps": [
                    (None, "`bash flags.sh`", "See the default settings."),
                    (None, "`bash flags.sh -v -o 'my reports' -- 'red apple.txt'`", "Change the folder and keep one file name with a space whole."),
                ],
                "after": "verbose=0 out=reports files=0\nverbose=1 out=my reports files=1",
                "meaning": "Reuse the parser: the script prints the parsed settings. Replace that final printf with your job when you reuse it.",
            },
            "practice": {
                "h2": "Check how to use the ready-made scripts",
                "qs": [
                    ("Mechanism", "How many sleeps occur when retry.sh 3 1 false always fails?", "Sleep only when another attempt remains.", ["Attempt 1 fails and sleeps.", "Attempt 2 fails and sleeps.", "Attempt 3 fails and exits."], "Two sleeps and three attempts."),
                    ("Keystrokes", "How do I preview the .jpeg renames, then apply them after checking the output?", "Use the default mode first.", ["Run `bash rename.sh`.", "Read the proposed names.", "Run `bash rename.sh --apply`."], "Preview first; apply second."),
                    ("Application", "How do I run wc -c on every .txt file directly inside text/?", "The batch helper supplies the file on stdin.", ["Choose text as the folder and txt as the extension.", "Pass wc and -c as the command."], "`bash each.sh text txt wc -c`."),
                    ("Common mistake", "Why must confirm.sh cancel when stdin closes without an answer?", "A missing answer cannot mean approval.", ["Read returns a failure at EOF.", "The fallback prints cancelled and exits 1."], "Treat EOF as no and stop before the protected work."),
                ],
            },
        },
    ],
}
