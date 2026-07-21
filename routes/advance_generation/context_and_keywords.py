from fastapi import APIRouter, HTTPException
from typing import List, Optional

import requests

from schema.query_schema import (
    ContextUpdateRequest,
    ContextUpdateResponse,
)

from service.serapi.serpapi_context import fetch_ai_mode_context
from service.serapi.google_service import fetch_keywords_from_api
from service.keywords.mistral_topic_describer import generate_topic_description
from service.keywords.advance_keywords_search import keywords_mistral

from logs import logger


model_context_router = APIRouter(
    tags=["Context API"],
    responses={404: {"description": "Not found"}},
)

# =====================================================
# SIMPLE CACHE
# =====================================================

context_cache = {}


@model_context_router.post(
    "/agent/topic/model-update",
    response_model=ContextUpdateResponse,
)
def update_context(request: ContextUpdateRequest):

    topic = request.topic.strip()

    if not topic:
        raise HTTPException(status_code=400, detail="topic is required")

    want_context = request.update_context
    want_keywords = request.update_keywords

    # =====================================================
    # RESOLVE FLAGS
    # neither sent -> full run (both)
    # one sent     -> the other is False
    # =====================================================

    if want_context is None and want_keywords is None:
        want_context = True
        want_keywords = True
    else:
        want_context = bool(want_context)
        want_keywords = bool(want_keywords)

    if not want_context and not want_keywords:
        raise HTTPException(
            status_code=400,
            detail="set update_context and/or update_keywords to true",
        )

    logger.info(
        f"Request for topic: {topic} "
        f"(context={want_context}, keywords={want_keywords})"
    )

    cache_key = topic.lower()

    # =====================================================
    # CACHE HIT (only for full runs)
    # =====================================================

    if want_context and want_keywords and cache_key in context_cache:
        logger.info(f"Returning cached context for: {topic}")
        return context_cache[cache_key]

    topic_description = ""
    examples = []
    keywords: List[str] = []
    description_context = request.context_source or ""

    # =====================================================
    # FETCH CONTEXT (only if needed and not supplied)
    # =====================================================

    need_fetch = want_context or (want_keywords and not description_context)

    if need_fetch:

        logger.info(f"Fetching AI Mode context for: {topic}")

        ai_context = fetch_ai_mode_context(topic)

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

    if want_context:

        rubric = generate_topic_description(
            topic=topic,
            context=description_context,
        )

        topic_description = rubric["topic_description"]
        examples = rubric["examples"]

        logger.info("Topic description generated")

    # =====================================================
    # GENERATE KEYWORDS (from context_source)
    # =====================================================

    if want_keywords:

        logger.info(f"Generating keywords for topic: {topic}")

        try:
            keywords = keywords_mistral(topic, context_source=description_context)
        except requests.Timeout:
            logger.error(f"Mistral timed out for topic '{topic}'")
            raise HTTPException(status_code=504, detail="Keyword model timed out")
        except requests.RequestException as e:
            logger.error(f"Mistral unreachable for topic '{topic}': {e}")
            raise HTTPException(status_code=502, detail="Keyword model unreachable")
        except Exception as e:
            logger.error(f"Keyword generation failed for topic '{topic}': {e}")
            raise HTTPException(status_code=500, detail="Keyword generation failed")

        keywords = list(
            dict.fromkeys([k.strip() for k in keywords if k and k.strip()])
        )

        if not keywords:
            logger.error(f"Model returned no usable keywords for topic: {topic}")
            raise HTTPException(status_code=422, detail="Model returned no usable keywords")

        logger.info(f"Generated {len(keywords)} keywords for topic: {topic}")

    # =====================================================
    # RESPONSE
    # =====================================================

    response = ContextUpdateResponse(
        topic_description=topic_description,
        examples=examples,
        context_source=description_context,
        keywords=keywords,
    )

    # =====================================================
    # SAVE CACHE (only full runs)
    # =====================================================

    if want_context and want_keywords:
        context_cache[cache_key] = response

    logger.info(f"Completed request for topic: {topic}")

    return response