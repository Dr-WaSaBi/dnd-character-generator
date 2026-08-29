#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : scripts/install_hooks.py                                  ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  One-time setup script that copies the tracked pre-commit hook into  ║
# ║  .git/hooks/ and makes it executable. Run after cloning the repo.    ║
# ╚══════════════════════════════════════════════════════════════════════╝

import shutil
import stat
from pathlib import Path


def main():
    """Copy scripts/pre-commit to .git/hooks/pre-commit and mark it executable."""
    root = Path(__file__).parent.parent
    src = root / "scripts" / "pre-commit"
    dst = root / ".git" / "hooks" / "pre-commit"

    shutil.copy2(src, dst)
    dst.chmod(dst.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Installed: {dst}")


if __name__ == "__main__":
    main()
