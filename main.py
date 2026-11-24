#!/usr/bin/env python3
"""news-image-20261124 entrypoint (pure stdlib).

Copies the bundled poster image to the grader's output location.
The poster itself is drawn by render_poster.py (Pillow, local only);
the grader runs vanilla Python with no Pillow and no fonts, so this
program never imports anything beyond the standard library.
"""
import hashlib
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("bundled entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    targets = []
    if out_dir:
        targets.append(os.path.join(out_dir, "entry.png"))
    targets.append("/output/entry.png")
    targets.append(os.path.join(os.getcwd(), "output.png"))
    data = open(src, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    wrote = None
    for t in targets:
        try:
            os.makedirs(os.path.dirname(t) or ".", exist_ok=True)
            with open(t, "wb") as f:
                f.write(data)
            os.chmod(t, 0o644)
            wrote = t
            break
        except OSError:
            continue
    if wrote is None:
        print("could not write entry.png to any target", file=sys.stderr)
        return 1
    print("entry.png %d bytes sha256 %s -> %s" % (len(data), sha, wrote))
    return 0


if __name__ == "__main__":
    sys.exit(main())
