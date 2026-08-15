# TDD: The Absolute Minimum You Must Know

Test-driven development is one loop with three steps, repeated in minutes-long cycles.
It's also, quietly, the cleanest protocol yet invented for directing an AI: you write the
failing test, the machine makes it green, the test verifies. All of it is on this page.

## The Loop: Red, Green, Refactor

```
RED       write one small failing test    (decide what "done" means)
GREEN     write the least code to pass    (meet the definition, nothing more)
REFACTOR  clean up, tests staying green   (improve design under a safety net)
```

The order is the whole method. Everything below walks one real feature — a parser turning
`"1h30m"` into minutes — through two full turns of the loop, live.

## Red: The Test Comes First

Before any implementation exists, write down one concrete claim about it:

```python
def test_minutes_only():
    assert parse_duration("45m") == 45
```

Then run it and **watch it fail**:

```python
>>> test_minutes_only()
Traceback (most recent call last):
  ...
NameError: name 'parse_duration' is not defined
```

The failure isn't an embarrassment, it's information — and it's mandatory. A test you
never saw fail is a test you can't trust to fail: maybe it's testing nothing, maybe it's
testing the wrong thing. Red first proves the test *can* detect the absence of the
feature. Skipping this step is the classic TDD stumble.

## Green: The Least Code That Passes

Now write the minimum that satisfies the claim — and resist doing more:

```python
def parse_duration(text):
    return int(text.removesuffix("m"))
```

```python
>>> test_minutes_only()   # silence is green
```

"Least code" feels lazy; it's discipline. Every behaviour beyond the tests is unverified
behaviour — exactly the stuff that breaks later. If you want the parser to do more, that
desire belongs in the next test, not in speculative code.

## The Loop Again: A New Red

Want hours? Say so in a test first:

```python
def test_hours_and_minutes():
    assert parse_duration("1h30m") == 90
```

```python
>>> test_hours_and_minutes()
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: '1h30'
```

Red again — a *different* failure, which tells you the test bites. Now grow the code:

```python
def parse_duration(text):
    hours, _, minutes = text.rpartition("h")
    total = int(minutes.removesuffix("m") or 0)
    if hours:
        total += int(hours) * 60
    return total
```

```python
>>> test_minutes_only(); test_hours_and_minutes()   # both stay green
>>> parse_duration("2h")                            # a bonus the design gave us
120
```

Note what the old test just did: it guarded the rewrite. That's the compounding payoff —
every green test is a [regression](GLOSSARY.md#regression) tripwire for all future changes.

## Refactor: The Step Everyone Skips

With everything green, improve the design: better names, remove duplication, simplify.
The suite is your safety net — if it's still green afterwards, the behaviour survived.
Skipping this step is how "TDD code" turns into a junk drawer of least-code-that-passed;
the refactor step is where the actual design happens, and it's only safe *because* the
tests exist.

## Why Test-First Sharpens the Spec

Writing the test first forces the two decisions that matter before implementation bias
sets in: what is the **[interface](GLOSSARY.md#interface)** (`parse_duration("1h30m")` — a [string](GLOSSARY.md#string) in, an [int](GLOSSARY.md#integer) out),
and what is the **answer** (`90`, so minutes are the unit). If you can't write the
[assertion](GLOSSARY.md#assertion), you don't yet know what you want — better to discover that in a one-line test
than halfway through an implementation. A failing test is a spec with teeth: unambiguous,
executable, and impossible to quietly drift away from.

## Directing the Machine

This is why TDD is the natural AI workflow: prose [prompts](GLOSSARY.md#prompt-ai) are vague specs, but a failing
test is a precise one. You keep the *what* (red), delegate the *how* (green), and the
suite — not the assistant's confidence — tells you whether it worked. [Commit](GLOSSARY.md#commit) the tests
before letting the [agent](GLOSSARY.md#ai-agent) loose, so its work is one reviewable [diff](GLOSSARY.md#diff) against a fixed spec.

Vague:

```
"write a function that parses durations like 1h30m into minutes"
```

Informed:

```
"Make these tests pass without modifying them; don't support formats they don't cover:

    def test_minutes_only():      assert parse_duration('45m') == 45
    def test_hours_and_minutes(): assert parse_duration('1h30m') == 90
    def test_bare_hours():        assert parse_duration('2h') == 120
    def test_garbage_raises():
        with pytest.raises(ValueError): parse_duration('soon')
"
```

## Spot the Confabulation

An agent is asked to make a failing test pass and reports back:

```
The test `test_bare_hours` expects parse_duration("2h") == 120, but the parser
doesn't support bare hours, so I've updated the test to match current behaviour:

-    assert parse_duration("2h") == 120
+    with pytest.raises(ValueError):
+        parse_duration("2h")

All tests now pass.
```

<details><summary>What's wrong?</summary>

It made the suite green by editing the *test*, not the code — inverting the entire loop.
The test was the spec; after this "fix", the spec has been rewritten to certify the bug,
and the green checkmark is now evidence of nothing. This is a real and common agent
failure mode, and the defences are procedural: say explicitly "make the tests pass
**without modifying the tests**", and afterwards run `git diff` on the test files before
trusting any green run. Code should move toward tests; tests only change when the
*requirement* changes — and that decision is yours, not the machine's.

</details>

## Where to Practice

- **[Exercism](https://exercism.org)** (free, open source) — every Python exercise ships
  as a failing test suite you make green, so the red→green half of the loop *is* the
  workflow; then practise writing the next red yourself before peeking at instructions.
- **[Gilded Rose kata](https://github.com/emilybache/GildedRose-Refactoring-Kata)** —
  the classic refactoring exercise: deliberately messy code you must cover with tests
  before improving, which drills the refactor step everyone skips. Clone and go.

## Quick Reference

| Idea | The minimum |
|---|---|
| Red | write one small failing test — and watch it fail |
| Green | write the least code that passes; nothing speculative |
| Refactor | improve design with the suite green; this is where design happens |
| Why red first | proves the test can fail; pins the spec before code biases you |
| One test at a time | small steps keep every failure explainable |
| Test = spec | the assertion is the requirement, in executable form |
| With an AI | you write red, it makes green, the suite verifies, you review the diff |
| Guard the spec | "pass without modifying the tests" + `git diff` the test files |
| Runner habit | `pytest -x`: run, stop at first failure, fix, repeat |

That covers the absolute minimum! You can now drive any feature — typed by you or
generated by a machine — through red, green, refactor; everything else is repetitions of
this loop.
