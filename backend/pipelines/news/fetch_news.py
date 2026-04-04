import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
#for hacker news fetch
BASE_URL = "https://hacker-news.firebaseio.com/v0"

def fetch_news():
    news = []

    #################
    #  NEWS API 
    #################

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

    #################
    #  HACKERNEWS API 
    #################

    categories = [
        "/topstories.json",
        "/newstories.json",
        "/beststories.json",
    ]

    allIds = []

    #collect IDs from all categories
    for category in categories:
        response = requests.get(BASE_URL + category)

        if response.status_code == 200:
            ids = response.json()[:20]
            allIds.extend(ids)

    allIds = list(set(allIds))

    #fetch each story
    for storyId in allIds:
        storyResponse = requests.get(BASE_URL + f"/item/{storyId}.json")

        if storyResponse.status_code == 200:
            story = storyResponse.json()

            if story and story.get("title") and story.get("type") == "story":
                news.append({
                    "title": story["title"],          
                    "source": "Hacker News",             
                    "url": story.get("url", ""),         
                    "category": "tech"                   
                })



    return news