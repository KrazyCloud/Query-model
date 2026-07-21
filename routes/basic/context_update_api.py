from fastapi import APIRouter

from schema.query_schema import (
    ContextUpdateRequest,
    ContextUpdateResponse,
)

from service.serapi.serpapi_context import fetch_ai_mode_context
from service.serapi.google_service import fetch_keywords_from_api
from service.keywords.mistral_topic_describer import generate_topic_description

from logs import logger


context_router = APIRouter(
    tags=["Context API"],
    responses={404: {"description": "Not found"}},
)

# =====================================================
# SIMPLE CACHE
# =====================================================

context_cache = {}


@context_router.post(
    "/agent/topic/context",
    response_model=ContextUpdateResponse,
)
def update_context(request: ContextUpdateRequest):

    topic = request.topic.strip()

    logger.info(f"Received context update request for topic: {topic}")

    cache_key = topic.lower()

    # =====================================================
    # CACHE HIT
    # =====================================================

    if cache_key in context_cache:

        logger.info(f"Returning cached context for: {topic}")

        return context_cache[cache_key]

    # =====================================================
    # PRIMARY CONTEXT (AI MODE)
    # =====================================================

    logger.info(f"Fetching AI Mode context for: {topic}")

    ai_context = fetch_ai_mode_context(topic)

    # =====================================================
    # FALLBACK (GOOGLE NEWS)
    # =====================================================

    if ai_context:

        description_context = ai_context
        logger.info("Using AI Mode context")

    else:

        logger.info("AI Mode unavailable. Falling back to Google News.")

        _, news_content = fetch_keywords_from_api(topic)

        description_context = news_content

    # =====================================================
    # GENERATE TOPIC DESCRIPTION
    # =====================================================

    rubric = generate_topic_description(
        topic=topic,
        context=description_context,
    )

    logger.info("Topic description generated")

    # =====================================================
    # RESPONSE
    # =====================================================

    response = ContextUpdateResponse(
        topic_description=rubric["topic_description"],
        examples=rubric["examples"],
        context_source=description_context,
    )

    # =====================================================
    # SAVE CACHE
    # =====================================================

    context_cache[cache_key] = response

    logger.info(f"Completed context update for topic: {topic}")

    return response