import os
import time
import random
import feedparser
from dotenv import load_dotenv
from newspaper import Article, Config
from googlenewsdecoder import gnewsdecoder
from sentence_transformers import SentenceTransformer, util

load_dotenv()

Topics_No=5
Articles_No=4

def News_Scrap():
              
    model=SentenceTransformer("all-MiniLM-L6-v2")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    T_url=os.getenv("T_url")
    T_feed=feedparser.parse(T_url)
    trending_news=[]

    for Topic in T_feed.entries[:Topics_No]:
        Sources=0
        T_title=Topic.title
        T_title=T_title.rsplit("-")
        query=T_title[0].replace(" ","+")
        schema={"Topic":T_title[0],"Sources":[]}
        print("Topic",T_title[0])

        A_url=f"https://news.google.com/rss/search?q={query}"
        A_feed=feedparser.parse(A_url)

        for entry in A_feed.entries[:Articles_No]:
            
            A_title=entry.title
            A_title=A_title.rsplit("-")
            
            T_title_emd=model.encode(T_title[0],convert_to_tensor=True)
            A_title_emd=model.encode(A_title[0],convert_to_tensor=True)
            Score=util.cos_sim(T_title_emd,A_title_emd)[0]
            score = Score.item()
            
            if (score>0.65):
                pass
            else:
                continue

            real_url = gnewsdecoder(entry.link)

            try:
                    article=Article(real_url["decoded_url"], config=config)
                    article.download()
                    article.parse()

                    if article.text:
                        schema["Sources"].append({"publisher":A_title[1],"text":article.text})
                        Sources+=1
                    else:
                        print("else none")
                        continue

            except Exception:
                    print("Exception none")
                    continue
            time.sleep(random.uniform(1, 3))

        if schema["Sources"]==[]:
                continue
        
        trending_news.append(schema)
        print(Sources)    
    print(trending_news)    
    return trending_news
       

    

      