"""Biblelib provides utilities for working with Bible books, references, pericopes, and other units.

This namespace is intentionally bare: see individual packages
(`books`, `words`, etc.) for imports.

"""

import requests
import socket


CANONIDS: set[str] = {
    "nt",
    "ot",
    # meaning the entire 66 book corpus
    "protestant",
}

VERSIFICATIONIDS: set[str] = {
    "eng",
    "org",
    "rso",
    # not yet implemented
    # "ethiopian_custom", "lxx", "rsc", "vul"
}


# def has_connection() -> bool:
#     """Return True if there is an active network connection."""
#     try:
#         _ = requests.head(url="http://example.com/", timeout=5)
#         return True
#     except requests.ConnectionError:
#         print("--- No internet connection.")
#         return False


# from Claude
def has_connection(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> bool:
    """
    Test for an active network connection.

    Args:
        host: Host to connect to (default: Google's DNS server)
        port: Port to connect to (default: 53 for DNS)
        timeout: Connection timeout in seconds (default: 3.0)

    Returns:
        True if connection successful, False otherwise
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except (socket.timeout, socket.error, OSError):
        return False


__all__ = [
    "CANONIDS",
    "VERSIFICATIONIDS",
    "has_connection",
]


# this is a bit slow to load: is it worth it?
# you can still load it directly with
# from biblelib.word import ubs
# try:
#     _ = requests.head(url="http://example.com/", timeout=5)
#     from .ubs import fromubs

#     _exportlist.append("fromubs")
# except requests.ConnectionError:
#     print("No internet connection, cannot load ubs.fromubs(), other functionality")
