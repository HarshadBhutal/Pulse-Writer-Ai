from datetime import datetime
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from apscheduler.schedulers.background import BackgroundScheduler

from scheduler import fetch_trending_topics, engine


def run_scraper():
    """Run scraping safely in the scheduler's background thread."""
    try:
        print("INFO: Background scraping started...")
        fetch_trending_topics()
        print("INFO: Background scraping completed.")
    except Exception as e:
        print(f"ERROR: Background scraping failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize database
    SQLModel.metadata.create_all(engine)

    # Initialize background scheduler
    scheduler = BackgroundScheduler()

    # Schedule the first scrape immediately, then every 10 minutes
    scheduler.add_job(
        func=run_scraper,
        trigger="interval",
        minutes=10,
        id="scraper_job",
        next_run_time=datetime.now(),
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    print("INFO: Scheduler started. Application is ready.")

    yield

    # Shutdown
    print("INFO: Shutting down resources...")
    scheduler.shutdown(wait=True)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "keep_alive": 0
                }
            )
        print("INFO: Ollama model unloaded.")

    except Exception as e:
        print(f"WARNING: Could not reach Ollama: {e}")

    print("INFO: Cleanup complete.")


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/article/trending")
def fetch_articles():
    from sqlmodel import Session, select, desc
    from models import Articles

    with Session(engine) as session:
        statement = select(Articles).order_by(desc(Articles.Id))
        return session.exec(statement).all()


app.mount(
    "/",
    StaticFiles(directory="../static", html=True),
    name="static"
)