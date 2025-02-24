from enum import Enum
from typing import Any, Self

from pydantic import BaseModel
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from lib.model import Base, CreationMetadataMixin
from user.model import User  # noqa: F401, E261


class NotificationCategory(str, Enum):
    chat = "chat"


class Notification(CreationMetadataMixin, Base):
    __tablename__ = "notifications"

    id: Mapped[int | None] = mapped_column(
        primary_key=True,
        nullable=False,
    )

    title: Mapped[str]
    body: Mapped[str] = mapped_column(Text)
    category: Mapped[NotificationCategory] = mapped_column(
        SQLEnum(NotificationCategory),
    )

    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    is_push_notification: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    is_read: Mapped[bool]

    @classmethod
    def from_JSON(self, nr: "NotificationRequest") -> Self:
        return self(**nr.model_dump())

    def to_JSON(self) -> "NotificationResponse":
        return NotificationResponse.model_validate(self.__dict__)


class NotificationRequest(BaseModel):
    title: str
    body: str
    category: NotificationCategory
    payload: dict[str, Any]
    is_push_notification: bool | None = None
    user_id: int
    is_read: bool = False


class NotificationReadRequest(BaseModel):
    id: int


class NotificationResponse(NotificationRequest):
    id: int
