# Jupyter Notebooks: The Absolute Minimum You Must Know

A notebook mixes runnable code, its output, and prose in one document — the standard
workbench for data exploration. Effective use rests on one uncomfortable mental model and
a handful of keystrokes, all on this page. Miss the model and notebooks will lie to you;
learn it and they're the best exploration tool there is.

## The Mental Model: Hidden State

A notebook *looks* like a document that reads top to bottom. It isn't. It's a chat
session with a running Python [process](GLOSSARY.md#process) — the **kernel** — and the kernel remembers every
cell you've *ever run this session*, in the order you ran them, no matter where those
cells sit on the page. **Execution order is not reading order.**

```
In [1]: x = 10          # you run this...
In [3]: x = x * 2       # ...then this...
In [2]: print(x)        # ...then scroll UP and run this: prints 20
```

The bracket numbers (`In [3]`) are the true story: they record the order cells actually
ran. Run cells out of order, delete a cell after running it, or re-run one halfway up the
page, and the kernel's memory no longer matches the document you're reading. This
**hidden state** is the cause of the two classic notebook mysteries: "it works for me
but errors for everyone else" and "it worked yesterday but the same notebook fails
today". A deleted cell's [variables](GLOSSARY.md#variable) live on in the kernel; a stale value hides behind a
freshly edited line.

**The honesty check: `Kernel > Restart & Run All`.** It throws away all kernel memory and
runs every cell top to bottom — the way your reader (or future you) will experience the
notebook. If that fails, your notebook was working by accident. Run it before you share,
commit, or believe a result.

## Two Kinds of Cell

**Code cells** hold Python; running one sends it to the kernel and pins the result
beneath. A cell's *last [expression](GLOSSARY.md#expression)* is displayed automatically — no `print()` needed —
which is why a cell ending in just `df` shows the DataFrame.

**Markdown cells** hold prose in [Markdown](GLOSSARY.md#markdown) (see `TAMYMN-Markdown.md`): headings,
explanations, conclusions. A notebook with no Markdown cells is just a [script](GLOSSARY.md#script) in
expensive packaging — the interleaved narrative is the point.

One subtlety: the pretty output saved in the `.ipynb` file is a *transcript*, not state.
Reopening a notebook shows yesterday's outputs, but the kernel is brand new and empty —
nothing is defined until you run cells again.

## Keyboard Basics: Two Modes

Jupyter has two modes, and knowing which you're in explains most "why did that keystroke
do something weird?" moments:

- **Edit mode** (press **Enter** on a cell, cursor visible): you're typing *inside* the
  cell — keys insert text.
- **Command mode** (press **Esc**, no cursor): keys are commands *about* cells:

```
Shift-Enter   # run the cell, move to the next — the keystroke you'll use most
a / b         # insert a new cell Above / Below
m / y         # turn the cell into Markdown / back to code
dd            # delete the cell (press d twice)
z             # undo cell deletion
```

If typing suddenly deletes cells or spawns new ones, you're in command mode — press
Enter to get back inside the cell.

## When Notebooks Are Right — and Wrong

**Right:** exploration. Poke at a dataset, try a transformation, see the plot, keep the
prose and the evidence together. The tight run-look-tweak loop is unbeatable for
analysis, teaching, and reports (see `TAMYMN-Pandas.md`, `TAMYMN-Matplotlib.md`).

**Wrong:** anything meant to be *depended on*. [Libraries](GLOSSARY.md#library), shared utilities, production
jobs. Notebooks resist code review (`.ipynb` is [JSON](GLOSSARY.md#json) — [diffs](GLOSSARY.md#diff) are noise), resist testing,
and hide state. The graduation move: when a [function](GLOSSARY.md#function) stops changing, cut it out of the
notebook into a plain `.py` [module](GLOSSARY.md#module), test it (`TAMYMN-Testing.md`), and `import` it back.
Explore in the notebook; *keep* code in modules.

## Directing the Machine

When you ask an AI about a broken notebook, the vital context is exactly what hidden
state hides: what `Restart & Run All` does, and which cell fails with what error. An AI
can't see your kernel's memory — tell it the reproducible story, not the accidental one.

Vague:

```
"my notebook says NameError: name 'df' is not defined but df definitely exists"
```

Informed:

```
"After Kernel > Restart & Run All, cell 4 raises NameError for df. Cell 4 uses df but
I see the cell that created df was one I deleted last week — the old kernel still had
it. Rewrite cell 4's context so the notebook defines df from data.csv before use, and
tell me how to confirm the whole notebook now runs clean top to bottom."
```

## Spot the Confabulation

An AI assistant explains why a shared notebook fails for a colleague:

```
Your notebook works for you because Jupyter saves your variable values into the
.ipynb file along with the outputs. Your colleague's copy failed because the file got
corrupted in transfer — re-download it, and the variables will load back into memory
when the notebook opens.
```

<details><summary>What's wrong?</summary>

The `.ipynb` file stores code, prose, and *display outputs* — never variables. Kernel
state lives only in the running process and dies with it; every fresh open starts an
empty kernel. The notebook "works for you" because your long-running kernel still
remembers cells you've since edited, deleted, or ran out of order — hidden state. The
real fix is to run `Restart & Run All` yourself, repair whatever breaks, and *then*
share.

</details>

## Where to Practice

- **[jupyter.org/try](https://jupyter.org/try)** — the official "Try Jupyter" pages run
  JupyterLab entirely in your browser (via JupyterLite): no install, no signup. Open a
  notebook and deliberately run cells out of order until you can predict the hidden
  state, then watch `Restart & Run All` expose it.
- **Google Colab** (`TAMYMN-Colab.md`) — the same notebook model hosted for free, when
  you want a real kernel with more muscle.

## Quick Reference

| Action / concept | Meaning |
|---|---|
| kernel | the running Python process holding ALL state |
| `In [n]` numbers | true execution order — not page order |
| **Restart & Run All** | the honesty check: does it run clean top to bottom? |
| saved outputs | a transcript in the file — not saved variables |
| **Shift-Enter** | run cell, advance |
| **Enter** / **Esc** | edit mode (type in cell) / command mode (act on cells) |
| `a` / `b` (command mode) | new cell above / below |
| `m` / `y` (command mode) | Markdown cell / code cell |
| `dd` / `z` (command mode) | delete cell / undo delete |
| last expression in a cell | auto-displayed, no `print()` needed |
| right for | exploration, analysis, teaching, reports |
| wrong for | libraries, production — extract stable code to `.py` modules |

That covers the absolute minimum! You can now explore honestly — run, verify with
Restart & Run All, and know when to graduate code out of the notebook; everything else
is a `h` (the command-mode help key) away.
