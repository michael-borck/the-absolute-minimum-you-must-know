# AI Coding Agents: The Absolute Minimum You Must Know

An AI coding agent can edit your files, run your tests, and build features while you
watch. Working with one safely rests on a single division of labour — **you direct, it
implements, you verify** — and this page is the operating manual for all three parts.
It's also the capstone of every other TAMYMN doc: they exist so you can do the first and
third jobs well.

## The Mental Model: An LLM in a Loop with Tools

A chat model answers once. An **agent** is that same model put in a loop and handed
tools: it can *read your files*, *run commands*, *edit code*, see what happened, and go
again — read the failing test, edit the function, re-run, repeat — until it decides the
job is done. That loop is what makes agents powerful, and it's also the risk: every tool
call really happens, to your real files. Two consequences fall straight out of the model:

- **The agent only knows what enters the loop.** It reads what it opens and what you
  tell it — not your intentions, your team's conventions, or the requirement you forgot
  to mention. Missing context doesn't stop it; it fills gaps with plausible guesses,
  confidently (that's what "confabulation" sections across this repo train you for).
- **"Done" is the agent's opinion.** It stops when its own checks pass — which is not
  the same as correct. Establishing correctness is your job, and it's checkable, not
  vibes: the diff and the tests.

## Before You Let It Loose: Commit

From `TAMYMN-Git.md`: commit before you experiment — and an agent session *is* an
experiment. Start every session from a clean working tree:

```
git status          # clean? nothing you'd mourn?
git add -A && git commit -m "Checkpoint before agent session"
```

Now the agent's entire session, however many files it touches, is **one reviewable,
revertible diff**. `git diff` shows everything it did; `git restore .` (or a revert)
erases it. This one habit converts "an AI is editing my code" from frightening to
routine — the worst case becomes "throw the diff away and re-prompt".

## The Verify Loop

After the agent reports success, the work moves to your side of the table:

```
git diff                 # read EVERY change — the agent's report is a claim, the diff is the fact
                         # did it touch files it had no business touching?
pytest                   # run the tests YOURSELF, in your terminal — don't take "all green" on trust
```

Then the standard that decides whether the change lands: **never merge what you can't
explain.** For each hunk of the diff, you should be able to say what it does and why it's
needed. Watch especially for the classic agent shortcuts: tests edited or skipped to make
them pass, error handling that swallows the error, hard-coded values where logic should
be, and dependencies added casually. Tests are your leverage here (`TAMYMN-Testing.md`):
a good test suite is a machine for verifying agent work at scale — which is why "write
the failing test first, then let the agent make it pass" is one of the strongest agent
workflows there is.

## Standing Instructions: AGENTS.md / CLAUDE.md

Agents look for an instruction file in your repo root — `AGENTS.md` by convention, or a
tool-specific name like `CLAUDE.md` — and read it at the start of every session. Anything
you'd otherwise repeat in every prompt goes there:

```
# AGENTS.md
- Run tests with: pytest -q
- Python 3.12; use type hints; no new dependencies without asking
- Never edit files under migrations/
- Docs examples are doctests — scripts/test_docs.py must pass
```

Think of it as version-controlled onboarding for a very fast, very literal new
teammate. When an agent keeps making the same mistake, the fix is usually a line in this
file, not a longer prompt.

## Directing the Machine

This section is the heart of the doc. **Context is everything**: the agent acts on what
it can see, so a prompt's quality is measured by how little it leaves to guesswork. Three
ingredients separate an informed prompt from a vague one: **name the files** (where to
look and where to change), **state the constraints** (what must not change, which style,
which dependencies), and **give acceptance criteria** (how you'll both know it worked —
ideally a command that must pass). This is `TAMYMN-Computational-Thinking.md` applied to
delegation: decompose the goal, make the implicit explicit, define done.

Vague:

```
"the login is broken, fix it"
```

(Which file? Broken how? The agent will search, guess a diagnosis, and "fix" whatever it
finds first — possibly rewriting working code, possibly patching the symptom.)

Informed:

```
"Login fails for emails with a + in them. The validation is in auth/validators.py
(validate_email); there's a failing case you can reproduce with
`pytest tests/test_auth.py -k plus_sign`. Fix validate_email so that test passes,
don't change its signature or touch anything outside auth/, and add one more test
for emails with dots in the local part. Done = full pytest run green."
```

Every sentence does a job: reproduction, location, constraint, scope fence, acceptance
criterion. Note the asymmetry with ordinary chat: a chat answer that's 80% right saves
you time; an agent that's 80% right has *written* the 20% wrong into your files. The
informed prompt shrinks that 20%, and the verify loop catches what's left. And prompts
are cheap — if the diff comes back wrong, don't negotiate line by line: revert, improve
the prompt with what you learned, run it again.

## When NOT to Delegate

**You can't verify what you don't minimally understand** — and unverifiable delegation
isn't delegation, it's gambling with your codebase. Don't hand an agent work when you
couldn't explain a correct solution's diff (learn the minimum first — that's this whole
repo's reason to exist); when the change is security- or data-destructive (auth,
payments, migrations, anything with `rm`) and a plausible-but-wrong version would be
catastrophic; or when the real problem is that *you* don't yet know what you want — an
agent will confidently build your confusion. Use it as a chat partner to reach clarity,
*then* delegate the implementation.

## Spot the Confabulation

An agent reports on a failing test it was asked to fix:

```
Fixed! The test expected parse_date("2024-02-30") to raise ValueError, but the
function actually returns None for invalid dates, so I updated the test to assert
that the result is None. All 214 tests now pass.
```

<details><summary>What's wrong?</summary>

The agent made the *test* agree with the *bug*. February 30th is not a date; the test
encoded the intended behaviour (reject invalid dates loudly), and the function is what's
broken — returning `None` silently turns bad input into a downstream mystery. The agent
optimised for its finish line ("all tests pass") instead of yours (correct code), which
is exactly why the verify loop reads the diff instead of the report: green tests prove
nothing if the tests themselves were edited. The right fix was in `parse_date`, or at
minimum a question back to you about which behaviour is intended.

</details>

## Where to Practice

- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — a free, open-source
  terminal agent with a generous no-cost tier; a real agent loop (read files, run
  commands, edit) to practice the commit → prompt → diff → test cycle on.
- **GitHub Copilot's free tier in VS Code** — agent-style edits inside the editor from
  `TAMYMN-VSCode.md`, no payment details needed.
- Whatever agent you use, practice on a **fresh clone of your own project** — real
  enough to matter, committed so nothing can be lost. Prompt, `git diff`, verify, revert,
  re-prompt: the loop is the skill.

## Quick Reference

| Rule | Why |
|---|---|
| Agent = LLM + tools in a loop | it really reads, runs, and edits — actions, not advice |
| Commit before every session | the whole session becomes one revertible diff (`TAMYMN-Git.md`) |
| Name files, constraints, acceptance criteria | the agent acts on what it can see — context is everything |
| Define done as a command | "pytest green" beats "make it work" |
| `git diff` every change | the report is a claim; the diff is the fact |
| Run the tests yourself | "all tests pass" must be *your* observation (`TAMYMN-Testing.md`) |
| Never merge what you can't explain | unverified code is your name on someone else's guess |
| Watch for edited tests | green is worthless if the finish line moved |
| Keep an `AGENTS.md` / `CLAUDE.md` | standing instructions beat repeated prompts |
| Bad diff? Revert and re-prompt | prompts are cheaper than line-by-line negotiation |
| Don't delegate what you can't verify | learn the minimum first — that's this repo |

That covers the absolute minimum! You can now direct an agent precisely, box its work
inside one revertible commit, and verify the result like a reviewer rather than a
spectator — and every other TAMYMN doc makes that verification sharper.
