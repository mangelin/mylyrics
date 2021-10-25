FROM python:3.10-alpine
RUN apk update && apk upgrade \
    && apk add py3-pip

COPY requirements/base.txt ./

RUN pip install -r base.txt

WORKDIR /app

COPY src/ /app/src
RUN touch /app/__init__.py

# Unit tests
COPY tests/ /app/tests

CMD [ "python", "./src/mylyrics.py" ]