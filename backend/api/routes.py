from fastapi import APIRouter
router = APIRouter()

# Root route
@router.get("/")
def root():
    return {"message": "Signal backend running"}

#future endpoint for the frontend
@router.get("/signals")
def get_signals():
    return {"signals": []}