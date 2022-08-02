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
        
    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        return self.create_session()


class Torrent_info():
    def __init__(self, path):
        self._path = path
        self._info = lt.torrent_info(self._path)

    def show_info():
        pass

    def create_torrent_info(self):
        self._info = lt.torrent_info(self._path)
        return self._info

    def __str__(self):
        pass

    def __repr__(self):
        pass
    
    def __call__(self):
        # return lt.torrent_info(self._path)
        return self.create_torrent_info()

class Downloader():
    def __init__(self, session: Session, torrent_info: Torrent_info, save_path):
        self._session = session 
        self._torrent_info = torrent_info 
        self._save_path = save_path
        self._file = None
        self._status = None

    # def create_downloadable_file(self):
    #     self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})
    #     return self._file.status()

    def status(self):
        if self._save_path == None:
            self._save_path = '.'

        self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})

        return self._file.status()

    def get_name(self):
        return self.status().name

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass

session1 = Session()

t_info = Torrent_info('test.torrent')
print(t_info())

downloader = Downloader(session1(), t_info(), '.')

print(downloader.get_name())