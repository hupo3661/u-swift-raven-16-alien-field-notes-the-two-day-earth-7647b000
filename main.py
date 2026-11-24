#!/usr/bin/env python3
"""Alien Field Notes: The Two Day Earth Review.

An alien tourist's one-line review of Earth, written to
``/output/entry.txt`` for the make.fun bounty of the same name.

The program is deliberately boring: no randomness, no network, no
clock, no dependencies. It validates the review against the bounty
rules (a single line, at most 200 characters), writes it to the
output file, reads the file back to prove the write landed, and
prints the review to stdout.
"""

import os
import sys

# Bounty rules.
MAX_ENTRY_LENGTH = 200
DEFAULT_OUTPUT_PATH = "/output/entry.txt"

# The review, exactly as submitted. Kept as one literal split across
# lines for readability; the joined string is the entry, character
# for character, with no formatting applied.
REVIEW = (
    "Three stars for Earth: gorgeous sunsets, friendly dogs \u2014 "
    "but the locals stare at glowing rectangles all day, then get upset "
    "when the rectangles don't love them back. Would visit again."
)


class EntryError(Exception):
    """Raised when the review breaks a bounty rule or a write fails."""


def check_length(text: str) -> None:
    """Enforce the bounty length limit, reporting the overrun."""
    if len(text) > MAX_ENTRY_LENGTH:
        raise EntryError(
            f"entry is {len(text)} characters, over the "
            f"{MAX_ENTRY_LENGTH} character limit"
        )


def check_review(text: str) -> None:
    """Make sure the review is a legal entry before anything is written."""
    if not text.strip():
        raise EntryError("entry must not be empty")
    if text != text.strip():
        raise EntryError("entry must not have leading or trailing whitespace")
    check_length(text)
    if "\n" in text or "\r" in text:
        raise EntryError("entry must be a single line with no newlines")


def resolve_output_path() -> str:
    """Where the entry goes: OUTPUT_PATH wins, otherwise the default."""
    return os.environ.get("OUTPUT_PATH", DEFAULT_OUTPUT_PATH)


def write_entry(path: str, text: str) -> None:
    """Create the output directory if needed and write the entry."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def read_back(path: str) -> str:
    """Read the entry file back so a bad write cannot slip through."""
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def run() -> str:
    """Validate, write, verify, and return the review text."""
    check_review(REVIEW)
    output_path = resolve_output_path()
    write_entry(output_path, REVIEW)
    written = read_back(output_path)
    if written != REVIEW:
        raise EntryError(
            "write verification failed: entry file content does not "
            "match the review"
        )
    return REVIEW


def main() -> int:
    try:
        review = run()
    except EntryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(review)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
