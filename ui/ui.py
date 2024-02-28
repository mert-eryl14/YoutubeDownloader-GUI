from customtkinter import *

from db.db import DbManager
from youtube.youtube import YoutubeDownloader, VideoUnavailable, RegexMatchError, YouTube
from utils.helpers import create_image_from_url, get_all_downloads_in_dir, find, open_download, open_url_in_browser

DL_PATH = './downloads'


class URLFrame(CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        url_label = CTkLabel(self, text='Youtube URL:', font=('Georgia', 15, 'bold'))
        url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = CTkEntry(self, placeholder_text='Please input the url here!', width=300, height=20)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        self.mp3_or_4 = CTkComboBox(self, values=['mp3', 'mp4'], width=300, height=20, dropdown_hover_color='blue', state='readonly')
        self.mp3_or_4.set('mp4')
        self.mp3_or_4.grid(row=1, column=1, padx=10, pady=10)

        self.error_label = CTkLabel(self, text='Errors:', text_color='red')
        self.error_label.grid(row=2, column=0, padx=10, pady=10)

        download_button = CTkButton(self, text='Download', width=300, height=50, command=master.download_video)
        download_button.grid(row=2, column=1, padx=10, pady=10)


class DownloadDetailsFrame(CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        details_label = CTkLabel(self, text='Download Details:', font=('Georgia', 15, 'bold'))
        details_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.download_progress = CTkProgressBar(self, border_color='black', progress_color='blue', border_width=2, width=300, height=20)
        self.download_progress.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')
        self.download_progress.set(0)


class DownloadsFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        downloads_label = CTkLabel(self, text='All Downloads:', font=('Georgia', 15, 'bold'))
        downloads_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)


class Settings(CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        setting_label = CTkLabel(self, text='Settings', font=('Georgia', 15, 'bold'))
        setting_label.grid(row=0, column=0, padx=5, pady=5)

        self.appearance_switch = CTkSwitch(self, text='Switch appearance mode', command=master.change_appearance_mode)
        self.appearance_switch.grid(row=1, column=0, padx=5, pady=5)


class App(CTk):

    def __init__(self):
        super().__init__()

        self.db = DbManager()

        # some variables and settings
        self.mode = 'dark'
        set_appearance_mode(self.mode)
        self.all_downloads_in_dir = []
        self.last_url = ''
        self.text_update_index = 0

        # creating the window
        self.geometry('900x520')
        self.title('Youtube Downloader')
        self.configure(fg_color=('gray99', 'gray21'))

        # setup grid to be responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.url_frame = URLFrame(master=self, border_width=0, width=420, height=160)
        self.grid_propagate(False)
        self.url_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nw')

        self.settings_frame = Settings(master=self, border_width=0, width=200, height=160)
        self.settings_frame.grid_propagate(False)
        self.settings_frame.grid(row=0, column=1, padx=20, pady=10, sticky='nw')

        self.download_frame = DownloadsFrame(self, border_width=0, width=425, height=303)
        self.grid_propagate(False)
        self.download_frame.grid(row=1, column=0, padx=20, pady=10, sticky='nw')

        self.details_frame = DownloadDetailsFrame(master=self, border_width=0, width=400, height=316)
        self.details_frame.grid_propagate(False)
        self.details_frame.grid(row=1, column=1, padx=20, pady=10, sticky='nw')

        self.toplevel = None

    def change_appearance_mode(self) -> None:

        if self.mode == 'dark':
            set_appearance_mode('light')
            self.mode = 'light'
        else:
            set_appearance_mode('dark')
            self.mode = 'dark'
        print(f'appearance mode changed to {self.mode}')

    def initialize_download_details(self) -> None:
        url = self.url_frame.url_entry.get()
        print('checking details for url')
        if not url == self.last_url:
            self.last_url = ''
            if url:
                self.last_url = url
                try:
                    yt = YouTube(url=url)

                    title_label = CTkLabel(self.details_frame, text=f'{yt.title}', font=('Arial', 20, 'bold'))
                    title_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

                    img = create_image_from_url(yt.thumbnail_url)
                    img_label = CTkLabel(self.details_frame, image=img, text='')
                    img_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')

                    self.update_text_movement(yt.title)
                    print(f'Found valid url: {url}')
                except VideoUnavailable:
                    self.destroy_detail_children()
                    print(f'not available: {url}')
                except RegexMatchError:
                    self.destroy_detail_children()
                    print(f'not a valid url: {url}')
            else:
                self.destroy_detail_children()
        self.after(1500, func=self.initialize_download_details)

    def update_text_movement(self, text) -> None:
        double = f'<{text}> <{text}>'
        display = double[self.text_update_index:self.text_update_index+25]
        try:
            self.details_frame.winfo_children()[2].configure(text=display)
        except IndexError:
            return

        self.text_update_index += 1
        if self.text_update_index >= len(double) // 2:
            self.text_update_index = 0

        self.after(200, func=lambda t=text: self.update_text_movement(text=t))

    def destroy_detail_children(self) -> None:
        children = self.details_frame.winfo_children()
        try:
            children[2].destroy()
        except IndexError:
            pass
        try:
            children[3].destroy()
        except IndexError:
            pass

    def download_video(self) -> None:
        # Get the variables and reset errors and progress bar

        url_entry = self.url_frame.url_entry
        url = url_entry.get()

        error_label = self.url_frame.error_label
        error_label.configure(text='Errors:')

        self.details_frame.download_progress.set(0)

        # download process, checking for errors
        if url:
            try:
                mp3_or_mp4 = self.url_frame.mp3_or_4.get()
                yt = YoutubeDownloader(url=url)
                if mp3_or_mp4 == 'mp4':
                    yt.download_stream('mp4')
                    self.db.add_video(
                        url=yt.url,
                        title=yt.title,
                        thumbnail=yt.thumbnail,
                        author=yt.author,
                        size=yt.size_mp4,
                        length=yt.length,
                        v_type='mp4'
                    )
                else:
                    yt.download_stream('mp3')
                    self.db.add_video(
                        url=yt.url,
                        title=yt.title,
                        thumbnail=yt.thumbnail,
                        author=yt.author,
                        size=yt.size_mp3,
                        length=yt.length,
                        v_type='mp3'
                    )
            except VideoUnavailable:
                error_label.configure(text=f'{error_label.cget('text')}\nVideo is currently unavailable.')
            except RegexMatchError:
                error_label.configure(text=f'{error_label.cget('text')}\nThis is not a valid url.')
            except OSError:
                error_label.configure(text=f'{error_label.cget('text')}\n'
                                           f'Could not download\n'
                                           f'video,because of \n'
                                           f'special character.\n'
                                           f'like "|", "\\" or "?"')
            else:
                self.details_frame.download_progress.set(100)
                self.display_downloads()
            finally:
                url_entry.delete(0, END)
        else:
            error_label.configure(text=f'{error_label.cget('text')}\nNo URL provided!')

    def display_downloads(self) -> None:
        for widget in self.download_frame.winfo_children():
            widget.destroy()

        all_downloads_in_dir = get_all_downloads_in_dir(DL_PATH)

        downloads_label = CTkLabel(self.download_frame, text='All Downloads:', font=('Georgia', 15, 'bold'))
        downloads_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        refresh_button = CTkButton(self.download_frame, text='Refresh', fg_color='green', command=self.display_downloads, hover_color='darkgreen')
        refresh_button.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        for idx, download in enumerate(all_downloads_in_dir):
            download_title = download.split('\\')[-1]
            button = CTkButton(self.download_frame, text=download_title, command=lambda t=download_title: self.download_details(title=t))
            button.grid(row=idx+2, column=0, columnspan=2, padx=5, pady=5, sticky='w')

        self.db.update_db(all_downloads_in_dir)

        print('downloads updated and displayed!')

    def download_details(self, title):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            video = self.db.get_video_by_title(title)
            print(f'Opened detail for: {video}')

            self.toplevel = CTkToplevel()
            self.toplevel.geometry('700x300')
            self.toplevel.title(f'{video.title}')
            self.configure(fg_color=('gray99', 'gray21'))

            label_header_font = CTkFont(family='Arial', size=14, weight='bold', underline=True)
            label_body_font = CTkFont(family='Arial', size=12, weight='normal')

            url_label = CTkLabel(self.toplevel, text='Video Url:', font=label_header_font)
            url_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
            video_url = CTkButton(self.toplevel, text=f'{video.url}', text_color='blue', fg_color=('grey92', 'gray14'),
                                  hover_color=('grey92', 'gray14'),
                                  command=lambda u=video.url: open_url_in_browser(url=u),
                                  font=CTkFont(family='Arial', size=11, weight='normal', underline=True))
            video_url.grid(row=0, column=1, padx=5, pady=5, sticky='w')

            img = create_image_from_url(video.thumbnail)
            thumbnail_label = CTkLabel(self.toplevel, text='', image=img)
            thumbnail_label.grid(row=0, column=2, rowspan=6, padx=5, pady=5)

            title_label = CTkLabel(self.toplevel, text='Video Title:', font=label_header_font)
            title_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
            video_title = CTkLabel(self.toplevel, text=f'{video.title[:-4:]}', font=label_body_font)
            video_title.grid(row=1, column=1, padx=5, pady=5, sticky='w')

            author_label = CTkLabel(self.toplevel, text='Video Author:', font=label_header_font)
            author_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
            video_author = CTkLabel(self.toplevel, text=f'{video.author}', font=label_body_font)
            video_author.grid(row=2, column=1, padx=5, pady=5, sticky='w')

            size_label = CTkLabel(self.toplevel, text='Video Size:', font=label_header_font)
            size_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
            video_size = CTkLabel(self.toplevel, text=f'{video.size} mb', font=label_body_font)
            video_size.grid(row=3, column=1, padx=5, pady=5, sticky='w')

            length_label = CTkLabel(self.toplevel, text='Video Length:', font=label_header_font)
            length_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
            video_length = CTkLabel(self.toplevel, text=f'{round(video.length)} m', font=label_body_font)
            video_length.grid(row=4, column=1, padx=5, pady=5, sticky='w')

            type_label = CTkLabel(self.toplevel, text='Video Type:', font=label_header_font)
            type_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
            video_type = CTkLabel(self.toplevel, text=f'{video.type}', font=label_body_font)
            video_type.grid(row=5, column=1, padx=5, pady=5, sticky='w')

            open_button = CTkButton(self.toplevel, text='Open', command=lambda t=video.title: open_download(v_title=t))
            open_button.grid(row=6, column=0, padx=5, pady=5, sticky='w')

            delete_button = CTkButton(self.toplevel, text='Delete', fg_color='red', hover_color='darkred', command=lambda v=video: self.delete_download(video=v))
            delete_button.grid(row=6, column=1, padx=5, pady=5, sticky='w')

            self.after(100, lambda: self.toplevel.focus())
        else:
            self.toplevel.focus()

    def delete_download(self, video) -> None:
        file_path = find(video.title, './downloads')
        os.remove(file_path)
        self.db.delete_video(video)
        print(f'Deleted File: <{file_path}>')
        self.toplevel.destroy()
        self.display_downloads()
