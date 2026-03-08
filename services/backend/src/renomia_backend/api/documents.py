"""
Documents router — CRUD placeholder.

Swap the stub implementations below with real DB queries
using the `session` dependency once you have your domain ready.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from renomia_backend.database import get_session
from renomia_backend.models import Document
from renomia_backend.schemas import DocumentCreate, DocumentRead

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/", response_model=list[DocumentRead])
async def list_documents(
    session: AsyncSession = Depends(get_session),
) -> list[Document]:
    result = await session.execute(select(Document))
    return list(result.scalars().all())


@router.post("/", response_model=DocumentRead, status_code=201)
async def create_document(
    payload: DocumentCreate,
    session: AsyncSession = Depends(get_session),
) -> Document:
    doc = Document(**payload.model_dump())
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return doc


@router.get("/{doc_id}", response_model=DocumentRead)
async def get_document(
    doc_id: int,
    session: AsyncSession = Depends(get_session),
) -> Document:
    doc = await session.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.delete("/{doc_id}", status_code=204)
async def delete_document(
    doc_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    doc = await session.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    await session.delete(doc)
    await session.commit()
