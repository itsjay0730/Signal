from pipelines.news.news_pipeline import run_news_pipeline
from pipelines.internships.internship_pipeline import run_internship_pipeline
from concurrent.futures import ThreadPoolExecutor

#Uses thread executor to concurrently
#call both pipelines 
def run_all_pipelines():
    with ThreadPoolExecutor() as executor:
        newsThread = executor.submit(run_news_pipeline)
        internshipThread = executor.submit(run_internship_pipeline)

        try:
            news = newsThread.result()
            internships = internshipThread.result()
        except Exception as e:
            print(f"Pipeline error: {e}")
            raise

    return {"news": news, "internships": internships}
