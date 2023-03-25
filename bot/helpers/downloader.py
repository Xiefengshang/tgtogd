import os
import wget
import glob
import yt_dlp
import asyncio
from pySmartDL import SmartDL
from urllib.error import HTTPError
from bot import DOWNLOAD_DIRECTORY, LOGGER


async def download_file(url, dl_path):
    try:
        dl = SmartDL(url, dl_path, progress_bar=False)
        LOGGER.info(f'Downloading: {url} in {dl_path}')
        dl.start()
        return True, dl.get_dest()
    except HTTPError as error:
        return False, error
    except Exception as error:
        try:
            filename = wget.download(url, dl_path)
            return True, os.path.join(f"{DOWNLOAD_DIRECTORY}/{filename}")
        except HTTPError:
            return False, error
        except FloodWait as e:
            print(f"Waiting for {e.x} seconds...")
            time.sleep(e.x)
            await download_file(url, dl_path)



async def utube_dl(link, path_own):
    ytdl_opts = {
        'outtmpl' : os.path.join(path_own, '%(title)s'),
        'noplaylist' : True,
        'logger': LOGGER,
        'format': 'bestvideo+bestaudio/best',
        'geo-bypass': True,
        'geo_bypass_country': 'TW'
    }
    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
        try:
            meta = ytdl.extract_info(link, download=True)
        except DownloadError as e:
            return False, str(e)
        for path in glob.glob(os.path.join(DOWNLOAD_DIRECTORY, '*')):
            if path.endswith(('.avi', '.mov', '.flv', '.wmv', '.3gp','.mpeg', '.webm', '.mp4', '.mkv')) and \
                path.startswith(ytdl.prepare_filename(meta)):
                return True, path
        return False, 'Something went wrong! No video file exists on server.'

