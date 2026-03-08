# CLAUDE.md — AI Agent Guide for Renomia Hackathon Monorepo

This file is the primary source of truth for AI coding agents (Claude Code, Cursor, Copilot, etc.).
Read this before touching any code.

---

## Project overview

Insurance-broker AI hackathon monorepo. Domain: **Renomia** (Czech insurance broker).
The stack combines a Next.js frontend, a FastAPI backend, and a FastAPI AI engine (LangGraph/ChromaDB).
Everything runs via Docker Compose in dev.

---

## Key commands

| Command | What it does |
|---|---|
| `make dev` | Start all services via `docker compose up` (hot reload via volume mounts) |
| `make stop` | Stop docker-compose services |
| `make build` | Build production Docker images |
| `make setup` | Install all Node + Python deps locally (no Docker) |
| `make lint` | Run ruff (Python) + eslint (JS) |
| `make typecheck` | Run mypy (Python) + tsc (TypeScript) |
| `make test` | Run pytest for both Python services |
| `make clean` | Remove `__pycache__`, `.mypy_cache`, `.ruff_cache`, `.next` |

Local dev without Docker (three terminals):
```
make dev-backend       # uvicorn on :5001
make dev-ai-engine     # uvicorn on :5002
make dev-frontend      # next dev on :3000
```

---

## Service map

| Service | Path | Port | Entry point |
|---|---|---|---|
| Frontend | `apps/frontend/` | 3000 | `src/app/` (Next.js App Router) |
| Backend | `services/backend/` | **5001** | `src/renomia_backend/main.py` |
| AI Engine | `services/ai-engine/` | **5002** | `src/ai_engine/main.py` |
| Shared AI pkg | `packages/ai/` | — | `src/renomia_ai/` (currently empty) |

Health endpoints: `GET /api/health` on backend (:5001) and ai-engine (:5002).

---

## Python source layout

```
services/backend/src/renomia_backend/
    main.py          # FastAPI app factory
    config.py        # pydantic-settings Config
    database.py      # SQLAlchemy async engine + session
    models.py        # ORM models
    schemas.py       # Pydantic DTOs
    api/             # Router modules (one file per feature)

services/ai-engine/src/ai_engine/
    main.py          # FastAPI app factory
    config.py        # pydantic-settings Config
    schemas.py       # Pydantic DTOs
    vectorstore.py   # ChromaDB client factory
    api/             # Router modules
    chains/          # LangGraph chains — implement AI logic here
```

---

## Code style

### Python (backend + ai-engine)
- Formatter/linter: **ruff** (`line-length = 100`, rules: E W F I UP)
- Type checker: **mypy** strict (`python_version = "3.12"`)
- Test runner: **pytest** with `asyncio_mode = "auto"`
- Use `async`/`await` throughout — SQLAlchemy sessions are async
- Pydantic v2 — use `model_config`, not `class Config`

> `packages/ai` uses `line-length = 120` — keep files in sync with their own pyproject.toml.

### TypeScript (frontend)
- Package manager: **npm** (v10.9.4) — do NOT use yarn/pnpm/bun
- Framework: Next.js 14 App Router — pages live under `src/app/`
- UI: Material UI v5
- API client: `src/lib/api.ts` — typed, extend it for new endpoints

---

## DOs

- Run `make lint` and `make typecheck` before committing
- Keep routers thin — business logic in service/chain modules
- Add tests under `tests/` in each service
- Extend `packages/ai/` for logic shared between backend and ai-engine
- Check `infrastructure/env/.env.example` before adding new env vars

## DON'Ts

- Do NOT hardcode API keys or secrets — use `.env` (gitignored)
- Do NOT use `yarn`, `pnpm`, or `bun` — this repo uses **npm**
- Do NOT call the ai-engine directly from the frontend — route through the backend
- Do NOT add new top-level directories without updating `docker-compose.yml` and this file

---

## AI engine setup

`chromadb`, `langchain`, `langchain-openai`, and `langchain-chroma` are now **active**.
`langgraph` and `tiktoken` remain commented — uncomment when needed.

1. Run `make setup-ai-engine` (or `make setup`) to install deps
2. Set `OPENAI_API_KEY` in `.env` (required for ingest/query; health works without it)
3. Extend chains in `services/ai-engine/src/ai_engine/chains/`
4. See `services/ai-engine/CLAUDE.md` for LLM synthesis instructions
5. Move shared utilities to `packages/ai/src/renomia_ai/`

---

## Environment variables

Copy `infrastructure/env/.env.example` to `.env` at the repo root.

| Variable | Service | Description |
|---|---|---|
| `BACKEND_URL` | Frontend | URL the Next.js server uses to reach the backend |
| `DATABASE_URL` | Backend | SQLAlchemy async DB URL (default: sqlite+aiosqlite) |
| `AI_ENGINE_URL` | Backend | Internal URL to reach ai-engine (docker: `http://ai-engine:5002`) |
| `OPENAI_API_KEY` | AI Engine | LLM provider key |
| `CHROMA_PERSIST_DIR` | AI Engine | ChromaDB storage path |

---

## Nested CLAUDE.md files

Each service may have its own `CLAUDE.md` with service-specific context.
Check `services/backend/CLAUDE.md`, `services/ai-engine/CLAUDE.md`, and `apps/frontend/CLAUDE.md`
if they exist before modifying that service.

---

## Architecture reference

See `ARCHITECTURE.md` for the full system design, data flow diagram, and network topology.
