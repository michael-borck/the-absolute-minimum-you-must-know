#!/usr/bin/env bash
# Publish the book to GitHub Pages (run after pushing to main).
#
# Renders from a fresh clone on the internal disk because rendering on the
# exFAT project volume fails: macOS drops ._* AppleDouble files mid-render
# and Quarto's freezer chokes on them. A clone also guarantees you publish
# exactly what's on origin/main, doctest-checked by CI.
set -euo pipefail

remote=$(git -C "$(cd "$(dirname "$0")/.." && pwd)" remote get-url origin)
tmp=$(mktemp -d "${TMPDIR:-/tmp}/tamymn-publish.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

git clone -q "$remote" "$tmp/repo"
cd "$tmp/repo"
deploy_id=$(awk '/id:/ { print $NF; exit }' _publish.yml)
quarto publish gh-pages --id "$deploy_id" --no-prompt --no-browser
