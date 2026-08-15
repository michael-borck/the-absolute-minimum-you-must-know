# TAMYMN Authoring Guide

Every TAMYMN document is a promise: *read this one page and you know enough to work, to
direct an AI at the topic, and to catch it when it's wrong.* `TAMYMN-Linux.md` and
`TAMYMN-Git.md` are the exemplars — match their voice and density, not the length of
whatever you happen to produce.

## The bar

- **120–200 lines.** Long enough to explain *why*, short enough to read in ten minutes.
- **Opinionated and direct.** Second person. Say what to do and why it works. Never write
  "In this article we will..." — just start.
- **Every fact earns its place.** If knowing it doesn't change what the reader does or
  catches, cut it.
- **Explain the model, not just the commands.** The Linux doc doesn't list `cd`; it explains
  absolute vs relative paths and *then* the commands are obvious. Find the two or three
  mental models that make the topic click.
- **Name the stumbles.** Each doc should defuse the classic beginner traps ("trapped in
  vim?", "why `./script.sh`?"). These are the highest-value lines in the doc.

## Required sections, in order

1. **Title**: `# <Topic>: The Absolute Minimum You Must Know`
2. **Intro** (2–4 lines): the promise — "effective use rests on about N ideas, all on this
   page."
3. **The topic itself**, in sections you choose. Models first, mechanics second.
4. **`## Directing the Machine`** — the AI-era section. Show one *vague* prompt and one
   *informed* prompt for a realistic task in this topic, and explain why the informed one
   works: it names the concepts from this page. One short paragraph of principle, two
   fenced examples.
5. **`## Spot the Confabulation`** — one plausible-but-wrong AI-style answer (code or
   explanation) in a fenced block. Ask the reader what's wrong with it. Put the answer in a
   `<details><summary>What's wrong?</summary>...</details>` block. The error must be the
   kind an LLM actually makes: plausible, confident, subtly broken — not a typo.
6. **`## Where to Practice`** — one or two *specific* free practice grounds, with a sentence
   on why each is good. Prefer things that still exist and don't need signup.
7. **`## Quick Reference`** — a table compressing the whole page.
8. **Closing line**: "That covers the absolute minimum! ..." — one sentence on what the
   reader can now do, and that everything else is discoverable from here.

## Jargon and the Glossary

Use each domain's real terminology — the words are part of the minimum. Don't define
basic terms inline (that's what `GLOSSARY.md` is for); instead, link the **first
occurrence** of a glossary term in your doc to its anchor, e.g.
`[staging area](GLOSSARY.md#staging-area)`. Link only in prose (never inside code
blocks or the Quick Reference table), and don't link terms your own doc teaches — your
doc is the better definition. If a term you lean on is missing from the glossary, add
it there.

## Code examples

- **Python examples are doctests and they must pass.** Write them as interpreter
  transcripts (`>>>` with expected output). `scripts/test_docs.py` executes every
  `python` fenced block in every doc; CI fails if any example is wrong. Blocks without
  `>>>` (e.g. a class definition used by later examples) are exec'd into the same
  per-file namespace, in document order, so later doctests can use them.
- **Deterministic and self-contained.** No network (web-scraping docs parse a literal HTML
  string), no wall-clock, no `input()`, no `plt.show()` (assert on figure properties
  instead), files via `tempfile` or `io.StringIO`, databases via `sqlite3 ':memory:'`.
- Shell/Git/config examples are plain fenced blocks with `#` comments per line, like the
  Linux doc.
- Allowed third-party imports: `pandas`, `matplotlib`, `bs4` — nothing else.

## Tone calibration, by example

Bad (the old stub style):
> Commit staged changes with a message: `git commit -m "..."`

Good (the exemplar style):
> A commit is a snapshot of *staged* changes only — `git add` is you composing the
> snapshot, `git commit` is the shutter. That's why a file you edited but didn't `add`
> isn't in the commit you just made.
