from fastapi import APIRouter

from schema.query_schema import QueryRequest, QueryResponse

from service.mistral_keyword_expander import expand_keywords_mistral
from service.google_service import fetch_keywords_from_api

from utils.query_builder import build_boolean_queries
from utils.social_search_builder import generate_social_search_links
from service.serpapi_context import fetch_ai_mode_context
from service.mistral_topic_describer import generate_topic_description

from logs import logger

query_router = APIRouter(
    tags=["Query API"],
    responses={404: {"description": "Not found"}}
)

# =====================================================
# SIMPLE CACHE
# =====================================================

search_cache = {}


@query_router.post(
    "/agent/query",
    response_model=QueryResponse
)
def agent_pipeline(request: QueryRequest):

    topic = request.topic.strip()

    logger.info(
        f"Received query for topic: {topic}"
    )

    cache_key = topic.lower()

    # =====================================================
    # CACHE HIT
    # =====================================================

    if cache_key in search_cache:

        logger.info(
            f"Returning cached result for: {topic}"
        )

        return search_cache[cache_key]

    # =====================================================
    # GOOGLE FETCH
    # =====================================================

    logger.info(
        f"Fetching Google API data for topic: {topic}"
    )

    initial_keywords, news_content = fetch_keywords_from_api(
        topic
    )

    logger.info(
        f"Initial keywords: {len(initial_keywords)}, "
        f"News content length: {len(news_content)}"
    )

    # =====================================================
    # KEYWORD GENERATION
    # =====================================================

    if not initial_keywords and not news_content:

        logger.info(
            "Using fallback keyword generation"
        )

        refined_keywords = expand_keywords_mistral(
            topic
        )

    else:

        logger.info(
            "Using contextual keyword generation"
        )

        refined_keywords = expand_keywords_mistral(
            topic,
            context=", ".join(initial_keywords)
            or news_content
        )

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    refined_keywords = list(
        dict.fromkeys(
            [
                keyword.strip()
                for keyword in refined_keywords
                if keyword and keyword.strip()
            ]
        )
    )

    logger.info(
        f"Final keywords count: "
        f"{len(refined_keywords)}"
    )

    # =====================================================
    # BOOLEAN QUERY
    # =====================================================

    boolean_query = build_boolean_queries(
        refined_keywords,
        mode="OR"
    )

    logger.info(
        "Boolean query generated"
    )

    # =====================================================
    # QUERY TEMPLATES
    # =====================================================

    social_links = generate_social_search_links()

    logger.info(
        "Social query templates generated"
    )

    # =====================================================
    # TOPIC DESCRIPTION RUBRIC
    # =====================================================

    ai_context = fetch_ai_mode_context(topic)

    description_context = (
        ai_context
        or news_content
        or ", ".join(initial_keywords)
    )

    rubric = generate_topic_description(topic, context=description_context)

    logger.info("Topic description rubric generated")


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    response = QueryResponse(
        keywords=refined_keywords,
        boolean_query=boolean_query,
        social_links=social_links,
        topic_description=rubric["topic_description"],
        examples=rubric["examples"],
        context_source=description_context
    )

    # =====================================================
    # SAVE CACHE
    # =====================================================

    search_cache[cache_key] = response

    logger.info(
        f"Completed processing for topic: {topic}, "
        f"keywords: {len(refined_keywords)}"
    )

    return response