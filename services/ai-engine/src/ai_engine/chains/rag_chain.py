"""RAG chain — retrieval only (no LLM synthesis yet)."""

from ai_engine.schemas import QueryRequest, QueryResponse
from ai_engine.vectorstore import get_vectorstore


async def run_rag_chain(request: QueryRequest) -> QueryResponse:
    """Retrieve top-k chunks from ChromaDB and return them directly."""
    docs = get_vectorstore(request.collection).similarity_search(request.query, k=request.top_k)

    if not docs:
        return QueryResponse(answer="No relevant documents found.", sources=[])

    # TODO: pipe `docs` + `request.query` through an LLM to synthesise an answer
    answer = "\n\n---\n\n".join(doc.page_content for doc in docs)
    seen: set[str] = set()
    sources: list[str] = []
    for doc in docs:
        src = doc.metadata.get("source", "")
        if src and src not in seen:
            seen.add(src)
            sources.append(src)

    return QueryResponse(answer=answer, sources=sources)
