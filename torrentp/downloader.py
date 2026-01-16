import asyncio
import time

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn
)


class Downloader:
    def __init__(self, session, torrent_info, save_path, libtorrent, is_magnet, stop_after_download=False):
        self._session = session
        self._torrent_info = torrent_info
        self._save_path = save_path
        self._file = None
        self._status = None
        self._name = ''
        self._state = ''
        self._lt = libtorrent
        self._add_torrent_params = None
        self._is_magnet = is_magnet
        self._paused = False
        self._stop_after_download = stop_after_download

    def status(self):
        if not self._is_magnet:
            self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})
            self._status = self._file.status()
        else:
            self._add_torrent_params = self._torrent_info
            self._add_torrent_params.save_path = self._save_path
            self._file = self._session.add_torrent(self._add_torrent_params)
            self._status = self._file.status()
            while (not self._file.has_metadata()):
                time.sleep(1)
        return self._status

    @property
    def name(self):
        self._name = self.status().name
        return self._name

    async def download(self):
        pbar = Progress(
            TextColumn("[bold blue]{task.description}", justify="right"),
            BarColumn(),
            TaskProgressColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            # TextColumn("[orange1]{task.fields[peers]} peers"), # Number of peers
            # TextColumn("[purple]{task.fields[status]}"), # current status
            TimeRemainingColumn(compact=True, elapsed_when_finished=True),
        )

        with pbar:
            status = self.status()
            task_id = pbar.add_task(f"{status.name}", total=status.total_wanted, peers=0, status=status.state)

            while not status.is_seeding:
                if not self._paused:
                    status = self.status()
                    pbar.update(task_id, completed=status.total_done, peers=status.num_peers, status=status.state)

                await asyncio.sleep(1)

        if self._stop_after_download:
            self.stop()

    def pause(self):
        print("Pausing download...")
        if self._file:
            self._file.pause()
            self._paused = True
            print("Download paused successfully.")
        else:
            print("Download file instance not found.")

    def resume(self):
        print("Resuming download...")
        if self._file:
            if self._paused:
                self._file.resume()
                self._paused = False
                print("Download resumed successfully.")
            else:
                print("Download is not paused. No action taken.")
        else:
            print("Download file instance not found.")

    def stop(self):
        print("Stopping download...")
        if self._file:
            self._session.remove_torrent(self._file)
            self._file = None
            print("Download stopped successfully.")
        else:
            print("Download file instance not found.")

    def is_paused(self):
        return self._paused

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass
