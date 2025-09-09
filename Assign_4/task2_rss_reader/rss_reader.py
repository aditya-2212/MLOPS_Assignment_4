import os
import time
import feedparser
import psycopg2
from datetime import datetime

def main():
    time.sleep(10)
    feed_url = os.environ.get("RSS_FEED_URL", "https://www.thehindu.com/news/national/?service=rss")
    poll_interval = int(os.environ.get("POLL_INTERVAL", "600"))  # default 10 minutes

    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "5432")
    db_user = os.environ.get("DB_USER", "postgres")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_name = os.environ.get("DB_NAME", "newsdb")

    print("RSS Reader script starting up...", flush=True)

    while True:
        print(f"Fetching RSS feed from {feed_url}...")
        feed = feedparser.parse(feed_url)

        # Connect to PostgreSQL
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                dbname=db_name
            )
            conn.autocommit = True
            cursor = conn.cursor()

            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = entry.get("summary", "")
                published_str = entry.get("published", "")
                # For now, store current time as publication_timestamp or parse published_str
                publication_timestamp = datetime.now()

                # Extract image if present
                image_url = ""
                if hasattr(entry, "media_content") and len(entry.media_content) > 0:
                    image_url = entry.media_content[0].get("url", "")

                # Insert data into your Task 1 table (rss_items or news_articles, etc.)
                insert_query = """
                    INSERT INTO rss_items
                    (title, publication_timestamp, weblink, image_path, tags, summary)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    title,
                    publication_timestamp,
                    link,
                    image_url,
                    None,  # or parse tags from entry.tags
                    summary
                ))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error inserting data into DB: {e}")

        print(f"Sleeping for {poll_interval} seconds...")
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()
