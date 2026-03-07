#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# dev-setup.sh — one-shot environment bootstrap for new contributors
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[setup]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC}  $*"; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ── Prerequisites check ───────────────────────────────────────────────────────
info "Checking prerequisites..."

check_cmd() {
  if ! command -v "$1" &>/dev/null; then
    warn "$1 not found. Please install it before continuing."
    exit 1
  fi
}

check_cmd node
check_cmd npm
check_cmd uv
check_cmd docker

node_version=$(node --version | tr -d 'v')
major="${node_version%%.*}"
if (( major < 20 )); then
  warn "Node.js >= 20 required (found $node_version). Use nvm or fnm to upgrade."
  exit 1
fi

info "All prerequisites satisfied."

# ── .env file ────────────────────────────────────────────────────────────────
if [[ ! -f .env ]]; then
  cp infrastructure/env/.env.example .env
  warn ".env created from template. Fill in API keys before running services."
else
  info ".env already exists — skipping."
fi

# ── Node dependencies ─────────────────────────────────────────────────────────
info "Installing Node dependencies..."
npm install

# ── Python virtual environments ───────────────────────────────────────────────
info "Creating Python venv for services/backend..."
cd services/backend && uv sync && cd "$REPO_ROOT"

info "Creating Python venv for services/ai-engine..."
cd services/ai-engine && uv sync && cd "$REPO_ROOT"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
info "Setup complete! Next steps:"
echo ""
echo "  1. Edit .env and add your API keys."
echo "  2. Run 'make dev'         to start all services via Docker."
echo "     OR"
echo "     Run 'make dev-local'   to start services directly (separate terminals)."
echo ""
