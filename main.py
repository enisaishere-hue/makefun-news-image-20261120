#!/usr/bin/env python3
"""Copy the pre-rendered poster into the output directory and verify it.

Standard library only. The grading sandbox has no Pillow and no fonts,
so this program never renders anything: it copies entry.png, which was
rendered beforehand with render_poster.py, and checks its SHA-256 so a
corrupt or stale copy can never pass silently.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "6294660c8e1c874d6b4b4709df3dab7aff42202495f35498b68c7e74eebca028"
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    with open(target, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    if digest != EXPECTED_SHA256:
        print("sha256 mismatch: got %s, expected %s" % (digest, EXPECTED_SHA256),
              file=sys.stderr)
        return 1
    print("wrote %s sha256=%s" % (target, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
