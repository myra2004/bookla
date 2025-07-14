from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, String, Column

from datetime import datetime, UTC

from app.db import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    isbn: Mapped[int] = mapped_column(String(13), nullable=False, unique=True)
    cover: Mapped[str] = mapped_column(String(100), nullable=True)
    page_count: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), onupdate=datetime.now(UTC))

    def __str__(self):
        return f'Book (name={self.name})'

