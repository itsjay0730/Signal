from fastapi import FastAPI
from api.routes import router
# app = FastAPI()
# @app.get("/")
# def root():
#     return {"message": "Signal up and running :)"}

app = FastAPI()

app.include_router(router)