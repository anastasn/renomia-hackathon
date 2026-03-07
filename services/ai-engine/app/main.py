from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import HealthResponse, QueryRequest, QueryResponse, IngestRequest, IngestResponse
from app.chains.rag_chain import run_rag_chain

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        vectorstore="not_configured",
    )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """
    RAG query endpoint.
    Delegates to the chain in app/chains/rag_chain.py.
    """
    return await run_rag_chain(request)


@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest) -> IngestResponse:
    """
    Document ingestion endpoint.
    TODO: split text into chunks, embed, and upsert into ChromaDB.
    """
    # Stub — replace with real chunking + embedding logic
    return IngestResponse(status="stub", chunks_added=0)


# ---------------------------------------------------------------------------
# Add more endpoints here:
#
#   @app.get("/collections")
#   async def list_collections(): ...
# ---------------------------------------------------------------------------
