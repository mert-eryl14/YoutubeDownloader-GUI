# YoutubeDownloader

YoutubeDownloader is a little Project written in Python. It is a GUI wrapper around pytube. It can download Videos with a [Youtube](https://www.youtube.com) Url, manage and store them for you.
Just test it yourself.

## Installation

The Project is build in Python version 3.12.
After you downloaded or cloned the Repo, go into YoutubeDownloader (if you download as zip it's YoutubeDownloader - master) directory.
It is recommended to create a virtual environment like this:

![image](https://github.com/eywa14/YoutubeDownloader/assets/85054971/787a0932-2876-4018-8f52-d9403e932231)

```bash
python -m venv .venv
```

Then activate the virtual environment.

- On Linux/MacOs:
```bash
source .venv/bin/activate
```

- On Windows:
```bash
.venv\Scripts\activate.bat
```
It should look somewhat like this now:

![image](https://github.com/eywa14/YoutubeDownloader/assets/85054971/4751104b-c3dd-4f05-956f-0655a15fb95a)

In the venv now use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

Now you are ready to go and run:
```bash
python run.py
```

Ps.: After usage deactivate the venv like this:
```bash
deactivate
```

## Preview
![image](https://github.com/eywa14/YoutubeDownloader/assets/85054971/d923a2f5-5047-4b12-98ba-d7d3c256a426)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.