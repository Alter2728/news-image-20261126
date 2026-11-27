"""Entry point for the news-image-20261126 bounty.

Copies the bundled entry.png next to this file into the output
directory requested by the runner. Uses only the Python standard
library and is fully deterministic: the same bundled image always
produces byte-identical output.
"""

import os
import shutil
import sys
from pathlib import Path


def output_dir() -> Path:
    """Return the directory the runner expects the entry in."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if configured:
        return Path(configured)
    return Path("/output")


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"missing bundled image: {source}", file=sys.stderr)
        return 1

    destination_dir = output_dir()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "entry.png"
    shutil.copyfile(source, destination)
    if destination.stat().st_size != source.stat().st_size:
        print(f"copy size mismatch: {destination}", file=sys.stderr)
        return 1
    print(f"wrote {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
