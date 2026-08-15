# Matplotlib: The Absolute Minimum You Must Know

Matplotlib's gallery is enormous, but every plot you'll ever make rests on one mental
model — the Figure and the Axes — and one idiom for using it. Learn that and the tutorials,
the gallery, and the AI-generated snippets all snap into focus.

## The Mental Model: Figure and Axes

A **Figure** is the whole canvas — the page you'll save or display. An **Axes** is one
plot living on that canvas: an x-axis, a y-axis, and the data drawn between them (one
Figure can hold several Axes, side by side). The one true idiom asks for both, then does
everything through the Axes object:

```python
import matplotlib.pyplot as plt   # the universal abbreviation
```

```python
>>> fig, ax = plt.subplots()
>>> _ = ax.plot([2021, 2022, 2023, 2024], [10, 12, 9, 15])
```

Why not `plt.plot(...)`, like half the tutorials on the internet? Those `plt.*` calls are
a convenience layer that operates on the "current" figure — an invisible global. With one
plot it works; the moment you have two plots, a loop, or a function that draws charts,
"current" stops being what you think it is and titles land on the wrong plot. `fig, ax =
plt.subplots()` gives you explicit handles, so there's never a doubt about which plot
you're talking to.

(The `_ =` is a doc-transcript habit: plotting methods return the objects they create,
and we're ignoring them. In a script you just call `ax.plot(...)` bare.)

## Labels, Title, Legend

An unlabelled plot is a rumour, not evidence (`TAMYMN-Visualisation.md` is the doc on
*what* to plot and how charts mislead). Every Axes gets three lines minimum:

And because the Axes is a real object, you can *ask it questions* afterwards — which is
also how you test plotting code without ever looking at a screen:

```python
>>> fig, ax = plt.subplots()
>>> _ = ax.plot([2021, 2022, 2023, 2024], [10, 12, 9, 15], label='Widgets')
>>> _ = ax.plot([2021, 2022, 2023, 2024], [8, 11, 13, 14], label='Gadgets')
>>> _ = ax.set_title('Sales by year')
>>> _ = ax.set_xlabel('Year')
>>> _ = ax.set_ylabel('Units sold (thousands)')
>>> legend = ax.legend()          # built from the label= of each plotted line
>>> ax.get_title()
'Sales by year'
>>> [t.get_text() for t in legend.get_texts()]
['Widgets', 'Gadgets']
```

## Other Charts, Same Idiom

Every chart type is just a different verb on the same `ax`: `ax.bar(labels, heights)` for
comparisons, `ax.hist(values)` for distributions, `ax.scatter(x, y)` for relationships,
`ax.plot(x, y)` for trends. Choosing among them is a thinking skill, not a matplotlib
skill — that's `TAMYMN-Visualisation.md`.

Several plots on one canvas is where the explicit-handles idiom pays off:

```python
>>> fig, (left, right) = plt.subplots(1, 2)   # one figure, two axes
>>> _ = left.bar(['A', 'B'], [3, 5])
>>> _ = right.scatter([1, 2, 3], [2, 4, 6])
>>> len(fig.axes)
2
```

## Saving (and the `plt.show()` Question)

Save from the *figure* — it's the canvas, after all:

```python
>>> fig, ax = plt.subplots()
>>> _ = ax.plot([2021, 2022, 2023, 2024], [10, 12, 9, 15])
>>> import io
>>> buf = io.BytesIO()                       # in a script: fig.savefig('sales.png', dpi=150)
>>> fig.savefig(buf, format='png')
>>> buf.getvalue()[:8] == b'\x89PNG\r\n\x1a\n'   # a real PNG came out
True
>>> plt.close('all')                         # done with these figures; free them
```

`plt.show()` opens an interactive window and **blocks until you close it** — it belongs
only at the very end of a desktop script, if anywhere. In Jupyter (`TAMYMN-Jupyter.md`)
figures render automatically without it, and on a server there is no screen at all. If
your goal is a file, `fig.savefig(...)` alone is the whole job — and it must come
*before* any `show()`, because closing the window discards the figure.

## Directing the Machine

AI assistants were trained on two decades of `plt.*` tutorials, so a vague prompt gets
you the global-state style and a `plt.show()` you didn't want. An informed prompt names
the model on this page — Figure, Axes, the subplots idiom — and states the output.

Vague:

```
"make a chart of my sales data in python"
```

Informed:

```
"Using fig, ax = plt.subplots(), draw revenue vs month as a line on ax. X label
'Month', y label 'Revenue (AUD)', title stating the takeaway, legend from label=.
Finish with fig.savefig('revenue.png', dpi=150) — no plt.show(), this runs
headless in CI."
```

## Spot the Confabulation

An AI assistant explains how to display a plot and also keep a copy:

```
plt.plot(months, revenue)
plt.title('Monthly revenue')
plt.show()                     # inspect it on screen first
plt.savefig('revenue.png')     # then save the same figure for the report
```

<details><summary>What's wrong?</summary>

The order. In a script, `plt.show()` hands the figure to the window, and closing that
window destroys it — afterwards the "current figure" is a brand-new empty one, so
`plt.savefig` writes a **blank white PNG**. No exception is raised, which is why this bug
ships. Save first, then show — or better, hold explicit handles (`fig, ax =
plt.subplots()`) and call `fig.savefig(...)`, which works regardless of what the global
"current figure" happens to be.

</details>

## Where to Practice

- **[The Matplotlib gallery](https://matplotlib.org/stable/gallery/index.html)** — every
  thumbnail links to complete runnable source. The practice loop: pick a chart, run its
  code, then convert it to the `fig, ax` idiom and swap in your own data. No signup.
- **[The Python Graph Gallery](https://python-graph-gallery.com)** — hundreds of
  copy-paste matplotlib examples organised by chart type, free and signup-less.

## Quick Reference

| Idiom | What it does |
|---|---|
| `fig, ax = plt.subplots()` | the one true starting line: canvas + one plot |
| `fig, (a, b) = plt.subplots(1, 2)` | one canvas, two plots side by side |
| `ax.plot(x, y, label='...')` | line (trend) |
| `ax.bar(labels, heights)` | bars (comparison) |
| `ax.hist(values)` | histogram (distribution) |
| `ax.scatter(x, y)` | points (relationship) |
| `ax.set_title/set_xlabel/set_ylabel` | the three lines every plot gets |
| `ax.legend()` | legend built from each line's `label=` |
| `ax.get_title()`, `fig.axes` | ask the objects — how you test plots |
| `fig.savefig('out.png', dpi=150)` | write the file — *before* any `show()` |
| `plt.show()` | interactive window; end-of-script only, never headless |
| `plt.close('all')` | discard figures you're done with |

That covers the absolute minimum! You can now build, label, combine, save, and *test* any
plot through its Figure and Axes handles — every fancier chart in the gallery is the same
idiom with a different verb on `ax`.
