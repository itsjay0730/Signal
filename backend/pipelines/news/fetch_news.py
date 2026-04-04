import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def fetch_news():
    news = []

    ##################################
    #  NEWS API 
    ##################################

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
                "category": "technology"
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

    ##################################
    #  HACKERNEWS API 
    ##################################
    
    hackerCategories = [
        "/topstories.json",
        "/newstories.json",
        "/beststories.json",
    ]
    HACKER_URL = "https://hacker-news.firebaseio.com/v0"

    allIds = []

    #collect IDs from all categories
    for category in hackerCategories:
        response = requests.get(HACKER_URL + category)

        if response.status_code == 200:
            ids = response.json()[:15]
            allIds.extend(ids)

    allIds = list(set(allIds))

    #fetch each story
    for storyId in allIds:
        storyResponse = requests.get(HACKER_URL + f"/item/{storyId}.json")

        if storyResponse.status_code == 200:
            story = storyResponse.json()

            if story and story.get("title") and story.get("type") == "story":
                news.append({
                    "title": story["title"].split(" - ")[0],          
                    "source": "Hacker News",             
                    "url": story.get("url", ""),         
                    "category": "tech"                   
                })

    ##################################
    #  GNEWS API 
    ##################################

    gnewsCategories = [
        "technology",
        "business",
    ]

    for category in gnewsCategories:
        gnewsResponse = requests.get(f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&max=20&apikey={GNEWS_API_KEY}")

        if gnewsResponse.status_code == 200:
            articles = gnewsResponse.json()["articles"]

            for article in articles:
                news.append({
                    "title": article["title"].split(" - ")[0],
                    "source": article["source"]["name"],
                    "url": article["url"],
                    "category": category
                })


    return news