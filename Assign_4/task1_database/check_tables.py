import os
import sys
import psycopg2

def check_and_fix_database():
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

        # Check if the rss_items table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'rss_items'
            );
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print("Table 'rss_items' does not exist. Recreating...")
            cursor.execute("""
                CREATE TABLE rss_items (
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
            print("Table 'rss_items' created successfully.")
        else:
            print("Table 'rss_items' already exists. No action needed.")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error during database check: {e}")
        return False

if __name__ == "__main__":
    if not check_and_fix_database():
        sys.exit(1)
    sys.exit(0)
