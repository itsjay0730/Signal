import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
#for hacker news fetch
BASE_URL = "https://hacker-news.firebaseio.com/v0"

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

def fetch_hacker_news():
    news = []

    #endpoints
    endpoints = [
        "/topstories.json",
        "/newstories.json",
        "/showstories.json",
        "/beststories.json",
        "/askstories.json",
        "/jobstories.json"
    ]

    all_ids = []

    #collect IDs from all endpoints
    for endpoint in endpoints:
        response = requests.get(BASE_URL + endpoint)

        if response.status_code == 200:
            ids = response.json()
            all_ids.extend(ids[:20])  # limit per source

    # remove duplicates
    all_ids = list(set(all_ids))

    #fetch item details
    for story_id in all_ids:
        storyResponse = requests.get(BASE_URL + f"/item/{story_id}.json")

        if storyResponse.status_code == 200:
            item = storyResponse.json()

            if item and item.get("title") and item.get("type") == "story":
                news.append({
                    "title": item["title"],          
                    "source": "Hacker News",             
                    "url": item.get("url", ""),         
                    "category": "tech"                   
                })
    return news