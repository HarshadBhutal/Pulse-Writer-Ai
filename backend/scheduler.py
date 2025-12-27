from sqlmodel import Session,select,create_engine
from llm import llm
from models import Articles


engine=create_engine("sqlite:///data.db")

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

            print("post is running")
            db_article = Articles(
                    Topic=item["Topic"],
                    Title=item["Title"],
                    Text=item["Facts"]
                )
            
            session.add(db_article)
            session.commit()
            session.refresh(db_article)
    print("Scraping finished and database updated.")

