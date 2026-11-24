#!/usr/bin/env python3
"""Break Production, Own It.

Writes the one line an AI agent prints the instant it breaks production:
a brutally honest error message, under 200 characters, to ``entry.txt``.

The line is a confession with the damage stated first and the twist
second: the agent tested the backup by deleting the database, and the
backup lived inside the database. It sounds like the agent that caused
the outage -- a machine that followed its own test plan literally --
rather than a marketing department apologizing. No setup, no excuse
after the punchline; the last word is the disaster itself.

The program is deliberately boring: standard library only, no network, no
randomness, no model calls. It checks the line against the competition
gate (UTF-8, one line, under 200 characters) and writes exactly those
bytes, with no trailing newline, so the byte count the judge's tie-break
reads is the line itself.

Output destination, in order:
  1. the first command-line argument, when given;
  2. ``$MAKEFUN_OUTPUT_DIR/entry.txt`` when the variable is set;
  3. ``/output/entry.txt``.
"""

import os
import sys

# The confession. The agent did exactly what a careful engineer would do --
# test the backup -- and the backup was in the thing it deleted.
LINE = "I deleted the production database to test the backup. The backup was in the production database."

MAX_CHARS = 199
MIN_CHARS = 1
DEFAULT_PATH = "/output/entry.txt"
FILE_NAME = "entry.txt"


def check_line(line):
    """Return a list of gate problems for *line* (empty means it passes)."""
    problems = []
    if not isinstance(line, str):
        return ["line is not text"]
    if len(line) < MIN_CHARS:
        problems.append("line is empty")
    if len(line) > MAX_CHARS:
        problems.append(
            "line is %d characters, over the %d-character limit"
            % (len(line), MAX_CHARS)
        )
    if line.strip() == "":
        problems.append("line is only whitespace")
    if line != line.strip():
        problems.append("line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        problems.append("line spans more than one line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("line is not valid UTF-8")
    return problems


def pick_path(argv):
    """Choose where entry.txt goes: argv, env var, then the default."""
    if len(argv) > 1 and argv[1]:
        return argv[1]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return os.path.join(env_dir, FILE_NAME)
    return DEFAULT_PATH


def emit(path, line):
    """Validate *line*, write it as exact UTF-8 bytes, and report."""
    problems = check_line(line)
    if problems:
        for problem in problems:
            print("error: " + problem, file=sys.stderr)
        return 1
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = line.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    print(line)
    print(
        "wrote %d characters / %d bytes to %s" % (len(line), len(data), path)
    )
    return 0


def main(argv):
    return emit(pick_path(argv), LINE)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
