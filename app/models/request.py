from datetime import datetime, date

from sqlalchemy import String, ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.enums import RequestStatus

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.employee import Employee


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[int] = mapped_column(
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )

    executor_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    deadline: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[RequestStatus] = mapped_column(
        default=RequestStatus.NEW
    )

    author: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="created_requests",
        foreign_keys=[author_id]
    )

    executor: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="assigned_requests",
        foreign_keys=[executor_id]
    )