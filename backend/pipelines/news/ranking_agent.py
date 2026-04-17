from datetime import datetime, timezone

def getRecencyScore(fetchedAt: str) -> float:
    try:
        #converts a string into a datetime object so we can use it for the calculation
        fetchedTime = datetime.fromisoformat(fetchedAt)
        #fetch current time
        now = datetime.now(timezone.utc)

        # check if it has the timezone if not it will assign a universal timezone 
        if fetchedTime.tzinfo is None:
            fetchedTime = fetchedTime.replace(tzinfo=timezone.utc)

        # calculates the hour
        hoursOld = (now - fetchedTime).total_seconds() / 3600

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

def normalizeCount(count: int) -> float:
    # we doing this because we want to keep things betwen 0-1 for consistency 
    return min(count, 5) / 5

def rankingAgent(signals: list) -> list:

    for signal in signals:
        #get give the value of the key
        count = signal.get("count", 1)

        #make sure you use the same spelling for this???
        impactScore = signal.get("impactScore", 0)
        relevanceScore = signal.get("relevanceScore", 0)
        fetchedAt = signal.get("fetched_at")

        normalizeCountVal = normalizeCount(count)
        recencyScore = getRecencyScore(fetchedAt)

        # this are not the perfect percent weightage it depends on what behavior do we want?
        score = ((normalizeCountVal * 0.30) + (recencyScore * 0.25) + (impactScore * 0.30) + (relevanceScore * 0.15))

        signal["score"] = round(score, 4)

    # this will take the score from the dict and sort
    rankedSignals = sorted(signals, key=lambda x: x["score"], reverse=True)
    return rankedSignals