from fastapi import APIRouter
from httpx import AsyncClient, HTTPError
from loguru import logger as log

from renomia_backend.config import settings
from renomia_backend.schemas import ServiceStatus

router = APIRouter(tags=["health"])


async def check_ai_engine() -> str:
    """
    Example function to check AI engine health.
    Replace with actual logic to ping your AI service.
    """
    try:
        async with AsyncClient() as client:
            response = await client.get(settings.ai_engine_url + "/api/health")
            response.raise_for_status()
            return "ok"
    except HTTPError as e:
        log.error(f"AI engine health check failed: {repr(e)}")
        return "unreachable"


@router.get("/health", response_model=ServiceStatus)
async def health() -> ServiceStatus:
    """
    Returns basic service health information.
    Extend the `services` dict to include real dependency checks
    (e.g., DB ping, ai-engine reachability).
    """
    ai_status = await check_ai_engine()
    return ServiceStatus(
        status="ok",
        version=settings.app_version,
        services={
            "database": "ok",
            "ai_engine": ai_status,
        },
    )
