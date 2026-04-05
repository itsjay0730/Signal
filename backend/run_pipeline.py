import time
import json
import logging
from datetime import datetime
import schedule

from pipelines.news.fetch_news import fetch_news


# ==============================
# CONFIG
# ==============================
FETCH_INTERVAL_HOURS = 3
OUTPUT_DIR = "data"

# ==============================
# LOGGING SETUP
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ==============================
# JOB FUNCTION
# ==============================
def run_pipeline():
    logger.info("Starting news fetch pipeline...")

    try:
        data = fetch_news()
        count = len(data)

        logger.info(f"Fetched {count} items")

        # create filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_DIR}/data_{timestamp}.json"

        # ensure directory exists
        import os
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # save data
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved output → {filename}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")


# ==============================
# SCHEDULER
# ==============================
def start_scheduler():
    logger.info(f"Scheduler started (every {FETCH_INTERVAL_HOURS} hours)")

    # run every X hours
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