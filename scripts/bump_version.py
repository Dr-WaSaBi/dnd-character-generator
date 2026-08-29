#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : scripts/bump_version.py                                   ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Pre-commit hook script that auto-increments the patch version in    ║
# ║  the ASCII header of every staged .py file before each git commit.   ║
# ╚══════════════════════════════════════════════════════════════════════╝

import re
import subprocess
import sys


VERSION_RE = re.compile(r"(# ║  Version : )(\d+)\.(\d+)\.(\d+)")


def get_staged_py_files():
    """Return a list of .py file paths that are currently staged for commit."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True
    )
    return [f for f in result.stdout.splitlines() if f.endswith(".py")]


def bump_patch(path):
    """Read the file at path, increment the patch version in the header, and write it back."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
    except OSError:
        return False

    def _inc(m):
        major, minor, patch = int(m.group(2)), int(m.group(3)), int(m.group(4))
        return f"{m.group(1)}{major}.{minor}.{patch + 1}"

    new_content, count = VERSION_RE.subn(_inc, content, count=1)
    if count == 0:
        return False

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new_content)
    return True


def restage(path):
    """Re-add the file to the git staging area after modifying its version line."""
    subprocess.run(["git", "add", path], check=True)


def main():
    """Find all staged .py files, bump their patch version, and re-stage them."""
    files = get_staged_py_files()
    for path in files:
        if bump_patch(path):
            restage(path)
            print(f"  bumped version: {path}")


if __name__ == "__main__":
    main()
    sys.exit(0)
