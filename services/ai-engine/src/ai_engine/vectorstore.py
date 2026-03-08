"""
ChromaDB vectorstore helper.

Uncomment and extend once you have chromadb + an embedding model configured.

Example:
    from chromadb import PersistentClient
    from langchain_openai import OpenAIEmbeddings
    from langchain_chroma import Chroma

    def get_vectorstore() -> Chroma:
        client = PersistentClient(path=settings.chroma_persist_dir)
        embeddings = OpenAIEmbeddings(model=settings.embedding_model)
        return Chroma(client=client, embedding_function=embeddings, collection_name="docs")
"""

# from app.config import settings


def get_vectorstore() -> None:  # type: ignore[return]
    """Placeholder — replace return type and body when ChromaDB is enabled."""
    raise NotImplementedError("ChromaDB is not configured yet. See vectorstore.py for instructions.")
