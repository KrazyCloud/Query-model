# serpapi_context.py
import re
import serpapi
from logs import logger
from config.env_load import SERPAPI_API_KEY


def _clean(snippet: str) -> str:
    """Strip trailing source tags like 'Wikipedia +4' / 'YouTube·FRANCE 24 +3'."""
    return re.sub(r"\s*[A-Za-z·.\s]+\+\d+\s*$", "", snippet).strip()


def fetch_ai_mode_context(topic: str) -> str:
    """
    Pull grounding context for a topic from Google AI Mode via SerpAPI.
    Flattens text_blocks (paragraphs, headings, lists) into plain prose.
    Returns "" on any failure so the pipeline can fall back.c
    """
    try:
        logger.info(f"Fetching AI-mode context for topic: {topic}")
        client = serpapi.Client(api_key=SERPAPI_API_KEY)
        results = client.search({
            "engine": "google_ai_mode",
            "q": f"What is {topic}"
        })

        blocks = results.get("text_blocks", [])
        parts = []
        for block in blocks:
            btype = block.get("type")
            if btype in ("paragraph", "heading"):
                snippet = block.get("snippet", "").strip()
                if snippet:
                    parts.append(_clean(snippet))
            elif btype == "list":
                for item in block.get("list", []):
                    snippet = item.get("snippet", "").strip()
                    if snippet:
                        parts.append("- " + _clean(snippet))

        context = "\n".join(parts)
        logger.info(f"AI-mode context length: {len(context)} for topic: {topic} (context: {context})")
        return context
    except Exception:
        logger.error(f"Error fetching AI-mode context for topic: {topic}")
        return ""