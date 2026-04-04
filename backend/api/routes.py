from fastapi import APIRouter
from pipelines.news.fetch_news import fetch_hacker_news
router = APIRouter()

# Root route
@router.get("/")
def root():
    return {"message": "Signal backend running"}

#future endpoint for the frontend
@router.get("/signals")
def get_signals():
    return {"signals": []}

#test the endpoint
@router.get("/test-hn")
def test_hn():
    data = fetch_hacker_news()
    return {"count": len(data), "data": data[:5]}