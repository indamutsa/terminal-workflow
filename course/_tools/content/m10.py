"""Module 10: Bash basics. Source: snippets run in /bin/bash 3.2 on macOS; no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


BASH_FIRST = "Type `bash` first: these snippets are bash, and zsh splits words differently. Type `exit` to return to zsh."

MODULE = {
    "n": 10,
    "folder": "m10-bash-basics",
    "title": "Bash basics",
    "footer": "Bash basics by task: variables, quoting, exit codes, if and case, for and while loops, script arguments and input",
    "tagline": "Look up the bash snippet for the job, type it, and see the real output.",
    "glossary": [
        ("tw-exit-code", "Exit code", ["exit code", "exit codes"], "A number every command leaves behind. 0 means it worked, anything else means it failed. Read it with $?."),
        ("tw-shebang", "Shebang", ["shebang"], "The first line of a script, such as #!/bin/bash. It names the program that runs the file."),
        ("tw-word-splitting", "Word splitting", ["word splitting"], "Bash cuts an unquoted $variable into words at every space, tab and newline (the IFS characters), then expands any * patterns. Quote it to keep it whole."),
    ],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Variables, quoting and exit codes",
            "subtitle": "Run a script, keep values in variables, quote them, and read whether a command worked.",
            "idea": (
                "Quote every variable, and read $? after a command to know if it worked.",
                [
                    ("Run a script", "bash hello.sh", "Or chmod +x it and run ./hello.sh."),
                    ("Keep a value", "name=Ada", "No spaces around the equals sign."),
                    ("Use it safely", "\"$name\"", "Double quotes keep spaces inside the value."),
                    ("Did it work", "echo $?", "0 is success, anything else is a failure."),
                ],
                None,
            ),
            "problem": {
                "fail": "A script works on `report.txt` and breaks on `my notes.txt`, or `name = Ada` says `command not found`.",
                "fix": "Write `name=Ada` with no spaces, and put `\"$name\"` in double quotes every time you use it.",
            },
            "drills": [
                {
                    "h2": "Run a script",
                    "intro": "A script is a text file of commands. Run it with `bash`, or make it executable and run it by path.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the sample files for this page", "code": C(r'''
mkdir -p /tmp/tw/vars && cd /tmp/tw/vars
cat > hello.sh <<'EOF'
#!/bin/bash
echo "Hello from a script"
EOF
printf 'first line\nsecond line\n' > 'my notes.txt'
cat hello.sh
'''),
                         "expect": "The two lines of the script print: `#!/bin/bash` and `echo \"Hello from a script\"`. The folder `/tmp/tw/vars` now holds `hello.sh` and `my notes.txt`."},
                        {"type": "cmd", "where": "shell", "title": "Run a script with bash, then run it as ./hello.sh", "code": C(r'''
cd /tmp/tw/vars
bash hello.sh
chmod +x hello.sh
./hello.sh
'''),
                         "expect": "`Hello from a script` prints twice, once from `bash hello.sh` and once from `./hello.sh`. Without the `chmod +x`, `./hello.sh` fails with `Permission denied`."},
                        {"type": "text", "body": "The first line `#!/bin/bash` is the shebang. It tells the system which program runs the file when you run `./hello.sh`. `bash hello.sh` ignores it."},
                    ],
                },
                {
                    "h2": "Variables and quotes",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Set a variable and print it", "code": C(r'''
name=Ada
echo "Hello, $name"
name = Ada
'''),
                         "expect": "`Hello, Ada` prints, then `bash: name: command not found`. With spaces, bash runs `name` as a command."},
                        {"type": "cmd", "where": "shell", "title": "Keep a $variable literal or expand it: double, single or no quotes", "code": C(r'''
name=Ada
echo "Hi $name"
echo 'Hi $name'
echo Hi $name
'''),
                         "expect": "Three lines: `Hi Ada`, `Hi $name`, `Hi Ada`. Single quotes print the text, double quotes and no quotes expand it."},
                        {"type": "cmd", "where": "shell", "title": "Stop a filename with a space from breaking", "code": C(r'''
cd /tmp/tw/vars
f='my notes.txt'
cat $f
cat "$f"
'''),
                         "expect": "`cat $f` fails twice: `cat: my: No such file or directory` and `cat: notes.txt: No such file or directory`. `cat \"$f\"` prints `first line` and `second line`."},
                        {"type": "cmd", "where": "shell", "title": "Put text right after a variable with ${var}", "code": C(r'''
fruit=apple
echo "$fruits"
echo "${fruit}s"
'''),
                         "expect": "The first `echo` prints an empty line, because `$fruits` is a different, unset variable. The second prints `apples`."},
                    ],
                },
                {
                    "h2": "Capture output and do arithmetic",
                    "intro": "`$(command)` swaps in what the command prints. `$(( ))` does whole-number maths.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Save a command's output in a variable with $(...)", "code": C(r'''
cd /tmp/tw/vars
first=$(head -1 'my notes.txt')
echo "First line: $first"
echo "Lines: $(wc -l < 'my notes.txt' | tr -d ' ')"
'''),
                         "expect": "`First line: first line` and `Lines: 2`."},
                        {"type": "cmd", "where": "shell", "title": "Do arithmetic with $(( ))", "code": C(r'''
a=7; b=3
echo $((a + b)) $((a * b)) $((a / b)) $((a % b))
((a++)); echo $a
echo "scale=2; 7/3" | bc
'''),
                         "expect": "Three lines: `10 21 2 1`, then `8`, then `2.33`. The integer sum, product, quotient and remainder come first, `((a++))` makes 7 into 8, and `bc` gives the decimals."},
                        {"type": "text", "body": "`$(( ))` drops the decimals: `7 / 3` is `2`. For decimals pipe the sum to `bc`."},
                        {"type": "cmd", "where": "shell", "title": "Print with echo or printf (tabs, padding, decimals)", "code": C(r'''
echo "a\tb"
printf 'a\tb\n'
printf '%s\n' one two three
printf '%05.2f\n' 3.14159
printf '%-6s|%4d\n' ab 7
'''),
                         "expect": "`echo` prints `a\\tb` with the backslash-t as typed. `printf` prints `a` and `b` with a real tab between them. Then `one`, `two`, `three` on separate lines, `03.14`, and `ab    |   7`."},
                    ],
                },
                {
                    "h2": "Exit codes",
                    "intro": "Every command leaves a number: `0` for success, anything else for failure. `$?` holds the last one.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Check if the last command worked with $?", "code": C(r'''
cd /tmp/tw/vars
ls hello.sh
echo $?
ls nope
echo $?
'''),
                         "expect": "`hello.sh` and `0`, then `ls: nope: No such file or directory` and `1`."},
                        {"type": "text", "body": "Linux differs: GNU `ls` exits with `2` for a missing file where macOS `ls` exits with `1`. Only `0` versus not `0` is portable."},
                        {"type": "cmd", "where": "shell", "title": "Exit a script with your own code, and read true and false", "code": C(r'''
cd /tmp/tw/vars
true; echo $?
false; echo $?
cat > check.sh <<'EOF'
echo "checking"
exit 3
EOF
bash check.sh
echo $?
'''),
                         "expect": "`0` for `true`, `1` for `false`, then `checking` from the script and `3`, the code `exit 3` set."},
                    ],
                },
            ],
            "rules": {
                "h2": "Variables and exit codes at a glance",
                "cards": [
                    ("Keep a value whole or let it split", "Bash splits an unquoted value at spaces, tabs and newlines (IFS), then expands `*` patterns. Quotes stop both.", ["Task", "Write"], [
                        ["Keep a value whole", "`\"$name\"`: one word, spaces kept. Use this by default."],
                        ["Print the text `$name` as typed", "`'$name'`: nothing expands."],
                        ["See what unquoted does", "`$name`: split and pattern-expanded, so `my notes.txt` breaks."],
                        ["Put text right after a value", "`\"${name}s\"`"],
                    ]),
                    ("Save output or do maths", "Three dollar forms that look alike.", ["Task", "Write"], [
                        ["Use a variable", "`$name`"],
                        ["Save what a command prints", "`first=$(head -1 file)`"],
                        ["Add or multiply whole numbers", "`$((a + b))`"],
                    ]),
                    ("Check if a command worked", "A command's success is a number.", ["Task", "Write"], [
                        ["Read the last command's result", "`echo $?`: 0 is success. Read it before running anything else."],
                        ["End a script with your own code", "`exit 3`"],
                        ["Make a command that always succeeds or fails", "`true` (code 0) or `false` (code 1)"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Print the line count of a file with a space in its name",
                "frame": "You want one sentence that says how many lines `my notes.txt` has.",
                "open": "cd /tmp/tw/vars",
                "steps": [
                    (None, "`file='my notes.txt'`", "The quotes keep the space inside the value."),
                    (None, "`n=$(wc -l < \"$file\" | tr -d ' ')`", "`wc -l` counts the lines. `tr -d ' '` removes the padding spaces macOS adds."),
                    (None, "`echo \"$file has $n lines\"`", "Double quotes keep the filename whole."),
                ],
                "after": "my notes.txt has 2 lines",
                "meaning": "Quote the variable and the filename stays one word, whatever is in it.",
            },
            "practice": {
                "h2": "Practice: variables and exit codes",
                "qs": [
                    ("Mechanism", "Why does `cat $f` fail when `f='my notes.txt'`, while `cat \"$f\"` works?",
                     "How many words does the command get?",
                     ["Without quotes bash cuts the value at the space.", "`cat` then gets two names, `my` and `notes.txt`.", "Quotes keep it as one name."],
                     "Unquoted `$f` splits into two words. `\"$f\"` stays one."),
                    ("Keystrokes", "Which line stores today's year in `y` and prints `Year: ...`?",
                     "Command substitution, then echo.",
                     ["Write `y=$(date +%Y)`.", "Write `echo \"Year: $y\"`."],
                     "`y=$(date +%Y)` then `echo \"Year: $y\"`."),
                    ("Application", "Make a script `fail.sh` that prints `oops` and ends with code 4. How do you check the code?",
                     "Put exit last, then read the code.",
                     ["Create it with `printf 'echo oops\\nexit 4\\n' > fail.sh`.", "Run `bash fail.sh`.", "Run `echo $?` straight after."],
                     "`bash fail.sh` prints `oops`, then `echo $?` prints `4`."),
                    ("Common mistake", "`count = 5` prints `count: command not found`. What is wrong?",
                     "Look at the spaces around the equals sign.",
                     ["Bash reads `count` as a command and `=` and `5` as its arguments.", "An assignment has no spaces around `=`."],
                     "Write `count=5`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Decisions",
            "subtitle": "Branch with if, test strings, numbers and files, and match patterns with case.",
            "idea": (
                "Put the test inside [[ ]] with spaces around everything, and let the exit code pick the branch.",
                [
                    ("Test a file", "[[ -f report.txt ]]", "Also -d, -e, -s and -x."),
                    ("Compare numbers", "[[ $n -gt 5 ]]", "Or (( n > 5 )) for maths."),
                    ("Match a pattern", "[[ $f == *.txt ]]", "No quotes around the pattern."),
                    ("Pick by value", "case $x in a) ... ;; esac", "Use | to join choices."),
                ],
                None,
            ),
            "problem": {
                "fail": "Your script tests `[ $name = Ada ]` and errors when the name is empty or has a space, or `[[ $n=5 ]]` is always true.",
                "fix": "Use `[[ ]]` with a space on every side of the operator: `[[ $n = 5 ]]`.",
            },
            "drills": [
                {
                    "h2": "if, elif, else",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the sample files for this page", "code": C(r'''
mkdir -p /tmp/tw/tests/data && cd /tmp/tw/tests
printf 'alpha\nbeta\n' > report.txt
: > empty.txt
printf '#!/bin/bash\necho run\n' > run.sh && chmod +x run.sh
ls
'''),
                         "expect": "`ls` lists `data`, `empty.txt`, `report.txt` and `run.sh`."},
                        {"type": "cmd", "where": "shell", "title": "Run one of three branches with if, elif and else", "code": C(r'''
n=7
if [[ $n -gt 10 ]]; then
  echo "big"
elif [[ $n -gt 5 ]]; then
  echo "medium"
else
  echo "small"
fi
'''),
                         "expect": "`medium` prints. The first test fails, the `elif` passes, and bash skips the `else`."},
                        {"type": "cmd", "where": "shell", "title": "Compare strings with = != -z -n", "code": C(r'''
s=hello
[[ $s == hello ]] && echo "same"
[[ $s != bye ]] && echo "different"
[[ -z "" ]] && echo "empty"
[[ -n $s ]] && echo "not empty"
'''),
                         "expect": "Four lines: `same`, `different`, `empty`, `not empty`."},
                        {"type": "cmd", "where": "shell", "title": "Compare numbers with -eq -lt -gt, and see why < fails", "code": C(r'''
[[ 3 -lt 10 ]] && echo "3 is less than 10"
[[ 5 -eq 5 ]] && echo "equal"
[[ 9 < 10 ]] || echo "as text, 9 sorts after 10"
'''),
                         "expect": "Three lines: `3 is less than 10`, `equal`, `as text, 9 sorts after 10`. Inside `[[ ]]`, `<` compares text, so use `-lt` for numbers."},
                    ],
                },
                {
                    "h2": "Test files and combine tests",
                    "intro": "Each file test is one letter. Join tests with `&&` and `||` inside the brackets.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Test if a file or folder exists with -f -d -e -s -x", "code": C(r'''
cd /tmp/tw/tests
[[ -f report.txt ]] && echo "file"
[[ -d data ]] && echo "folder"
[[ -e nope ]] || echo "missing"
[[ -s empty.txt ]] || echo "empty file"
[[ -x run.sh ]] && echo "runnable"
'''),
                         "expect": "Five lines: `file`, `folder`, `missing`, `empty file`, `runnable`."},
                        {"type": "cmd", "where": "shell", "title": "Combine tests with && and || inside [[ ]]", "code": C(r'''
cd /tmp/tw/tests
n=12
[[ -f report.txt && -s report.txt ]] && echo "has content"
[[ $n -lt 0 || $n -gt 10 ]] && echo "out of range"
'''),
                         "expect": "Two lines: `has content` and `out of range`."},
                        {"type": "cmd", "where": "shell", "title": "Match a filename pattern like *.txt", "code": C(r'''
f=notes.txt
[[ $f == *.txt ]] && echo "text file"
[[ $f == n* ]] && echo "starts with n"
[[ $f == "*.txt" ]] || echo "quoted, it is just those characters"
'''),
                         "expect": "Three lines: `text file`, `starts with n`, `quoted, it is just those characters`. A quoted pattern matches only itself."},
                        {"type": "cmd", "where": "shell", "title": "Test numbers with maths using (( ))", "code": C(r'''
n=7
(( n > 5 )) && echo "over 5"
(( n % 2 == 0 )) || echo "odd"
(( n * 2 == 14 )) && echo "double is 14"
'''),
                         "expect": "Three lines: `over 5`, `odd`, `double is 14`."},
                        {"type": "cmd", "where": "shell", "title": "Spot the missing spaces in [[ ]]", "code": C(r'''
n=7
[[ $n=5 ]] && echo "always true"
[[ $n = 5 ]] || echo "really false"
'''),
                         "expect": "`always true` prints because `7=5` is one non-empty word, so the test never compares. The second test, with spaces, is false, so `really false` prints."},
                    ],
                },
                {
                    "h2": "case and short-circuit",
                    "intro": "`case` picks a branch by pattern. `&&` and `||` run the next command on success or failure.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Pick a branch by value with case, patterns and |", "code": C(r'''
ans=yes
case $ans in
  y|yes) echo "going ahead" ;;
  n|no)  echo "stopping" ;;
  *)     echo "unknown: $ans" ;;
esac
'''),
                         "expect": "`going ahead` prints. `y|yes` matches `yes`, and each branch ends with `;;`."},
                        {"type": "cmd", "where": "shell", "title": "Run a different command by file extension with case", "code": C(r'''
for f in a.txt b.sh c.md; do
  case $f in
    *.txt|*.md) echo "$f: text" ;;
    *.sh)       echo "$f: script" ;;
  esac
done
'''),
                         "expect": "Three lines: `a.txt: text`, `b.sh: script`, `c.md: text`."},
                        {"type": "cmd", "where": "shell", "title": "Run a command only if another worked: cmd && echo ok || echo fail", "code": C(r'''
cd /tmp/tw/tests
[[ -f report.txt ]] && echo ok || echo fail
[[ -f nope ]] && echo ok || echo fail
'''),
                         "expect": "`ok` for the file that exists, `fail` for the one that does not."},
                        {"type": "cmd", "where": "shell", "title": "Fix the && || trap: fail prints even when the test passed", "code": C(r'''
cd /tmp/tw/tests
[[ -f report.txt ]] && false || echo "fail printed anyway"
if [[ -f report.txt ]]; then false; else echo "fail"; fi
echo "if/else done"
'''),
                         "expect": "`fail printed anyway` comes from the `&&` `||` line, because `false` failed. The `if` line prints no `fail`, because `else` runs only when the test fails. Then `if/else done`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Tests at a glance",
                "cards": [
                    ("Check a file or folder", "One letter after the dash.", ["Task", "Write"], [
                        ["Check a file exists", "`[[ -f x ]]` (a regular file)"],
                        ["Check a folder exists", "`[[ -d x ]]`"],
                        ["Check something exists (a broken symlink counts as missing)", "`[[ -e x ]]`"],
                        ["Check a file is not empty", "`[[ -s x ]]`"],
                        ["Check a file can be run (or a folder entered)", "`[[ -x x ]]`"],
                    ]),
                    ("Compare text and numbers", "Quote the right side of `=` to match it as literal text. Unquoted, it is a pattern.", ["Task", "Write"], [
                        ["Check two strings match", "`[[ $a = \"$b\" ]]` (`!=` for different)"],
                        ["Check a string is empty or not", "`[[ -z $a ]]` or `[[ -n $a ]]`"],
                        ["Compare whole numbers", "`[[ $a -lt $b ]]`. Also `-le -gt -ge -eq -ne`."],
                        ["Compare with maths symbols", "`(( a > b ))`"],
                    ]),
                    ("Run a command on pass or fail", "`a && b || c` is not if/else.", ["Task", "Write"], [
                        ["Run b only when a works", "`a && b`"],
                        ["Run c only when a fails", "`a || c`"],
                        ["Choose between two branches safely", "`if a; then b; else c; fi`"],
                        ["Avoid this shape", "`a && b || c` also runs c when b fails."],
                    ]),
                ],
            },
            "worked": {
                "h2": "Check that a file exists and has content",
                "frame": "A script should only read `report.txt` when it is there and not empty.",
                "open": "cd /tmp/tw/tests",
                "steps": [
                    (None, "`f=report.txt`", "Name the file once."),
                    (None, "`if [[ -f $f && -s $f ]]; then echo \"$f has data\"; else echo \"$f is missing or empty\"; fi`", "`-f` and `-s` must both pass."),
                    (None, "`f=empty.txt`, then run the `if` line again", "The file exists but `-s` fails."),
                ],
                "after": "report.txt has data\nempty.txt is missing or empty",
                "meaning": "One [[ ]] with && checks both facts before the script touches the file.",
            },
            "practice": {
                "h2": "Practice: decisions",
                "qs": [
                    ("Mechanism", "Why does `[[ 9 < 10 ]]` come out false?",
                     "Is `<` a number test or a text test?",
                     ["Inside `[[ ]]`, `<` compares text in dictionary order.", "As text, `9` sorts after `10`."],
                     "Use `-lt` for numbers: `[[ 9 -lt 10 ]]`."),
                    ("Keystrokes", "Which test is true when `$f` ends in `.log`?",
                     "A pattern on the right, no quotes.",
                     ["Use `==` inside `[[ ]]`.", "Put `*.log` on the right, unquoted."],
                     "`[[ $f == *.log ]]`."),
                    ("Application", "Write a case that prints `weekend` for `sat` or `sun` and `weekday` for anything else.",
                     "Join two choices with a pipe.",
                     ["Start with `case $d in`.", "Add `sat|sun) echo weekend ;;`.", "Add `*) echo weekday ;;` and `esac`."],
                     "`case $d in sat|sun) echo weekend ;; *) echo weekday ;; esac`."),
                    ("Common mistake", "`[[ -f report.txt ]] && false || echo fail` prints `fail` though the file exists. Why?",
                     "What runs after the middle command fails?",
                     ["`&&` runs `false`, which fails.", "`||` then runs on that failure."],
                     "`a && b || c` also runs `c` when `b` fails. Use `if` and `else`."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Loops",
            "subtitle": "Repeat a command over a list, files, a range, a counter or the lines of a file.",
            "idea": (
                "for walks a list, while repeats until a test fails, and while read walks lines.",
                [
                    ("Loop over files", "for f in *.txt; do ...; done", "Quote \"$f\" inside."),
                    ("Count to five", "for i in {1..5}; do ...; done", "Or for ((i=0; i<5; i++))."),
                    ("Read lines", "while read -r line; do ...; done < file", "Safe with spaces in a line."),
                    ("Split columns", "while IFS=, read -r a b", "IFS is the separator."),
                ],
                None,
            ),
            "problem": {
                "fail": "`for x in $(cat file)` cuts every line at its spaces, and a loop after a pipe loses the variable it set.",
                "fix": "Read lines with `while IFS= read -r line; do ...; done < file`, and quote `\"$f\"` in every loop.",
            },
            "drills": [
                {
                    "h2": "for loops",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the sample files for this page", "code": C(r'''
mkdir -p /tmp/tw/loops && cd /tmp/tw/loops
printf 'one\n' > a.txt
printf 'one\ntwo\n' > b.txt
printf 'one\ntwo\nthree\n' > 'c d.txt'
printf 'red apple\ngreen pear\nblue plum\n' > names.txt
printf 'Ada,36\nBo,41\nCy,29\n' > people.csv
ls
'''),
                         "expect": "`ls` lists `a.txt`, `b.txt`, `c d.txt`, `names.txt` and `people.csv`."},
                        {"type": "cmd", "where": "shell", "title": "Loop over a list of words", "code": C(r'''
for fruit in apple pear plum; do
  echo "fruit: $fruit"
done
'''),
                         "expect": "Three lines: `fruit: apple`, `fruit: pear`, `fruit: plum`."},
                        {"type": "cmd", "where": "shell", "title": "Loop over every .txt file", "code": C(r'''
cd /tmp/tw/loops
for f in *.txt; do
  echo "$f has $(wc -l < "$f" | tr -d ' ') lines"
done
'''),
                         "expect": "Four lines: `a.txt has 1 lines`, `b.txt has 2 lines`, `c d.txt has 3 lines`, `names.txt has 3 lines`. The name with a space stays whole."},
                        {"type": "cmd", "where": "shell", "title": "Skip the loop when no file matches *.zip", "code": C(r'''
cd /tmp/tw/loops
for f in *.zip; do echo "got $f"; done
for f in *.zip; do [[ -e $f ]] || continue; echo "got $f"; done
echo "done"
'''),
                         "expect": "The first loop prints `got *.zip`: no file matched, so the pattern itself is the value. The guarded loop prints nothing. Then `done`."},
                        {"type": "cmd", "where": "shell", "title": "Count from 1 to 5 with a range {1..5}", "code": C(r'''
for i in {1..5}; do printf '%s ' "$i"; done; echo
for c in {a..e}; do printf '%s ' "$c"; done; echo
'''),
                         "expect": "`1 2 3 4 5` on one line, then `a b c d e`."},
                        {"type": "cmd", "where": "shell", "title": "Count with a C-style for ((i=0; i<3; i++))", "code": C(r'''
for ((i=0; i<3; i++)); do
  echo "i=$i"
done
'''),
                         "expect": "Three lines: `i=0`, `i=1`, `i=2`."},
                        {"type": "cmd", "where": "shell", "title": "Count to a variable or by steps with seq", "code": C(r'''
n=3
echo {1..$n}
for i in $(seq 1 $n); do printf '%s ' "$i"; done; echo
seq 1 3 10
'''),
                         "expect": "`{1..3}` prints as typed, because braces do not expand a variable. Then `1 2 3` from `seq`, then `1`, `4`, `7`, `10` on separate lines: start 1, step 3, stop at 10."},
                        {"type": "text", "body": "`{1..$n}` does not expand a variable. Use `seq`. GNU `seq` works the same on Linux."},
                    ],
                },
                {
                    "h2": "while and until",
                    "intro": "`while` repeats as long as its test passes. `until` repeats as long as it fails.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Repeat while a counter is small", "code": C(r'''
i=1
while [[ $i -le 3 ]]; do
  echo "round $i"
  i=$((i + 1))
done
'''),
                         "expect": "Three lines: `round 1`, `round 2`, `round 3`."},
                        {"type": "cmd", "where": "shell", "title": "Repeat until a counter passes 3", "code": C(r'''
i=1
until [[ $i -gt 3 ]]; do
  echo "i=$i"
  ((i++))
done
'''),
                         "expect": "Three lines: `i=1`, `i=2`, `i=3`."},
                        {"type": "cmd", "where": "shell", "title": "Stop early with break, skip one with continue", "code": C(r'''
for i in 1 2 3 4 5; do
  [[ $i -eq 2 ]] && continue
  [[ $i -eq 4 ]] && break
  echo "i=$i"
done
'''),
                         "expect": "Two lines: `i=1` and `i=3`. Round 2 is skipped, and round 4 ends the loop."},
                    ],
                },
                {
                    "h2": "Read lines and columns",
                    "intro": "Use `while read -r` to take one line at a time. Feed it a file with `< file`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Read a file line by line with while read -r", "code": C(r'''
cd /tmp/tw/loops
while IFS= read -r line || [[ -n $line ]]; do
  echo "> $line"
done < names.txt
'''),
                         "expect": "Each line of `names.txt` with `> ` in front: `> red apple`, `> green pear`, `> blue plum`."},
                        {"type": "text", "body": "`|| [[ -n $line ]]` keeps a last line that has no newline at the end: `read` fails on it, but `$line` is still set."},
                        {"type": "cmd", "where": "shell", "title": "Loop over every line of a command's output", "code": C(r'''
cd /tmp/tw/loops
ls *.txt | while IFS= read -r f; do
  echo "got: $f"
done
'''),
                         "expect": "One line per file: `got: a.txt`, `got: b.txt`, `got: c d.txt`, `got: names.txt`."},
                        {"type": "cmd", "where": "shell", "title": "Split simple comma-separated lines (no quoted fields) with while IFS=, read -r", "code": C(r'''
cd /tmp/tw/loops
while IFS=, read -r name age; do
  echo "$name is $age"
done < people.csv
'''),
                         "expect": "Three lines: `Ada is 36`, `Bo is 41`, `Cy is 29`."},
                        {"type": "cmd", "where": "shell", "title": "Fix a counter that stays 0 after a pipe into while", "code": C(r'''
cd /tmp/tw/loops
count=0
cat names.txt | while read -r x; do count=$((count + 1)); done
echo "after pipe: $count"
while read -r x; do count=$((count + 1)); done < names.txt
echo "after redirect: $count"
'''),
                         "expect": "`after pipe: 0` and `after redirect: 3`. The piped loop ran in a subshell and counted a copy."},
                        {"type": "cmd", "where": "shell", "title": "Loop over lines safely, not with for x in $(cat file)", "code": C(r'''
cd /tmp/tw/loops
for w in $(cat names.txt); do echo "[$w]"; done
while IFS= read -r l || [[ -n $l ]]; do echo "[$l]"; done < names.txt
'''),
                         "expect": "Six lines first, one per word: `[red]`, `[apple]`, `[green]`, `[pear]`, `[blue]`, `[plum]`. Then three whole lines: `[red apple]`, `[green pear]`, `[blue plum]`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Loops at a glance",
                "cards": [
                    ("Pick a loop", "Pick by what you are walking.", ["Task", "Write"], [
                        ["Loop over every file", "`for f in *.txt; do ...; done`"],
                        ["Repeat a fixed count", "`for i in {1..5}` or `for ((i=0; i<5; i++))`"],
                        ["Repeat a count held in a variable", "`for i in $(seq 1 $n)`"],
                        ["Read every line of a file", "`while IFS= read -r line || [[ -n $line ]]; do ...; done < file`"],
                        ["Split a line into columns", "`while IFS=, read -r a b; do ...; done < file`"],
                    ]),
                    ("Stop, skip or repeat", "Four words steer a loop.", ["Task", "Write"], [
                        ["Leave the loop now", "`break`"],
                        ["Skip to the next round", "`continue`"],
                        ["Repeat while a test passes", "`while test; do ...; done`"],
                        ["Repeat until a test passes", "`until test; do ...; done`"],
                    ]),
                    ("Avoid two traps", "Both lose data without an error.", ["Task", "Write"], [
                        ["Loop over lines that contain spaces", "`while IFS= read -r x; do ...; done < file`, not `for x in $(cat file)`"],
                        ["Keep a variable set inside the loop", "`while read ...; done < file`, not `cmd | while read`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Add up the ages in a CSV",
                "frame": "`people.csv` has `name,age` on each line. You want the total of the ages.",
                "open": "cd /tmp/tw/loops",
                "steps": [
                    (None, "`total=0`", "Start the sum."),
                    (None, "`while IFS=, read -r name age; do total=$((total + age)); done < people.csv`", "Each line splits at the comma. The loop reads from the file, so `total` survives."),
                    (None, "`echo \"total age: $total\"`", "Print the sum."),
                ],
                "after": "total age: 106",
                "meaning": "Redirecting the file in keeps the loop in your shell, so the variable is still set afterwards.",
            },
            "practice": {
                "h2": "Practice: loops",
                "qs": [
                    ("Mechanism", "Why is `count` still `0` after `cat f | while read -r x; do count=$((count+1)); done`?",
                     "Where does each side of a pipe run?",
                     ["Each side of a pipe runs in its own subshell.", "The loop changes a copy of `count`.", "The copy disappears when the pipe ends."],
                     "Feed the loop with `< f` instead of a pipe."),
                    ("Keystrokes", "Which loop prints `a.txt`, `b.txt` and the rest of the `.txt` files, even when a name has a space?",
                     "A glob, with quotes on the variable.",
                     ["Use `for f in *.txt; do`.", "Write `echo \"$f\"`.", "Close with `done`."],
                     "`for f in *.txt; do echo \"$f\"; done`."),
                    ("Application", "Print `Ada`, `Bo` and `Cy` from `people.csv`, one per line.",
                     "Split at the comma and ignore the age.",
                     ["Write `while IFS=, read -r name age; do`.", "Write `echo \"$name\"`.", "End with `done < people.csv`."],
                     "`while IFS=, read -r name age; do echo \"$name\"; done < people.csv`."),
                    ("Common mistake", "`for f in *.zip` prints `*.zip` when there are no zip files. How do you stop that?",
                     "Test that the file exists inside the loop.",
                     ["With no match the pattern stays as text.", "Add `[[ -e $f ]] || continue` as the first line of the loop."],
                     "`for f in *.zip; do [[ -e $f ]] || continue; ...; done`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Script input",
            "subtitle": "Read arguments, flags and typed answers, and stop with a usage message on bad input.",
            "idea": (
                "A script reads its arguments from $1, $2 and $@, and its flags from a case loop or getopts.",
                [
                    ("Read the first argument", "$1", "$2 is the second, $# is the count."),
                    ("Give a default", "${1:-world}", "Used when $1 is empty."),
                    ("Parse flags", "getopts \"vn:\" opt", "A colon means the flag takes a value."),
                    ("Ask the user", "read -p \"Name: \" name", "-s hides it, -t 5 times out."),
                ],
                None,
            ),
            "problem": {
                "fail": "Your script breaks on `bash backup.sh \"my folder\"`, or runs with a missing argument and does the wrong thing.",
                "fix": "Quote `\"$@\"` and `\"$1\"`, require what you need with `${1:?usage}`, and print usage and `exit 1` on bad input.",
            },
            "drills": [
                {
                    "h2": "Arguments",
                    "intro": "Each script is created with a here-doc and run with `bash name.sh args`, so it works from zsh too.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Read the arguments: $0 $1 $2 $# and $@", "code": C(r'''
mkdir -p /tmp/tw/args && cd /tmp/tw/args
cat > show.sh <<'EOF'
echo "script: $0"
echo "first:  $1"
echo "second: $2"
echo "count:  $#"
echo "all:    $@"
EOF
bash show.sh apple "red pear" plum
'''),
                         "expect": "Five lines: `script: show.sh`, `first:  apple`, `second: red pear`, `count:  3`, `all:    apple red pear plum`. The quoted `red pear` is one argument."},
                        {"type": "cmd", "where": "shell", "title": "Keep arguments with spaces whole: \"$@\" versus $* and \"$*\"", "code": C(r'''
cd /tmp/tw/args
cat > each.sh <<'EOF'
for a in "$@"; do echo "[$a]"; done
echo ---
for a in $*; do echo "[$a]"; done
echo ---
for a in "$*"; do echo "[$a]"; done
EOF
bash each.sh one "two words" three
'''),
                         "expect": "Three groups. `\"$@\"` prints `[one]`, `[two words]`, `[three]`. `$*` prints `[one]`, `[two]`, `[words]`, `[three]`. `\"$*\"` prints `[one two words three]`. Each group is separated by `---`."},
                        {"type": "cmd", "where": "shell", "title": "Walk through every argument with shift", "code": C(r'''
cd /tmp/tw/args
cat > shiftall.sh <<'EOF'
while [[ $# -gt 0 ]]; do
  echo "arg: $1 (left: $#)"
  shift
done
EOF
bash shiftall.sh a b c
'''),
                         "expect": "Three lines: `arg: a (left: 3)`, `arg: b (left: 2)`, `arg: c (left: 1)`. Each `shift` drops `$1` and the rest move up."},
                        {"type": "cmd", "where": "shell", "title": "Take arguments two at a time with shift 2", "code": C(r'''
cd /tmp/tw/args
cat > pairs.sh <<'EOF'
[[ $(( $# % 2 )) -eq 0 ]] || { echo "usage: pairs.sh KEY VALUE ..." >&2; exit 1; }
while [[ $# -gt 0 ]]; do
  echo "$1 = $2"
  shift 2
done
EOF
bash pairs.sh host web port 80
'''),
                         "expect": "Two lines: `host = web` and `port = 80`. With an odd count, such as `bash pairs.sh host web port`, it prints `usage: pairs.sh KEY VALUE ...` and stops."},
                    ],
                },
                {
                    "h2": "Defaults, required values and usage",
                    "intro": "`${1:-x}` falls back to `x`. `${1:?message}` stops the script with the message when `$1` is missing.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Give an argument a default value with ${1:-default}", "code": C(r'''
cd /tmp/tw/args
cat > greet.sh <<'EOF'
name=${1:-world}
echo "Hello, $name"
EOF
bash greet.sh
bash greet.sh Ada
'''),
                         "expect": "`Hello, world` with no argument, then `Hello, Ada`."},
                        {"type": "cmd", "where": "shell", "title": "Require an argument with ${1:?usage}", "code": C(r'''
cd /tmp/tw/args
cat > need.sh <<'EOF'
file=${1:?usage: need.sh FILE}
echo "using $file"
EOF
bash need.sh
echo "exit: $?"
bash need.sh data.csv
'''),
                         "expect": "`need.sh: line 1: 1: usage: need.sh FILE` and `exit: 1`: the script stopped. Then `using data.csv`."},
                        {"type": "cmd", "where": "shell", "title": "Print a usage message and exit 1 on bad input", "code": C(r'''
cd /tmp/tw/args
cat > copy2.sh <<'EOF'
usage() { echo "usage: copy2.sh SRC DEST" >&2; exit 1; }
[[ $# -eq 2 ]] || usage
echo "copying $1 to $2"
EOF
bash copy2.sh a
echo "exit: $?"
bash copy2.sh a b
'''),
                         "expect": "`usage: copy2.sh SRC DEST` and `exit: 1` for one argument. Then `copying a to b`."},
                        {"type": "text", "body": "`usage() { ...; }` is a function. Module 11 covers them."},
                    ],
                },
                {
                    "h2": "Flags",
                    "intro": "Two ways to read flags: a `case` loop with `shift`, or the built-in `getopts`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Read -n NAME and --name NAME flags with a case loop", "code": C(r'''
cd /tmp/tw/args
cat > parse.sh <<'EOF'
name=world
loud=0
while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--name) [[ $# -ge 2 && -n $2 ]] || { echo "missing NAME" >&2; exit 1; }; name=$2; shift 2 ;;
    -l|--loud) loud=1; shift ;;
    *) echo "unknown option: $1"; exit 1 ;;
  esac
done
msg="Hello, $name"
[[ $loud -eq 1 ]] && msg=$(echo "$msg" | tr a-z A-Z)
echo "$msg"
EOF
bash parse.sh --name Ada
bash parse.sh -l -n Bo
bash parse.sh --bogus
echo "exit: $?"
'''),
                         "expect": "Four lines: `Hello, Ada`, `HELLO, BO`, `unknown option: --bogus`, `exit: 1`."},
                        {"type": "cmd", "where": "shell", "title": "Read a script's flags with getopts", "code": C(r'''
cd /tmp/tw/args
cat > opts.sh <<'EOF'
verbose=0
name=world
while getopts "vn:" opt; do
  case $opt in
    v) verbose=1 ;;
    n) name=$OPTARG ;;
    *) echo "usage: opts.sh [-v] [-n NAME] [file...]"; exit 1 ;;
  esac
done
shift $((OPTIND - 1))
echo "verbose=$verbose name=$name rest=$*"
EOF
bash opts.sh -v -n Ada one two
bash opts.sh -x
'''),
                         "expect": "`verbose=1 name=Ada rest=one two`. Then for `-x`, getopts prints `opts.sh: illegal option -- x` and the script prints its usage line."},
                        {"type": "text", "body": "In `getopts \"vn:\"`, `v` is a switch and `n:` takes a value, held in `$OPTARG`. `OPTIND` is the index of the next argument, so `shift $((OPTIND - 1))` leaves only the files."},
                    ],
                },
                {
                    "h2": "Ask the user",
                    "intro": "`read` waits for a typed line. These scripts wait for you, so type the answer and press Enter.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Ask a question and store the answer with read -p", "code": C(r'''
cd /tmp/tw/args
cat > ask.sh <<'EOF'
read -p "Your name: " name
echo "Hi $name"
EOF
bash ask.sh
'''),
                         "expect": "`Your name: ` waits. Type `Ada` and press Enter: `Hi Ada` prints."},
                        {"type": "cmd", "where": "shell", "title": "Type a password without showing it using read -s", "code": C(r'''
cd /tmp/tw/args
cat > secret.sh <<'EOF'
read -s -p "Password: " pw
echo
echo "got ${#pw} characters"
EOF
bash secret.sh
'''),
                         "expect": "`Password: ` waits and shows nothing as you type. After Enter, the cursor moves to a new line and `got 7 characters` prints for a 7-letter password such as `hunter2`."},
                        {"type": "cmd", "where": "shell", "title": "Give up waiting for input after 3 seconds with read -t", "code": C(r'''
cd /tmp/tw/args
cat > quick.sh <<'EOF'
read -t 3 -p "Answer in 3 seconds: " a || echo " too slow"
EOF
bash quick.sh
'''),
                         "expect": "`Answer in 3 seconds: ` waits. With no input, after 3 seconds ` too slow` appears on the same line."},
                        {"type": "cmd", "where": "shell", "title": "Keep backslashes in typed text with read -r", "code": C(r'''
printf 'C:\\temp\n' | { read line; echo "plain: $line"; }
printf 'C:\\temp\n' | { read -r line; echo "raw:   $line"; }
'''),
                         "expect": "`plain: C:temp`, because plain `read` eats the backslash. Then `raw:   C:\\temp`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Script input at a glance",
                "cards": [
                    ("Read the arguments", "Set by bash when the script starts.", ["Task", "Write"], [
                        ["Read the first argument", "`$1` (`$2` is the second)"],
                        ["Count the arguments", "`$#`"],
                        ["Pass every argument on, each kept whole", "`\"$@\"`"],
                        ["Print the script name", "`$0`"],
                        ["Avoid this one", "`$*` cuts arguments at spaces"],
                    ]),
                    ("Default, required or checked", "Decide what a missing argument means.", ["Task", "Write"], [
                        ["Use a default when $1 is empty", "`${1:-world}`"],
                        ["Stop with a message when $1 is empty", "`${1:?usage: x FILE}`"],
                        ["Run your own usage check", "`[[ $# -eq 2 ]] || usage`"],
                    ]),
                    ("Ask the user", "Flags that change how read waits.", ["Task", "Write"], [
                        ["Show a prompt", "`read -p \"Name: \" name`"],
                        ["Hide what is typed", "`read -s pw`"],
                        ["Give up after 5 seconds", "`read -t 5 a`"],
                        ["Keep backslashes as typed", "`read -r line`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Greet by name with a default and a loud switch",
                "frame": "`parse.sh` greets `world` by default, takes `-n NAME`, and shouts with `-l`.",
                "open": "cd /tmp/tw/args",
                "steps": [
                    (None, "`bash parse.sh`", "No flags: the default name stays."),
                    (None, "`bash parse.sh -l -n Bo`", "The loop reads `-l`, then `-n` and its value with `shift 2`."),
                ],
                "after": "Hello, world\nHELLO, BO",
                "meaning": "A case loop with shift handles flags in any order, and the `*)` branch rejects anything else.",
            },
            "practice": {
                "h2": "Practice: script input",
                "qs": [
                    ("Mechanism", "What do `\"$@\"` and `$*` do differently with `one \"two words\" three`?",
                     "Count the words each one produces.",
                     ["`\"$@\"` gives three words, keeping `two words` together.", "Unquoted `$*` gives four words."],
                     "`\"$@\"` keeps each argument whole. `$*` cuts at spaces."),
                    ("Keystrokes", "Which line sets `dir` to the first argument, or `.` when none is given?",
                     "A default with a colon and a dash.",
                     ["Use `${1:-.}`.", "Assign it with `dir=`."],
                     "`dir=${1:-.}`."),
                    ("Application", "Write the line that makes a script stop with `usage: run.sh FILE` when no file is given.",
                     "A required value with a question mark.",
                     ["Use `${1:?...}`.", "Put the usage text after the question mark."],
                     "`file=${1:?usage: run.sh FILE}`."),
                    ("Common mistake", "Your `getopts \"vn:\"` script sees `-n` but `$name` is empty. What did you forget?",
                     "Where does getopts put a flag's value?",
                     ["A flag that ends in `:` takes a value.", "The value is in `$OPTARG`, not in `$1`."],
                     "Write `n) name=$OPTARG ;;`."),
                ],
            },
        },
    ],
}
