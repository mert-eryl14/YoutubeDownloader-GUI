with open('dl_path.txt') as file:
    dl_path = file.read()
mp4_output_folder = f"{dl_path}\\mp4"
mp3_output_folder = f"{dl_path}\\mp3"


def change_dl_path(new_dl_path) -> None:
    with open('dl_path.txt', 'w') as txt_file:
        txt_file.write(new_dl_path)
