from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    topic: str

class ExampleItem(BaseModel):
    text: str
    relevance: str
    stance: str
    sentiment: str
    spam: bool

class QueryResponse(BaseModel):
    keywords: List[str]
    boolean_query: str
    social_links: Dict[str, Dict[str, Dict[str, Any]]]
    topic_description: str = ""
    examples: List[ExampleItem] = []
    context_source: str = ""

class ExampleItem(BaseModel):
    text: str
    relevance: str
    stance: str
    sentiment: str
    spam: bool

class ContextUpdateRequest(BaseModel):
    topic: str
    update_context: Optional[bool] = None
    update_keywords: Optional[bool] = None
    context_source: str = ""


class ContextUpdateResponse(BaseModel):
    topic_description: str = ""
    examples: List[ExampleItem] = []
    context_source: str = ""
    keywords: List[str] = []