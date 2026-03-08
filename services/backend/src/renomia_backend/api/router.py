from fastapi import APIRouter

from renomia_backend.api.documents import router as documents_router
from renomia_backend.api.health import router as health_router

api_router = APIRouter(prefix="/api", tags=["api"])
api_router.include_router(documents_router)
api_router.include_router(health_router)
