"""
torrentp.

A great library-wrapper for downloading from torrent.
"""

__version__ = "0.1.1"
__author__ = 'Nima Akbarzade'
__author_email__ = "iw4p@protonmail.com"
__license__ = "BSD 2-clause"
__url__ = "https://github.com/iw4p/torrentp"

PYPI_SIMPLE_ENDPOINT: str = "https://pypi.org/project/torrentp"

from .torrent_downloader import Torrent_downloader, Session, Downloader, Torrent_info 

__all__ = [
    "Torrent_downloader",
    "Session",
    "Downloader",
    "Torrent_info",
    "PYPI_SIMPLE_ENDPOINT",
]