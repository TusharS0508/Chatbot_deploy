FROM python:3.11-slim-bookworm

WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

COPY . .

RUN find /usr/local/lib/python3.11 -type d -name '__pycache__' -exec rm -rf {} + && \
    find /usr/local/lib/python3.11 -name '*.so' -exec strip {} \;

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]