# SQLite: The Absolute Minimum You Must Know

SQLite is a complete relational database that lives in a single ordinary file — no
server, no installation, no password, and Python's standard library already speaks it.
Effective use rests on one loop (connect → execute → fetch → commit), a dozen words of
SQL, and one non-negotiable rule about parameters — all on this page.

## The Mental Model: A Database in a File

A relational database is a set of **tables** (like DataFrames that live on disk —
`TAMYMN-Pandas.md`), and SQLite is the smallest honest implementation: the entire
database — tables, data, indexes — is one file you can copy, email, or commit. Where a
"real" database is a server you connect to over the network, SQLite is just a library
reading that file. `sqlite3.connect('app.db')` opens (or creates) it;
`sqlite3.connect(':memory:')` builds a throwaway database in RAM — perfect for tests and
for every example here.

```python
import sqlite3

conn = sqlite3.connect(':memory:')
```

## The Loop: Execute, Fetch, Commit

You talk to the database in SQL strings via `conn.execute()`, and read answers back with
`fetchone()` / `fetchall()`, which return tuples:

```python
>>> _ = conn.execute("""
...     CREATE TABLE students (
...         id   INTEGER PRIMARY KEY,
...         name TEXT,
...         unit TEXT,
...         mark INTEGER
...     )
... """)
>>> _ = conn.executemany(
...     "INSERT INTO students (name, unit, mark) VALUES (?, ?, ?)",
...     [('Ava', 'ISYS2001', 72), ('Ben', 'ISYS2001', 58), ('Chloe', 'COMP1005', 91)])
>>> conn.commit()
```

Writes are buffered in a transaction until **`conn.commit()`** makes them permanent —
forgetting it is the classic "my inserts vanished when the program ended" bug. Reads need
no commit:

```python
>>> conn.execute("SELECT name, mark FROM students WHERE mark >= 65"
...              " ORDER BY mark DESC").fetchall()
[('Chloe', 91), ('Ava', 72)]
>>> conn.execute("SELECT COUNT(*) FROM students").fetchone()
(3,)
```

When you're done: `conn.close()` (a `:memory:` database vanishes at that moment).

## Parameters: The Non-Negotiable Rule

**Never build SQL by pasting values into the string** — no f-strings, no `+`, no
`.format()`. If the value came from a user, gluing it into the SQL means the user is
writing your SQL: the input `x' OR '1'='1` turns your login check into "match every
row", and nastier inputs delete tables. This is **SQL injection**, it has been the top
web vulnerability for twenty years, and the fix costs nothing: put `?` where each value
goes and pass the values as a tuple — the database then treats them as pure data, never
as SQL. (Bonus: `O'Brien` stops crashing your queries too.)

```python
>>> unit = 'ISYS2001'                     # imagine this arrived from a web form
>>> conn.execute("SELECT name FROM students WHERE unit = ?", (unit,)).fetchall()
[('Ava',), ('Ben',)]
```

Mind the comma: parameters must be a sequence, so one value is `(unit,)` — a one-item
tuple — not `(unit)`, which is just a parenthesised string.

## The Minimum SQL, In One Breath

Six words carry almost everything: **CREATE TABLE** declares a table's columns and types;
**INSERT** adds rows; **SELECT** columns **FROM** a table asks; **WHERE** filters the
rows (and belongs on every **UPDATE** and **DELETE** you ever run — without it they hit
*every* row); **ORDER BY** sorts; **JOIN** lines two tables up on a shared key so a query
can answer across both:

```python
>>> _ = conn.execute("CREATE TABLE units (code TEXT PRIMARY KEY, coordinator TEXT)")
>>> _ = conn.executemany("INSERT INTO units VALUES (?, ?)",
...                      [('ISYS2001', 'Dr Reed'), ('COMP1005', 'Dr Chen')])
>>> conn.execute("""
...     SELECT s.name, u.coordinator
...     FROM students s JOIN units u ON s.unit = u.code
...     WHERE s.mark >= 90
... """).fetchone()
('Chloe', 'Dr Chen')
```

For analysis, hand a query straight to pandas —
`pd.read_sql_query("SELECT ...", conn)` returns a DataFrame — and continue in
`TAMYMN-Pandas.md`.

## Directing the Machine

AI assistants produce fluent SQL, and just as fluently interpolate variables straight
into it. The informed prompt names the schema and demands `?` placeholders, turning
"write a query" into "write a query I can trust with user input".

Vague:

```
"write python code to look up a user in my database"
```

Informed:

```
"Using sqlite3, table students(id, name, unit, mark): a function that takes a unit
code and a pass mark and returns (name, mark) tuples, ORDER BY mark DESC. Use ?
placeholders for both values — no f-strings in SQL — and one execute call."
```

## Spot the Confabulation

An AI assistant writes a search function:

```
def find_student(conn, name):
    query = f"SELECT id, mark FROM students WHERE name = '{name}'"
    return conn.execute(query).fetchall()

Since this is SQLite — a local file, not a web-facing database server — SQL
injection isn't a concern here, and the f-string keeps the code readable.
```

<details><summary>What's wrong?</summary>

The reassurance is the confabulation. Injection has nothing to do with *where the
database lives* and everything to do with *where the value comes from*: pass
`name = "x' OR '1'='1"` and this function returns every student in the table; pass a name
containing `;` fragments and it does worse. Even innocent input breaks it — searching for
`O'Brien` raises a syntax error, because the quote ends the string early. The correct
version is shorter than the excuse:
`conn.execute("SELECT id, mark FROM students WHERE name = ?", (name,))`.

</details>

## Where to Practice

- **[SQLBolt](https://sqlbolt.com)** — interactive SQL lessons that run entirely in the
  browser, no signup; lessons 1–6 and 12–13 cover every keyword on this page.
- **The `sqlite3` command-line shell** — already on most systems: run
  `sqlite3 scratch.db`, type SQL, see results. `.tables` and `.schema` show what's
  inside any SQLite file you're handed.

## Quick Reference

| Idiom | What it does |
|---|---|
| `sqlite3.connect('app.db')` | open/create the database file |
| `sqlite3.connect(':memory:')` | throwaway in-RAM database (tests!) |
| `conn.execute(sql, (v1, v2))` | run SQL with `?` placeholders — always |
| `conn.executemany(sql, rows)` | one statement, many parameter tuples |
| `cur.fetchone()` / `cur.fetchall()` | one tuple / list of tuples |
| `conn.commit()` | make writes permanent — forget it and they vanish |
| `conn.close()` | done (`:memory:` evaporates here) |
| `CREATE TABLE t (col TYPE, ...)` | declare a table |
| `INSERT INTO t VALUES (?, ...)` | add a row |
| `SELECT cols FROM t WHERE ...` | ask — WHERE filters rows |
| `UPDATE` / `DELETE` ... `WHERE` | change/remove rows — never without WHERE |
| `ORDER BY col DESC` | sort the answer |
| `t1 JOIN t2 ON t1.k = t2.k` | answer across two tables |
| `(value,)` | a one-parameter tuple needs its comma |

That covers the absolute minimum! You can now create, fill, query, and join tables in a
real database from pure standard-library Python — safely, with placeholders — and
everything bigger (Postgres, MySQL) reuses this exact mental model.
