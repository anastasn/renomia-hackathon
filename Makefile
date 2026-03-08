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
	npm install

setup-backend:
	cd services/backend && $(UV) sync

setup-ai-engine:
	cd services/ai-engine && $(UV) sync

# ── Development ──────────────────────────────────────────────────────────────

dev:
	@cp -n infrastructure/env/.env.example .env 2>/dev/null || true
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
	npm run lint --workspace=apps/frontend

lint-backend:
	cd services/backend && $(UV) run ruff check .

lint-ai-engine:
	cd services/ai-engine && $(UV) run ruff check .

# ── Typecheck ────────────────────────────────────────────────────────────────

typecheck: typecheck-frontend typecheck-backend typecheck-ai-engine

typecheck-frontend:
	npm run typecheck --workspace=apps/frontend

typecheck-backend:
	cd services/backend && $(UV) run mypy app

typecheck-ai-engine:
	cd services/ai-engine && $(UV) run mypy app

# ── Test ─────────────────────────────────────────────────────────────────────

test: test-backend test-ai-engine

test-backend:
	cd services/backend && $(UV) run pytest tests/ -v

test-ai-engine:
	cd services/ai-engine && $(UV) run pytest tests/ -v

# ── Clean ────────────────────────────────────────────────────────────────────

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .next      -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete 2>/dev/null; true
	@echo "Cleaned."
