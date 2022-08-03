import sys
import time

class Downloader():
    def __init__(self, session, torrent_info, save_path):
        self._session = session
        self._torrent_info = torrent_info 
        self._save_path = save_path
        self._file = None
        self._status = None
        self._name = ''
        self._state = ''

    def status(self):
        if self._save_path == None:
            self._save_path = '.'    
        self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})
        self._status = self._file.status()

        return self._status

    @property
    def name(self):
        self._name = self.status().name
        return self._name

    def download(self):
        print(f'Start downloading {self.name}')
        while (not self._status.is_seeding):
            
            s = self.status()

            print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                s.num_peers, s.state), end=' ')
            
            sys.stdout.flush()
            time.sleep(1)

        print(self._status.name, 'downloaded successfully.')        

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass