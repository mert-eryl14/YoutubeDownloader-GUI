from PIL import Image
from customtkinter import CTkImage

import os
from io import BytesIO
import urllib.request
import webbrowser

from config import dl_path


def length_in_minutes(video_length: int) -> float:
    return video_length / 60


def get_all_downloads_in_dir(path) -> list:
    all_downloads_in_dir = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            all_downloads_in_dir.append(os.path.join(path, name))
    print(f'All Downloads: {all_downloads_in_dir}')
    return all_downloads_in_dir


def create_image_from_url(img_url, output_size: tuple[int, int] = (200, 200)) -> CTkImage:
    with urllib.request.urlopen(img_url) as url:
        raw_data = url.read()
    img = CTkImage(light_image=Image.open(BytesIO(raw_data)), dark_image=Image.open(BytesIO(raw_data)), size=output_size)
    return img


def find(name, path) -> str | bytes:
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def open_download(v_title) -> None:
    file_path = find(v_title, dl_path)
    os.startfile(file_path)
    print(f'Opened File: <{file_path}>')


def open_url_in_browser(url) -> None:
    webbrowser.open(url=url, new=0, autoraise=True)
