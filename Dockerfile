FROM python:3.10

ENV PYTHONUNBUFFERED=true

WORKDIR /usr/app

RUN pip install --no-cache-dir --user poetry

COPY poetry.lock pyproject.toml ./

RUN python -m poetry config virtualenvs.create false

RUN python -m poetry install

COPY . .

EXPOSE 28996

CMD ["python", "-m", "poetry", "run", "uvicorn", "src.routes:app", "--host", "0.0.0.0", "--port", "28996"]