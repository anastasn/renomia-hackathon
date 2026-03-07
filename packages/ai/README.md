# packages/ai

Shared AI utilities — importable by any Python service in the monorepo.

## Purpose

This package is the right home for:

- Prompt templates reused across multiple services
- Shared LangChain / LangGraph node definitions
- Custom tool definitions (web search, SQL executor, etc.)
- Evaluation helpers and tracing utilities

## Structure (suggested)

```
packages/ai/
├── pyproject.toml
└── renomia_ai/
    ├── __init__.py
    ├── prompts/          # Prompt templates
    │   └── rag.py
    ├── tools/            # LangChain tool wrappers
    │   └── search.py
    └── graphs/           # LangGraph state-machine definitions
        └── rag_graph.py
```

## Usage

Add the package as a dependency in any service's `pyproject.toml`:

```toml
[project]
dependencies = [
    "renomia-ai @ file://../../../packages/ai",
]
```

Then import normally:

```python
from renomia_ai.prompts.rag import RAG_PROMPT
```
