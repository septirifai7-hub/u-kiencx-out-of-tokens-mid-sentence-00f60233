#!/usr/bin/env python3
"""Entry for make.fun bounty "Out of Tokens, Mid-Sentence".

An AI agent runs out of tokens in the middle of a sentence and
prints one error message. This program writes exactly that one
line, 1 to 140 characters, as UTF-8 text to entry.txt in the
output directory, with no trailing newline. The judge compares
it pairwise against the other entries, weighing first whether it
reads like a real error message from an agent that just ran dry,
then freshness, then the flat error tone turning into the joke.
The trailing em dash is deliberate: the line ends exactly where
the tokens did, so the reader finishes the sentence the agent
could not.

The joke is the line itself being cut off: the error message
announces it is unfinished and then stops mid-word, exactly like
the sentence it was supposed to explain. The program holds the
line as a constant, checks it against the gate before writing
anything, and writes it byte-for-byte. If the line ever drifted
outside the gate, it fails loudly instead of producing an
invalid entry. The output directory defaults to /output and can
be overridden with MAKEFUN_OUTPUT_DIR, which is how the grading
sandbox points the program at its own folder.
"""

import os
import sys
from pathlib import Path

ENTRY = "Error: out of tokens mid-sentence. This error message is also unfinished, much like my—"

MAX_CHARS = 140


def validate(text: str) -> None:
    """Enforce the gate: 1-140 characters, one line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "\t" in text:
        raise ValueError("entry must not contain tab characters")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    target = out_dir / "entry.txt"
    target.write_text(text, encoding="utf-8")
    # The grader collects the output as another user, so the file
    # must stay readable by everyone, not just its owner.
    target.chmod(0o644)


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = ENTRY.strip()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
