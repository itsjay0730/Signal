# pipelines/news/dedup.py

def normalize(title: str) -> str:
    """
    Normalize the title for consistent comparison.
    Converts to lowercase and removes leading/trailing spaces.
    """
    return title.lower().strip()


def group_duplicates(news):
    """
    Groups duplicate news items based on normalized titles.

    Parameters:
        news (list): List of news dictionaries

    Returns:
        list: List of grouped news signals
    """
    grouped = {}

    for item in news:
        # Normalize title for comparison
        title = normalize(item.get("title", ""))

        # Skip empty titles
        if not title:
            continue

        if title not in grouped:
            grouped[title] = {
                "title": item["title"],              
                "sources": [item.get("source")],     
                "urls": [item.get("url")],           
                "count": 1,                        
                "category": item.get("category"),
                "fetched_at": item.get("fetched_at"),
            }
        else:
            # If duplicate → update existing group
            grouped[title]["sources"].append(item.get("source"))
            grouped[title]["urls"].append(item.get("url"))
            grouped[title]["count"] += 1

    # Remove duplicate sources and URLs
    for item in grouped.values():
        item["sources"] = list(set(item["sources"]))
        item["urls"] = list(set(item["urls"]))

    return list(grouped.values())