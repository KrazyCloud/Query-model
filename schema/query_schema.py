from pydantic import BaseModel
from typing import List, Dict, Any

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

