# TorrentP

##  Wrapped python library for downloading from torrent

[![Torrentp](https://github.com/iw4p/torrentp/raw/master/images/tintin.jpeg
)](https://pypi.org/project/torrentp/)

### Download from torrent with .torrent file or magnet link. With just 3 lines of python code.

[![PyPI version](https://img.shields.io/pypi/v/TorrentP.svg)](https://pypi.org/project/TorrentP)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/TorrentP.svg)](#Installation)
[![Downloads](https://pepy.tech/badge/TorrentP)](https://pepy.tech/project/TorrentP)

### Installation

```sh
$ pip install torrentp
```
Also can be found on [pypi](https://pypi.org/project/torrentp/)

### How can I use it?
  - Install the package by pip package manager.
  - After installing, you can use it and call the library.
  - You have to pass magnet link or torrent file, and a path for saving the file. use . (dot) for saving in current directory.

Download with magnet link:
```python
from torrentp import TorrentDownloader
torrent_file = TorrentDownloader("magnet:...", '.')
torrent_file.start_download()
```
Or download with .torrent file:
```python
from torrentp import TorrentDownloader
torrent_file = TorrentDownloader("test.torrent", '.')
torrent_file.start_download()
```

### To do list
- [ ] User can change the port
- [ ] CLI
- [ ] Pause / Resume

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=iw4p/torrentp&type=Date)](https://star-history.com/#iw4p/torrentp&Date)

### Issues
Feel free to submit issues and enhancement requests or contact me via [vida.page/nima](https://vida.page/nima).

### Contributing
Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Update the Version** inside __init__.py
 4. **Commit** changes to your own branch
 5. **Push** your work back up to your fork
 6. Submit a **Pull request** so that we can review your changes
