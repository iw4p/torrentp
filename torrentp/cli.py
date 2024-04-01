from .torrent_downloader import TorrentDownloader
import asyncclick as click
import asyncio

async def handle_input(torrent_file):
    while True:
        action = await asyncio.get_event_loop().run_in_executor(None, input, "Enter action (pause/resume/stop): ")
        if action.lower() == 'pause':
            torrent_file.pause_download()
        elif action.lower() == 'resume':
            torrent_file.resume_download()
        elif action.lower() == 'stop':
            torrent_file.stop_download()
            print("The Program is exiting...")
            raise SystemExit
        else:
            print("Invalid action. Please enter 'pause', 'resume', or 'stop'.")

@click.command()
@click.option('--link', required=True, help="Torrent link. Example: [--link 'file.torrent'] or [--link 'magnet:...']", type=str)
@click.option('--download_speed',  default=0, help='Download speed with a specific number (kB/s). Default: 0, means unlimited speed', type=int)
@click.option('--upload_speed',  default=0, help='Upload speed with a specific number (kB/s). Default: 0, means unlimited speed', type=int)
@click.option('--save_path',  default='.', help="Path to save the file, default: '.' ", type=str)
async def run_cli(link, download_speed, upload_speed, save_path):
    try:
        torrent_file = TorrentDownloader(link, save_path)
        
        input_task = asyncio.create_task(handle_input(torrent_file))
        download_task = asyncio.create_task(torrent_file.start_download(download_speed=download_speed, upload_speed=upload_speed))
        
        await asyncio.gather(input_task, download_task)

    except asyncio.TimeoutError or KeyboardInterrupt:
        print("The Program is terminated manually!")
        raise SystemExit


if __name__ == '__main__':
    run_cli(_anyio_backend="asyncio")
