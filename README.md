# Renomia Hackathon — Monorepo Starter

Production-style monorepo template for 24-hour AI hackathons.
Stack: **Next.js · FastAPI · LangGraph · ChromaDB · SQLite · Docker**

---

## Repository structure

```
renomia-hackathon/
├── apps/
│   └── frontend/               # Next.js + React + Material UI  (port 3000)
│       └── src/
│           ├── app/            # Next.js App Router pages
│           ├── components/     # React components
│           └── lib/api.ts      # Typed backend API client
│
├── services/
│   ├── backend/                # FastAPI + SQLite + SQLAlchemy  (port 5001)
│   │   └── src/renomia_backend/
│   │       ├── api/            # Routers (one file per feature area)
│   │       ├── models.py       # ORM models
│   │       ├── schemas.py      # Pydantic DTOs
│   │       └── main.py
│   │
│   └── ai-engine/              # FastAPI + LangGraph + ChromaDB (port 5002)
│       └── src/ai_engine/
│           ├── chains/         # ← implement AI logic here
│           ├── vectorstore.py  # ChromaDB client factory
│           └── main.py
│
├── packages/
│   └── ai/                     # Shared AI utilities (prompts, tools, graphs)
│
├── infrastructure/
│   ├── docker/                 # Per-service Dockerfiles
│   └── env/
│       └── .env.example        # Environment variable template
│
├── docker-compose.yml          # Development orchestration
├── Makefile                    # Developer shortcuts
├── CLAUDE.md                   # Guide for AI coding agents
└── ARCHITECTURE.md             # Full system design reference
```

---

## Starting development

### Option A — Docker (recommended, no local Python/Node required)

```bash
# 1. Bootstrap
bash scripts/dev-setup.sh

# 2. Fill in API keys
nano .env

# 3. Start everything
make dev
```

Services will be available at:
- Frontend → http://localhost:3000
- Backend API → http://localhost:5001
- Backend docs → http://localhost:5001/docs
- AI Engine → http://localhost:5002
- AI Engine docs → http://localhost:5002/docs

### Option B — Local (faster iteration, no Docker)

Prerequisites: Node >= 20, Python 3.12, [uv](https://github.com/astral-sh/uv)

```bash
# Install all dependencies
make setup

# Start services (each in its own terminal)
make dev-backend      # terminal 1
make dev-ai-engine    # terminal 2
make dev-frontend     # terminal 3
```

---

## Common tasks

| Command | What it does |
|---|---|
| `make dev` | Start all services via docker-compose |
| `make stop` | Stop docker-compose services |
| `make build` | Build production Docker images |
| `make lint` | Run ruff + eslint |
| `make typecheck` | Run mypy + tsc |
| `make test` | Run pytest for both Python services |
| `make clean` | Remove build artefacts |

---

## Where to implement AI logic

### 1. RAG pipeline

Open `services/ai-engine/src/ai_engine/chains/` and implement your chain logic.

Steps:
1. Uncomment the AI dependencies in `services/ai-engine/pyproject.toml`
2. Configure your LLM API key in `.env`
3. Implement the retrieval + generation logic
4. (Optional) move shared chains to `packages/ai/`

### 2. Document ingestion

The `/ingest` endpoint in `services/ai-engine/src/ai_engine/main.py` is a stub.
Implement text chunking, embedding, and ChromaDB upsert there.

### 3. Vectorstore

`services/ai-engine/src/ai_engine/vectorstore.py` has a commented-out example.
Uncomment and adapt it once chromadb is installed.

---

## How to add new services

1. Create a new directory under `services/` or `apps/`
2. Add a `pyproject.toml` (Python) or `package.json` (Node)
3. Add a `Dockerfile` under `infrastructure/docker/`
4. Add a new service block in `docker-compose.yml`
5. Add `make` targets for `dev`, `lint`, `typecheck`, and `test`

---

## Environment variables

Copy `infrastructure/env/.env.example` to `.env` at the repo root.
The `.env` file is read by docker-compose and each service's `pydantic-settings` config.

Key variables:

| Variable | Service | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Frontend | Backend URL (production builds) |
| `DATABASE_URL` | Backend | SQLAlchemy async DB URL |
| `AI_ENGINE_URL` | Backend | Internal URL of the AI engine |
| `OPENAI_API_KEY` | AI Engine | LLM provider key |
| `CHROMA_PERSIST_DIR` | AI Engine | ChromaDB storage path |

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, React 18, Material UI |
| Backend | FastAPI, Pydantic v2, SQLAlchemy 2 async |
| AI engine | FastAPI, LangGraph, ChromaDB |
| Database | SQLite (aiosqlite) |
| Python tooling | uv, ruff, mypy, pytest |
| Node tooling | npm workspaces, TypeScript, ESLint |
| Infrastructure | Docker, docker-compose |

---

## For AI agents

This repository includes authoritative documentation for AI coding assistants:

- **`CLAUDE.md`** — commands, code style rules, DOs/DON'Ts, service map (start here)
- **`AGENTS.md`** — same content, for editors that read AGENTS.md (Cursor, Zed)
- **`ARCHITECTURE.md`** — full system design, data flow, network topology, tech stack table
