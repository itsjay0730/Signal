import requests
from datetime import datetime, timezone

#helps to find the internship through keywords like mainly for tech
def isTechInternship(title: str) -> bool:
    title = title.lower()

    keywords = [
        "intern",
        "internship",
        "software",
        "engineer",
        "developer",
        "backend",
        "frontend",
        "full stack",
        "swe"
    ]

    for k in keywords:
        if k in title:
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

            #filter only tech internships
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

    return internships