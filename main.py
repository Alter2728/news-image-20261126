"""Entry point for the news-image-20261126 make.fun bounty.

Copies the bundled front-page image to the grader output directory.
Standard library only; the copy is byte-identical on every run.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        raise FileNotFoundError(f"bundled image missing: {source}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise OSError("copied image size mismatch")


if __name__ == "__main__":
    main()
