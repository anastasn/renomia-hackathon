"""Pydantic schemas (request/response DTOs)."""

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

class ServiceStatus(BaseModel):
    status: str
    version: str
    services: dict[str, str]


# ---------------------------------------------------------------------------
# Document — example CRUD schemas
# ---------------------------------------------------------------------------

class DocumentCreate(BaseModel):
    title: str
    content: str
    source: str | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    source: str | None


# ---------------------------------------------------------------------------
# AI Engine passthrough
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []
