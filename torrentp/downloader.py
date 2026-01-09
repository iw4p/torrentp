import asyncio
import time

from pedros import get_logger
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn
)


class Downloader:
    def __init__(self, session, torrent_info, save_path, libtorrent, is_magnet, stop_after_download=False,
                 progress: bool = True):
        self._logger = get_logger()
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
        self._progress = progress

    def status(self):
        if not self._is_magnet:
            self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})
            self._status = self._file.status()
        else:
            self._add_torrent_params = self._torrent_info
            self._add_torrent_params.save_path = self._save_path
            self._file = self._session.add_torrent(self._add_torrent_params)
            self._status = self._file.status()
            while not self._file.has_metadata():
                time.sleep(1)
        return self._status

    @property
    def name(self):
        self._name = self.status().name
        return self._name

    async def download(self):
        with Progress(
                TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                BarColumn(bar_width=None),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "•",
                DownloadColumn(),
                "•",
                TransferSpeedColumn(),
                "•",
                TextColumn("[orange1]peers: {task.fields[peers]}"),
                "•",
                TextColumn("[yellow]{task.fields[status]}"),
                "•",
                TimeRemainingColumn()
        ) as progress:

            s = self.status()
            task_id = progress.add_task(
                "download",
                filename=self.name,
                total=s.total_wanted,
                peers=0,
                status="initializing"
            )

            while not s.is_seeding:
                if not self._paused:
                    s = self.status()
                    progress.update(
                        task_id,
                        completed=s.total_done,
                        peers=s.num_peers,
                        status=str(s.state),
                        refresh=True
                    )

                await asyncio.sleep(1)

        if self._stop_after_download:
            self.stop()

    def pause(self):
        self._logger.info("Pausing download...")
        if self._file:
            self._file.pause()
            self._paused = True
            self._logger.info("Download paused successfully.")
        else:
            self._logger.warning("Download file instance not found.")

    def resume(self):
        self._logger.info("Resuming download...")
        if self._file:
            if self._paused:
                self._file.resume()
                self._paused = False
                self._logger.info("Download resumed successfully.")
            else:
                self._logger.info("Download is not paused. No action taken.")
        else:
            self._logger.warning("Download file instance not found.")

    def stop(self):
        self._logger.info("Stopping download...")
        if self._file:
            self._session.remove_torrent(self._file)
            self._file = None
            self._logger.info("Download stopped successfully.")
        else:
            self._logger.warning("Download file instance not found.")

    def is_paused(self):
        return self._paused

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass
