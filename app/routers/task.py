from fastapi import APIRouter
from sqlalchemy import select
from app.database.db import SessionDep
from app.schemas.task import TaskCreateSchema, TaskReadSchema, TaskUpdateSchema
from app.models.task import TaskModel
from typing import List
from fastapi import HTTPException
import logging

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.get("/", status_code=200, summary="Получить все таски")
async def get_all_tasks(db: SessionDep) -> List[TaskReadSchema]:
    result = await db.execute(select(TaskModel))
    tasks = result.scalars().all()
    logging.info(f'Пользователь запросил /tasks/ и сервер вернул {len(tasks)} тасок!')
    return tasks


@router.post("/", status_code=201, summary="Создать таску")
async def create_task(db: SessionDep, data: TaskCreateSchema) -> TaskReadSchema:
    new_task = TaskModel(**data.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    logging.info(f'Пользователь создал новую таску - {new_task.title}!')
    return new_task


@router.put("/{id}", summary="Изменить задание")
async def update_task(
    db: SessionDep, data: TaskUpdateSchema, id: int
):
    result = await db.execute(select(TaskModel).filter(TaskModel.id == id))
    task = result.scalars().first()
    if not task:
        logging.info(f"Пользователь попытался найти таску но таски с таким ID ({id}) не существует!")
        return HTTPException(status_code=404, detail="No task found!")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    logging.info(f'Пользователь изменил таску - {task.title}!')
    return task


@router.get("/{id}", summary="Получить задание по ID")
async def get_task_by_id(
    db: SessionDep, id: int
):
    result = await db.execute(select(TaskModel).filter(TaskModel.id == id))
    task = result.scalars().first()
    if not task:
        logging.info(f"Пользователь попытался найти таску но таски с таким ID ({id}) не существует!")
        return HTTPException(status_code=404, detail="No task found!")
    
    logging.info(f'Пользователь получил таску по ID ({id}) - {task.id}-{task.title}!')
    return task

@router.delete("/{id}", summary="Удалить задание")
async def delete_task(
    db: SessionDep, id: int
):
    result = await db.execute(select(TaskModel).filter(TaskModel.id == id))
    task = result.scalars().first()
    if not task:
        logging.info(f"Пользователь попытался найти таску но таски с таким ID ({id}) не существует!")
        return HTTPException(status_code=404, detail="No task found!")
    await db.delete(task)
    await db.commit()
    logging.info(f'Пользователь удалил таску по ID ({id})')

    return {'success': True}

