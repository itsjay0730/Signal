from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Signal up and running :)"}

@app.get("/signals")
def get_signals():
    return {
        "signals": [
            {"id": 1, "title": "AI Agents trending", "score": 9.2},
            {"id": 2, "title": "Rust adoption rising", "score": 8.8}
        ]
    }