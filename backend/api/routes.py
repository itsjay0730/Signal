from fastapi import APIRouter
router = APIRouter()

# Root route
@router.get("/")
def root():
    return {"message": "Signal backend running"}
