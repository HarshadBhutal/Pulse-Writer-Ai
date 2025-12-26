from sqlmodel import Session,select,create_engine
from llm import llm
from models import Articles


engine=create_engine("sqlite:///../data/data.db")

def fetch_trending_topics():
    print("Scraping started...")
    llm_data=llm()
    response_data=[]
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
            response_data.append({
                "id": db_article.id,
                "Topic": db_article.Topic,
                "Title": db_article.Title,
                "Text": item["Facts"], 
                "Created_at": db_article.Created_at
            })
    print("Scraping finished and database updated.")

