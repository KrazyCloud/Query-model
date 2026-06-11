import json
import re
from logs import logger
import requests
from config.env_load import MISTRAL_API_IP


def generate_topic_description(topic, context="", model_url=f"http://{MISTRAL_API_IP}:11434/api/generate"):
    """
    Generate a structured annotation rubric for a sentiment/stance classifier:
    - topic_description: analyst note covering stance landscape + traps
    - examples: few-shot demonstrations with the multi-label schema
    Returns {"topic_description": str, "examples": [...]}.
    """
    prompt = f"""
You are an analyst writing a labeling rubric for a social media sentiment and stance classifier focused on India.

Topic: "{topic}"
News / API context: "{context}"

Produce a JSON object with exactly two keys:

1. "topic_description": a 3-5 sentence note that explains:
   - what the topic is and why it matters on Indian social media
   - the stance landscape: who supports it, who opposes it, and what language/hashtags each side uses
   - any traps for a classifier — e.g. sarcasm, reclaimed insults, in-group symbols, or words that mean the opposite of their surface tone in this context

2. "examples": an array of 3 short demonstration items. Each must be an object with:
   - "text": a realistic example post (may mix Hindi/English as seen on Indian social media)
   - "relevance": "on_topic" or "off_topic"
   - "stance": "support", "oppose", or "neutral"
   - "sentiment": "positive", "negative", or "neutral"
   - "spam": true or false
   Include at least one off_topic/spam example and one example that demonstrates a trap from the description.

Rules:
- Base the description on the provided context. Do not invent specific named people or hashtags that are not implied by the topic or context.
- Output ONLY the raw JSON object. No markdown, no code fences, no preamble.
"""
    logger.info(f"Generating topic description rubric for: {topic}")
    payload = {"model": "mistral-small3.1:latest", "prompt": prompt, "stream": False}

    try:
        response = requests.post(model_url, json=payload, timeout=180)
        response.raise_for_status()
        raw = response.json()["response"].strip()

        # Strip code fences if the model added them anyway
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())

        # Grab the outermost JSON object in case of stray text
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            raw = match.group(0)

        parsed = json.loads(raw)
        return {
            "topic_description": parsed.get("topic_description", "").strip(),
            "examples": parsed.get("examples", []),
        }
    except json.JSONDecodeError:
        logger.error(f"Failed to parse rubric JSON for topic: {topic}")
        return {"topic_description": "", "examples": []}
    except Exception:
        logger.error(f"Error generating topic description for: {topic}")
        return {"topic_description": "", "examples": []}