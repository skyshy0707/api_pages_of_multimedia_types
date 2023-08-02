FROM python:3.8-slim-buster

WORKDIR /code
COPY ./src/ ./src
COPY ./requirements.txt ./src/requirements.txt
COPY ./autotests-entrypoint.sh ./src/autotests-entrypoint.sh
COPY ./runserver-entrypoint.sh ./src/runserver-entrypoint.sh
COPY ./worker-entrypoint.sh ./src/worker-entrypoint.sh

RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r ./src/requirements.txt

RUN chmod +x /code/src/autotests-entrypoint.sh
RUN chmod +x /code/src/runserver-entrypoint.sh
RUN chmod +x /code/src/worker-entrypoint.sh