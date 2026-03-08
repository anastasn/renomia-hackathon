from fastapi import APIRouter

from renomia_backend.config import settings
from renomia_backend.schemas import ServiceStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ServiceStatus)
async def health() -> ServiceStatus:
    """
    Returns basic service health information.
    Extend the `services` dict to include real dependency checks
    (e.g., DB ping, ai-engine reachability).
    """
    return ServiceStatus(
        status="ok",
        version=settings.app_version,
        services={
            "database": "ok",
            "ai_engine": "not_checked",
        },
    )
