from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.basic.advance_query_api import query_router
from routes.basic.context_update_api import context_router
from routes.advance_generation.advance_keyword_api import update_keywords_router
from routes.advance_generation.context_and_keywords import model_context_router
from routes.topic_orchestrator import topic_orchestrator_router

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
app.include_router(update_keywords_router)
app.include_router(model_context_router)
app.include_router(topic_orchestrator_router)