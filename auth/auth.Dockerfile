FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential libpq-dev && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

RUN flask db init && flask db migrate && flask db upgrade

EXPOSE 8080

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"  ]

