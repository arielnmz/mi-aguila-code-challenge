FROM python:3.9 as base

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends build-essential

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY django_api django_api

FROM base as prod

ENV PYTHONPATH="/app/django_api:${PYTHONPATH}"
ENV PYTHONUNBUFFERED=1

WORKDIR /app/django_api

VOLUME ["/app/django_api/db"]

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
