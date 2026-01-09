import asyncio
import time
from typing import Optional

import libtorrent as lt
from pedros import get_logger
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn
)

from .torrent_info import TorrentInfo


class TorrentDownloader:
    """
    Main class for downloading torrents with simplified architecture.
    
    This class handles both magnet links and .torrent files, providing
    download, pause, resume, and stop functionality in a single unified interface.
    """

    def __init__(self, file_path: str, save_path: str, port: int = 6881, stop_after_download: bool = False):
        """
        Initialize the TorrentDownloader.
        
        Args:
            file_path: Path to .torrent file or magnet link
            save_path: Directory to save downloaded files
            port: Port for torrent session (default: 6881)
            stop_after_download: Whether to stop after download completes (default: False)
        """
        self._logger = get_logger()
        self._file_path = file_path
        self._save_path = save_path
        self._port = port
        self._stop_after_download = stop_after_download

        self._lt = lt
        self._session: Optional[lt.session] = None
        self._torrent_handle: Optional[lt.torrent_handle] = None
        self._torrent_info: Optional[TorrentInfo] = None
        self._add_torrent_params: Optional[lt.add_torrent_params] = None
        self._is_magnet: bool = False
        self._paused: bool = False

        self._initialize_session()

    def _initialize_session(self) -> None:
        """Initialize the libtorrent session."""
        try:
            self._session = self._lt.session({
                'listen_interfaces': f'0.0.0.0:{self._port}'
            })
            self._logger.debug(f"Session initialized on port {self._port}")
        except Exception as e:
            self._logger.error(f"Failed to initialize session: {e}")
            raise

    def _setup_torrent(self) -> None:
        """Set up torrent based on file path (magnet or .torrent file)."""
        try:
            if self._file_path.startswith('magnet:'):
                self._is_magnet = True
                self._add_torrent_params = self._lt.parse_magnet_uri(self._file_path)
                self._add_torrent_params.save_path = self._save_path
                self._logger.debug("Magnet link parsed successfully")
            else:
                self._is_magnet = False
                self._torrent_info = TorrentInfo(self._file_path, self._lt)
                self._logger.debug(f"Torrent file loaded: {self._torrent_info.name}")
        except Exception as e:
            self._logger.error(f"Failed to setup torrent: {e}")
            # raise

    def _add_torrent_to_session(self) -> lt.torrent_handle:
        """Add torrent to the session and return the handle."""
        try:
            if not self._is_magnet:
                self._torrent_handle = self._session.add_torrent({
                    'ti': self._torrent_info.get_info(),
                    'save_path': self._save_path
                })
            else:
                self._torrent_handle = self._session.add_torrent(self._add_torrent_params)
                while not self._torrent_handle.has_metadata():
                    time.sleep(1)

            self._logger.debug(f"Torrent added to session: {self._torrent_handle.name()}")
            return self._torrent_handle
        except Exception as e:
            self._logger.error(f"Failed to add torrent to session: {e}")
            # raise

    def set_speed_limits(self, download_speed: int = 0, upload_speed: int = 0) -> None:
        """Set download and upload speed limits.
        
        Args:
            download_speed: Download speed limit in kB/s (0 = unlimited)
            upload_speed: Upload speed limit in kB/s (0 = unlimited)
        """
        try:
            download_limit = int(-1 if download_speed == 0 else (1 if download_speed == -1 else download_speed * 1024))
            upload_limit = int(-1 if upload_speed == 0 else (1 if upload_speed == -1 else upload_speed * 1024))

            self._session.set_download_rate_limit(download_limit)
            self._session.set_upload_rate_limit(upload_limit)

            self._logger.debug(f"Speed limits set: download={download_speed}kB/s, upload={upload_speed}kB/s")
        except Exception as e:
            self._logger.error(f"Failed to set speed limits: {e}")
            raise

    async def start_download(self, download_speed: int = 0, upload_speed: int = 0) -> None:
        """Start the torrent download.
        
        Args:
            download_speed: Download speed limit in kB/s (0 = unlimited)
            upload_speed: Upload speed limit in kB/s (0 = unlimited)
        """
        try:
            self._setup_torrent()
            self._add_torrent_to_session()
            self.set_speed_limits(download_speed, upload_speed)
            await self._download_with_progress()

        except Exception as e:
            self._logger.error(f"Download failed: {e}")
            # raise

    async def _download_with_progress(self) -> None:
        """Download with progress bar using Rich library."""
        try:
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

                status = self._torrent_handle.status()
                task_id = progress.add_task(
                    "download",
                    filename=status.name,
                    total=status.total_wanted,
                    peers=0,
                    status="initializing"
                )

                while not status.is_seeding:
                    if not self._paused:
                        status = self._torrent_handle.status()
                        progress.update(
                            task_id,
                            completed=status.total_done,
                            peers=status.num_peers,
                            status=str(status.state),
                            refresh=True
                        )

                    await asyncio.sleep(1)

                self._logger.debug(f"Download completed: {status.name}")

                if self._stop_after_download:
                    self.stop_download()

        except Exception as e:
            self._logger.error(f"Progress tracking failed: {e}")
            # raise

    def pause_download(self) -> None:
        """Pause the current download."""
        try:
            if self._torrent_handle:
                self._torrent_handle.pause()
                self._paused = True
                self._logger.debug("Download paused successfully")
            else:
                self._logger.warning("No active download to pause")
        except Exception as e:
            self._logger.error(f"Failed to pause download: {e}")
            raise

    def resume_download(self) -> None:
        """Resume a paused download."""
        try:
            if self._torrent_handle:
                if self._paused:
                    self._torrent_handle.resume()
                    self._paused = False
                    self._logger.debug("Download resumed successfully")
                else:
                    self._logger.debug("Download is not paused, no action needed")
            else:
                self._logger.warning("No active download to resume")
        except Exception as e:
            self._logger.error(f"Failed to resume download: {e}")
            # raise

    def stop_download(self) -> None:
        """Stop the current download and cleanup."""
        try:
            if self._torrent_handle:
                self._session.remove_torrent(self._torrent_handle)
                self._torrent_handle = None
                self._logger.info("Download stopped successfully")

            self.shutdown_session()
        except Exception as e:
            self._logger.error(f"Failed to stop download: {e}")
            raise

    def shutdown_session(self) -> None:
        """Shutdown the torrent session."""
        try:
            if self._session:
                self._session.pause()
                del self._session
                self._session = None
                self._logger.debug("Session shutdown successfully")
        except Exception as e:
            self._logger.error(f"Failed to shutdown session: {e}")
            # raise

    @property
    def name(self) -> str:
        """Get the name of the torrent.
        
        Returns:
            Name of the torrent or empty string if not available
        """
        if self._torrent_handle:
            return self._torrent_handle.status().name
        elif self._torrent_info:
            return self._torrent_info.name or ""
        return ""

    def __str__(self) -> str:
        """String representation of the TorrentDownloader."""
        return f"TorrentDownloader(file_path='{self._file_path}', save_path='{self._save_path}')"

    def __repr__(self) -> str:
        """Detailed representation of the TorrentDownloader."""
        return (f"TorrentDownloader(file_path='{self._file_path}', save_path='{self._save_path}', "
                f"port={self._port}, stop_after_download={self._stop_after_download})")
