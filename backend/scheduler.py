import os
from llm import llm
from models import Articles
from dotenv import load_dotenv
from sqlmodel import Session,select,create_engine

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)

def fetch_trending_topics():
    print("Scraping started...")
    llm_data=llm()
    for item in llm_data:

        with Session(engine) as session:
        
            statement=select(Articles).where(Articles.Topic==item["Topic"])
            existing=session.exec(statement).first()

            if existing:
                print(f"Topic already exists {item["Topic"]}")
                continue

            print("sending to the database")
            db_article = Articles(
                    Topic=item["Topic"],
                    Title=item["Title"],
                    Text=item["Text"],
                    Sources_used=item["Sources_used"]
                )
            
            session.add(db_article)
            session.commit()
            session.refresh(db_article)
    print("Scraping finished and database updated.")

