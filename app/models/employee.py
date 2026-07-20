from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.request import Request


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    position: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    created_requests: Mapped[list["Request"]] = relationship(
        "Request",
        back_populates="author",
        foreign_keys="[Request.author_id]"
    )

    assigned_requests: Mapped[list["Request"]] = relationship(
        "Request",
        back_populates="executor",
        foreign_keys="[Request.executor_id]"
    )