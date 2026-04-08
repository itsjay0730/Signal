
from datetime import datetime, timezone

def get_recency_score(fetched_at: str) -> float:
    """
    Convert timestamp → recency score (0–1)
    """
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
    

# def ranking_agent():
