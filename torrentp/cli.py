from .torrent_downloader import TorrentDownloader
import asyncclick as click
import asyncio

@click.command()
@click.option('--link', required=True, help="Torrent link. Example: [--link 'file.torrent'] or [--link 'magnet:...']", type=str)
@click.option('--download_speed',  default=0, help='Download speed with a specific number (kB/s). Default: 0, means unlimited speed', type=int)
@click.option('--upload_speed',  default=0, help='Upload speed with a specific number (kB/s). Default: 0, means unlimited speed', type=int)
@click.option('--save_path',  default='.', help="Path to save the file, default: '.' ", type=str)
async def run_cli(link, download_speed, upload_speed, save_path):
    try:
        torrent_file = TorrentDownloader(link, save_path)
        await torrent_file.start_download(download_speed=download_speed, upload_speed=upload_speed)

    except asyncio.TimeoutError or KeyboardInterrupt:
        print("The Program is terminated manually!")
        raise SystemExit


if __name__ == '__main__':
    run_cli(_anyio_backend="asyncio")