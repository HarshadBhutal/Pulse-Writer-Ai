import time
import random
import feedparser
from newspaper import Article, Config
from googlenewsdecoder import gnewsdecoder
from sentence_transformers import SentenceTransformer, util


Top_n=5

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
        re_title=" "
        for i in range(len(title)):
            if title[-i]=="-":
                val=i
                break
        re_title=title[:-val]
        query=re_title.replace(" ","+")

        schema={"Topic":re_title,"Sources":[]}

        

        url_1=f"https://news.google.com/rss/search?q={query}"
        feed_1=feedparser.parse(url_1)

        for entry_1 in feed_1.entries[:4]:

            title=entry_1.title
            for i in range(len(title)):
                if title[-i]=="-":
                    val=i
                break
            re_title_1=title[:-val]

            title_emd=model.encode(re_title,convert_to_tensor=True)
            title_1_emd=model.encode(re_title_1,convert_to_tensor=True)
            Score=util.cos_sim(title_emd,title_1_emd)[0]

            if Score<=0.5:
                continue
            
            real_url = gnewsdecoder(entry_1.link)

            try:
                    article=Article(real_url["decoded_url"], config=config)
                    article.download()
                    article.parse()
                    if article.text:
                        print("Topic: ",re_title)
                        text=article.text.replace("\n\n","\n")
                        text=text.replace("\"","")
                        schema["Sources"].append({"publisher":title[-val:],"text":text})
                        value+=1

                    else:
                        continue

            except Exception:
                    continue
            time.sleep(random.uniform(1, 3))

        print(value)
        trending_news.append(schema)   

    print(trending_news)
    return trending_news
       

    

      