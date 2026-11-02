> This content is from *TAMYMN-Matplotlib.md*, part of *The Absolute Minimum You Must Know*.

# Matplotlib: The Absolute Minimum You Must Know

Matplotlib's gallery is enormous, but every plot you'll ever make rests on one mental
model — the Figure and the Axes — and one idiom for using it. Learn that and the tutorials,
the gallery, and the AI-generated snippets all snap into focus.

## The Mental Model: Figure and Axes

A **Figure** is the whole canvas — the page you'll save or display. An **Axes** is one
plot living on that canvas: an x-axis, a y-axis, and the data drawn between them (one
Figure can hold several Axes, side by side). The one true idiom asks for both, then does
everything through the Axes object:

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

## Other Charts, Same Idiom

Every chart type is just a different verb on the same `ax`: `ax.bar(labels, heights)` for
comparisons, `ax.hist(values)` for distributions, `ax.scatter(x, y)` for relationships,
`ax.plot(x, y)` for trends. Choosing among them is a thinking skill, not a matplotlib
skill — that's `TAMYMN-Visualisation.md`.

Several plots on one canvas is where the explicit-handles idiom pays off:

## Saving (and the `plt.show()` Question)

Save from the *figure* — it's the canvas, after all:

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

Informed:

## Spot the Confabulation

An AI assistant explains how to display a plot and also keep a copy:

What's wrong?

The order. In a script, `plt.show()` hands the figure to the window, and closing that
window destroys it — afterwards the "current figure" is a brand-new empty one, so
`plt.savefig` writes a **blank white PNG**. No exception is raised, which is why this bug
ships. Save first, then show — or better, hold explicit handles (`fig, ax =
plt.subplots()`) and call `fig.savefig(...)`, which works regardless of what the global
"current figure" happens to be.

## Where to Practice

- **The Matplotlib gallery** — every
  thumbnail links to complete runnable source. The practice loop: pick a chart, run its
  code, then convert it to the `fig, ax` idiom and swap in your own data. No signup.
- **The Python Graph Gallery** — hundreds of
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
