import json
import httpx
from sqlmodel import SQLModel,create_engine,Session,select
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import fetch_trending_topics
from models import Articles

engine=create_engine("sqlite:///../data/data.db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    SQLModel.metadata.create_all(engine)
    scheduler=BackgroundScheduler()
    # Start your background task
    scheduler.add_job(func=fetch_trending_topics, trigger="interval", minutes=1, id="scraper_job")
    scheduler.start()
    print("INFO: Scheduler started.")
    
    yield  # The FastAPI app is running now
    
    # --- SHUTDOWN ---
    print("INFO: Shutting down resources...")
    
    # 1. Stop the Scheduler threads cleanly
    scheduler.shutdown()
    
    # 2. Tell Ollama to unload the model from GPU immediately
    # This prevents the 'ollama directly stopped' issue
    try:
        async with httpx.AsyncClient() as client:
            # Setting keep_alive to 0 tells Ollama to unload the model right now
            await client.post("http://localhost:11434/api/generate", 
                             json={"model": "your-model-name", "keep_alive": 0})
        print("INFO: Ollama model unloaded.")
    except Exception as e:
        print(f"WARNING: Could not reach Ollama to unload: {e}")

    print("INFO: Cleanup complete. Safe to exit.")

app=FastAPI(lifespan=lifespan)

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
    with Session(engine) as session:
        articles = session.exec(select(Articles)).all()
        return articles
    



    
