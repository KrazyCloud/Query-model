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
   - key actions and events that shape how people react (e.g. police action, detentions, closures, court orders, official statements). Say who describes an action in which way, e.g. "police detained them for an unpermitted gathering"
   - how to read posts about related actors: say whether criticizing or praising each actor's SPECIFIC conduct in this topic (e.g. the police response, the voter list revision) typically signals support or opposition toward the topic. Do not generalize to unrelated praise or criticism of the same actor.
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
- Do not give your own opinion, judge any side, or say who is right or wrong.
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



def _call_mistral(prompt, max_tokens=800, model_url=None):
    url = model_url or f"http://{MISTRAL_API_IP}:8000/v1/chat/completions"
    payload = {
        "model": "mistralai/Mistral-Small-3.1-24B-Instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
        "stream": False,
    }
    response = requests.post(url, json=payload, timeout=180)
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    return json.loads(match.group(0) if match else raw)


def generate_report_overview(topic, context=""):
    """
    Neutral, reader-facing overview for reports (NOT for the classifier).
    Returns {"report_overview": str, "info_used": [str, ...]}.
    """
    prompt = f"""
You are writing a short, neutral background section for a social media analysis report about India.

Topic: "{topic}"
News / API context: "{context}"

Produce a JSON object with exactly two keys:

1. "report_overview": 4-6 sentences, plain prose, covering:
   - what the topic is, when it is happening, and who is involved (name every person, group and place in the context)
   - why it is happening (the stated trigger)
   - the main sides and their arguments, each attributed ("critics say...", "the government states...")
   - key events, actions and official or public statements that shape the discussion, saying who describes them and how

2. "info_used": an array of 4-8 short strings. Each string is one specific fact from the context that the overview relies on (e.g. "Police detained hundreds of protesters", "Home Minister rejected the claims as disinformation"). Only list facts that actually appear in the context.

Rules:
- Use only the provided context. No outside knowledge.
- Do not state allegations or disputed claims as facts. Attribute them to the side making them.
- Do NOT mention classification, labels, stance, sentiment, hashtags, traps, or how to read posts.
- Do not give your own opinion, judge any side, or say who is right or wrong.
- Ignore non-content lines in the context (e.g. "Watch this video...").
- Output ONLY the raw JSON object. No markdown, no preamble.
"""
    logger.info(f"Generating report overview for: {topic}")
    try:
        parsed = _call_mistral(prompt, max_tokens=800)
        return {
            "report_overview": parsed.get("report_overview", "").strip(),
            "info_used": [s for s in parsed.get("info_used", []) if isinstance(s, str)],
        }
    except Exception as e:
        logger.error(f"Report overview failed for '{topic}': {e}")
        return {"report_overview": "", "info_used": []}