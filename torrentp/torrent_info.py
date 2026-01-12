from dataclasses import dataclass
from typing import Optional
import libtorrent as lt


@dataclass
class TorrentInfo:
    """
    Dataclass for storing torrent information.
    
    Attributes:
        path: Path to the torrent file
        libtorrent: libtorrent module instance
        info: Parsed torrent info (optional)
        name: Name of the torrent (optional)
        size: Size of the torrent in bytes (optional)
        files: List of files in the torrent (optional)
    """
    path: str
    libtorrent: type[lt]
    info: Optional[lt.torrent_info] = None
    name: Optional[str] = None
    size: Optional[int] = None
    files: Optional[list] = None

    def __post_init__(self):
        """Initialize torrent info after dataclass creation."""
        self.load_torrent_info()

    def load_torrent_info(self) -> None:
        """Load and parse torrent information."""
        try:
            self.info = self.libtorrent.torrent_info(self.path)
            if self.info:
                self.name = self.info.name()
                self.size = self.info.total_size()
                self.files = [file.path for file in self.info.files()]
        except Exception as e:
            raise ValueError(f"Failed to load torrent info: {e}")
    
    def get_info(self) -> lt.torrent_info:
        """Get the parsed torrent info.
        
        Returns:
            Parsed torrent info object
            
        Raises:
            ValueError: If torrent info is not loaded
        """
        if not self.info:
            self.load_torrent_info()
        return self.info
    
    def __str__(self) -> str:
        """String representation of torrent info."""
        return f"TorrentInfo(name='{self.name}', size={self.size}, files={len(self.files) if self.files else 0})"
    
    def __repr__(self) -> str:
        """Detailed representation of torrent info."""
        return (f"TorrentInfo(path='{self.path}', name='{self.name}', "
                f"size={self.size}, files={len(self.files) if self.files else 0})")
