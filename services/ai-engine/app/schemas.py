"""Pydantic schemas for the AI engine API."""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    collection: str = "docs"


class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []


class IngestRequest(BaseModel):
    text: str
    metadata: dict[str, str] = {}
    collection: str = "docs"


class IngestResponse(BaseModel):
    status: str
    chunks_added: int


class HealthResponse(BaseModel):
    status: str
    version: str
    vectorstore: str
