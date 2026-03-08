from fastapi import APIRouter

from ai_engine.config import settings
from ai_engine.schemas import HealthResponse
from ai_engine.vectorstore import get_chroma_client

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    try:
        collections = get_chroma_client().list_collections()
        vectorstore = f"ok ({len(collections)} collections)"
    except Exception as e:
        vectorstore = f"error: {e}"

    return HealthResponse(
        status="ok",
        version=settings.app_version,
        vectorstore=vectorstore,
    )
