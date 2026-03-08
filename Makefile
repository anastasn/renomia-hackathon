# ─────────────────────────────────────────────────────────────────────────────
# Renomia Hackathon — Developer Makefile
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: help setup dev stop build lint typecheck test clean

PYTHON := python3
UV     := uv

# Default target
help:
	@echo ""
	@echo "  Renomia Hackathon — available targets"
	@echo ""
	@echo "  setup      Install all dependencies (Node + Python venvs)"
	@echo "  dev        Start all services via docker-compose (hot reload)"
	@echo "  dev-local  Start services locally without Docker"
	@echo "  stop       Stop docker-compose services"
	@echo "  build      Build production Docker images"
	@echo "  lint       Run linters (ruff + eslint)"
	@echo "  typecheck  Run type checkers (mypy + tsc)"
	@echo "  test       Run all tests"
	@echo "  clean      Remove build artefacts and __pycache__"
	@echo ""

# ── Setup ────────────────────────────────────────────────────────────────────

setup: setup-frontend setup-backend setup-ai-engine
	@echo "All dependencies installed."

setup-frontend:
	cd apps/frontend &&	npm install

setup-backend:
	cd services/backend && $(UV) sync

setup-ai-engine:
	cd services/ai-engine && $(UV) sync

# ── Development ──────────────────────────────────────────────────────────────

dev:
	docker compose up 

dev-local: dev-backend dev-ai-engine dev-frontend

dev-frontend:
	npm run dev &

dev-backend:
	cd services/backend && $(UV) run uvicorn renomia_backend.main:app --reload --port 5001 &

dev-ai-engine:
	cd services/ai-engine && $(UV) run uvicorn ai_engine.main:app --reload --port 5002 &

stop:
	docker compose down

# ── Build ────────────────────────────────────────────────────────────────────

build:
	docker compose build

# ── Lint ─────────────────────────────────────────────────────────────────────

lint: lint-frontend lint-backend lint-ai-engine

lint-frontend:
	npm run lint --fix --workspace=apps/frontend

lint-backend:
	cd services/backend && $(UV) run ruff format . && uv run ruff check --fix .

lint-ai-engine:
	cd services/ai-engine && $(UV) run ruff format . && uv run ruff check --fix .

# ── Typecheck ────────────────────────────────────────────────────────────────

typecheck: typecheck-backend typecheck-ai-engine

typecheck-backend:
	cd services/backend && $(UV) run mypy src

typecheck-ai-engine:
	cd services/ai-engine && $(UV) run mypy src

# ── Clean ────────────────────────────────────────────────────────────────────

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .next      -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete 2>/dev/null; true
	@echo "Cleaned."
