from logs import logger
import requests
import re
from urllib.parse import quote
from config.env_load import GOOGLE_SERVER_IP
import os


def fetch_keywords_from_api(topic: str, api_url=f"http://{GOOGLE_SERVER_IP}:9000/google-search"):
    """Fetch initial keywords from external API. Return [] if not found."""
    try:
        logger.info(f"Fetching keywords from API for topic: {topic}")

        response = requests.get(f"{api_url}?keyword={quote(topic)}")
        if response.status_code == 404:
            logger.info(f"API returned 404 for topic: {topic}")
            return [], ""
        
        logger.info(f"API response for topic: {topic}")
        response.raise_for_status()
        data = response.json()
        news_content = data.get("news", "")
        if not news_content:  # API returned but no useful content
            logger.info(f"API returned empty news content for topic: {topic}")
            return [], ""
        keywords = re.findall(r'\b[A-Z][a-zA-Z0-9&]+\b', news_content)
        keywords = list(dict.fromkeys(keywords))
        return keywords, news_content
    except Exception:
        # Fail gracefully (instead of raising HTTPException) so pipeline can fallback
        logger.error(f"Error occurred while fetching keywords for topic: {topic}")
        return [], ""