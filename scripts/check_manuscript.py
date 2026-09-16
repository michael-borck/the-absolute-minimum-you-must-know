#!/usr/bin/env python3
"""Smoke checks for the web-only companion (stdlib only).

TAMYMN is a living quick reference, not a KDP book: no ISBN, no print
formats. These checks cover the basics — clean sources, no stale links,
and the companion cross-links to the series introduced in 2026-09-16.
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STALE_LINKS = (
    "michaelborck.dev",
    "michaelborck.education",
    "ship-it-python-in-production",
)


def skip_appledouble(paths):
    return [p for p in paths if not p.name.startswith("._")]


class ManuscriptChecks(unittest.TestCase):
    def test_source_encoding_is_utf8(self):
        paths = skip_appledouble(sorted(ROOT.glob("**/*.qmd")))
        for path in paths:
            if "_book" in path.parts or "_print_source" in path.parts:
                continue
            with self.subTest(file=str(path)):
                path.read_text(encoding="utf-8")

    def test_no_stale_links(self):
        for path in skip_appledouble(sorted(ROOT.glob("**/*.qmd"))):
            if "_book" in path.parts or "_print_source" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for target in STALE_LINKS:
                with self.subTest(file=str(path), target=target):
                    self.assertNotIn(target, text)

    def test_home_page_links_to_the_series(self):
        text = (ROOT / "index.qmd").read_text(encoding="utf-8")
        self.assertIn("Go deeper with the series", text)
        for book in ("think-python-direct-ai",
                     "code-python-consult-ai",
                     "ship-python-orchestrate-ai",
                     "converse-python-partner-ai"):
            with self.subTest(book=book):
                self.assertIn(book, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
