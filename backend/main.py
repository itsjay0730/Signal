from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Signal up and running :)"}

#Cloned the repo