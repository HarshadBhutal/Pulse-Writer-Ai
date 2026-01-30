import httpx
from models import Articles
from fastapi import FastAPI,staticfiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from scheduler import fetch_trending_topics,engine
from sqlmodel import SQLModel,Session,select,desc
from apscheduler.schedulers.background import BackgroundScheduler


@asynccontextmanager
async def lifespan(app: FastAPI):

    SQLModel.metadata.create_all(engine)
    scheduler=BackgroundScheduler()
    scheduler.add_job(func=fetch_trending_topics, trigger="interval", minutes=10, id="scraper_job")
    scheduler.start()
    print("INFO: Scheduler started.")
    yield 
    print("INFO: Shutting down resources...")
    scheduler.shutdown()
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post("http://127.0.0.1:11434/api/generate", 
                             json={"model": "llama3.2", "keep_alive": 0})
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
         
         statement = select(Articles).order_by(desc(Articles.Id))
         latest_article = session.exec(statement).all()

         return latest_article
    
app.mount("/", staticfiles.StaticFiles(directory="../static", html=True), name="static")



    
