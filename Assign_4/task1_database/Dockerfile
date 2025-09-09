FROM postgres:latest

# 1. Install Python, venv support, and build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-dev \
    build-essential \
    libpq-dev

# 2. Create a virtual environment in /opt/venv
RUN python3 -m venv /opt/venv

# 3. Activate the venv and install packages
RUN . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install psycopg2 feedparser

# 4. Copy your Python scripts and custom entrypoint
COPY db_init.py /usr/local/bin/db_init.py
COPY check_tables.py /usr/local/bin/check_tables.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 5. Override the default Postgres entrypoint with your custom script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
