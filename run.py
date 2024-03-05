import subprocess
import sys
import os

from ui.ui import App
from config import dl_path


def run():
    # making directories if not there
    try:
        os.mkdir(f"{dl_path}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{dl_path}\\mp4")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{dl_path}\\mp3")
    except FileExistsError:
        pass

    #  activating app
    app = App()
    app.display_downloads()
    app.initialize_download_details()

    def check_for_restart():
        if app.restart:
            print('restarting...')
            # Get the command used to run the current program
            command = [sys.executable] + sys.argv
            # Spawn a new process with the same command
            subprocess.Popen(command)
            # Close the current process
            sys.exit(0)

        app.after(500, check_for_restart)

    check_for_restart()

    app.mainloop()


if __name__ == '__main__':
    run()
