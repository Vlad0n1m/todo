from fastapi import APIRouter
from sqlalchemy import select
from app.database.db import SessionDep
from app.schemas.task import TaskCreateSchema, TaskReadSchema, TaskUpdateSchema
from app.models.task import TaskModel
from typing import List
from fastapi import HTTPException

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.get("/", status_code=200, summary="Получить все таски")
async def get_all_tasks(db: SessionDep) -> List[TaskReadSchema]:
    result = await db.execute(select(TaskModel))
    tasks = result.scalars().all()
    return tasks


@router.post("/", status_code=201, summary="Создать таску")
async def create_task(db: SessionDep, data: TaskCreateSchema) -> TaskReadSchema:
    new_task = TaskModel(**data.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.put("/{id}", summary="Изменить задание")
async def update_task(
    db: SessionDep, data: TaskUpdateSchema, id: int
):
    result = await db.execute(select(TaskModel).filter(TaskModel.id == id))
    task = result.scalars().first()
    if not task:
        return HTTPException(status_code=404, detail="No task found!")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)

    return task


@router.get("/{id}", summary="Получить задание по ID")
async def get_task_by_id(
    db: SessionDep, id: int
):
    result = await db.execute(select(TaskModel).filter(TaskModel.id == id))
    task = result.scalars().first()
    if not task:
        return HTTPException(status_code=404, detail="No task found!")
    return task

@router.delete("/{id}", summary="Удалить задание")
async def delete_task(
    db: SessionDep, id: int
):
    result = await db.execute(select(TaskModel).filter(TaskModel.id == id))
    task = result.scalars().first()
    if not task:
        return HTTPException(status_code=404, detail="No task found!")
    await db.delete(task)
    await db.commit()
    return {'success': True}

