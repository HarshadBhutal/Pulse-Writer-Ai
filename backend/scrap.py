import time
import math
import random
import feedparser
from newspaper import Article, Config
from googlenewsdecoder import gnewsdecoder
from sentence_transformers import SentenceTransformer, util


Top_n=5
next_n=3

def News_Scrap():
              
    model=SentenceTransformer("all-MiniLM-L6-v2")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    url="https://news.google.com/rss/search?q=India&hl=en-IN&gl=IN&ceid=IN:en"
    feed=feedparser.parse(url)
    trending_news=[]

    for entry in feed.entries[:Top_n]:
        value=0
        title=entry.title
        title=title.rsplit("-")
        query=title[0].replace(" ","+")
        schema={"Topic":title[0],"Sources":[]}
        print("Topic",title[0])

        url_1=f"https://news.google.com/rss/search?q={query}"
        feed_1=feedparser.parse(url_1)

        for entry_1 in feed_1.entries[:next_n]:
            
            title_1=entry_1.title
            title_1=title_1.rsplit("-")
            
            title_emd=model.encode(title[0],convert_to_tensor=True)
            title_1_emd=model.encode(title_1[0],convert_to_tensor=True)
            Score=util.cos_sim(title_emd,title_1_emd)[0]
            score = Score.item()
            print(Score)
            
            if (score>0.65):
                pass
            else:
                continue

            real_url = gnewsdecoder(entry_1.link)

            try:
                    article=Article(real_url["decoded_url"], config=config)
                    article.download()
                    article.parse()
                    if article.text:
                        print("Topic: ",title_1[0])
                        schema["Sources"].append({"publisher":title_1[1],"text":article.text})
                        value+=1
                    else:
                        print("enone")
                        continue

            except Exception:
                    print("none")
                    continue
            time.sleep(random.uniform(1, 3))

        if schema["Sources"]==[]:
                continue
        
        print("Total sources",value)
        trending_news.append(schema)
        print(40*"-")
        
    print(trending_news)
    return trending_news
       

    

      