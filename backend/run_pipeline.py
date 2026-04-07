import time
import json
import logging
from datetime import datetime
import schedule
import os

from pipelines.news.fetch_news import fetch_news
from pipelines.news.group_dupes import group_duplicates


# ==============================
# CONFIG
# ==============================
FETCH_INTERVAL_HOURS = 3
OUTPUT_DIR = "data"

# ==============================
# LOGGING
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ==============================
# PIPELINE JOB
# ==============================
def run_pipeline():
    logger.info("Starting pipeline")

    try:
        raw_data = fetch_news()
        logger.info(f"Fetched {len(raw_data)} raw items")

        # group duplicates
        signals = group_duplicates(raw_data)
        logger.info(f"Generated {len(signals)} signals")

        # sort by importance
        signals = sorted(signals, key=lambda x: x["count"], reverse=True)

        # ensure output folder exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_DIR}/signals_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(signals, f, indent=2)

        logger.info(f"Saved signals to {filename}")

        # preview top signals
        logger.info("Top signals:")
        for s in signals[:5]:
            logger.info(f"{s['count']} | {s['title']}")

    except Exception as e:
        logger.error(f"Pipeline error: {e}")


# ==============================
# SCHEDULER
# ==============================
def start_scheduler():
    logger.info(f"Scheduler started (every {FETCH_INTERVAL_HOURS} hours)")

    schedule.every(FETCH_INTERVAL_HOURS).hours.do(run_pipeline)

    # run once immediately
    run_pipeline()

    while True:
        schedule.run_pending()
        time.sleep(60)


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    start_scheduler()