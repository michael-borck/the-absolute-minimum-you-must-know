#!/usr/bin/env bash
# Publish the book to GitHub Pages (run after pushing to main).
#
# Renders from a fresh clone on the internal disk because rendering on the
# exFAT project volume fails: macOS drops ._* AppleDouble files mid-render
# and Quarto chokes on them. A clone also guarantees you publish exactly
# what's on origin/main, doctest-checked by CI.
#
# Publishes by force-pushing the rendered _book/ to the gh-pages branch
# (what `quarto publish gh-pages` does, minus its fragile non-interactive
# deployment resolution).
set -euo pipefail

remote=$(git -C "$(cd "$(dirname "$0")/.." && pwd)" remote get-url origin)
tmp=$(mktemp -d "${TMPDIR:-/tmp}/tamymn-publish.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

git clone -q "$remote" "$tmp/repo"
cd "$tmp/repo"
quarto render

cd _book
touch .nojekyll
git init -q -b gh-pages
git add -A
git commit -q -m "Publish book ($(git -C "$tmp/repo" rev-parse --short HEAD))"
git push -q -f "$remote" gh-pages
echo "Published to gh-pages."
