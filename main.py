import time
import random
import feedparser
from newspaper import Article, Config
from googlenewsdecoder import gnewsdecoder

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

url="https://news.google.com/rss/search?q=India&hl=en-IN&gl=IN&ceid=IN:en"
feed=feedparser.parse(url)

for entry in feed.entries[:3]:
    title=entry.title
    re_title=" "
    for i in range(len(title)):
        if title[-i]=="-":
            val=i
            break
    re_title=title[:-val]
    print(re_title)
    query=re_title.replace(" ","+")

    url_1=f"https://news.google.com/rss/search?q={query}"
    feed_1=feedparser.parse(url_1)
    for entry_1 in feed_1.entries[:3]:
        print(entry_1.title)
        print(entry_1.link)
        real_url = gnewsdecoder(entry_1.link)
        print(real_url)
        article=Article(real_url["decoded_url"], config=config)
        article.download()
        article.parse()
        print(article.text)
        print("-" * 40) 
        time.sleep(random.uniform(1, 3))
    print("end")
    

      