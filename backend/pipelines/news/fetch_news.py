import os
import requests
import feedparser
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def fetch_news():
    news = []

    ##################################
    #  NEWS API 
    ##################################

    newsCategories = ["technology", "business"]

    for category in newsCategories:
        newsResponse = requests.get(
            f"https://newsapi.org/v2/top-headlines?category={category}&pageSize=30&apiKey={NEWS_API_KEY}"
        )

        if newsResponse.status_code == 200:
            articles = newsResponse.json().get("articles", [])

            for article in articles:
                title = article.get("title", "").split(" - ")[0].strip()

                if title:
                    news.append({
                        "id": hash(title),
                        "title": title,
                        "source": article.get("source", {}).get("name", ""),
                        "source_type": "news",
                        "url": article.get("url", ""),
                        "category": category,
                        "fetched_at": datetime.utcnow().isoformat()
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

    for category in hackerCategories:
        response = requests.get(HACKER_URL + category)

        if response.status_code == 200:
            ids = response.json()[:15]
            allIds.extend(ids)

    allIds = list(set(allIds))

    for storyId in allIds:
        storyResponse = requests.get(HACKER_URL + f"/item/{storyId}.json")

        if storyResponse.status_code == 200:
            story = storyResponse.json()

            if story and story.get("title") and story.get("type") == "story":
                title = story.get("title", "").split(" - ")[0].strip()

                if title:
                    news.append({
                        "id": hash(title),
                        "title": title,
                        "source": "Hacker News",
                        "source_type": "hn",
                        "url": story.get("url", ""),
                        "category": "tech",
                        "fetched_at": datetime.utcnow().isoformat()
                    })


    ##################################
    #  GNEWS API 
    ##################################

    gnewsCategories = ["technology", "business"]

    for category in gnewsCategories:
        gnewsResponse = requests.get(
            f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&max=20&apikey={GNEWS_API_KEY}"
        )

        if gnewsResponse.status_code == 200:
            articles = gnewsResponse.json().get("articles", [])

            for article in articles:
                title = article.get("title", "").split(" - ")[0].strip()

                if title:
                    news.append({
                        "id": hash(title),
                        "title": title,
                        "source": article.get("source", {}).get("name", ""),
                        "source_type": "news",
                        "url": article.get("url", ""),
                        "category": category,
                        "fetched_at": datetime.utcnow().isoformat()
                    })


    ##################################
    #  REDDIT RSS
    ##################################

    redditUrls = [
        "https://www.reddit.com/r/technology/.rss",
        "https://www.reddit.com/r/artificial/.rss",
        "https://www.reddit.com/r/programming/.rss",
        "https://www.reddit.com/search.rss?q=software+engineering+internship&sort=new"
    ]

    for url in redditUrls:
        feed = feedparser.parse(
            url,
            request_headers={"User-Agent": "SignalApp/1.0 (by u/testuser)"}
        )

        for entry in feed.entries[:10]:
            title = getattr(entry, "title", "").strip()

            if title:
                #simple internship detection
                if "intern" in title.lower():
                    category = "internship"
                else:
                    category = "tech"

                news.append({
                    "id": hash(title),
                    "title": title,
                    "source": "Reddit",
                    "source_type": "reddit",
                    "url": getattr(entry, "link", ""),
                    "category": category,
                    "fetched_at": datetime.utcnow().isoformat()
                })

    return news