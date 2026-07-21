# advance_keywords_search.py

from logs import logger
import requests
import re
from utils.asci_helper import is_ascii
from config.env_load import MISTRAL_API_IP

MISTRAL_MODEL = "mistral-small3.1:latest"
REQUEST_TIMEOUT_SECONDS = 60
MAX_CONTEXT_CHARS = 2000  # truncate long context_source so it doesn't drown out instructions


def _build_prompt(topic: str, context: str, indian_language: bool) -> str:
    """Single prompt builder, anchored on extracting specifics from context."""

    language_instruction = (
        "- If the input query is in an Indian language (Hindi, Tamil, Bengali, etc.), "
        "generate most keywords in that language and some in English. Do NOT translate "
        "the query into another language."
        if indian_language else
        "- Write keywords in English."
    )

    keyword_count = "15-20" if indian_language else "12-18"

    return f"""
    You will be given the name of a specific real-world event/topic, and a background
    explanation of what that event/topic actually is -- who is involved, what happened,
    where, and any current status. Your job is NOT to summarize this. Your job is to
    understand the event well enough to think like a person who wants to find social
    media posts (Twitter/X, Instagram, Facebook) that people are writing about THIS
    specific event right now.

    Topic name: "{topic}"
    Background on this specific event/topic: "{context}"

    Instructions:
    - Read the background and identify the specific people, organizations, places,
      case/policy names, dates, and sub-events it mentions. These are the anchors
      real posts about this event will actually use.
    - Produce {keyword_count} search terms that someone would type into a platform
      search bar to find posts discussing THIS event -- not the general subject area.
      Do NOT output vague single words (e.g. not just "India" or "crime" alone) --
      every keyword must be traceable to a specific detail in the topic or background.
    - Include a mix of: exact search phrases (2-5 words), hashtags, and named-entity
      combinations (e.g. "<Person Name> <Place/Case>", "#<Event/Person><Year>").
    - Include terms for BOTH sides of any public debate/reaction visible in the
      background (e.g. supporting and opposing hashtags), if applicable -- real
      discussion of an event usually splits into camps, and search terms should
      surface all of it, not just one side.
    - Localize to India's angle unless the background is already India-specific.
    {language_instruction}
    - Only output strings someone would actually type into a platform search bar.
    - Output one keyword/phrase per line. No numbering, no explanation.
    """


def keywords_mistral(topic: str, context_source: str = "", model_url: str = None) -> list[str]:
    """
    Generate social-search keywords for `topic`, using `context_source` --
    background info describing what this specific event/topic actually is --
    to anchor keywords on real, specific details rather than generic tags.
    """

    if model_url is None:
        model_url = f"http://{MISTRAL_API_IP}:11434/api/generate"

    truncated_context = (context_source or "")[:MAX_CONTEXT_CHARS]
    indian_language = not is_ascii(topic)
    prompt = _build_prompt(topic, truncated_context, indian_language)

    payload = {"model": MISTRAL_MODEL, "prompt": prompt, "stream": False}

    logger.info(f"Requesting keywords from Mistral for topic: {topic}")

    try:
        response = requests.post(model_url, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        result = response.json()["response"]
    except requests.Timeout:
        logger.error(f"Mistral request timed out for topic: {topic}")
        raise
    except requests.RequestException as e:
        logger.error(f"Mistral request failed for topic '{topic}': {e}")
        raise
    except (KeyError, ValueError) as e:
        logger.error(f"Unexpected Mistral response shape for topic '{topic}': {e}")
        raise

    keywords = []
    for line in result.split("\n"):
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^\d+[\.\-\)\s]*", "", line)
        cleaned = re.sub(r"\(.*?\)|\[.*?\]", "", cleaned)
        cleaned = cleaned.strip('"').strip("'").strip()
        if cleaned:
            keywords.append(cleaned)

    logger.info(f"Generated {len(keywords)} raw keywords for topic: {topic}")
    return keywords