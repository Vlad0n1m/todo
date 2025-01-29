from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.extras.enums import TaskStatusEnum


class TaskBaseSchema(BaseModel):
    title: str = Field(..., example="Создать коллекцию в Postman")
    description: Optional[str] = Field(
        None, example="Вызвать каждый эндпоинт и созранить"
    )
    status: TaskStatusEnum = Field(
        TaskStatusEnum.IN_PROGRESS,
        examples=[
            TaskStatusEnum.IN_PROGRESS,
            TaskStatusEnum.CANCELED,
            TaskStatusEnum.COMPLETED,
        ],
    )


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, example="Протестировать апи")
    description: Optional[str] = Field(None, example="Обновленное описание")
    status: Optional[TaskStatusEnum] = Field(
        None,
        examples=[
            TaskStatusEnum.IN_PROGRESS,
            TaskStatusEnum.CANCELED,
            TaskStatusEnum.COMPLETED,
        ],
    )


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskReadSchema(TaskBaseSchema):
    id: int
    date_created: datetime
    date_updated: datetime

    class Config:
        from_attributes = True
