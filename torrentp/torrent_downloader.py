from .session import Session
from .torrent_info import TorrentInfo
from .downloader import Downloader
import libtorrent as lt


class TorrentDownloader:
    def __init__(self, file_path, save_path, port=6881, stop_after_download=False):
        self._file_path = file_path
        self._save_path = save_path
        self._port = port  # Default port is 6881
        self._downloader = None
        self._torrent_info = None
        self._lt = lt
        self._file = None
        self._add_torrent_params = None
        self._session = Session(self._lt, port=self._port)  # Pass port to Session
        self._stop_after_download = stop_after_download

    async def start_download(self, download_speed=0, upload_speed=0):
        if self._file_path.startswith('magnet:'):
            self._add_torrent_params = self._lt.parse_magnet_uri(self._file_path)
            self._add_torrent_params.save_path = self._save_path
            self._downloader = Downloader(
                session=self._session(), torrent_info=self._add_torrent_params, 
                save_path=self._save_path, libtorrent=lt, is_magnet=True, stop_after_download=self._stop_after_download
            )

        else:
            self._torrent_info = TorrentInfo(self._file_path, self._lt)
            self._downloader = Downloader(
                session=self._session(), torrent_info=self._torrent_info(), 
                save_path=self._save_path, libtorrent=None, is_magnet=False, stop_after_download=self._stop_after_download
            )

        self._session.set_download_limit(download_speed)
        self._session.set_upload_limit(upload_speed)

        self._file = self._downloader
        await self._file.download()

    def pause_download(self):
        if self._downloader:
            self._downloader.pause()

    def resume_download(self):
        if self._downloader:
            self._downloader.resume()

    def stop_download(self):
        if self._downloader:
            self._downloader.stop()
        if self._session:
            self._session.shutdown()

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass
