from fastapi import APIRouter
router = APIRouter()

# Root route
@router.get("/")
def root():
    return {"message": "Signal backend running"}

# Just to check the connections
@router.get("/signals")
def get_signals():
    return {
        "signals": [
            {
                "id": 1,
                "title": "AI Agents trending",
                "score": 9.2,
                "trend": "up"
            },
            {
                "id": 2,
                "title": "Rust adoption rising",
                "score": 8.8,
                "trend": "up"
            }
        ]
    }

# Get single signal
@router.get("/signals/{signal_id}")
def get_signal(signal_id: int):
    return {
        "id": signal_id,
        "title": "Sample Signal",
        "summary": "This is a test signal",
        "why_it_matters": "Important for AI space"
    }