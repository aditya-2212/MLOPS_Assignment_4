import os
import time
import psycopg2

def wait_for_db():
    db_user = os.environ.get('POSTGRES_USER')
    db_name = os.environ.get('POSTGRES_DB')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_host = os.environ.get('POSTGRES_HOST', 'localhost')
    db_port = os.environ.get('POSTGRES_PORT', '5432')

    num_retries = 30
    for i in range(num_retries):
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.close()
            print("Database is ready!")
            return True
        except psycopg2.OperationalError:
            print(f"Waiting for database... {i+1}/{num_retries}")
            time.sleep(2)

    print("Failed to connect to the database after multiple attempts.")
    return False

def initialize_database():
    db_name = os.environ.get('POSTGRES_DB')
    db_user = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_host = os.environ.get('POSTGRES_HOST', 'localhost')
    db_port = os.environ.get('POSTGRES_PORT', '5432')

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rss_items (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                publication_timestamp TIMESTAMP NOT NULL,
                weblink TEXT NOT NULL,
                image_path TEXT,
                tags TEXT[],
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        print("Database initialization completed successfully.")
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error during database initialization: {e}")
        return False

if __name__ == "__main__":
    # 1. Wait for DB
    if not wait_for_db():
        exit(1)

    # 2. Create table if needed
    if not initialize_database():
        exit(1)

    exit(0)
