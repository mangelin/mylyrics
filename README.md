[![build and test](https://github.com/mangelin/mylyrics/actions/workflows/build.yml/badge.svg)]
[![codecov](https://codecov.io/gh/mangelin/mylyrics/branch/main/graph/badge.svg?token=UK2LPV47KB)](https://codecov.io/gh/mangelin/mylyrics)


# MyLyrics

Welcome to `mylyrics` a simple Command Line Interface (CLI) to download lyrics of your preferred songs.

`mylyrics` is able to download lyrics from different provider (check the below paragraph to know witch providers are actually supported).

### Quickstart

To check and show on standard output the lyrics of `Mint car` by `The Cure` open a terminal and type the following commands:

```
$ python mylyrics.py -a "cure" -l "Mint car" -p ezlyrics
```

you can also save your song locally using the `-s` flag, as shown
in the following example:

```
$ python mylyrics.py -a "cure" -l "Mint car" -p ezlyrics -s
```

by default all songs are saved in the a `provider/artist` directory in `txt` format. You can change base directory setting the environment variable `DEFAULT_SAVE_DIRECTORY` (default is current dir).

The `-h` flag show you all the available options:

```
$ python mylyrics.py -h
```

### Environment

You can customize environment variables for the followings value:

* Providers base and search url
* Output format (currently sonly txt file format is supported)
* Default save directory.

#### Providers variables

* AZLYRICS_BASE_URL
* ELYRICS_BASE_URL
* AZLYRICS_SEARCH_URL
* ELYRICS_SEARCH_URL

#### Output format

* DEFAULT_OUTPUT_FORMAT

#### Default save directory

* DEFAULT_SAVE_DIRECTORY

## Installation

### Prerequisite

* python3.x
* python-dotenv
* requests
* python-slugify

in order to running unit tests, you need the following other modules:

* pytest
* coverage
* Faker

For the specific version of every single packages, check the requirements folder.
### Create virtualenv

The better choice to test the package is to use a virtualenv.

Check [https://virtualenv.pypa.io/en/latest/] to know how to install virtualenv on your OS.

On Linux you can use the following commands to setup a virtualenv for python3:

```
$ virtualenv -p=python3 py3
$ source py3/bin/activate
```

### installing depencencies

Dependencies required to run the command:

```
$ pip install -r requirements/base.txt
```

Dependencies required to run unit tests:

```
$ pip install -r requirements/test.txt
```

### Running unit tests

```
$ coverage run -m pytest
```

to check code coverage, type the following command:

```
$ coverage html
```

and open with your preferred browser "htmlcov/index.html"

## Add more providers

In order to add e new provider you need to follow this steps:

* create a provider implementing AbstractLyricsRetriverProxy interface
* register the provider in config module
* that's all

### Create a provider implementing AbstractLyricsRetriverProxy interface

Open the project folder with your preferred editor and add a new file in proxy 
module folder:

```bash
$ cd proxy
$ touch .myAwesomeProxy.py
```

edit `myAwesomeProxy,py` and create a concrete class that implements 
AbstractLyricsRetriverProxy interface.

```python
from bs4 import BeautifulSoup as bs
import requests, re
import config

from .abstractLyrics import AbstractLyricsRetriverProxy
from .helpers import helper_retrive_url

# AzLyrics.com proxy
class Myawesomeproxy(AbstractLyricsRetriverProxy):
    def __init__(self):
        super().__init__()

        self._name = config.MY_AWESOME_PROXY
        self._az_search_url = config.MY_AWESOME_PROXY_SEARCH_URL

    """
    Return the absolute url for the artist page
    Args:
        artist  name of the artist
    
    Return:
        a string apresenting a url
    """
    def get_artist_page_url(self, artist:str)->str:
        """
        your code
        """

    """
    Return the absolute url for the song song_name
    Args:
        artist_page_url  a string rapresenting the artist url page
        song_name        the song name
    
    Return:
        a string apresenting a url
    """
    def get_lyrics_url(self, artist_page_url:str, song_name:str)->str:
        """
        your code
        """

    """
        retrun the content of the lyrics_url
        Args:
            lyrics_url  a string, the url to retrive the song
    """
    def fetch_lyric_content(self, lyrics_url:str)->str:
        return helper_retrive_url(lyrics_url) # pragma: no cover

    """
        Tranform the lyrics in txt
        Args:
            lyrics  some encoded object rapresenting the lyrics

        Return:
            the lyrics in txt format
    """
    def to_txt(self, lyrics)->str:
        """
        your code
        """
```

`NOTE` : class name must be a capitalized string.

### Registering the new provider

To register a new provider so that can be available for user, you have to
add some code in `config` module. Open `config/.__init__.py` file with your
preferred editor and add the followig line in the `USER CONFIG` section:

```python

MY_AWESOME_PROXY_SEARCH_URL="http//myawesonproxy.org/q="
MY_AWESOME_PROXY="MyAwesomeProxy"
register_provider(MY_AWESOME_PROXY)
```
