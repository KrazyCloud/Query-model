from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

import requests

from service.advance_keywords_search import keywords_mistral
from logs import logger

update_keywords_router = APIRouter(
    tags=["Keyword Generation API"]
)


class UpdateKeywordsRequest(BaseModel):
    topic: str
    context_source: str = ""


class UpdateKeywordsResponse(BaseModel):
    topic: str
    keywords: List[str]


@update_keywords_router.post(
    "/update_keywords",
    response_model=UpdateKeywordsResponse
)
def update_keywords(request: UpdateKeywordsRequest):

    topic = request.topic.strip()
    context_source = request.context_source or ""

    if not topic:
        raise HTTPException(status_code=400, detail="topic is required")

    logger.info(f"Generating keywords for topic: {topic}")

    try:
        keywords = keywords_mistral(topic, context_source=context_source)
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
        dict.fromkeys(
            [k.strip() for k in keywords if k and k.strip()]
        )
    )

    if not keywords:
        logger.error(f"Model returned no usable keywords for topic: {topic}")
        raise HTTPException(status_code=422, detail="Model returned no usable keywords")

    logger.info(f"Generated {len(keywords)} keywords for topic: {topic}")

    return UpdateKeywordsResponse(topic=topic, keywords=keywords)