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

```python
def discounted(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)
```

```python
>>> discounted(200, 10)            # Arrange: the arguments. Act: the call.
180.0
>>> discounted(200, 10) == 180.0   # Assert: does the result match the claim?
True
```

The whole assertion language you need is Python's `assert`: silent when the condition is
true, `AssertionError` (with your message) when it's false.

```python
>>> assert discounted(100, 25) == 75.0                       # true: silence
>>> assert discounted(100, 50) == 49.0, "half of 100 is 50"  # false: it objects
Traceback (most recent call last):
  ...
AssertionError: half of 100 is 50
```

A test is just a function named `test_*` that makes assertions. If it returns without
raising, it passed:

```python
def test_boundaries():
    assert discounted(80, 0) == 80.0     # 0% is a legitimate discount
    assert discounted(80, 100) == 0.0    # so is 100%
```

```python
>>> test_boundaries()   # no output means it passed — pytest automates exactly this
```

## pytest: The Default Runner

`unittest` ships with Python, but the community default is **pytest**: plain functions,
plain `assert`, and when an assertion fails it shows the values on both sides.

```
pip install pytest
pytest              # run every test_* function in every test_*.py file
pytest -x           # stop at the first failure
pytest -k boundary  # run only tests whose names match
pytest --lf         # re-run only what failed last time
```

Names are how pytest *finds* tests — a function called `check_boundaries` in `mytests.py`
is silently ignored, the classic "0 tests collected" stumble. And one idiom you'll need on
day one — asserting that code raises:

```
import pytest

def test_rejects_silly_percent():
    with pytest.raises(ValueError):
        discounted(100, 150)
```

## What to Test: Behaviour, Not Implementation

Test the contract — inputs in, outputs out — never the internal steps. A test that checks
"the function calls `round()`" breaks the moment the implementation changes even when the
behaviour is still correct; a test that checks the observable promise survives any
rewrite that keeps it:

```python
>>> discounted(19.99, 10)   # the promise: money comes back to 2 decimal places
17.99
```

This is what makes a behavioural suite AI-proof: an assistant can replace the entire
function body, and your tests still judge the result fairly. If a test would fail after a
correct refactor, it's testing the *how*, not the *what* — rewrite it.

## Edge Cases: Where the Bugs Live

Happy paths almost always work; bugs cluster at the edges. For any function, ask: zero,
empty, exactly on the boundary, just past the boundary, wrong type, absurdly large. This
matters double for generated code, which notoriously nails the happy path and confabulates
the edges — edge-case tests are where your review effort pays off most.

```python
>>> discounted(0, 50)        # zero price
0.0
>>> discounted(100, 150)     # just past the boundary must fail loudly
Traceback (most recent call last):
  ...
ValueError: percent must be between 0 and 100
```

A workable ratio: one happy-path test, one test per boundary, one per way it can fail.

## Directing the Machine

Ask an AI to "write tests" for existing code and it will happily generate tests that
mirror whatever the code currently does — bugs included. Tests derived from the
implementation can never catch the implementation being wrong. The informed prompt states
the contract and the edges, so the tests come from the *spec*, not the code.

Vague:

```
"write some tests for this function"
```

Informed:

```
"Contract for discounted(price, percent): percent outside 0–100 raises ValueError;
results are rounded to 2 decimal places; discounted(x, 0) == x and
discounted(x, 100) == 0.0. Write pytest tests from this contract only — don't read
the implementation — covering the happy path, both boundaries, one value past each
boundary, and the rounding promise."
```

## Spot the Confabulation

An AI assistant is asked to test `converter.convert(amount, currency)`, which calls a live
exchange-rate API, and proudly reports "test added, passing":

```
def test_convert(monkeypatch):
    monkeypatch.setattr(converter, "convert", lambda amount, currency: 90.0)
    assert converter.convert(100, "EUR") == 90.0
```

<details><summary>What's wrong?</summary>

It mocked away the thing under test. The `monkeypatch` line replaces `convert` itself with
a lambda that returns `90.0`, and the assertion then checks that the lambda returns `90.0`
— a tautology that passes even if the real `convert` is deleted. Mocking is for the
*collaborator* you can't control (the API call that fetches the rate), so the code under
test still runs for real: patch `converter.get_rate` to return a fixed rate, then assert
on `convert`'s actual arithmetic. Any test that still passes with the real code removed is
testing nothing — and "all green" from an assistant deserves exactly this check.

</details>

## Where to Practice

- **[Exercism](https://exercism.org)** (free, open source) — the Python track hands you a
  test suite and an empty file; making tests green is the entire workflow, and reading its
  suites teaches you what good behavioural tests look like.
- **[Python Koans](https://github.com/gregmalcolm/python_koans)** — a runnable path of
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
