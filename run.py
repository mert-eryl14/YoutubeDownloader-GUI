from ui.ui import App


def run():
    app = App()
    app.display_downloads()
    app.initialize_download_details()
    app.mainloop()


if __name__ == '__main__':
    run()
