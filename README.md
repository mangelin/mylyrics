### Build Image

```
docker-compose -f local.yml build
```

### Running unit tests

```
docker-compose -f local.yml run --rm mylyrics coverage run -m pytest
```

to check code coverage, type the following command:

```
docker-compose -f local.yml run --rm mylyrics coverage html
```

and open with your preferred browser "htmlcov/index.html"