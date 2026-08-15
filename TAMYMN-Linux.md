# Linux Command Line: The Absolute Minimum You Must Know

The Linux command line looks intimidating, but effective daily use rests on about twenty
commands and a handful of survival keys — all on this page. Read it once, then keep it open
beside your terminal until the commands are muscle memory.

## Reading the Prompt

When you open a terminal or log into a Linux machine, you'll see something like:

```
root@station:/office#
analyst@station:~$
```

That's **who** you are `@` **which machine** `:` **which directory you're standing in**, then
`#` or `$`. A `#` means you are **root** (the all-powerful administrator); a `$` means a normal
user. The `~` is shorthand for your **home directory**. Glance at the prompt whenever you're
unsure — it answers "who am I and where am I?" before you ask.

## Where Am I? Moving Around

```
pwd            # print the directory you're standing in
ls             # list the files here
ls -l          # long listing: permissions, owner, size
ls -a          # include hidden files (names starting with .)
cd /var/log    # go to a directory by absolute path
cd reports     # go into a subdirectory (relative to here)
cd ..          # go up one level
cd             # jump back to your home directory
```

Two kinds of path: an **absolute** path starts with `/` and works from anywhere
(`/var/log/syslog`); a **relative** path is measured from where you're standing
(`reports/summary.txt`). Three abbreviations: `.` is the directory you're in, `..` is its
parent, `~` is your home.

That also explains a common stumble: `./start.sh` means "run the file `start.sh` *right
here*". The shell won't run a program from the current directory by name alone — that's a
safety feature — so you spell out the `./`.

## Looking Inside Files

```
cat notes.txt        # print the whole file at once — fine for short files
less /var/log/syslog # page through a long file
man grep             # read a command's manual (opens in less)
```

Inside `less` (and `man`): **space** or arrow keys to move, **`/text`** then Enter to search,
**`q`** to quit. If your terminal ever seems frozen showing a wall of text with a `:` or
`(END)` at the bottom, you're in a pager — press `q`.

## The Keys That Save You

- **Tab** — autocompletes file and command names; press it twice to see the options. Use it
  constantly: it's faster than typing and it can't misspell a filename.
- **↑ (arrow-up)** — brings back previous commands to edit and re-run.
- **Ctrl-C** — stops the command that's currently running.
- **`q`** — leaves `less` and `man`.
- **`exit`** — leaves the current shell (or an `ssh` session).
- Trapped in `vi`/`vim` by accident? Press **Esc**, type **`:q!`**, press Enter.

## Editing a File

```
nano answers.md
```

Type normally. **Ctrl-O** then Enter saves ("write **O**ut"); **Ctrl-X** exits. The shortcuts
are printed along the bottom of the screen — `^` means Ctrl. That's the whole [editor](GLOSSARY.md#editor).

## Everyday Housekeeping

```
mkdir reports              # make a directory
cp data.zip backup.zip     # copy
mv draft.txt final.txt     # move — also how you rename
rm old.log                 # delete — there is no recycle bin
```

## Permissions in One Breath

```
$ ls -l salaries.csv
-rw-r----- 1 root hr 1204 Aug 15 10:02 salaries.csv
```

Read `rw-r-----` as three triplets — **owner**, **group**, **others** — each `r`ead, `w`rite,
e`x`ecute. Here the owner (`root`) can read and write, the `hr` group can read, everyone else
gets nothing. Change it numerically (`chmod 640 file` — 4=read, 2=write, 1=execute, added up
per triplet) or symbolically (`chmod g+w file`). `chown root:hr file` sets owner and group;
`id jane` shows which groups jane belongs to.

## Combining Commands

The shell's superpower is plumbing small commands together. Four fittings cover most needs:

```
sort names.txt > sorted.txt      # >  sends output into a file (overwrites it)
ps aux | grep ssh                # |  pipes output into the next command
echo "today is $(date)"          # $( ) drops one command's output into another
wc -w texts/*.txt                # *  matches every file ending in .txt
```

Quotes matter: `'single quotes'` keep text exactly as typed; `"double quotes"` still let
`$(...)` and `$variables` expand. When a command's argument contains spaces or symbols,
quote it.

`grep` deserves its own line — it finds text: `grep 'password=' access.log` prints matching
lines, `-c` counts them instead, `-a` forces a binary-ish file to be treated as text.

## Being Someone Else, Being Somewhere Else

```
sudo systemctl restart nginx   # run one command as root
sudo -u rico cat report.txt    # run one command as a different user (rico)
```

```
ssh pc2                        # log into another machine — watch the prompt change
exit                           # ...and come back
ssh server 'uptime'            # run ONE command over there and return immediately
```

Note the difference: bare `ssh pc2` moves you there until you `exit`; `ssh host 'command'`
comes straight back on its own — no `exit` needed.

## What's Running? What's Listening?

```
ps aux                # every process; pipe into grep to find one
ss -tlnp              # TCP ports something is listening on, and which process owns them
```

These two are how you ask a machine "what are you actually doing right now?"

## Where to Practice

The best free practice ground is **[OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)** —
a security-themed wargame where each level is one small Linux puzzle, played over `ssh` from
any terminal (levels 0–10 cover everything on this page). Each level's page lists the commands
you might need, so it doubles as a guided tour.

## Quick Reference

| Command | What it does |
|---|---|
| `pwd` | print current directory |
| `ls` / `ls -l` / `ls -a` | list files / with details / including hidden |
| `cd dir` / `cd ..` / `cd` | enter a directory / go up / go home |
| `cat file` | print a whole file |
| `less file` | page through a file (`q` quits, `/` searches) |
| `man cmd` | manual for a command (`q` quits) |
| `nano file` | edit a file (Ctrl-O save, Ctrl-X exit) |
| `mkdir` / `cp` / `mv` / `rm` | make dir / copy / move-rename / delete |
| `chmod 640 file` | change permissions (numeric or `g+w` style) |
| `chown user:group file` | change owner and group |
| `id user` | show a user's groups |
| `grep 'text' file` | find lines containing text (`-c` count, `-a` force text) |
| `cmd > file` | send output into a file |
| `cmd1 \| cmd2` | pipe output into the next command |
| `"$(cmd)"` | use a command's output as an argument |
| `sudo cmd` / `sudo -u user cmd` | run as root / as another user |
| `ssh host` / `ssh host 'cmd'` | log in remotely / run one remote command |
| `ps aux` | list running processes |
| `ss -tlnp` | list listening ports |
| `exit` | leave this shell or ssh session |
| **Tab** / **↑** / **Ctrl-C** | autocomplete / previous command / stop |

That covers the absolute minimum! With these twenty-odd commands and the survival keys, you
can navigate, read, edit, and investigate on any Linux system — everything else is a `man`
page away.
