from .session import Session
from .torrent_info import Torrent_info
from .downloader import Downloader
import libtorrent as lt

class Torrent_downloader():
    def __init__(self, file_path, save_path):
        self._file_path = file_path
        self._save_path = save_path
        self._lt = lt
        self._session = Session(self._lt)
        

        self._torrent_info = Torrent_info(self._file_path, self._lt)
        self._downloader = Downloader(self._session(), self._torrent_info(), self._save_path)
        self._file = None

    def start_download(self):
        self._file = self._downloader
        self._file.download()

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass