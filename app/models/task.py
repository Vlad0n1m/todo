from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base
from app.extras.enums import TaskStatusEnum
from sqlalchemy import func, DateTime
from datetime import datetime


class TaskModel(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[TaskStatusEnum] = mapped_column(default=TaskStatusEnum.IN_PROGRESS)
    description: Mapped[str] = mapped_column(nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False, onupdate=func.now()
    )
