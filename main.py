#!/usr/bin/env python3
"""The One-Line Laugh — entry program.

Writes one original funny line to /output/entry.txt (or
$OUTPUT_DIR/entry.txt). The line is fixed and hand-written for this
bounty; the program checks it against the competition gate before
writing: UTF-8 text of 1-200 characters, not only whitespace, a single
sentence on one line.
"""

import os
import sys

LINE = (
    "My phone's battery dies at 2% like it's making a dramatic exit, "
    "then turns back on just long enough to show me the low-battery "
    "warning again."
)


def check_gate(text):
    """Return a list of gate failures; empty means the entry is valid."""
    problems = []
    if not text.strip():
        problems.append("entry is blank")
    # Gate is in characters (1-200), not bytes: a line with non-ASCII
    # characters can be <= 200 characters yet > 200 UTF-8 bytes, and
    # must still pass. (The entry itself is plain ASCII, so this
    # changes nothing for it — it only makes the gate correct.)
    size = len(text)
    if not 1 <= size <= 200:
        problems.append(
            "entry is %d characters, gate needs 1-200" % size
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        problems.append("entry must be a single sentence")
    return problems


def main():
    problems = check_gate(LINE)
    if problems:
        for problem in problems:
            print("gate failure: " + problem, file=sys.stderr)
        sys.exit(1)

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)

    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    if written != LINE:
        print("entry mismatch after write", file=sys.stderr)
        sys.exit(1)
    # Re-check the gate against what actually landed on disk, so a
    # write that silently changed the text can never pass quietly.
    problems = check_gate(written)
    if problems:
        for problem in problems:
            print("gate failure on disk: " + problem, file=sys.stderr)
        sys.exit(1)

    print(
        "Wrote entry.txt: %d characters (%d bytes)"
        % (len(written), len(written.encode("utf-8")))
    )


if __name__ == "__main__":
    main()
