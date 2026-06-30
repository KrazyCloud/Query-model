from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.advance_query_api import query_router
from routes.context_update_api import context_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)
app.include_router(context_router)