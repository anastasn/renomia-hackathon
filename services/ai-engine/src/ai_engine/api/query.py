from fastapi import APIRouter

from ai_engine.chains.rag_chain import run_rag_chain
from ai_engine.schemas import QueryRequest, QueryResponse

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """
    RAG query endpoint.
    Delegates to the chain in app/chains/rag_chain.py.
    """
    return await run_rag_chain(request)
