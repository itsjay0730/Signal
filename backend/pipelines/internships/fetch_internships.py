import requests
from datetime import datetime, timezone
import feedparser

#helps find the internship through keywords mainly for tech
def isTechInternship(title: str) -> bool:
    title = title.lower()

    keywords = [
        # "intern",        lowkey dont think we need these two bc were fetching internships,
        # "internship",    always return and wont filter for tech only
        "software",
        "engineer",
        "developer",
        "backend",
        "frontend",
        "full stack",
        "swe"
    ]

    for keyword in keywords:
        if keyword in title:
            return True
    return False 

def fetch_internships():
    internships = []

    ##################################
    #  ARBEITNOW API
    ##################################

    ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"

    response = requests.get(ARBEITNOW_URL)

    if response.status_code == 200:
        jobs = response.json().get("data", [])

        for job in jobs:
            #removes extra spaces from the beginning and end of a string
            title = job.get("title", "").strip()

            if not title:
                continue

            #filter only for tech internships
            if not isTechInternship(title):
                continue

            internships.append({
                "id": hash(title),
                "title": title,
                "description": job.get("description", ""),
                "source": "Arbeitnow",
                "url": job.get("url", ""),
                "category": "internship",
                "fetched_at": datetime.now(timezone.utc).isoformat()
            })
    ##################################
    #  REDDIT RSS (INTERNSHIPS)
    ##################################

    redditUrls = [
        "https://www.reddit.com/search.rss?q=software+engineering+internship&sort=new",
        "https://www.reddit.com/search.rss?q=swe+internship&sort=new"
    ]
    for url in redditUrls:
        feed = feedparser.parse(
            url,
            request_headers={"User-Agent": "SignalApp/1.0 (by u/testuser)"}
        )
        for entry in feed.entries[:10]:
            title = getattr(entry, "title", "").strip()

            if title:
                internships.append({
                    "id": hash(title),
                    "title": title,
                    "description": getattr(entry, "summary", ""),
                    "source": "Reddit",
                    "url": getattr(entry, "link", ""),
                    "category": "technology",
                    "fetched_at": datetime.now(timezone.utc).isoformat()
                })

    return internships