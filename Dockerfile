FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY ./pyproject.toml .

RUN poetry install

COPY ./shortener.py .
COPY ./admin.html .

CMD ["poetry", "run", "uvicorn", "shortener:app", "--host", "0.0.0.0"]
