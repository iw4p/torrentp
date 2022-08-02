import libtorrent as lt
import sys
import time

class Session():
    def __init__(self):
        self._user_agent: str = 'python client v0.1'
        self._listen_interfaces: str = '0.0.0.0'
        self._port: int = '6881'
        self._download_rate_limit: int = 0
        self._download_rate_limit: int = 0
    
    def create_session(self):
        return lt.session({'listen_interfaces': '0.0.0.0:6881'})
        # return lt.session({'listen_interfaces':f'{self._listen_interfaces}:{self._port}'})
        
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
        self._name = ''
        self._statistics = {'progress': 0, 'download_rate': 0, 'upload_rate': 0, 'num_peers': 0}
        self._state = ''


    def status(self):
        if self._save_path == None:
            self._save_path = '.'
        print(self._torrent_info)
        self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})
        self._status = self._file.status()

        return self._status

    @property
    def name(self):
        self._name = self.status().name
        return self._name

    def start_download(self):
        while (not self._status.is_seeding):
            s = self.status()
            self._statistics['progress'] = s.progress
            self._statistics['download_rate'] = s.download_rate
            self._statistics['upload_rate'] = s.upload_rate
            self._statistics['num_peers'] = s.num_peers
            self._statistics['state'] = s.state

            print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                s.num_peers, s.state), end=' ')
            
            # alerts = self._session.pop_alerts()
            # for a in alerts:
            #     if a.category() & lt.alert.category_t.error_notification:
            #         print(a)

            # sys.stdout.flush()

            time.sleep(1)

        print(self._status.name, 'downloaded successfully.')        

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass

session1 = Session()

t_info = Torrent_info('./4FBB8AB86F4E3A9F6B76F824CAA25C9F93C58125.torrent')
print(t_info())

downloadable_file = Downloader(session1(), t_info(), '.')

print(downloadable_file.name)
downloadable_file.start_download()

