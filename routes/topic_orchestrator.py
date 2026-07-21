from fastapi import APIRouter, HTTPException
from logs import logger
from schema.query_schema import ContextUpdateRequest, ContextUpdateResponse, ContextMode
from service.serapi.serpapi_context import fetch_ai_mode_context
from service.context_keywords.mistral_topic_describer import generate_topic_description
from service.context_keywords.advance_keywords_search import keywords_mistral

topic_orchestrator_router = APIRouter(prefix="/topic", tags=["topic-orchestration"])

REQUIRED_EXAMPLE_KEYS = {"text", "relevance", "stance", "sentiment", "spam"}

@topic_orchestrator_router.post("/context", response_model=ContextUpdateResponse)
def update_topic_context(request: ContextUpdateRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="topic must not be empty")

    mode = request.mode
    logger.info(f"Context orchestration for '{topic}' (mode={mode.value})")

    topic_description = ""
    examples = []
    description_context = request.context_source.strip()

    if mode in (ContextMode.FULL, ContextMode.CONTEXT_ONLY):
        serp_context = fetch_ai_mode_context(topic)
        if not serp_context:
            logger.error(f"AI-mode context empty for '{topic}'")
            raise HTTPException(status_code=502, detail="search context fetch failed")

        rubric = generate_topic_description(topic, serp_context)
        topic_description = rubric.get("topic_description", "")

        if not topic_description:
            logger.error(f"Rubric generation returned empty description for: {topic}")
            raise HTTPException(status_code=502, detail="topic description generation failed")

        examples = [
            e for e in rubric.get("examples", [])
            if isinstance(e, dict) and REQUIRED_EXAMPLE_KEYS <= e.keys()
        ]

        example_lines = "\n".join(
            f"- {e['text'].strip()}" for e in examples if str(e.get("text", "")).strip()
        )
        description_context = topic_description
        if example_lines:
            description_context += f"\n\nExample posts on this topic:\n{example_lines}"

    keywords = []
    if mode in (ContextMode.FULL, ContextMode.KEYWORDS_ONLY):
        if not description_context:
            logger.error(f"No context available for keyword generation: {topic}")
            raise HTTPException(status_code=400, detail="context_source required for mode=keywords")

        try:
            keywords = keywords_mistral(topic, description_context)
        except Exception as e:
            logger.error(f"Keyword stage failed for '{topic}': {e}")
            raise HTTPException(status_code=502, detail="keyword generation failed")

    return ContextUpdateResponse(
        topic_description=topic_description,
        examples=examples,
        context_source=description_context,
        keywords=keywords,
    )