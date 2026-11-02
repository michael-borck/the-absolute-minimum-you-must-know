> This content is from *TAMYMN-Markdown.md*, part of *The Absolute Minimum You Must Know*.

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

The `#` characters need a space after them, and headings need a blank line around them.
Most "why isn't my Markdown rendering?" mysteries are a missing blank line or a missing
space after a marker.

## Lists

## Line Breaks: The Classic Stumble

A single Enter does **not** start a new line in the output — consecutive lines are joined
into one paragraph. A **blank line** starts a new paragraph. This is the number-one
beginner surprise: your carefully arranged lines render as one run-on blob. When you
genuinely need a break without a paragraph gap, end the line with two spaces or ``.

## Links and Images

The only difference between a link and an image is the leading `!`. Forget it and you get
a clickable link to your picture instead of the picture.

## Code: Inline and Fenced

Backticks mark code. Single backticks for `inline` mentions of commands or filenames;
triple-backtick **fences** for blocks:

`python
print("hello")
`

Always put the **language tag** after the opening fence. It buys you two things: renderers
apply syntax highlighting, and *tools can find and act on your code* — formatters and
linters process tagged blocks, and this very repository's test suite executes every
`python `
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

Informed:

## Spot the Confabulation

An AI assistant explains how to finish a README:

What's wrong?

Both claims are confidently false. `logo.png` is a *link* — file extension
is irrelevant; embedding an image requires the leading `!`: ``. And
single newlines are collapsed into the same paragraph, so the address block renders as
one run-on line; you need a blank line between paragraphs, or two trailing spaces /
`` for a hard break.

## Where to Practice

- **CommonMark's ten-minute tutorial** — the
  people who standardised Markdown teach it interactively, one construct per lesson with
  instant feedback. No signup.
- **Markdown Live Preview** — a split-pane editor:
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
| two trailing spaces or `` | hard line break |
| `text` | link |
| `` | image — the `!` is the whole difference |
| `` `code` `` | inline code |
| `lang `` ` | fenced code block — always tag the language |
| `\| a \| b \|` rows + `\|---\|---\|` | table |

That covers the absolute minimum! You can now write a README, a GitHub issue, or a
structured AI prompt that renders exactly as intended — everything fancier is a
CommonMark spec lookup away.
