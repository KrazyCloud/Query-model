from fastapi import APIRouter
from schema.query_schema import QueryRequest, QueryResponse
from service.mistral_keyword_expander import expand_keywords_mistral
from service.google_service import fetch_keywords_from_api
from utils.query_builder import build_boolean_queries
from logs import logger

query_router = APIRouter(
    tags=["Query API"],
    responses={404: {"description": "Not found"}}
)

@query_router.post("/agent/query", response_model=QueryResponse)
def agent_pipeline(request: QueryRequest):
    topic = request.topic

    logger.info(f"Received query for topic Started: {topic}")

    # 1️⃣ Try external API first
    logger.info(f"Fetching Update News from Google API for topic: {topic}")
    initial_keywords, news_content = fetch_keywords_from_api(topic)
    logger.info(f"Initial keywords: {len(initial_keywords)}, News content: {len(news_content)}")

    # 2️⃣ If API gave nothing, fallback to mistral without context
    if not initial_keywords and not news_content:
        refined_keywords = expand_keywords_mistral(topic)
        logger.info(f"Generated keywords without context: {len(refined_keywords)}")
    else:
        refined_keywords = expand_keywords_mistral(topic, context=", ".join(initial_keywords) or news_content)
        logger.info(f"Generated keywords with context: {len(refined_keywords)}")

    # 3️⃣ Build boolean query
    boolean_query = build_boolean_queries(refined_keywords, mode="OR")

    logger.info(f"Completed processing for topic: {topic}, keywords: {len(refined_keywords)}")
    
    return QueryResponse(
        keywords=refined_keywords,
        boolean_query=boolean_query
    )