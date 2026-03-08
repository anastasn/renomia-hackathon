from fastapi import APIRouter

from ai_engine.schemas import IngestRequest, IngestResponse

router = APIRouter(tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest) -> IngestResponse:
    """
    Document ingestion endpoint.
    TODO: split text into chunks, embed, and upsert into ChromaDB.
    """
    # Stub — replace with real chunking + embedding logic
    return IngestResponse(status="stub", chunks_added=0)
