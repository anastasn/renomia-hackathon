# Architecture Overview

## System diagram

```
Browser
  │
  │  HTTPS / HTTP
  ▼
┌─────────────────────────────────┐
│  Frontend  (Next.js · port 3000)│
│  apps/frontend                  │
└────────────────┬────────────────┘
                 │  REST /api/*
                 ▼
┌─────────────────────────────────┐
│  Backend  (FastAPI · port 8000) │
│  services/backend               │
│                                 │
│  ┌──────────────────────────┐   │
│  │ SQLite via SQLAlchemy    │   │
│  │ services/backend/data/   │   │
│  └──────────────────────────┘   │
└────────────────┬────────────────┘
                 │  REST (internal)
                 ▼
┌─────────────────────────────────┐
│  AI Engine (FastAPI · port 8001)│
│  services/ai-engine             │
│                                 │
│  ┌──────────────────────────┐   │
│  │  LangGraph chains        │   │
│  │  app/chains/             │   │
│  └──────────────────────────┘   │
│  ┌──────────────────────────┐   │
│  │  ChromaDB vectorstore    │   │
│  │  data/chroma/            │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

## Services

### Frontend (`apps/frontend`)

- **Framework:** Next.js 14 (App Router) + React 18 + Material UI
- **Role:** User interface, calls backend via `/api/*` rewrites
- **Key files:**
  - `src/app/page.tsx` — main page
  - `src/lib/api.ts` — typed API client functions
  - `src/components/` — reusable React components

### Backend (`services/backend`)

- **Framework:** FastAPI + Pydantic v2
- **Storage:** SQLite via SQLAlchemy async ORM
- **Role:** Main application API. Owns business logic and data persistence.
  Delegates AI tasks to the AI engine.
- **Key files:**
  - `app/main.py` — application factory & middleware
  - `app/routers/` — one file per feature area
  - `app/models.py` — SQLAlchemy ORM models
  - `app/schemas.py` — Pydantic request/response DTOs
  - `app/database.py` — async engine & session factory

### AI Engine (`services/ai-engine`)

- **Framework:** FastAPI + LangGraph + ChromaDB
- **Role:** Isolated AI processing service. Keeps heavy AI dependencies
  separate from the core backend so they can scale independently.
- **Key files:**
  - `app/main.py` — FastAPI app with `/query` and `/ingest` endpoints
  - `app/chains/rag_chain.py` — implement your LangGraph pipeline here
  - `app/vectorstore.py` — ChromaDB client factory

### Shared AI package (`packages/ai`)

Optional shared library for prompts, tools, and LangGraph definitions that
are used by more than one service. See `packages/ai/README.md`.

## Data flow — RAG query

```
User types query
  → Frontend POST /api/query
  → Backend receives, validates with Pydantic
  → Backend POST http://ai-engine:8001/query
  → AI Engine retrieves relevant chunks from ChromaDB
  → AI Engine calls LLM (OpenAI / Anthropic)
  → AI Engine returns { answer, sources }
  → Backend forwards response to Frontend
  → Frontend renders answer
```

## Design decisions

| Decision | Rationale |
|---|---|
| SQLite over Postgres | Zero infrastructure for a hackathon; swap URL to migrate |
| Separate AI Engine service | Keeps heavy ML dependencies isolated; scales independently |
| Next.js rewrites as API proxy | Avoids CORS in dev; trivially replaced by nginx in production |
| uv for Python | Fast dependency resolution; compatible with pyproject.toml |
| Async throughout | Paves the way for high concurrency without re-architecting |

## Adding a new feature

1. **New data model** → add class in `services/backend/app/models.py`
2. **New API endpoint** → add router in `services/backend/app/routers/`, register in `main.py`
3. **New UI page** → add `src/app/<route>/page.tsx`, call backend via `src/lib/api.ts`
4. **New AI chain** → implement in `services/ai-engine/app/chains/`, expose via `main.py`
5. **Shared AI utility** → add to `packages/ai/renomia_ai/`
