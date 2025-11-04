from fastapi import FastAPI

from app.api.v1.passenger import router as passenger_router

api_version = "v1"

app_v1 = FastAPI()
app_v1.include_router(passenger_router)
