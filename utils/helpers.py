from PIL import Image
from customtkinter import CTkImage

import os
from io import BytesIO
import urllib.request
import webbrowser

from config import dl_path


def length_in_minutes(video_length: int) -> float:
    """
    :param video_length: The length of a video in seconds
    :return: The video length in minutes
    """
    return video_length / 60


def get_all_downloads_in_dir(path: str) -> list:
    """
    :param path: The path of the downloads folder
    :return: A list of all the .mp4 and .mp3 files in the downloads folder
    """
    all_downloads_in_dir = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            if name.endswith('.mp4') or name.endswith('.mp3'):
                all_downloads_in_dir.append(os.path.join(path, name))
    print(f"All Downloads: {all_downloads_in_dir}")
    return all_downloads_in_dir


def create_image_from_url(img_url: str, output_size: tuple[int, int] = (200, 200)) -> CTkImage:
    """
    :param img_url: The image url
    :param output_size: The size of the final image, the default size = 200x200px
    :return: A CTkImage by the url and with the given size
    """
    with urllib.request.urlopen(img_url) as url:
        raw_data = url.read()
    img = CTkImage(light_image=Image.open(BytesIO(raw_data)), dark_image=Image.open(BytesIO(raw_data)), size=output_size)
    return img


def find(name: str, path: str) -> str | bytes:
    """
    :param name: The name of file
    :param path: The path of the directory the file is in
    :return: The absolute path to file
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def open_download(v_title: str) -> None:
    """
    It opens a file in the default media player by the video title.
    :param v_title: The video title
    :return: None
    """
    file_path = find(v_title, dl_path)
    os.startfile(file_path)
    print(f"Opened File: <{file_path}>")


def open_url_in_browser(url: str) -> None:
    """
    It opens a given url in the default browser.
    :param url: Url to open
    :return: None
    """
    webbrowser.open(url=url, new=0, autoraise=True)
