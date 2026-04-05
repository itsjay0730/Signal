# pipelines/news/dedup.py

def normalize(title: str) -> str:
    return title.lower().strip()

def group_duplicates(news):
    grouped = {}

    for item in news:
        title = normalize(item.get("title", ""))

        if not title:
            continue

        if title not in grouped:
            grouped[title] = {
                "title": item["title"],  # keep original
                "sources": [item.get("source")],
                "urls": [item.get("url")],
                "count": 1,
                "category": item.get("category"),
                "fetched_at": item.get("fetched_at"),
            }
        else:
            grouped[title]["sources"].append(item.get("source"))
            grouped[title]["urls"].append(item.get("url"))
            grouped[title]["count"] += 1

    # 🔥 optional: remove duplicate sources
    for item in grouped.values():
        item["sources"] = list(set(item["sources"]))
        item["urls"] = list(set(item["urls"]))

    return list(grouped.values())