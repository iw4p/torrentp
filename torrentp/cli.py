from .torrent_downloader import TorrentDownloader
import asyncclick as click
import asyncio
from pedros import get_logger

_logger = get_logger()

async def handle_input(torrent_file: TorrentDownloader) -> None:
    """Handle user input for download control."""
    while True:
        action = await asyncio.get_event_loop().run_in_executor(None, input, "Enter action (pause/resume/stop): ")
        if action.lower() == 'pause':
            torrent_file.pause_download()
        elif action.lower() == 'resume':
            torrent_file.resume_download()
        elif action.lower() == 'stop':
            torrent_file.stop_download()
            _logger.info("The Program is exiting...")
            raise SystemExit
        else:
            _logger.warning("Invalid action. Please enter 'pause', 'resume', or 'stop'.")

@click.command()
@click.option('--link', required=True, help="Torrent link. Example: [--link 'file.torrent'] or [--link 'magnet:...']", type=str)
@click.option('--download_speed',  default=0, help='Download speed with a specific number (kB/s). Default: 0, means unlimited speed', type=int)
@click.option('--upload_speed',  default=0, help='Upload speed with a specific number (kB/s). Default: 0, means unlimited speed', type=int)
@click.option('--save_path',  default='.', help="Path to save the file, default: '.' ", type=str)
@click.option('--stop_after_download', is_flag=True, help="Stop the download immediately after completion without seeding")
async def run_cli(link: str, download_speed: int, upload_speed: int, save_path: str, stop_after_download: bool) -> None:
    """Main CLI function for torrent downloading."""
    try:
        _logger.info(f"Starting torrent download: {link}")
        torrent_file = TorrentDownloader(link, save_path, stop_after_download=stop_after_download)
        
        input_task = asyncio.create_task(handle_input(torrent_file))
        download_task = asyncio.create_task(torrent_file.start_download(download_speed=download_speed, upload_speed=upload_speed))
        
        await asyncio.gather(input_task, download_task)

    except asyncio.TimeoutError:
        _logger.error("The Program timed out!")
        raise SystemExit
    except KeyboardInterrupt:
        _logger.error("The Program was terminated manually!")
        raise SystemExit
    except Exception as e:
        _logger.error(f"An error occurred: {e}")
        raise SystemExit


if __name__ == '__main__':
    run_cli(_anyio_backend="asyncio")
