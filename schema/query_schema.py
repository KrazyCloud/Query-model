
# query_schema.py

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enum import Enum

class ExampleItem(BaseModel):
    text: str
    relevance: str
    stance: str
    sentiment: str
    spam: bool


class ContextUpdateResponse(BaseModel):
    topic_description: str = ""
    report_overview: str = ""          # NEW: for the report
    info_used: List[str] = []          # NEW: facts the overview was built from
    examples: List[ExampleItem] = []
    context_source: str = ""
    keywords: List[str] = []
    boolean_query: str = ""
    social_links: Dict[str, Dict[str, Dict[str, Any]]]


class ContextMode(str, Enum):
    FULL = "full"              # SerpAPI -> rubric -> keywords
    CONTEXT_ONLY = "context"   # SerpAPI -> rubric, no keywords
    KEYWORDS_ONLY = "keywords" # use supplied context_source -> keywords


class ContextUpdateRequest(BaseModel):
    topic: str
    mode: ContextMode = ContextMode.FULL
    context_source: str = ""