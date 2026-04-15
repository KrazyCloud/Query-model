from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    topic: str

class QueryResponse(BaseModel):
    keywords: List[str]
    boolean_query: str