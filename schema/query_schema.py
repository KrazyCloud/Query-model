from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    topic: str

class QueryResponse(BaseModel):
    keywords: List[str]
    boolean_query: str
    social_links: Dict[str, Dict[str, Dict[str, Any]]]