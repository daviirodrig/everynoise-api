FROM python:3.10-slim

ENV PYTHONUNBUFFERED=true

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install --disable-pip-version-check --no-cache-dir --user -r requirements.txt

COPY . .

EXPOSE 28996

CMD ["python", "-m", "uvicorn", "src.routes:app", "--host", "0.0.0.0", "--port", "28996", "--reload"]