FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "python", "/app/healthy_docker/main.py"]