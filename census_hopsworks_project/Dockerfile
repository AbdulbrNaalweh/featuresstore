FROM python:3.10-slim-bookworm AS deps


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev libc6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt nest_asyncio \
    && rm /tmp/requirements.txt

COPY scripts/ /app/scripts/
COPY config/ /app/config/
RUN rm -rf /app/scripts/__pycache__ \
    && mkdir -p /app/data /app/results

WORKDIR /app/scripts

CMD ["python", "run.py"]

