> This content is from *TAMYMN-Git.md*, part of *The Absolute Minimum You Must Know*.

# Git: The Absolute Minimum You Must Know

Git looks like a hundred commands, but daily use rests on one mental model and about a
dozen commands — all on this page. In the AI age this doc matters *more*, not less: when
an assistant writes your code, `git diff` is how you review what it actually did, and a
commit is how you make its work safe to undo.

## The Mental Model: Three Places Your Code Lives

Every file exists in up to three places at once:

`git add` is you *composing* the next snapshot; `git commit` is the shutter click. That
one idea explains most beginner confusion: a file you edited but didn't `add` is not in
the commit you just made, and `git status` is simply a report of what's in which of the
three places.

## The Everyday Loop

A good commit message says *why*, not *what* — the diff already shows what. "Fix
off-by-one in pagination" beats "update utils.py".

## Starting: Init or Clone

`git init` creates a hidden `.git/` folder — that folder *is* the repository. Delete it
and the history is gone; copy the directory and the whole history comes along.

## Branches: Cheap Parallel Universes

A branch is just a movable label pointing at a commit — creating one costs nothing.

Work on a branch, keep `main` always working. If a merge stops with a **conflict**, don't
panic: Git has marked the clashing lines in the files with `>>>>>>`. Edit each marked file to keep what you want, delete the markers, then
`git add` the file and `git commit`. That's the whole procedure.

## Remotes: Push and Pull

`origin` is just the default nickname for "the remote you cloned from". Push rejected?
Someone pushed before you — `git pull`, resolve any conflict, push again.

## Undo, Safely

The habit that makes everything else low-stakes: **commit before you experiment.**
Committed work is essentially impossible to lose; uncommitted work is one bad command
from gone. This is also the rule for AI sessions — commit *before* letting an agent loose
on the code, and its whole session becomes one reviewable, revertible diff.

## Directing the Machine

An AI can run Git for you, but the informed prompt names the model on this page — the
three places, branches, staging — so you get exactly the operation you meant, and you can
verify it with `git status` afterwards.

Vague:

(Which changes — working directory, staged, or committed? Each needs a different command,
and the wrong one destroys work.)

Informed:

## Spot the Confabulation

An AI assistant explains how to undo a pushed commit:

```
Just run `git reset --hard HEAD~1` and then `git push`. This removes the bad
commit from the branch, and the push updates the remote to match.
```

What's wrong?

Two things. The push will be **rejected** — after `reset` your branch is *behind* the
remote, and Git refuses a push that would delete remote history (the AI would then
plausibly suggest `--force`, which rewrites history others may have already pulled).
And `--hard` also destroys any uncommitted work in your working directory as collateral
damage. The safe answer for anything already pushed is `git revert `: a *new*
commit that undoes the old one, which pushes normally.

## Where to Practice

- **Learn Git Branching** — an interactive
  visualisation where every command moves a commit graph you can see. The fastest way to
  make branches stop being abstract. No signup.
- **Oh My Git!** — a free open-source game that drills the same
  ideas with a real Git repository under the hood.

## Quick Reference

| Command | What it does |
|---|---|
| `git status` | what's changed and what's staged — run constantly |
| `git diff` / `git diff --staged` | unstaged / staged changes, line by line |
| `git add file` / `git add -p` | stage a file / stage hunk-by-hunk |
| `git commit -m "why"` | snapshot the staged changes |
| `git log --oneline` | history, one line per commit |
| `git init` / `git clone url` | new repo here / copy an existing one |
| `git switch -c name` / `git switch name` | create-and-enter a branch / move to one |
| `git merge name` | bring a branch's commits into this one |
| `git push origin main` / `git pull` | send commits up / bring commits down |
| `git restore file` | discard uncommitted edits (destructive!) |
| `git restore --staged file` | unstage, keeping the edits |
| `git revert ` | safe undo: new commit that reverses an old one |

That covers the absolute minimum! You can now snapshot, branch, sync, review any diff —
human or AI — and undo mistakes; everything else is a `git help ` away.
