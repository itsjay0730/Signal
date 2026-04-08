
from datetime import datetime, timezone

def get_recency_score(fetched_at: str) -> float:
    try:
        #converts a string into a datetime object so we can use it for the calculation
        fetched_time = datetime.fromisoformat(fetched_at)
        #fetch current time
        now = datetime.now(timezone.utc)

        # check if it has the timezone if not it will assign a universal timezone 
        if fetched_time.tzinfo is None:
            fetched_time = fetched_time.replace(tzinfo=timezone.utc)

        # calculates the hours
        hoursOld = (now - fetched_time).total_seconds() / 3600

        if hoursOld <= 3:
            return 1.0
        elif hoursOld <= 6:
            return 0.8
        elif hoursOld <= 12:
            return 0.6
        elif hoursOld <= 24:
            return 0.4
        else:
            return 0.2

    except Exception:
        return 0.5  

def normalize_count(count: int) -> float:
    # we doing this because we want to keep things betwen 0-1 for consistency 
    return min(count, 5) / 5

def ranking_agent(signals: list) -> list:

    for signal in signals:
        #get give the value of the key
        count = signal.get("count", 1)

        #make sure you use the same spelling for this???
        impactScore = signal.get("impactScore", 0)
        relevanceScore = signal.get("relevanceScore", 0)
        fetched_at = signal.get("fetched_at")

        normalizeCount = normalize_count(count)
        recencyScore = get_recency_score(fetched_at)

        # this are not the perfect percent weightage it depends on what behavior do we want?
        score = ((normalizeCount * 0.30) + (recencyScore * 0.25) + (impactScore * 0.30) + (relevanceScore * 0.15))

        signal["score"] = round(score, 4)

    # this will take the score from the dict and sort
    rankedSignals = sorted(key=lambda x: x["score"], reverse=True)
    return rankedSignals