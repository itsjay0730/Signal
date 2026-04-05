# import time
# import schedule
# import json
# from datetime import datetime

# from pipelines.news.fetch_news import fetch_news


# def job():
#     print("\n==============================")
#     print(f"⏰ Running job at {datetime.now()}")
#     print("==============================")

#     try:
#         data = fetch_news()

#         print(f"✅ Fetched {len(data)} items")

#         # save to file (for now)
#         filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

#         with open(filename, "w") as f:
#             json.dump(data, f, indent=2)

#         print(f"💾 Saved to {filename}")

#     except Exception as e:
#         print("❌ Error:", e)


# # run every 3 hours
# schedule.every(3).hours.do(job)

# # run once immediately
# job()

# # keep running
# while True:
#     schedule.run_pending()
#     time.sleep(60)