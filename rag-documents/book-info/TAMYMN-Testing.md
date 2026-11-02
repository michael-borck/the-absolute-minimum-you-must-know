> This content is from *TAMYMN-Testing.md*, part of *The Absolute Minimum You Must Know*.

# Testing: The Absolute Minimum You Must Know

In the AI era you write less of the code, but you still answer for all of it — and a test
is how you check work you didn't write. Effective testing rests on about five ideas: the
anatomy of a test, one runner, what to test, and where the bugs hide — all on this page.

## Why Testing Is Now THE Core Skill

The division of labour has shifted: an assistant generates code faster than you can read
it, and reading is a weak check anyway — plausible-looking code is exactly what an LLM is
optimised to produce. A test is a stronger check: an executable claim about behaviour that
the code either meets or doesn't, regardless of who wrote it or how confident they
sounded. When a machine writes the function, your test is the one part of the exchange you
*know* is true. So the scarce skill is no longer producing code; it's specifying and
verifying it — which is precisely what a test does.

Tests also make change safe. A suite that passes before and after an edit is what lets you
— or an agent — restructure code without fear, the same way a commit makes an AI session
revertible in Git.

## Anatomy of a Test: Arrange, Act, Assert

Every test in every framework has three beats: **arrange** the inputs, **act** by calling
the code, **assert** that the result matches the claim. Here's a function to test:

The whole assertion language you need is Python's `assert`: silent when the condition is
true, `AssertionError` (with your message) when it's false.

A test is just a function named `test_*` that makes assertions. If it returns without
raising, it passed:

## pytest: The Default Runner

`unittest` ships with Python, but the community default is **pytest**: plain functions,
plain `assert`, and when an assertion fails it shows the values on both sides.

Names are how pytest *finds* tests — a function called `check_boundaries` in `mytests.py`
is silently ignored, the classic "0 tests collected" stumble. And one idiom you'll need on
day one — asserting that code raises:

## What to Test: Behaviour, Not Implementation

Test the contract — inputs in, outputs out — never the internal steps. A test that checks
"the function calls `round()`" breaks the moment the implementation changes even when the
behaviour is still correct; a test that checks the observable promise survives any
rewrite that keeps it:

This is what makes a behavioural suite AI-proof: an assistant can replace the entire
function body, and your tests still judge the result fairly. If a test would fail after a
correct refactor, it's testing the *how*, not the *what* — rewrite it.

## Edge Cases: Where the Bugs Live

Happy paths almost always work; bugs cluster at the edges. For any function, ask: zero,
empty, exactly on the boundary, just past the boundary, wrong type, absurdly large. This
matters double for generated code, which notoriously nails the happy path and confabulates
the edges — edge-case tests are where your review effort pays off most.

A workable ratio: one happy-path test, one test per boundary, one per way it can fail.

## Directing the Machine

Ask an AI to "write tests" for existing code and it will happily generate tests that
mirror whatever the code currently does — bugs included. Tests derived from the
implementation can never catch the implementation being wrong. The informed prompt states
the contract and the edges, so the tests come from the *spec*, not the code.

Vague:

Informed:

## Spot the Confabulation

An AI assistant is asked to test `converter.convert(amount, currency)`, which calls a live
exchange-rate API, and proudly reports "test added, passing":

What's wrong?

It mocked away the thing under test. The `monkeypatch` line replaces `convert` itself with
a lambda that returns `90.0`, and the assertion then checks that the lambda returns `90.0`
— a tautology that passes even if the real `convert` is deleted. Mocking is for the
*collaborator* you can't control (the API call that fetches the rate), so the code under
test still runs for real: patch `converter.get_rate` to return a fixed rate, then assert
on `convert`'s actual arithmetic. Any test that still passes with the real code removed is
testing nothing — and "all green" from an assistant deserves exactly this check.

## Where to Practice

- **Exercism** (free, open source) — the Python track hands you a
  test suite and an empty file; making tests green is the entire workflow, and reading its
  suites teaches you what good behavioural tests look like.
- **Python Koans** — a runnable path of
  deliberately failing assertions you fix one by one; clone and run, no signup.

## Quick Reference

| Idea / command | The minimum |
|---|---|
| Arrange–Act–Assert | set up inputs, call the code, assert on the result |
| `assert expr, "msg"` | silent if true, `AssertionError` if false |
| `test_*` in `test_*.py` | the naming convention pytest uses to find tests |
| `pytest` | run everything; failures show both sides of the `==` |
| `pytest -x` / `-k name` / `--lf` | stop at first failure / filter by name / re-run failures |
| `with pytest.raises(ValueError):` | assert that code fails loudly |
| Behaviour, not implementation | test the contract; a correct refactor must stay green |
| Edge cases | zero, empty, on-boundary, past-boundary, wrong type |
| AI-era rule | never accept generated code without a test *you* understand |

That covers the absolute minimum! You can now write a test for any claim a human or a
machine makes about code — and everything else in testing is refinement of these five
ideas.
