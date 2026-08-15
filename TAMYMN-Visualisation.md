# Data Visualisation: The Absolute Minimum You Must Know

A chart is not decoration — it's an argument, and it can lie as fluently as a sentence
can. Effective visualisation rests on two skills, both on this page: matching the chart
to the question, and refusing the standard ways charts mislead. (For the mechanics of
drawing, see `TAMYMN-Matplotlib.md`; this page is about *what* to draw.)

## Start With the Question, Not the Data

Every chart answers exactly one of four questions. Name your question first and the chart
type falls out — this table is nine-tenths of visualisation:

| Your question | The answer is a... | matplotlib verb |
|---|---|---|
| **Comparison** — which is bigger? | bar chart | `ax.bar` |
| **Distribution** — how are values spread? | histogram | `ax.hist` |
| **Relationship** — do these move together? | scatter plot | `ax.scatter` |
| **Trend** — how does it change over time? | line chart | `ax.plot` |

If you can't say which question you're asking, no chart type will save you — and if you
ask an AI for "a visualisation" without naming the question, it can't know either.

## Why Pie Charts Mislead

A pie chart encodes values as angles and wedge areas — and human eyes are *bad* at
comparing angles. Is the 23% slice bigger than the 26% one? You genuinely cannot tell;
turn the same numbers into bars and the answer is instant, because bars encode value as
**length**, which eyes compare superbly. A pie is defensible only for "one obvious slice
versus the rest of the whole" — beyond two or three wedges, or for any comparison that
matters, use a bar chart. (A pie of values that don't even sum to a meaningful whole —
say, average temperatures by city — is not a chart, it's an accident.)

## Label Your Axes — With Units

An unlabelled axis makes the chart unfalsifiable: "sales" of *what*, in *which units*,
over *what period*? The non-negotiable minimum is an x-label, a y-label **with units**,
and a title — and the strongest titles state the takeaway ("Rent rose 12% in 2025"), not
the topic ("Rent data"). In matplotlib that's three `set_*` calls, and because Axes are
objects you can verify them in tests:

```python
>>> import matplotlib.pyplot as plt
>>> fig, ax = plt.subplots()
>>> _ = ax.bar(['Perth', 'Sydney'], [402, 415])
>>> _ = ax.set_ylabel('Median weekly rent (AUD)')
>>> _ = ax.set_title('Sydney rents edge out Perth')
>>> ax.get_ylabel()
'Median weekly rent (AUD)'
>>> float(ax.get_ylim()[0])     # bars start from zero — an honest comparison
0.0
>>> plt.close(fig)
```

## The Lie Factor: Truncated Axes

Edward Tufte's **lie factor** is the size of the effect *shown* divided by the size of
the effect *in the data*; an honest chart scores about 1. The classic inflator is the
**truncated axis**: rechart Perth (402) vs Sydney (415) with the y-axis starting at 400
and Sydney's bar towers at four times Perth's height — a visual 300% shouting about a
real 3%. The rules that keep you honest:

- **Bar charts start at zero, always.** A bar's length *is* its value; cutting the axis
  cuts the truth. (Matplotlib does the right thing by default, as the doctest above
  shows — truncation requires a deliberate `ax.set_ylim(400, ...)`.)
- **Line charts may zoom** — a trend lives in the slope, not the bar length — but say so
  visibly when the baseline isn't zero.
- Read others' charts with the same eye: axis starts, doubled y-axes, and 3-D
  perspective are where the lies live.

## Directing the Machine

An AI will happily generate *a* chart for any data you paste; only a prompt that names
the question type, the encoding, and the honesty rules gets you the *right* chart. You
are the one who knows what question the audience is asking.

Vague:

```
"visualise this sales data"
```

Informed:

```
"This is a trend question: monthly revenue over 24 months. Line chart (not bars),
x label 'Month', y label 'Revenue (AUD, thousands)', title stating the takeaway.
The y-axis needn't start at zero, but annotate the baseline if it doesn't.
Use the fig, ax = plt.subplots() idiom from TAMYMN-Matplotlib.md."
```

## Spot the Confabulation

An AI assistant polishes a chart comparing two branches' quarterly sales (Branch A:
$1.02M, Branch B: $1.07M):

```
ax.bar(['Branch A', 'Branch B'], [1.02, 1.07])
ax.set_ylim(1.00, 1.08)   # zoom in so the difference is easier to see —
                          # without this the bars look almost identical
```

<details><summary>What's wrong?</summary>

"The bars look almost identical" is the *truth* — the branches differ by about 5%, and an
honest bar chart is supposed to look that way. Truncating the axis to `(1.00, 1.08)`
makes B's bar roughly three times A's height: a lie factor near 70. The comment even
confesses the motive. If the 5% gap genuinely matters, keep the zero baseline and
annotate the bars with their values, or plot the *difference* explicitly — don't redraw
the ruler until the answer looks impressive.

</details>

## Where to Practice

- **[From Data to Viz](https://www.data-to-viz.com)** — a decision tree that walks from
  "what kind of data do I have?" to a recommended chart, with the classic caveats
  (including the pie-chart problem) explained on the way. Free, no signup.
- **[WTF Visualizations](https://viz.wtf)** — a stream of real published charts that
  mislead. Practise naming *why* each one fails; it trains the same eye you'll use on
  your own drafts.

## Quick Reference

| Rule | In short |
|---|---|
| Name the question first | comparison / distribution / relationship / trend |
| Comparison → `ax.bar` | lengths, from zero |
| Distribution → `ax.hist` | shape, spread, outliers |
| Relationship → `ax.scatter` | one point per observation |
| Trend → `ax.plot` | slope carries the message |
| Pie charts | angles are unreadable — use bars beyond 2–3 wedges |
| Labels | x, y **with units**, takeaway title — or it's a rumour |
| Lie factor ≈ 1 | shown effect ÷ real effect; keep it honest |
| Bars start at zero | truncated bar axes manufacture drama |
| Zoomed line charts | allowed, but flag the non-zero baseline |

That covers the absolute minimum! You can now pick the chart that answers the question,
label it so it can be checked, and spot a lying axis at twenty paces — the drawing
mechanics are all in `TAMYMN-Matplotlib.md`.
