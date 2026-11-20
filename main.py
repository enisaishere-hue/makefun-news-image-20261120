#!/usr/bin/env python3
"""news-image-20261120 entry.

Copies the pre-rendered poster (entry.png, shipped in this repo) to the
grader output directory and verifies the copy byte-for-byte against its
known SHA-256 hash. Standard library only; no rendering happens here,
because the grader sandbox has no image libraries or fonts.
"""

import hashlib
import os
import shutil
import sys

ENTRY_NAME = "entry.png"
ENTRY_SHA256 = "b1af05dbb10ee1b5a0db8e5d72cd59f62b3ad4720d88cd1d3693b2a7c4d0934c"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv):
    output_dir = argv[1] if len(argv) > 1 else "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ENTRY_NAME)
    target = os.path.join(output_dir, ENTRY_NAME)

    if not os.path.isfile(source):
        print("error: %s not found next to main.py" % ENTRY_NAME, file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)
    if os.path.isdir(target):
        print("error: %s is a directory" % target, file=sys.stderr)
        return 1

    # Verify the shipped poster before copying, so a damaged repo file
    # fails fast with a clear message instead of a bad copy.
    source_hash = sha256_of(source)
    if source_hash != ENTRY_SHA256:
        print("error: shipped %s failed its hash check" % ENTRY_NAME, file=sys.stderr)
        print("  expected: %s" % ENTRY_SHA256, file=sys.stderr)
        print("  actual:   %s" % source_hash, file=sys.stderr)
        return 1

    shutil.copyfile(source, target)

    actual = sha256_of(target)
    if actual != ENTRY_SHA256:
        print("error: hash mismatch for %s" % target, file=sys.stderr)
        print("  expected: %s" % ENTRY_SHA256, file=sys.stderr)
        print("  actual:   %s" % actual, file=sys.stderr)
        return 1

    print("wrote %s (sha256 %s)" % (target, actual))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
