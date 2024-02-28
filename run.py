import subprocess
import sys

from ui.ui import App


def run():
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
