# VS Code: The Absolute Minimum You Must Know

VS Code has thousands of features, but productive daily use rests on one master shortcut,
one habit about how you open projects, and a handful of built-ins — all on this page.
Learn these and the rest of the editor reveals itself on demand.

## The One Shortcut: The Command Palette

**Cmd-Shift-P** (macOS) / **Ctrl-Shift-P** (Windows/Linux) opens the **Command Palette** —
a search box over *everything the editor can do*. Every menu item, every setting, every
extension command lives there under a typeable name. You never need to memorise where a
feature is buried; you type roughly what you want:

```
>Python: Select Interpreter     # choose which Python runs your code
>Format Document                # reformat the current file
>Preferences: Open Settings     # any setting, searchable
>Toggle Word Wrap               # ...and literally everything else
```

This is the single highest-value fact about VS Code. When any guide says "go to menu X,
submenu Y", you can ignore it: palette, type three words, Enter. Its sibling **Cmd/Ctrl-P**
(no Shift) does the same for *files* — type part of a filename, Enter, you're there.

## Open the Folder, Not the File

Beginners double-click one `.py` file and wonder why nothing works well. **Always open the
project's folder** (`File > Open Folder...`, or `code .` from a [terminal](GLOSSARY.md#terminal) in that
directory). The open folder is your **workspace**, and it's what gives you the features
that matter: file-wide search (Cmd/Ctrl-Shift-F), [Git](GLOSSARY.md#git) integration, relative [imports](GLOSSARY.md#import) and
[paths](GLOSSARY.md#path) resolving correctly, and per-project settings. A lone file has none of that. If the
sidebar's file tree is empty, you opened a file, not a folder — fix that first.

## The Integrated Terminal

**Ctrl-`** (backtick) opens a real terminal *inside* the editor, already `cd`'d into your
workspace folder. It's the same shell as your system terminal — everything from
`TAMYMN-Linux.md` applies. Run your [scripts](GLOSSARY.md#script), run `git`, run [tests](GLOSSARY.md#test), all without leaving the
window. This matters for a subtle reason: the terminal is where you *verify* — the editor
shows what code says, the terminal shows what code does.

## Extensions: The Minimum Is One

VS Code out of the box is a fast text editor; extensions make it a Python IDE. Open the
Extensions sidebar (Cmd/Ctrl-Shift-X) and install **Python** (by Microsoft). That one
gives you error squiggles, autocompletion, go-to-definition, and the Run button. Then
stop. Resist collecting extensions — each one is startup time and noise, and most "top 10
extensions" lists are solving problems you don't have yet.

One habit the Python extension demands: check the **[interpreter](GLOSSARY.md#interpreter)** shown in the status bar
(bottom of the window). That's which Python environment runs your code and resolves your
imports — if VS Code can't find a package you *know* you installed, you almost certainly
installed it into a different environment than the one selected. `Python: Select
Interpreter` from the palette fixes it.

## Multi-Cursor in One Breath

Select a word, press **Cmd-D** / **Ctrl-D** repeatedly — each press adds a cursor at the
next occurrence, and everything you then type happens at every cursor at once
(**Alt/Option-click** places cursors anywhere). Rename five occurrences in one motion,
edit ten similar lines simultaneously. Esc returns to one cursor. That's the whole
feature, and it replaces an enormous amount of tedious repeated editing.

## Settings Sync Exists

Turn on **Settings Sync** (via the account icon, bottom-left) and your settings,
keybindings, and extensions follow your GitHub account to any machine. Set up once, never
reconfigure a fresh install by hand again. That's all you need to know — just that it
exists, so you don't lovingly hand-tune an editor you'll lose.

## Directing the Machine

AI help with editor problems is only as good as your description of the environment —
which folder is open, which interpreter is selected, what the terminal says. Vague
environment questions get generic answers; naming the concepts on this page gets the fix.

Vague:

```
"vscode can't find pandas, how do I fix it"
```

Informed:

```
"VS Code workspace is my project folder with a .venv/ inside it. The status bar shows
the interpreter as /usr/bin/python3, but I installed pandas into .venv. How do I make
the workspace use .venv's interpreter, and how do I check the integrated terminal
activates it too?"
```

The informed prompt has already localised the fault (interpreter mismatch), so the answer
can be exact instead of a checklist of guesses.

## Spot the Confabulation

An AI assistant troubleshoots a `ModuleNotFoundError`:

```
VS Code bundles its own Python for running your scripts, so open any terminal and run
`pip install requests` — VS Code shares one global Python installation, and the Run
button will pick the package up immediately.
```

<details><summary>What's wrong?</summary>

VS Code bundles no Python at all — it runs whichever interpreter is *selected* for the
workspace (shown in the status bar), and there is no "one global Python" shared with
every terminal. If the selected interpreter is a virtual environment and you
`pip install` into a different one, the error remains. The real fix: `Python: Select
Interpreter` to pick the right environment, then install into *that* environment (e.g.
from the integrated terminal with it activated).

</details>

## Where to Practice

- **[vscode.dev](https://vscode.dev)** — the real VS Code running in a browser tab, no
  install or signup. Open a folder and drill the palette, quick-open, and multi-cursor
  until they're reflexes.
- **The built-in walkthroughs** — `Help > Editor Playground` and the `Welcome` page's
  "Get Started" walkthroughs are interactive tours inside your own editor, covering
  multi-cursor and friends with live examples.

## Quick Reference

| Shortcut / action | What it does |
|---|---|
| **Cmd/Ctrl-Shift-P** | Command Palette — every feature, searchable |
| **Cmd/Ctrl-P** | jump to any file by typed name |
| `File > Open Folder` / `code .` | open the *project*, not one file |
| **Ctrl-`** | integrated terminal, already in your workspace |
| **Cmd/Ctrl-Shift-F** | search across the whole workspace |
| **Cmd/Ctrl-Shift-X** | Extensions sidebar — install **Python**, then stop |
| status bar interpreter / `Python: Select Interpreter` | which Python runs your code |
| **Cmd/Ctrl-D** (repeat) | add cursor at next occurrence — multi-edit |
| **Alt/Option-click** | place a cursor anywhere |
| Settings Sync (account icon) | settings and extensions follow you across machines |

That covers the absolute minimum! With the palette as your master key, a folder open, and
one extension installed, you can edit, run, and verify real projects — every other
feature is a Cmd-Shift-P search away.
