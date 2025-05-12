FROM python:3.11.5-slim AS builder
RUN apt-get update && apt-get install -y curl nano
WORKDIR /connector
# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock

RUN pip3 install poetry
RUN poetry config virtualenvs.in-project true

RUN poetry install --only main

# 1 - copy the source code folders
COPY . .

# 2 - run the app
CMD ["poetry", "run", "python", "main.py"]
