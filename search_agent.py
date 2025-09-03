from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from itertools import combinations
import re
from urllib.parse import quote
from fastapi.middleware.cors import CORSMiddleware

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class QueryRequest(BaseModel):
    topic: str

class QueryResponse(BaseModel):
    keywords: List[str]
    boolean_query: str

# ---------- Helpers ----------
def is_ascii(s: str) -> bool:
    indian_script_patterns = [
        r'[\u0900-\u097F]',  # Devanagari
        r'[\u0B80-\u0BFF]',  # Tamil
        r'[\u0C00-\u0C7F]',  # Telugu
        r'[\u0C80-\u0CFF]',  # Kannada
        r'[\u0D00-\u0D7F]',  # Malayalam
        r'[\u0A80-\u0AFF]',  # Gujarati
        r'[\u0A00-\u0A7F]',  # Gurmukhi
        r'[\u0980-\u09FF]',  # Bengali / Assamese
        r'[\u0B00-\u0B7F]',  # Odia
    ]
    for pattern in indian_script_patterns:
        if re.search(pattern, s):
            return False
    return all(ord(c) < 128 for c in s if c.isalpha())


def fetch_keywords_from_api(topic: str, api_url="http://172.31.32.224:9001/search-keywords"):
    """Fetch initial keywords from external API. Return [] if not found."""
    try:
        response = requests.get(f"{api_url}?keyword={quote(topic)}")
        if response.status_code == 404:  # API returns not found
            return [], ""
        response.raise_for_status()
        data = response.json()
        news_content = data.get("news", "")
        if not news_content:  # API returned but no useful content
            return [], ""
        keywords = re.findall(r'\b[A-Z][a-zA-Z0-9&]+\b', news_content)
        keywords = list(dict.fromkeys(keywords))
        return keywords, news_content
    except Exception:
        # Fail gracefully (instead of raising HTTPException) so pipeline can fallback
        return [], ""


def expand_keywords_mistral(topic, context="", model_url="http://localhost:11434/api/generate"):
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

    prompt = english_prompt if is_ascii(topic) else indian_prompt

    payload = {"model": "mistral-small3.1:latest", "prompt": prompt, "stream": False}
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

def build_boolean_queries(keywords, mode="OR"):
    if not keywords:
        return ""
    if mode.upper() == "OR":
        return " OR ".join([f'"{k}"' for k in keywords])
    elif mode.upper() == "AND":
        return " AND ".join([f'"{k}"' for k in keywords])
    elif mode.upper() == "COMBO":
        combos = combinations(keywords, 2)
        return [" AND ".join(c) for c in combos]



@app.post("/agent/query", response_model=QueryResponse)
def agent_pipeline(request: QueryRequest):
    topic = request.topic

    # 1️⃣ Try external API first
    initial_keywords, news_content = fetch_keywords_from_api(topic)
    print(f"Initial keywords: {len(initial_keywords)}, News content: {len(news_content)}")

    # 2️⃣ If API gave nothing, fallback to mistral without context
    if not initial_keywords and not news_content:
        refined_keywords = expand_keywords_mistral(topic)
    else:
        refined_keywords = expand_keywords_mistral(topic, context=", ".join(initial_keywords) or news_content)

    # 3️⃣ Build boolean query
    boolean_query = build_boolean_queries(refined_keywords, mode="OR")

    print(f"Completed processing for topic: {topic}, keywords: {len(refined_keywords)}")
    
    return QueryResponse(
        keywords=refined_keywords,
        boolean_query=boolean_query
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
