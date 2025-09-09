FROM python:3.10-slim

# Install the system packages needed to build psycopg2 from source
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY rss_reader.py /app/rss_reader.py

CMD ["python", "/app/rss_reader.py"]