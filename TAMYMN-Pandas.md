# Pandas: The Absolute Minimum You Must Know

Pandas looks like a thousand methods, but daily use rests on one data structure, one
selection idiom, and one habit — all on this page. Master `.loc` with a boolean mask and
the rest of the library becomes variations on a theme.

## The Mental Model: A DataFrame Is a Dict of Columns

A **DataFrame** is a table: a dictionary whose keys are column names and whose values are
**Series** — one-dimensional arrays that all share the same row labels (the **index**, the
bold numbers down the left). That's why you build one from a dict literal, and why
`df['mark']` gets you a column, not a row:

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Ava', 'Ben', 'Chloe', 'Dan'],
    'unit': ['ISYS2001', 'ISYS2001', 'COMP1005', 'COMP1005'],
    'mark': [72, 58, 91, 64],
})
```

...and it displays as the table it is, index down the left:

```python
>>> df
    name      unit  mark
0    Ava  ISYS2001    72
1    Ben  ISYS2001    58
2  Chloe  COMP1005    91
3    Dan  COMP1005    64
```

In real work the dict literal is replaced by `pd.read_csv('marks.csv')` — everything after
that line is identical. Operations are **vectorised**: `df['mark'] + 5` adds 5 to every
row at once. If you're writing a `for` loop over rows, you're almost always fighting the
library instead of using it.

## The Habit: Look at Your Data First

Every analysis starts the same way, before any cleverness:

```python
>>> df.head(2)          # the first rows — is this the shape you expected?
  name      unit  mark
0  Ava  ISYS2001    72
1  Ben  ISYS2001    58
>>> df.shape            # (rows, columns)
(4, 3)
```

Then `df.info()` (column types and missing-value counts — the number-that-loaded-as-text
bug lives here) and `df.describe()` (summary statistics — impossible values like a mark
of 910 jump out). Thirty seconds of looking saves hours of debugging a "clean" analysis
built on dirty data.

## Selecting: `loc`, `iloc`, and Boolean Masks

This is *the* core idea. Two indexers, one rule: **`.loc` selects by label,
`.iloc` selects by position**, both as `[row, column]`:

```python
>>> df.loc[2, 'name']        # row labelled 2, column 'name'
'Chloe'
>>> df.iloc[0, 0]            # first row, first column, by position
'Ava'
>>> df['mark'].tolist()      # a bare [] with a name is column shorthand
[72, 58, 91, 64]
```

The power move is putting a **boolean mask** — a Series of True/False built from a
comparison — in the row slot. Read it as "the rows *where*":

```python
>>> df['mark'] >= 65                       # a mask: True/False per row
0     True
1    False
2     True
3    False
Name: mark, dtype: bool
>>> df.loc[df['mark'] >= 65, 'name'].tolist()
['Ava', 'Chloe']
```

Combine conditions with `&` (and), `|` (or), `~` (not) — **not** Python's `and`/`or`,
which raise a `ValueError` — and parenthesise each comparison, because `&` binds tighter
than `>=`:

```python
>>> passed = (df['unit'] == 'ISYS2001') & (df['mark'] >= 50)
>>> df.loc[passed, 'name'].tolist()
['Ava', 'Ben']
```

## Groupby in One Breath

`groupby` is "split the rows into groups, apply something to each group, glue the results
back together" — the pandas spelling of a pivot table:

```python
>>> df.groupby('unit')['mark'].mean()
unit
COMP1005    77.5
ISYS2001    65.0
Name: mark, dtype: float64
```

Read it right to left: the mean of the mark column, per unit. Swap `.mean()` for
`.count()`, `.max()`, or `.agg(['mean', 'count'])` and you've covered most reporting.

## The SettingWithCopy Trap

To *change* values in a filtered selection, you must do the filter and the assignment in
**one** `.loc`:

```python
>>> df.loc[df['mark'] < 60, 'mark'] = 60     # one loc: select AND assign
>>> df['mark'].tolist()
[72, 60, 91, 64]
```

The tempting two-step version — `df[df['mark'] < 60]['mark'] = 60` — is **chained
indexing**: the first `[]` returns a *copy*, the second `[]` writes to that copy, and the
copy is thrown away. Since pandas 3.0 (Copy-on-Write) this is guaranteed to change
nothing, and pandas emits a `ChainedAssignmentError` warning to tell you so. One `.loc`,
always.

## Directing the Machine

An AI writes pandas fluently, but only an informed prompt — one that names columns, masks,
`.loc`, and `groupby` — gets you code you can verify instead of code that merely runs.
Vague prompts invite row loops and chained indexing.

Vague:

```
"clean up the marks in my dataframe and summarise it"
```

Informed:

```
"In df (columns: name, unit, mark), set marks below 50 to 50 using a single .loc
assignment — no chained indexing, no row loop. Then give me the mean and count of
mark per unit with one groupby. I'll check the result with df.describe()."
```

## Spot the Confabulation

An AI assistant explains how to cap the outliers:

```
Filter down to the affected rows, then assign the new value:

    high = df[df['mark'] > 100]
    high['mark'] = 100

Because `high` is a view of `df`, the original DataFrame now has the capped marks.
```

<details><summary>What's wrong?</summary>

`high` is not a view — filtering with `[]` returns a **copy**, so `high['mark'] = 100`
edits a throwaway object and `df` is untouched. The code runs without an exception, which
is what makes it dangerous: the analysis continues on uncapped data. Under pandas 3.0's
Copy-on-Write this no-op is guaranteed (you'll see a `ChainedAssignmentError` warning).
The fix is one line: `df.loc[df['mark'] > 100, 'mark'] = 100`.

</details>

## Where to Practice

- **[100 pandas puzzles](https://github.com/ajcr/100-pandas-puzzles)** — a free notebook
  of short exercises graded from easy to hard; the first thirty drill exactly the
  selection and groupby idioms on this page. No signup.
- **[10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)** — the
  official guided tour; keep it open as the next step whenever this page runs out.

## Quick Reference

| Idiom | What it does |
|---|---|
| `pd.DataFrame({'col': [...]})` | build a table from a dict of columns |
| `pd.read_csv('file.csv')` | build the same table from a file |
| `df.head()` / `df.shape` | first rows / (rows, columns) |
| `df.info()` / `df.describe()` | types & missing values / summary stats |
| `df['col']` | one column, as a Series |
| `df.loc[row, 'col']` | select by **label** |
| `df.iloc[i, j]` | select by **position** |
| `df.loc[mask, 'col']` | the rows *where* the mask is True |
| `(m1) & (m2)`, `\|`, `~` | combine masks — never `and`/`or`, always parenthesise |
| `df.loc[mask, 'col'] = x` | filtered assignment — one `.loc`, never chained `[]` |
| `df.groupby('key')['col'].mean()` | split-apply-combine summary |
| `series.tolist()` | back to a plain Python list |

That covers the absolute minimum! You can now load a table, look before you leap, select
and change exactly the rows you mean, and summarise per group — and to plot what you
found, see `TAMYMN-Matplotlib.md`; everything else in pandas is a variation on these
idioms.
