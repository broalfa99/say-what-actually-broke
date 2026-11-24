#!/usr/bin/env python3
"""Say What Actually Broke.

Writes one line of software error copy, at most 200 characters, that tells
the user the brutal truth about the failure and makes them laugh, to
/output/entry.txt.

The line: an upload that saved as 0 bytes. The brutal truth is that we
stored nothing; the joke is that we did it in record time; the next step is
to attach the file and try again, because this time we will actually keep it.
"""

import os
from pathlib import Path

LINE = (
    "Your upload saved as 0 bytes. We stored nothing, in record time. "
    "Attach the file and try again; this time we'll actually keep it."
)


def main() -> None:
    line = LINE.strip()
    # Explicit checks (not assert): asserts are stripped under `python -O`,
    # so a bad line would slip through silently instead of failing loudly.
    if not 1 <= len(line) <= 200:
        raise ValueError(f"line must be 1-200 chars, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(line, encoding="utf-8")
    # Read back and confirm the file holds exactly the validated line.
    if out_path.read_text(encoding="utf-8") != line:
        raise RuntimeError(f"written entry does not match validated line: {out_path}")
    print(f"wrote {len(line)}-char line to {out_path}")


if __name__ == "__main__":
    main()
