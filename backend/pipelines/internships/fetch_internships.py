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

