from fastapi import APIRouter

from ai_engine.config import settings
from ai_engine.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        vectorstore="not_configured",
    )
