# CLAUDE.md — AI Engine Service

## Overview

FastAPI service on port **5002**. Entry point: `src/ai_engine/main.py`.

## Current state

ChromaDB is **active** with OpenAI embeddings (`text-embedding-3-small`).

| Endpoint | File | Status |
|---|---|---|
| `GET /api/health` | `api/health.py` | Live — reports ChromaDB collection count |
| `POST /api/ingest` | `api/ingest.py` | Live — paragraph-splits text, embeds, upserts |
| `POST /api/query` | `api/query.py` | Live — similarity search, returns raw chunks |

`OPENAI_API_KEY` is **required** for `/api/ingest` and `/api/query` (embeddings).
`GET /api/health` works without it.

## Active vs commented deps (`pyproject.toml`)

| Package | State | Reason |
|---|---|---|
| `langchain` | active | base abstractions |
| `langchain-openai` | active | OpenAI embeddings |
| `langchain-chroma` | active | LangChain ↔ ChromaDB bridge |
| `chromadb` | active | vector store |
| `langgraph` | commented | not needed until multi-step agent added |
| `tiktoken` | commented | not needed until token-counting required |

## Adding LLM synthesis to rag_chain.py

1. Uncomment `langchain-openai` (already active) — `ChatOpenAI` is available.
2. In `chains/rag_chain.py`, after the similarity search, build a prompt and call the LLM:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template(
    "Answer based on context:\n\n{context}\n\nQuestion: {question}"
)
chain = prompt | llm
result = await chain.ainvoke({"context": answer, "question": request.query})
return QueryResponse(answer=result.content, sources=sources)
```

3. Replace the `# TODO` comment in `run_rag_chain()`.

## Running tests locally

```bash
cd services/ai-engine
uv run pytest
```

Or via make from the repo root:

```bash
make test
```
