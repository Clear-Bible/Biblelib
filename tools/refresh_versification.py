"""Refresh the bundled versification data from the Copenhagen Alliance.

The Copenhagen scheme JSON (eng/org/rso) ships in the package, and the vref
`.txt` files are derived from it. This tool keeps both in sync.

By default it re-downloads the *pinned* Copenhagen commit
(`biblelib.versification.Enumerator.COPENHAGEN_SHA`) and regenerates the vref
`.txt` -- reproducible, and a no-op unless the pin was bumped. With --latest it
resolves the current Copenhagen master HEAD, downloads from there, regenerates
vref, and rewrites COPENHAGEN_SHA to the new commit.

Either way: review `git diff`, run `pytest tests/versification`, and commit the
JSON + regenerated `.txt` (+ the pin bump, with --latest) together.

Usage:
    poetry run python tools/refresh_versification.py            # from the pinned commit
    poetry run python tools/refresh_versification.py --latest   # fetch + repin to master HEAD
"""

import argparse
import re
from pathlib import Path

import requests

import biblelib.versification.Enumerator as enum_mod

REPO = "Copenhagen-Alliance/versification-specification"
SCHEMES = ("eng", "org", "rso")
SCOPE = {
    "nt": {"nt_only": True},
    "ot": {"ot_only": True},
    "protestant": {"with_deuterocanon": False},
}
VDIR = Path(enum_mod.__file__).resolve().parent  # biblelib/versification/
ENUM_FILE = Path(enum_mod.__file__)


def latest_sha() -> str:
    """Return the current Copenhagen master HEAD commit SHA."""
    resp = requests.get(f"https://api.github.com/repos/{REPO}/commits/master", timeout=30)
    resp.raise_for_status()
    return str(resp.json()["sha"])


def json_url(sha: str, scheme: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{sha}/versification-mappings/standard-mappings/{scheme}.json"


def repin(sha: str) -> None:
    """Rewrite COPENHAGEN_SHA in Enumerator.py to the given commit."""
    text = ENUM_FILE.read_text(encoding="utf-8")
    text, n = re.subn(r'COPENHAGEN_SHA = "[0-9a-f]+"', f'COPENHAGEN_SHA = "{sha}"', text, count=1)
    assert n == 1, "could not locate COPENHAGEN_SHA to repin"
    ENUM_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--latest",
        action="store_true",
        help="fetch Copenhagen master HEAD and repin (default: use the pinned commit)",
    )
    args = parser.parse_args()

    sha = latest_sha() if args.latest else enum_mod.COPENHAGEN_SHA
    print(f"Copenhagen commit: {sha} ({'latest' if args.latest else 'pinned'})")

    # 1. download the scheme JSON
    for scheme in SCHEMES:
        resp = requests.get(json_url(sha, scheme), timeout=30)
        resp.raise_for_status()
        dest = VDIR / f"{scheme}.json"
        old = dest.read_bytes() if dest.exists() else b""
        dest.write_bytes(resp.content)
        state = "UPDATED" if resp.content != old else "unchanged"
        print(f"  {scheme}.json: {len(resp.content):>7} bytes  [{state}]")

    # 2. repin (after a successful download)
    if args.latest:
        repin(sha)
        print(f"  repinned COPENHAGEN_SHA -> {sha}")

    # 3. regenerate the derived vref .txt from the freshly-downloaded JSON
    for scheme in SCHEMES:
        for canon, scope_kw in SCOPE.items():
            out = VDIR / f"{scheme}-{canon}-vref.txt"
            enum_mod.Enumerator(scheme).write_enumeration(out, **scope_kw)
        print(f"  {scheme}: regenerated nt/ot/protestant vref")

    print("\nDone. Review `git diff`, run `pytest tests/versification`, then commit.")


if __name__ == "__main__":
    main()
