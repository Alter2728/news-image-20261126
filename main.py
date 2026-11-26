#!/usr/bin/env python3
"""Publish the bundled front-page image for 26 November 2026 (stdlib only)."""
import hashlib
import os
import shutil
import sys


def publish():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, "entry.png")
    if not os.path.isfile(source):
        print("missing entry.png beside main.py", file=sys.stderr)
        return 1
    destination_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, "entry.png")
    shutil.copyfile(source, destination)
    with open(destination, "rb") as handle:
        payload = handle.read()
    print("entry.png", len(payload), "bytes", hashlib.sha256(payload).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(publish())
