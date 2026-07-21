from logs import logger
import requests
import re
from utils.asci_helper import is_ascii
from config.env_load import MISTRAL_API_IP

def expand_keywords_mistral(topic, context="", model_url=f"http://{MISTRAL_API_IP}:11434/api/generate"):
    """Generate refined keywords using Mistral model with context."""
    english_prompt = f"""
    You are a keyword generator for social media monitoring.

    Task:
    - The user query is: "{topic}"
    - Context from news or API: "{context}"

    Instructions:
    - Always generate keywords, hashtags, or short phrases that are **specific to India or India’s perspective** on this topic.
    - If the query is global (like Trump tariff, Climate change, Ukraine war), localize it to **India’s relevance** (e.g., "Trump India tariff", "India-US trade war", "India climate policy").
    - Output 10 to 15 unique keywords or hashtags commonly used on Indian social media (Twitter/X, Instagram, Facebook).
    - Do not translate, do not explain. Only return one keyword or hashtag per line.    
    
    """
    indian_prompt = f"""
    You are a keyword generator for social media monitoring in India.

    Task:
    - The user query is: "{topic}"
    - Context from news or API: "{context}"

    Instructions:
    - Always generate 15 to 20 keywords, hashtags, or short phrases that are **specific to India or India’s perspective** on this topic.
    - If the input query is in an Indian language (Hindi, Tamil, Bengali, etc.), generate most keywords in that language and some in English.
    - Make sure outputs are the kind of words, hashtags, or phrases actually used on Indian social media (Twitter/X, Facebook, Instagram).
    - Do NOT translate the query into another language.
    - Only return one keyword/hashtag per line, no explanations.
    """

    logger.info(f"Generating keywords for topic: {topic}")
    prompt = english_prompt if is_ascii(topic) else indian_prompt

    payload = {"model": "mistral-small3.1:latest", "prompt": prompt, "stream": False}
    logger.info(f"Sending request to Mistral model for topic: {topic}")

    response = requests.post(model_url, json=payload)
    result = response.json()['response']
    keywords = []
    for line in result.split("\n"):
        line = line.strip()
        if line:
            cleaned = re.sub(r"^\d+[\.\-\)\s]*", "", line)
            cleaned = re.sub(r"\(.*?\)|\[.*?\]", "", cleaned)
            keywords.append(cleaned.strip('"').strip("'").strip())
    return keywords
