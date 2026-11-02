> This content is from *TAMYMN-Doctest.md*, part of *The Absolute Minimum You Must Know*.

# Doctest: The Absolute Minimum You Must Know

A doctest is an example that is also a test: you paste an interpreter session into a
docstring, and Python re-runs it to check the outputs still hold. The whole tool is one
idea and three rules of transcript-writing — all on this page.

## The Idea: Examples That Cannot Rot

Documentation lies. Not on the day it's written — later, when the code changes and the
examples don't. Doctest kills that failure mode: because the example *is* a test, an
example that stops being true becomes a build failure instead of a trap for the next
reader. That's the honest-documentation guarantee, and no comment or README paragraph can
offer it.

A doctest lives in a docstring and looks exactly like the interactive interpreter:

Lines starting `>>>` are statements to run (`...` continues a multi-line one); the lines
below each are the expected output, matched **exactly** — same text, same spacing.

## Writing a Transcript

The reliable way to write one is not to write it at all: run the code in a real
interpreter and paste the session. Everything doctest-shaped in this page is live, so the
rules below demonstrate themselves. First the function:

**Rule 1 — expressions are compared against their `repr`.** That's why strings show their
quotes, and why `print` output doesn't:

Mixing these up is *the* classic doctest stumble — expecting `Ada` from a bare expression
fails on the missing quotes.

**Rule 2 — exceptions get a stub traceback.** Write the header line, a literal `...` for
the messy middle, then the final error line:

**Rule 3 — a blank output line must be spelled ``**, because a real blank line
means "the expected output ends here":

Keep transcripts deterministic: no `random`, no clock, no dict-of-object reprs like
`` — if the output can vary, doctest is the wrong tool for that line.

## Running Doctests

Silence-on-success surprises people: no news is a pass. Add `-v` when you want proof.

## When Doctest Beats pytest — and When It Doesn't

Doctest wins wherever a human will read the example anyway: docstrings of pure functions,
tutorials, READMEs. One artefact serves as spec, documentation, and test, and it can't
drift. It loses everywhere else: no fixtures or parametrisation, clumsy with setup and
side effects, brittle with floats and volatile reprs, and its failure output is thin. The
working split: **doctest for the contract you show humans, pytest for the deep coverage**
— a couple of honest examples per function, and the exhaustive edge-case grid in
`test_*.py`.

## The Meta-Point: This Page Is Testing Itself

This very repository eats its own cooking: `scripts/test_docs.py` executes **every**
`python` block in these documents — blocks containing `>>>` run as doctests, the rest are
exec'd into the same per-file namespace — and CI fails if any example is wrong. The
`fahrenheit` transcripts above didn't just look right, they *ran*. That's the doctest idea
scaled up to a whole book: it cannot lie about its own examples.

## Directing the Machine

An AI writes docstring examples from the code's apparent intent, not from running it — so
the expected outputs are guesses, and a wrong guess becomes confident false documentation.
The informed prompt names the transcript rules and demands the proof.

Vague:

Informed:

```
"Add docstring examples to slugify covering a title with punctuation, internal
whitespace collapsing, and the empty string. Outputs must be exact reprs — quotes
included. Then run `python -m doctest slugify.py -v` and paste the run: every
example must pass, and I want to see the PASS lines, not a claim."

def average(nums):
    """Mean of a list of numbers.

    >>> average([1, 2, 3])
    2.0
    >>> average([])
    0
    """
    return sum(nums) / len(nums)
```

What's wrong?

The second example documents behaviour the code doesn't have: `average([])` divides by
`len([])` and raises `ZeroDivisionError` — it does not return `0`. The AI wrote the
example it *wished* were true (graceful empty-list handling is what a helper "should" do),
which is exactly the confabulation pattern: plausible, confident, unexecuted. And this is
doctest's whole value — `python -m doctest` fails immediately on that docstring, turning a
lie in the documentation into a red build. Run the examples; never trust a transcript
nobody executed.

## Where to Practice

- **This repository** — clone it, change one expected output in any doc, run
  `python3 scripts/test_docs.py`, and watch the book catch its own lie; then write a new
  passing block. No signup, and the feedback loop is seconds.
- **Your own codebase** — pick one pure utility function, paste a real interpreter session
  into its docstring, and wire `python -m doctest` (or `pytest --doctest-modules`) into
  CI. One function is enough to make the habit stick.

## Quick Reference

| Thing | The minimum |
|---|---|
| `>>>` line | a statement to run; `...` continues it |
| Line(s) below | expected output, matched exactly |
| Expression result | compared against its `repr` — strings keep their quotes |
| `print(...)` | compared against the printed text — no quotes |
| No output expected | assignments, imports, `None` |
| Exception | `Traceback (most recent call last):` + `  ...` + final error line |
| `` | stands for an empty line in expected output |
| `python -m doctest f.py` | run a file's examples; silence = pass |
| `python -m doctest -v f.py` | narrate every example |
| `pytest --doctest-modules` | collect doctests alongside pytest tests |
| Use doctest for | the honest examples humans read |
| Use pytest for | setup, side effects, exhaustive edge cases |

That covers the absolute minimum! You can now write documentation that proves itself on
every run — and the moment an example outgrows a transcript, you know it belongs in
pytest instead.
