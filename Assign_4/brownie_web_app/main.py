import os
import psycopg2
from datetime import datetime, date
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up Jinja2 templates (assuming templates/ is inside /app)
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "5432")
    db_user = os.environ.get("DB_USER", "postgres")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_name = os.environ.get("DB_NAME", "newsdb")

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname=db_name
    )
    return conn

@app.get("/", response_class=HTMLResponse)
def index(request: Request, date_str: str = None):
    """
    Display news articles filtered by date (default: today's date).
    Usage: /?date_str=YYYY-MM-DD
    """
    # Defaults to today's date if none provided
    if not date_str:
        filter_date = date.today()
    else:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT title, publication_timestamp, weblink, image_path, summary
        FROM rss_items
        WHERE DATE(publication_timestamp) = %s
        ORDER BY publication_timestamp DESC
    """
    cursor.execute(query, (filter_date,))
    articles = cursor.fetchall()

    cursor.close()
    conn.close()

    # articles is a list of tuples: (title, publication_timestamp, weblink, image_path, summary)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": articles,
        "filter_date": filter_date
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)