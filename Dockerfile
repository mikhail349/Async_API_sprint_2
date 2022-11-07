FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN groupadd -r app \
    && useradd -d /app -r -g app app \
    && chown app:app -R /app

USER app

EXPOSE 8000

CMD ["gunicorn", "src.main:app", "--worker-class", \
     "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
