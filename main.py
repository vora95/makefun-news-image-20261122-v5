#!/usr/bin/env python3
"""THE NOON EDITION — copy the finished front page to the output dir.

The image for Sunday 22 November 2026 is already drawn and stored next
to this file as entry.png (1024x1024, under 1 MiB). Running this program
places an identical copy at <output>/entry.png. It reads nothing from
the network and writes the same bytes on every run.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def _out_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR")
    if raw:
        return Path(raw)
    return Path.cwd() / "out"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    dst_dir = _out_dir()
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / "entry.png"
    shutil.copyfile(src, dst)
    if dst.stat().st_size > 1_048_576:
        print("entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    # Determinism self-check: a second copy must hash identically.
    probe = dst_dir / ".entry-probe.png"
    shutil.copyfile(src, probe)
    same = _sha256(probe) == _sha256(dst)
    probe.unlink(missing_ok=True)
    if not same:
        print("nondeterministic copy", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({dst.stat().st_size} bytes, sha256 {_sha256(dst)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
