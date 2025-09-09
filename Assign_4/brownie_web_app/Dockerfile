FROM python:3.10-slim

# 1. Installing system packages needed for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY main.py /app/main.py
COPY templates /app/templates

EXPOSE 5000
CMD ["python", "/app/main.py"]
