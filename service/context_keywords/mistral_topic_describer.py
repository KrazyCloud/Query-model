# mistral_topic_describer.py
import json
import re
from logs import logger
import requests
from config.env_load import MISTRAL_API_IP


def generate_topic_description(topic, context="", model_url=f"http://{MISTRAL_API_IP}:8000/v1/chat/completions"):
    """
    Generate a structured annotation rubric for a sentiment/stance classifier.
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
- Base the description on the provided context. Prefer hashtags and phrases that appear in or are directly implied by the context.
- IMPORTANT: Some movements adopt an insult as their own badge. Before assigning stance, check the context: if a seemingly-derogatory term (an animal, an insult) is used by supporters about themselves, then that language is PRO the movement, and attacks come from the opposite framing. State which case applies in the description.
- Output ONLY the raw JSON object. No markdown, no code fences, no preamble.
"""
    logger.info(f"Generating topic description rubric for: {topic}")
    payload = {
        "model": "mistralai/Mistral-Small-3.1-24B-Instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.2,
        "stream": False,
    }

    try:
        response = requests.post(model_url, json=payload, timeout=180)
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()

        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            raw = match.group(0)

        parsed = json.loads(raw)
        return {
            "topic_description": parsed.get("topic_description", "").strip(),
            "examples": parsed.get("examples", []),
        }
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse rubric JSON for topic: {topic}: {e}")
        logger.error(f"Raw model output:\n{raw}")
        return {"topic_description": "", "examples": []}
    except Exception as e:
        logger.error(f"Error generating topic description for: {topic}: {e}")
        return {"topic_description": "", "examples": []}