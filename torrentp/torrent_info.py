class Torrent_info():
    def __init__(self, path, libtorrent):
        self._path = path
        self._lt = libtorrent
        self._info = None

    def show_info():
        pass

    def create_torrent_info(self):
        self._info = self._lt.torrent_info(self._path)
        return self._info

    def create_add_torrent_params(self):
        self._info = self._lt.parse_magnet_uri(self._path)
        return self._info

    def __str__(self):
        pass

    def __repr__(self):
        pass
    
    def __call__(self):
        if self.path.startsWith('magnet:'):
            return self.create_add_torrent_params()
        else:
            return self.create_torrent_info()