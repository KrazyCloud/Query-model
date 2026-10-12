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
#     prompt = f"""
# You are an analyst writing a labeling rubric for a social media sentiment and stance classifier focused on India.

# Topic: "{topic}"
# News / API context: "{context}"

# Produce a JSON object with exactly two keys:

# 1. "topic_description": a 3-5 sentence note that explains:
#    - what the topic is and why it matters on Indian social media
#    - the stance landscape: who supports it, who opposes it, and what language/hashtags each side uses
#    - any traps for a classifier — e.g. sarcasm, reclaimed insults, in-group symbols, or words that mean the opposite of their surface tone in this context

# 2. "examples": an array of 3 short demonstration items. Each must be an object with:
#    - "text": a realistic example post (may mix Hindi/English as seen on Indian social media)
#    - "relevance": "on_topic" or "off_topic"
#    - "stance": "support", "oppose", or "neutral"
#    - "sentiment": "positive", "negative", or "neutral"
#    - "spam": true or false
#    Include at least one off_topic/spam example and one example that demonstrates a trap from the description.

# Rules:
# - Base the description on the provided context. Prefer hashtags and phrases that appear in or are directly implied by the context.
# - IMPORTANT: Some movements adopt an insult as their own badge. Before assigning stance, check the context: if a seemingly-derogatory term (an animal, an insult) is used by supporters about themselves, then that language is PRO the movement, and attacks come from the opposite framing. State which case applies in the description.
# - Output ONLY the raw JSON object. No markdown, no code fences, no preamble.
# """

    prompt = f"""
You are an analyst writing a neutral labeling rubric for a social media sentiment and stance classifier focused on India.

Topic: "{topic}"
News / API context: "{context}"

LABEL DEFINITIONS (very important):
Both labels are measured toward the TOPIC itself ("{topic}"), not the emotional tone of the post.
- stance: "support" = the post backs the topic or its cause (even if angry at its opponents); "oppose" = the post criticizes or dismisses the topic or its cause (even if polite); "neutral" = no clear position (news reporting, questions, off-topic).
- sentiment: "positive" = favorable toward the topic; "negative" = unfavorable toward the topic; "neutral" = neither.
- Normally support = positive, oppose = negative, neutral = neutral. Only deviate if the post clearly shows a mixed case, and then explain it in the description.

Produce a JSON object with exactly two keys:

1. "topic_description": a 5-8 sentence note that covers ALL of the following, using only the context:
   - what the topic is, when it is happening, and why it matters in India
   - what "support" and "oppose" mean for this specific topic, in one line
   - the stated trigger or reason for the topic, and every named person and place in the context (including founders and leaders), each with its side or role
   - the main sides and their arguments, given equal weight and attributed to each side (e.g. "critics say...", "the government states..."). If one side's description of events is disputed (e.g. police calling a gathering "illegal"), attribute it to that side
   - key actions and events that shape how people react (e.g. police action, detentions, closures, court orders, official statements)
   - how to read posts about related actors: say whether criticizing or praising each actor (e.g. police, the Election Commission, the government) typically signals support or opposition toward the topic
   - hashtags or phrases each side uses ONLY if they appear in the context; otherwise write "no specific hashtags stated in context"
   - classifier traps ONLY if the context shows them. Check specifically: (a) a movement, group or hashtag whose NAME contains a word that would normally be an insult or negative term (say it is a name, not an insult, and that posts using it may be supportive); (b) sarcasm or in-group symbols; (c) words whose tone is reversed in this context. List every trap found. Write "no specific traps identified" ONLY if you found none. Never write both.

2. "examples": an array of 3 short demonstration items. Each must be an object with:
   - "text": a realistic example post (may mix Hindi/English)
   - "relevance": "on_topic" or "off_topic"
   - "stance": "support", "oppose", or "neutral"
   - "sentiment": "positive", "negative", or "neutral"
   - "spam": true or false
   Include at least one off_topic/spam example, and include examples from both sides, not just one. If the description names a trap, one example should show it. Use only names and terms found in the context.

Rules:
- Use only facts in the provided context. Do not add outside knowledge or invent hashtags, slogans, or slang.
- Do not state contested allegations as facts. Attribute them to the side that makes them.
- If the context describes an action against one side (arrests, bans, crackdowns), say that posts criticizing the action usually support the affected side.
- If a seemingly derogatory term is used by supporters about themselves in the context, say so explicitly. Do not assume this unless the context shows it.
- Ignore any non-content lines in the context (e.g. "Watch this video...").
- Output ONLY the raw JSON object. No markdown, no code fences, no preamble.
"""
    
    logger.info(f"Generating topic description rubric for: {topic}")
    payload = {
        "model": "mistralai/Mistral-Small-3.1-24B-Instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        # "max_tokens": 1024,
        # "temperature": 0.2,
        "max_tokens":1500,
        "temperature": 0.0,
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