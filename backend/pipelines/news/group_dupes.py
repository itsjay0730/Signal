from difflib import SequenceMatcher
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


#local model  the text is for that helps to that turns titles into meaning-based number vectors.
model = SentenceTransformer("all-MiniLM-L6-v2")

def normalize(title: str) -> str:
    title = title.lower()
    title = re.sub(r'[^\w\s]', '', title)  
    title = re.sub(r'\s+', ' ', title).strip() 
    return title

def similarity(a: str, b: str) -> float:
    """Returns a similarity ratio between 0.0 and 1.0"""
    return SequenceMatcher(None, a, b).ratio()

def find_group_key(grouped: dict, title: str, threshold: float = 0.80) -> str | None:
    """
    scans your already grouped titles and asks does this new title belong to any existing group?
    """
    for key in grouped:
        if similarity(title, key) >= threshold:
            return key
    return None

def groupDuplicates(news, threshold: float = 0.80):
    grouped = {}

    for item in news:
        title = normalize(item.get("title", ""))

        if not title:
            continue

        matched_key = find_group_key(grouped, title, threshold)

        if matched_key is None:
            #No similar title found, create a new group
            grouped[title] = {
                "id": hash(title),
                "title": item["title"],              
                "sources": [item.get("source")],     
                "urls": [item.get("url")],           
                "count": 1,                        
                "category": item.get("category"),
                "fetched_at": item.get("fetched_at"),
            }
        else:
            #Similar title found → merge into existing group
            grouped[matched_key]["sources"].append(item.get("source"))
            grouped[matched_key]["urls"].append(item.get("url"))
            grouped[matched_key]["count"] += 1

    for item in grouped.values():
        item["sources"] = list(set(item["sources"]))
        item["urls"] = list(set(item["urls"]))

    return list(grouped.values())