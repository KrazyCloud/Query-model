# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.topic_orchestrator import topic_orchestrator_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topic_orchestrator_router)