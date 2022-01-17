FROM python:3.9 as base

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends build-essential

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY django_postcodes django_postcodes

FROM base as prod

ENV PYTHONPATH="/app/django_postcodes:${PYTHONPATH}"
ENV PYTHONUNBUFFERED=1

WORKDIR /app/django_postcodes

EXPOSE 8001

CMD python manage.py runserver 0.0.0.0:8001
