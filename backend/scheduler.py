from llm import llm
from models import Articles
from sqlmodel import Session,select,create_engine


DATABASE_URL="sqlite:///data.db"
engine=create_engine(DATABASE_URL)

def fetch_trending_topics():
    print("Scraping started...")
    llm_data = llm()
    

    with Session(engine) as session:
        for item in llm_data:
            try:
                statement = select(Articles).where(Articles.Topic == item["topic"])
                existing = session.exec(statement).first()

                if existing:
                    print(f"Topic already exists: {item['topic']}")
                    continue

                print(f"Adding to batch: {item['topic']}")
                db_article = Articles(
                    Topic=item["topic"],
                    Title=item["title"],
                    Text=item["text"],
                    Sources_used=item["sources_used"]
                )
                
                session.add(db_article)
            
            except (KeyError, TypeError) as e:
                print(f"Skipping item due to bad JSON structure: {e}")
                continue

        print("Committing all new articles to database...")
        session.commit()
        
    print("Scraping finished and database updated.")

