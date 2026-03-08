from uuid import uuid4

from fastapi import APIRouter

from ai_engine.schemas import IngestRequest, IngestResponse
from ai_engine.vectorstore import get_vectorstore

router = APIRouter(tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest) -> IngestResponse:
    """Split text into paragraph chunks, embed, and upsert into ChromaDB."""
    raw_chunks = [c.strip() for c in request.text.split("\n\n")]
    chunks = [c for c in raw_chunks if c] or [request.text.strip()]

    metadatas = [dict(request.metadata) for _ in chunks]
    ids = [str(uuid4()) for _ in chunks]

    get_vectorstore(request.collection).add_texts(chunks, metadatas=metadatas, ids=ids)
    return IngestResponse(status="ok", chunks_added=len(chunks))
