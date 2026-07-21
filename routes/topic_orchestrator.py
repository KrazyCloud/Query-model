from fastapi import APIRouter, HTTPException
from logs import logger
from schema.query_schema import (
    ContextUpdateRequest,
    ContextUpdateResponse,
    ContextMode,
)
from service.serapi.serpapi_context import fetch_ai_mode_context
from service.context_keywords.mistral_topic_describer import (
    generate_topic_description,
)
from service.context_keywords.advance_keywords_search import (
    keywords_mistral,
)

topic_orchestrator_router = APIRouter(
    prefix="/topic",
    tags=["topic-orchestration"],
)

REQUIRED_EXAMPLE_KEYS = {
    "text",
    "relevance",
    "stance",
    "sentiment",
    "spam",
}


@topic_orchestrator_router.post(
    "/context",
    response_model=ContextUpdateResponse,
)
def update_topic_context(request: ContextUpdateRequest):

    topic = request.topic.strip()

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="topic must not be empty",
        )

    logger.info(
        f"Context orchestration for '{topic}' (mode={request.mode.value})"
    )

    serp_context = ""
    topic_description = ""
    examples = []
    keywords = []

    # --------------------------------------------------
    # FULL / CONTEXT_ONLY
    # --------------------------------------------------

    if request.mode in (
        ContextMode.FULL,
        ContextMode.CONTEXT_ONLY,
    ):

        serp_context = fetch_ai_mode_context(topic)

        if not serp_context:
            logger.error(f"AI-mode context empty for '{topic}'")
            raise HTTPException(
                status_code=502,
                detail="search context fetch failed",
            )

        rubric = generate_topic_description(
            topic,
            serp_context,
        )

        topic_description = rubric.get(
            "topic_description",
            "",
        ).strip()

        if not topic_description:
            logger.error(
                f"Topic description generation failed for '{topic}'"
            )
            raise HTTPException(
                status_code=502,
                detail="topic description generation failed",
            )

        examples = [
            e
            for e in rubric.get("examples", [])
            if isinstance(e, dict)
            and REQUIRED_EXAMPLE_KEYS <= e.keys()
        ]

    # --------------------------------------------------
    # KEYWORD GENERATION
    # --------------------------------------------------

    if request.mode in (
        ContextMode.FULL,
        ContextMode.KEYWORDS_ONLY,
    ):

        if request.mode == ContextMode.FULL:
            keyword_context = serp_context
        else:
            keyword_context = request.context_source.strip()

        if not keyword_context:
            raise HTTPException(
                status_code=400,
                detail="context_source required for keyword generation",
            )

        try:

            keywords = keywords_mistral(
                topic,
                keyword_context,
            )

        except Exception as e:
            logger.error(
                f"Keyword generation failed for '{topic}': {e}"
            )
            raise HTTPException(
                status_code=502,
                detail="keyword generation failed",
            )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return ContextUpdateResponse(
        topic_description=topic_description,
        examples=examples,
        context_source=serp_context if serp_context else request.context_source,
        keywords=keywords,
    )