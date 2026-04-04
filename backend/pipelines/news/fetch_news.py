import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news():
    news = []

    #fetch newsapi tech related data
    techUrl = f"https://newsapi.org/v2/top-headlines?category=technology&pageSize=30&apiKey={NEWS_API_KEY}"
    techResponse = requests.get(techUrl)

    if techResponse.status_code == 200:
        articles = techResponse.json()["articles"]

        for article in articles:
            news.append({
                "title": article["title"].split(" - ")[0],
                "source": article["source"]["name"],
                "url": article["url"],
                "category": "tech"
            })

    #fetch newsapi business related data
    businessUrl = f"https://newsapi.org/v2/top-headlines?category=business&pageSize=30&apiKey={NEWS_API_KEY}"
    businessResponse = requests.get(businessUrl)

    if businessResponse.status_code == 200:
        articles = businessResponse.json()["articles"]

        for article in articles:
            news.append({
                "title": article["title"].split(" - ")[0],
                "source": article["source"]["name"],
                "url": article["url"],
                "category": "business"
            })

    return news
