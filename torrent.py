import libtorrent as lt

class Session():
    def __init__(self):
        self._user_agent: str = 'python client v0.1'
        self._listen_interfaces: str = '0.0.0.0'
        self._port: int = 6881
        self._download_rate_limit: int = 0
        self._download_rate_limit: int = 0
    
    def create_session(self):
        return lt.session({'listen_interfaces':f'{self._listen_interfaces}:{self._port}'})
        
    def __str__():
        pass

    def __repr__():
        pass

    def __call__(self):
        return create_session(self)


class Torrent_info():
    def __init__(self, path):
        self._path = path
        self._info = lt.torrent_info(self._path)

    def show_info():
        pass

    def create_torrent_info(self, path):
        self._info = lt.torrent_info(path)
        return self._info

    def __str__():
        pass

    def __repr__():
        pass
    
    def __call__(self, path):
        # return lt.torrent_info(self._path)
        return create_torrent_info(self, self._path)

class Downloader():
    def __init__(self):
        pass
        
    def __str__():
        pass

    def __repr__():
        pass

    def __call__(self):
        pass

