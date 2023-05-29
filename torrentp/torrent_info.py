class TorrentInfo:
    def __init__(self, path, libtorrent):
        self._path = path
        self._lt = libtorrent
        self._info = self._lt.torrent_info(self._path)

    def show_info(self):
        pass

    def create_torrent_info(self):
        self._info = self._lt.torrent_info(self._path)
        return self._info

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        return self.create_torrent_info()
