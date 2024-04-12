FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential libpq-dev && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

EXPOSE 8080

ENTRYPOINT [ "python3", "views.py"  ]
#CMD ['flask', 'db', 'init']
#CMD ['flask', 'db', 'upgrade']