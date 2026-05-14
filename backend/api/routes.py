from fastapi import APIRouter
from database.db import get_all_signals, get_all_internships

router = APIRouter()

# Root route
@router.get("/")
def root():
    return {"message": "Signal backend running"}

#future endpoint for the frontend
@router.get("/signals")
def get_signals():
    signals = get_all_signals()
    return {"signals": signals}

@router.get("/internships")
def get_internships():
    internships = get_all_internships()
    return {"internships": internships}

