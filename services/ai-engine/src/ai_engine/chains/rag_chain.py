"""
RAG chain placeholder.

Replace the stub below with a real LangGraph / LangChain pipeline.

Example flow (uncomment dependencies in pyproject.toml first):

    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_chroma import Chroma
    from langgraph.graph import StateGraph

Steps to implement:
    1. Load ChromaDB vectorstore (see vectorstore.py).
    2. Retrieve top-k chunks relevant to the user query.
    3. Pass chunks + query to an LLM for answer synthesis.
    4. Return structured QueryResponse.
"""

from ai_engine.schemas import QueryRequest, QueryResponse


async def run_rag_chain(request: QueryRequest) -> QueryResponse:
    """
    Stub implementation — returns a placeholder answer.
    Replace with your LangGraph pipeline.
    """
    # TODO: implement real RAG logic
    return QueryResponse(
        answer=f"[STUB] Query received: '{request.query}'. Implement run_rag_chain() to add AI.",
        sources=[],
    )
