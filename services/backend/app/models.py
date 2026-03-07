"""
SQLAlchemy ORM models.

Add your domain models here.  Each model class should inherit from Base.
"""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# ---------------------------------------------------------------------------
# Example model — replace or extend with your domain entities
# ---------------------------------------------------------------------------

class Document(Base):
    """Placeholder model representing an ingested document."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str | None] = mapped_column(String(512), nullable=True)

    def __repr__(self) -> str:
        return f"<Document id={self.id} title={self.title!r}>"
