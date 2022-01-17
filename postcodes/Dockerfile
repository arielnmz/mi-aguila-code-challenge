FROM python:3.9 as base

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends build-essential

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM base as prod

RUN exit 1
