from fastapi import APIRouter

from ai_engine.api.health import router as health_router
from ai_engine.api.ingest import router as ingest_router
from ai_engine.api.query import router as query_router

api_router = APIRouter(prefix="/api", tags=["api"])
api_router.include_router(health_router)
api_router.include_router(query_router)
api_router.include_router(ingest_router)
