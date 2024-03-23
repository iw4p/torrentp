from torrent_downloader import TorrentDownloader
import asyncclick as click
import asyncio
import sys
import os

@click.command()
@click.option('--link', required=True, help='Download with magnet link: magnet:... Or download with .torrent file: test.torrent', type=str)
@click.option('--download_speed',  default=0, help='Download Using 0 (default number) means unlimited speed. Or download with specifc number (kB/s)', type=int)
@click.option('--upload_speed',  default=0, help='Upload Using 0 (default number) means unlimited speed. Or Upload with specifc number (kB/s)', type=int)
@click.option('--save_path',  default='.', help='Path to save the file', type=str)
async def run_cli(link, download_speed, upload_speed, save_path):
    try:
        torrent_file = TorrentDownloader(link, save_path)
        await torrent_file.start_download(download_speed=download_speed, upload_speed=upload_speed)
        sys.stdout.flush()

    except asyncio.TimeoutError or KeyboardInterrupt:
        print("The Program is terminated manually!")
        raise SystemExit


if __name__ == '__main__':
    run_cli(_anyio_backend="asyncio")