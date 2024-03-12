from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

from typing import Literal

from utils.helpers import length_in_minutes
from ui.ui import CTkProgressBar
from config import mp4_output_folder, mp3_output_folder


class YoutubeDownloader:

    def __init__(self, url: str, progressbar: CTkProgressBar):
        self.yt = YouTube(url=url, on_progress_callback=self.on_progress)
        self.progressbar = progressbar

        self.mp4_stream = self.yt.streams.get_highest_resolution()
        self.mp3_stream = self.yt.streams.filter(only_audio=True).first()

        self.url = url
        self.title = self.yt.title
        self.thumbnail = self.yt.thumbnail_url
        self.author = self.yt.author
        self.size_mp4 = self.mp4_stream.filesize_mb
        self.size_mp3 = self.mp3_stream.filesize_mb
        self.length = length_in_minutes(self.yt.length)

    def download_stream(self, dl_type: Literal['mp4', 'mp3']):
        try:
            if dl_type == 'mp4':
                self.mp4_stream.download(filename=f"{self.title}.mp4", output_path=mp4_output_folder)
            else:
                self.mp3_stream.download(filename=f"{self.title}.mp3", output_path=mp3_output_folder)
        except VideoUnavailable:
            raise VideoUnavailable
        except RegexMatchError:
            raise RegexMatchError
        except OSError:
            raise OSError

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        perc_in_dec = bytes_downloaded / total_size
        self.progressbar.set(perc_in_dec)
        self.progressbar.update()
