#!/usr/bin/env python3
"""Run every python fenced block in the TAMYMN docs.

Blocks containing ``>>>`` are executed as doctests; other python blocks are
exec'd (definitions for later examples). All blocks in one document share a
namespace, in document order, so the docs read like one interpreter session.

Usage: python3 scripts/test_docs.py [files...]   (default: all TAMYMN-*.md)
"""

import doctest
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # docs must never open a window

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^```python\s*$(.*?)^```\s*$", re.MULTILINE | re.DOTALL)


def check_file(path: Path) -> list[str]:
    failures = []
    namespace: dict = {"__name__": "__tamymn__"}
    text = path.read_text(encoding="utf-8")
    for i, match in enumerate(FENCE.finditer(text), start=1):
        block = match.group(1)
        line_no = text[: match.start()].count("\n") + 2
        label = f"{path.name}: block {i} (line {line_no})"
        if ">>>" in block:
            parser = doctest.DocTestParser()
            runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS)
            test = parser.get_doctest(block, namespace, label, str(path), line_no)
            out: list[str] = []
            runner.run(test, out=out.append)
            if runner.failures:
                failures.append(f"{label}\n{''.join(out)}")
        else:
            try:
                exec(compile(block, label, "exec"), namespace)
            except Exception as exc:  # noqa: BLE001 - report and continue
                failures.append(f"{label}\n  exec failed: {exc!r}")
    return failures


def main() -> int:
    args = [Path(a) for a in sys.argv[1:]]
    files = args or sorted(ROOT.glob("TAMYMN-*.md"))
    all_failures = []
    checked = 0
    for path in files:
        fails = check_file(path)
        blocks = len(FENCE.findall(path.read_text(encoding="utf-8")))
        checked += blocks
        status = "ok" if not fails else f"{len(fails)} FAILED"
        print(f"{path.name}: {blocks} python block(s) {status}")
        all_failures.extend(fails)
    print(f"\n{checked} blocks checked across {len(files)} file(s), "
          f"{len(all_failures)} failure(s)")
    for failure in all_failures:
        print("\n--- " + failure)
    return 1 if all_failures else 0


if __name__ == "__main__":
    sys.exit(main())
