# Architecture — Renomia Hackathon Monorepo

## Directory layout

```
renomia-hackathon/
├── apps/
│   └── frontend/               # Next.js 14 + React 18 + Material UI  (port 3000)
│       └── src/
│           ├── app/            # App Router pages & layouts
│           ├── components/     # React components
│           └── lib/api.ts      # Typed backend API client
│
├── services/
│   ├── backend/                # FastAPI + SQLAlchemy 2 async + aiosqlite  (port 5001)
│   │   └── src/renomia_backend/
│   │       ├── main.py
│   │       ├── config.py
│   │       ├── database.py
│   │       ├── models.py       # ORM models
│   │       ├── schemas.py      # Pydantic v2 DTOs
│   │       └── api/            # Routers (one file per feature area)
│   │
│   └── ai-engine/              # FastAPI + LangGraph + ChromaDB  (port 5002)
│       └── src/ai_engine/
│           ├── main.py
│           ├── config.py
│           ├── schemas.py
│           ├── vectorstore.py  # ChromaDB client factory
│           ├── api/            # Routers
│           └── chains/         # LangGraph chains — AI logic lives here
│
├── packages/
│   └── ai/                     # Shared Python pkg: renomia-ai
│       └── src/renomia_ai/     # Currently empty — add shared prompts/tools/graphs
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile.frontend
│   │   ├── Dockerfile.backend
│   │   └── Dockerfile.ai-engine
│   └── env/
│       └── .env.example
│
├── docker-compose.yml
├── Makefile
├── turbo.json                  # Turborepo task graph (JS tasks)
├── package.json                # npm workspaces root
├── CLAUDE.md                   # AI agent guide (primary)
├── AGENTS.md                   # Alias of CLAUDE.md for Cursor/Zed
└── ARCHITECTURE.md             # This file
```

---

## Service ports

| Service | Host port | Container port | Health check |
|---|---|---|---|
| Frontend | 3000 | 3000 | — |
| Backend | **5001** | 5001 | `GET http://localhost:5001/api/health` |
| AI Engine | **5002** | 5002 | `GET http://localhost:5002/api/health` |

---

## Data flow

```
Browser
  │  HTTP (port 3000)
  ▼
Next.js Frontend  ──────────────────────────────────────┐
  │                                                      │
  │  HTTP via lib/api.ts                                 │
  ▼                                                      │
FastAPI Backend  (port 5001)                             │
  │  SQLAlchemy async                                    │
  ├──► SQLite / aiosqlite  (volume: backend_data)        │
  │                                                      │
  │  HTTP (internal: http://ai-engine:5002)              │
  ▼                                                      │
FastAPI AI Engine  (port 5002)                           │
  │  LangGraph chains                                    │
  ├──► LLM API  (OpenAI / Anthropic — external)          │
  │  ChromaDB                                            │
  └──► Vector store  (volume: ai_engine_data)            │
                                                         │
◄────────────────────────────────────────────────────────┘
           Response back to browser
```

**Rule:** The frontend never calls the AI engine directly. All AI requests flow through the backend.

---

## Tech stack

| Layer | Technology | Version constraint |
|---|---|---|
| Frontend framework | Next.js | 14.x |
| Frontend UI | React | 18.x |
| Frontend component lib | Material UI | v5 |
| Frontend language | TypeScript | latest |
| Backend framework | FastAPI | >=0.111 |
| Backend validation | Pydantic | v2 (>=2.7) |
| Backend ORM | SQLAlchemy | 2.x async |
| Backend database | SQLite via aiosqlite | — |
| Backend HTTP client | httpx | >=0.27 |
| AI engine framework | FastAPI | >=0.111 |
| AI orchestration | LangGraph | >=0.1 (commented out until needed) |
| AI chains | LangChain | >=0.2 (commented out until needed) |
| Vector store | ChromaDB | >=0.5 (commented out until needed) |
| Python runtime | CPython | 3.12 |
| Python package mgr | uv | latest |
| Node package mgr | npm | 10.9.4 |
| Monorepo (JS) | Turborepo + npm workspaces | — |
| Monorepo (Python) | uv workspace | — |
| Containerisation | Docker + Compose | — |
| Python linter/fmt | ruff | >=0.4 |
| Python types | mypy | >=1.10, strict |
| Python tests | pytest + pytest-asyncio | >=8.2 |

---

## Docker Compose network topology

All services are on a single default bridge network named `renomia-hackathon_default`.

```
docker network: renomia-hackathon_default
  frontend   → depends_on: backend (healthy)
  backend    → depends_on: ai-engine (healthy)
  ai-engine  → (no internal dependencies)
```

Internal DNS names match service names: `backend`, `ai-engine`, `frontend`.

### Named volumes

| Volume | Mounted at | Purpose |
|---|---|---|
| `backend_data` | `/app/data` in backend container | SQLite database persistence |
| `ai_engine_data` | `/app/data` in ai-engine container | ChromaDB persistence |

### Hot-reload volume mounts (dev only)

| Host path | Container path | Service |
|---|---|---|
| `./services/backend` | `/app/services/backend` | backend |
| `./services/ai-engine` | `/app/services/ai-engine` | ai-engine |
| `./packages/ai` | `/app/packages/ai` | backend + ai-engine |

---

## Python packaging

Both Python services use **uv** with `src/` layout and are declared as workspace members.

```
uv workspace root: repo root
  members:
    services/backend   → package: renomia-backend  (renomia_backend)
    services/ai-engine → package: ai-engine         (ai_engine)
    packages/ai        → package: renomia-ai         (renomia_ai)
```

Install a workspace package into another:
```bash
cd services/backend
uv add renomia-ai --editable  # or pin a version
```

---

## Ruff line-length per package


| Path | line-length |
|---|---|
| `services/backend` | 100 |
| `services/ai-engine` | 100 |
| `packages/ai` | 120 |


