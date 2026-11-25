#!/usr/bin/env python3
"""news-20261125-timeline entry point.

Copies the pre-rendered entry.png (drawn by draw_timeline.py) into
$MAKEFUN_OUTPUT_DIR/entry.png, byte-for-byte.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1 * 1024 * 1024  # competition cap: image at most 1 MiB

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(SRC):
        print(f"error: {SRC} not found", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, dst)
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(dst)
    if src_size != dst_size:
        print(f"error: incomplete copy ({dst_size} of {src_size} bytes)",
              file=sys.stderr)
        return 1
    if dst_size > MAX_BYTES:
        print(f"error: entry.png is {dst_size} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    # byte-for-byte check: the copy must hash identically to the source
    def _sha(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    if _sha(SRC) != _sha(dst):
        print("error: copy hash differs from source", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({dst_size} bytes, sha256 {_sha(dst)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
