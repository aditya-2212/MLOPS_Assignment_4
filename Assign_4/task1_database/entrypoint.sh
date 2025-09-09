#!/bin/bash
set -m  # Enable job control so we can background/foreground processes

# 1. Activate the virtual environment
source /opt/venv/bin/activate

# 2. Start Postgres (the official entrypoint) in the background
/usr/local/bin/docker-entrypoint.sh postgres &

# 3. Run your Python scripts, which now have access to psycopg2 in the venv
python /usr/local/bin/db_init.py
python /usr/local/bin/check_tables.py

# 4. Bring the Postgres job back to the foreground so Docker doesn't exit
fg %1
