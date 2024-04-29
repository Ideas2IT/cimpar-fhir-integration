from fastapi import FastAPI
from A01.routers.router import patient_router

app = FastAPI()

app.include_router(patient_router)