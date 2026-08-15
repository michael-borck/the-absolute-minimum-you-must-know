# Markdown: The Absolute Minimum You Must Know

Markdown is plain text with a handful of conventions that render as formatted documents.
The whole language that matters fits on this page, and it's the format of READMEs, GitHub
issues, Jupyter text cells, and your prompts to AI models — learn it once, use it
everywhere, forever.

## The Mental Model: Readable Raw, Rendered Pretty

A Markdown file is just a `.md` text file. The design rule behind every piece of syntax:
**the raw text should already look like what it means.** `# Title` looks like a title,
`- item` looks like a bullet, `**bold**` shouts. That's why you can read a raw README in
a terminal and why Git diffs of Markdown stay reviewable. If your source is becoming
unreadable, you're fighting the format — simplify.

## Headings and Emphasis

```
# Heading 1          — one per document: the title
## Heading 2         — main sections
### Heading 3        — subsections; stop here in practice
*italic*  **bold**   — emphasis; don't stack more than this
```

The `#` characters need a space after them, and headings need a blank line around them.
Most "why isn't my Markdown rendering?" mysteries are a missing blank line or a missing
space after a marker.

## Lists

```
- unordered item     — also works with * or +; pick - and stick with it
- another item
  - indent two spaces to nest

1. ordered item      — the numbers auto-correct when rendered,
1. next item         — so you can write 1. every time and reorder freely
```

## Line Breaks: The Classic Stumble

A single Enter does **not** start a new line in the output — consecutive lines are joined
into one paragraph. A **blank line** starts a new paragraph. This is the number-one
beginner surprise: your carefully arranged lines render as one run-on blob. When you
genuinely need a break without a paragraph gap, end the line with two spaces or `<br>`.

## Links and Images

```
[link text](https://example.com)      — text in brackets, destination in parentheses
![alt text](diagram.png)              — same, plus ! in front: embed, don't link
```

The only difference between a link and an image is the leading `!`. Forget it and you get
a clickable link to your picture instead of the picture.

## Code: Inline and Fenced

Backticks mark code. Single backticks for `inline` mentions of commands or filenames;
triple-backtick **fences** for blocks:

````
```python
print("hello")
```
````

Always put the **language tag** after the opening fence. It buys you two things: renderers
apply syntax highlighting, and *tools can find and act on your code* — formatters and
linters process tagged blocks, and this very repository's test suite executes every
```` ```python ```` block to prove the examples work. An untagged block is a screenshot;
a tagged block is data.

## Tables

```
| Command | Effect |
|---------|--------|
| `ls`    | list   |
| `cd`    | move   |
```

Header row, a `|---|` separator row, then data rows. The pipes don't need to line up in
the source — the renderer aligns everything. Tables are the one place raw Markdown gets
ugly; keep them small.

## The Lingua Franca

Markdown isn't one tool's format — it's the shared writing layer of modern computing.
GitHub renders your `README.md` as the project's front page and every issue and pull
request comment is Markdown. Jupyter's text cells are Markdown. And AI chat runs on it in
*both directions*: models answer in Markdown, and a structured prompt — headings for
context, bullets for requirements, fenced blocks for code — is parsed more reliably than
a wall of prose. Fencing code in a prompt tells the model exactly where your code starts
and stops, so it can't blur your instructions into your program.

## Directing the Machine

When you ask an AI to write or fix Markdown, name the constructs on this page — fences,
language tags, blank-line rules — and use them in the prompt itself, so the model can't
misread which text is content and which is instruction.

Vague:

```
"make my readme look better"
```

Informed:

```
"Here's my README between the fences below. Restructure it: one # title, ## sections
for Install / Usage / License, a fenced bash block with a language tag for the install
commands, and a small table of CLI flags. Keep the raw text readable — no HTML."
```

## Spot the Confabulation

An AI assistant explains how to finish a README:

```
To show your logo, write [logo.png](logo.png) — Markdown sees the image extension
and renders it inline. For the address block, just press Enter at the end of each
line; every newline in the source becomes a line break in the output.
```

<details><summary>What's wrong?</summary>

Both claims are confidently false. `[logo.png](logo.png)` is a *link* — file extension
is irrelevant; embedding an image requires the leading `!`: `![logo](logo.png)`. And
single newlines are collapsed into the same paragraph, so the address block renders as
one run-on line; you need a blank line between paragraphs, or two trailing spaces /
`<br>` for a hard break.

</details>

## Where to Practice

- **[CommonMark's ten-minute tutorial](https://commonmark.org/help/tutorial/)** — the
  people who standardised Markdown teach it interactively, one construct per lesson with
  instant feedback. No signup.
- **[Markdown Live Preview](https://markdownlivepreview.com)** — a split-pane editor:
  type on the left, watch it render on the right. Perfect for testing the blank-line and
  line-break rules until they're intuition.

## Quick Reference

| Syntax | Meaning |
|---|---|
| `# H1` / `## H2` / `### H3` | headings (space after `#`, blank lines around) |
| `*italic*` / `**bold**` | emphasis |
| `- item` | bullet list (indent 2 spaces to nest) |
| `1. item` | numbered list (numbers auto-correct) |
| blank line | new paragraph — single Enter does nothing |
| two trailing spaces or `<br>` | hard line break |
| `[text](url)` | link |
| `![alt](file.png)` | image — the `!` is the whole difference |
| `` `code` `` | inline code |
| ```` ```lang ```` … ```` ``` ```` | fenced code block — always tag the language |
| `\| a \| b \|` rows + `\|---\|---\|` | table |

That covers the absolute minimum! You can now write a README, a GitHub issue, or a
structured AI prompt that renders exactly as intended — everything fancier is a
[CommonMark spec](https://commonmark.org) lookup away.
