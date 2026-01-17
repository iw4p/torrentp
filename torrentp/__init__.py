"""
torrentp.

A great wrapped library for downloading from torrent.
"""
import logging

from pedros import setup_logging

from .downloader import Downloader
from .session import Session
from .torrent_downloader import TorrentDownloader
from .torrent_info import TorrentInfo

setup_logging(level=logging.WARNING)

__version__ = "0.2.6"
__author__ = 'Nima Akbarzade'
__author_email__ = "iw4p@protonmail.com"
__license__ = "BSD 2-clause"
__url__ = "https://github.com/iw4p/torrentp"

PYPI_SIMPLE_ENDPOINT: str = "https://pypi.org/project/torrentp"

__all__ = [
    "TorrentDownloader",
    "Session",
    "Downloader",
    "TorrentInfo",
    "PYPI_SIMPLE_ENDPOINT",
]
