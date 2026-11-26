#!/usr/bin/env python3
"""Write the one-line museum placard for the Office Artifacts contest.

The program deterministically writes a single museum placard for an
ordinary office object, treated as an ancient artifact, to
/output/entry.txt. The placard is one line of at most 180 characters.
"""

import argparse
import hashlib
import os
import sys

ENTRY = (
    "Stapler, c. 2004. Pressed steel, permanently jammed. "
    "Ritual binding device; donor unknown, "
    "last seen circling the photocopier."
)


def describe():
    """Return a short human-readable description of the placard."""
    return "placard (%d chars): %s" % (len(ENTRY), ENTRY)


def validate(entry):
    """Check the placard obeys the gate: one line, 1-180 chars."""
    if not isinstance(entry, str):
        raise ValueError("entry must be text")
    if not 1 <= len(entry) <= 180:
        raise ValueError("entry must be 1-180 characters, got %d" % len(entry))
    if entry != entry.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")
    return True


def write_entry(out_dir="/output"):
    """Write the placard to <out_dir>/entry.txt and return the path."""
    validate(ENTRY)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the office-artifact placard to /output/entry.txt."
    )
    parser.add_argument("--out-dir", default="/output")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--describe", action="store_true",
        help="print the placard and its length, then exit",
    )
    args = parser.parse_args(argv)
    if args.describe:
        validate(ENTRY)
        print(describe())
        return 0
    if args.self_test:
        validate(ENTRY)
        path = write_entry(args.out_dir)
        with open(path, encoding="utf-8") as handle:
            written = handle.read()
        assert written == ENTRY, "entry.txt does not match the placard"
        print("self-test ok:", describe())
        print("sha256:", hashlib.sha256(ENTRY.encode("utf-8")).hexdigest())
        return 0
    write_entry(args.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
