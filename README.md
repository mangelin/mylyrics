### Prerequisite

* python3.x

check requirements folder for all required packages.

### Create virtualenv

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