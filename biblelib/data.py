"""On-demand download and local caching of large word-mapping data.

Most Biblelib data ships inside the package (book metadata, versification
vref files and scheme JSON). The two Macula word-mapping tables, however, are
large (~12 MB each) and low-churn, so they are downloaded on first use and
cached locally rather than bundled in the wheel.

The cache lives in an OS-appropriate location (see :func:`pooch.os_cache`),
e.g. ``~/Library/Caches/biblelib`` on macOS or ``~/.cache/biblelib`` on Linux.
Set the ``BIBLELIB_DATA_DIR`` environment variable to relocate it (useful for
CI, offline, or air-gapped environments).

To pre-populate the cache while online -- for offline use, or to avoid many
concurrent downloads when running tests in parallel (pytest-xdist) -- run the
bundled console script::

    biblelib-download-data

Downloads are verified against pinned SHA256 hashes. The source files are
pinned to specific upstream commits so the hashes are reproducible; to refresh
the data for a new release, update the commit SHA and hash below and re-run
``biblelib-download-data``.
"""

from pathlib import Path

import pooch

# Data-file names (also the keys used in the pooch registry).
GNT_MAPPINGS = "mappings-GNT-stripped.tsv"
WLCM_MAPPINGS = "macula_to_marble_map.tsv"

# Upstream commits the pinned hashes correspond to. Bump these (and the hashes)
# to refresh the data.
GNT_SHA = "17a9e44bf9fee4783f1e89b62f8d5a83f3de68c9"
HEB_SHA = "766cb79aa0ec1e1afeabfcf3b486b985f24d2e90"

REGISTRY = {
    GNT_MAPPINGS: "sha256:9d5f114d6c75a43203aad5108611bbf05f2818ac771f0d7aa3ca1e2cb8a9bb1b",
    WLCM_MAPPINGS: "sha256:f4468aebe59279c018f9e3e79a5d4b37d50a409803a535d77658841775b5bc18",
}

URLS = {
    GNT_MAPPINGS: (
        f"https://raw.githubusercontent.com/Clear-Bible/macula-greek/{GNT_SHA}"
        "/sources/Clear/mappings/mappings-GNT-stripped.tsv"
    ),
    WLCM_MAPPINGS: (
        f"https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/{HEB_SHA}"
        "/mappings/tsv/macula_to_marble_map.tsv"
    ),
}

# Per-file URLs are supplied via `urls`, so `base_url` is unused.
POOCH_STORE = pooch.create(
    path=pooch.os_cache("biblelib"),
    base_url="",
    env="BIBLELIB_DATA_DIR",
    registry=REGISTRY,
    urls=URLS,
)


def fetch(name: str) -> Path:
    """Return a local path to a data file, downloading and verifying on first use.

    On subsequent calls the cached, checksum-verified copy is returned without
    any network access. Raises a RuntimeError with actionable guidance if the
    file cannot be obtained (e.g. offline with an empty cache, or a hash
    mismatch).
    """
    try:
        return Path(POOCH_STORE.fetch(name))
    except Exception as err:
        raise RuntimeError(
            f"Could not obtain data file {name!r}. Run `biblelib-download-data` "
            "while online to populate the cache, or point the BIBLELIB_DATA_DIR "
            "environment variable at a pre-populated cache directory."
        ) from err


def download_all() -> list[Path]:
    """Download and cache every registered data file. Returns their local paths."""
    return [fetch(name) for name in REGISTRY]


def main() -> None:
    """Console-script entry point: pre-populate the local data cache."""
    for path in download_all():
        print(f"cached {path}")
