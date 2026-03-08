"""ChromaDB vectorstore helpers."""

import chromadb
from chromadb.api import ClientAPI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from ai_engine.config import settings


def get_chroma_client() -> ClientAPI:
    """Return a persistent ChromaDB client (no embeddings — safe to call without an API key)."""
    return chromadb.PersistentClient(path=settings.chroma_persist_dir)


def get_vectorstore(collection_name: str = "docs") -> Chroma:
    """Return a LangChain Chroma wrapper backed by OpenAI embeddings."""
    client = get_chroma_client()
    embeddings = OpenAIEmbeddings(model=settings.embedding_model)
    return Chroma(client=client, embedding_function=embeddings, collection_name=collection_name)
