# MyLyrics

Welcome to `mylyrics` a simple Command Line Interface (CLI) to download lyrics of your preferred songs.

`mylyrics` is able to download lyrics from different provider (check the followind paragraph to know witch providers are actually supported).

### Simple usage

To check and show on standard output the lyrics of `Mint car` by `The Cure` open a terminal and type the following commands:

```
$ python mylyrics.py -a "cure" -l "Mint car" -p ezlyrics
```

you can also save your song locally using the `-s` flag, as shown
in the following example:

```
$ python mylyrics.py -a "cure" -l "Mint car" -p ezlyrics
```

by default all songs are saved in the a `provider/artist` directory in `txt` format. You can change base directory setting the environment variable `DEFAULT_SAVE_DIRECTORY` (default is current dir).

The `-h` flag show you all the available options:

```
$ python mylyrics.py -h
```

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

```
$ pip install -r requirements
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