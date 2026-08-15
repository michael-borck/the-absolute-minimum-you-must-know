# The Absolute Minimum You Must Know

<!-- BADGES:START -->
[![documentation](https://img.shields.io/badge/-documentation-blue?style=flat-square)](https://github.com/topics/documentation) [![python](https://img.shields.io/badge/-python-3776ab?style=flat-square)](https://github.com/topics/python) [![self-directed-learning](https://img.shields.io/badge/-self--directed--learning-blue?style=flat-square)](https://github.com/topics/self-directed-learning) [![book](https://img.shields.io/badge/-book-795548?style=flat-square)](https://github.com/topics/book) [![assessment](https://img.shields.io/badge/-assessment-blue?style=flat-square)](https://github.com/topics/assessment)
<!-- BADGES:END -->

[![Test docs](https://github.com/michael-borck/the-absolute-minimum-you-must-know/actions/workflows/test.yml/badge.svg)](https://github.com/michael-borck/the-absolute-minimum-you-must-know/actions/workflows/test.yml)

For every topic in software development there is a minimum viable set of ideas that
unlocks everything else. Each `TAMYMN-*.md` file here is one page: read it in ten
minutes, know enough to work — and know enough to **direct an AI at the topic and catch
it when it's wrong**.

That second half is the thesis. In the age of AI assistants, the minimum you must know
is no longer "enough to do everything by hand" — it is enough to *decompose a problem,
give a precise instruction, and verify the result*. Every chapter therefore ends with:

- **Directing the Machine** — a vague prompt vs an informed prompt, and why the informed
  one works (it names the concepts on the page);
- **Spot the Confabulation** — a plausible-but-wrong AI answer for you to catch;
- **Where to Practice** and a **Quick Reference** table.

## Read it

- **As a book** — **[minimum.borck.education](https://minimum.borck.education)**: the
  rendered site (built with [Quarto](https://quarto.org)), with search, guided trails,
  a "where should I start?" self-diagnostic, and an in-browser Python playground.
- **As plain files** — every chapter is a standalone Markdown file, readable right here
  on GitHub. Start anywhere; each page stands alone.
- **In a real environment** — open the repo in **GitHub Codespaces** (it ships a
  [dev container](.devcontainer/devcontainer.json)): a genuine Linux shell, Git, Python
  and every library the chapters use, zero install.

## This book checks its own examples

Every ```` ```python ```` block in every chapter is executed as a
[doctest](TAMYMN-Doctest.md) by [`scripts/test_docs.py`](scripts/test_docs.py), and CI
refuses to publish the book if a single example is wrong. The repository practices the
verification it preaches:

```bash
pip install pandas matplotlib beautifulsoup4
python3 scripts/test_docs.py            # run every example in every chapter
```

## Structure

| Part | Chapters |
|---|---|
| — | Start Here (absolute-beginner on-ramp) |
| Thinking | Computational Thinking · Algorithms · Data Structures |
| Python | Python · Functions · File IO · Functional Programming · Event-Driven Programming |
| Objects | OOP · Classes · Encapsulation · Abstraction · Inheritance · Polymorphism · Composition |
| Verification | Testing · Doctest · TDD |
| Data | Pandas · Matplotlib · Visualisation · SQLite · Web Scraping |
| Tools | Linux · Git · Markdown · VS Code · Jupyter · Colab |
| Directing AI | AI Coding Agents |
| Appendices | Glossary · in-browser Python Playground |

## Contributing

Contributions welcome. Read [`STYLE.md`](STYLE.md) first — it defines the bar every
chapter must meet (the required sections, the 120–200 line budget, and the rule that
Python examples are passing doctests). `TAMYMN-Linux.md` and `TAMYMN-Git.md` are the
exemplars. Then the usual: fork, branch, PR. CI will run your examples.

Publishing is manual (CI only tests): after merging to `main`, run
`scripts/publish.sh`, which renders from a fresh clone and pushes the book to the
`gh-pages` branch.

## License

MIT — see [LICENSE](LICENSE).
