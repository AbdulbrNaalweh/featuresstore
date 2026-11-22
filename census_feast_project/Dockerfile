FROM python:3.10-slim-bookworm AS deps


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1


COPY requirements.txt /tmp/requirements.txt

RUN sed -i 's/pyarrow==14.0.0/pyarrow==14.0.1/' /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


COPY --from=deps /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY feature_repo/ /app/feature_repo/

COPY data/raw/ /app/data/raw/
COPY data/download_data.py /app/data/download_data.py

RUN rm -rf /app/feature_repo/__pycache__ /app/feature_repo/results \
    && mkdir -p /app/results

WORKDIR /app/feature_repo

EXPOSE 8001 8888

CMD ["sh", "-c", "[ -s ../data/raw/adult.csv ] || (cd ../data && python download_data.py) && python data_ingestion.py && python materialize.py && { feast ui --host 0.0.0.0 --port 8888 & uvicorn api_server:app --host 0.0.0.0 --port 8000; }"]


