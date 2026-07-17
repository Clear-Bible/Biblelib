"""Shared pytest configuration for the Biblelib test suite."""

import tempfile
from pathlib import Path

from filelock import FileLock

from biblelib import data


def pytest_configure(config: object) -> None:
    """Pre-seed the on-demand data cache before test collection.

    Some test modules instantiate the Macula mapping classes at import
    time, which would otherwise download the data during collection --
    once per pytest-xdist worker, concurrently, hammering GitHub. A file
    lock serializes this so only one process downloads and the rest read
    the shared, checksum-verified cache. On a warm cache this is a fast
    no-op; if offline with a cold cache it is skipped, and the mapping
    tests surface the missing data individually.
    """
    lock = Path(tempfile.gettempdir()) / "biblelib-data-cache.lock"
    try:
        with FileLock(str(lock)):
            data.download_all()
    except Exception as err:  # offline or fetch failure: don't block other tests
        print(f"biblelib: could not pre-seed data cache ({err})")
