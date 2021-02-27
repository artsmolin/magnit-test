import asyncio

import pydantic
from aiohttp.web import Request
from aiohttp.web import Response
from aiohttp.web import json_response

from magnit_test import exceptions
from magnit_test import models
from magnit_test.storages import tasks_storage
from magnit_test.utils import handle_exceptions


@handle_exceptions(pydantic.ValidationError, exceptions.EmptyBody)
async def create_task(request: Request) -> Response:
    """
    Создать таску

    - Сохранить таску в хранилище
    - Запустить асинхронный обработчик таски

    Parameters
    ----------
    request

    Returns
    -------
    Response:
        ID созданной таски
    """
    if not request.body_exists:
        raise exceptions.EmptyBody()

    task_data = await request.json()
    task = models.Task(**task_data)
    tasks_storage.set(task.id, task)
    asyncio.Task(task.execute())
    return Response(text=task.id)


async def get_task_result(request: Request) -> Response:
    """Вернуть результат вычисления для указанного ID таски"""
    task_id: str = request.match_info["id"]
    try:
        task = tasks_storage.get(task_id)
    except KeyError:
        return Response(status=404)
    return Response(text=str(task.result))


async def get_tasks(_) -> Response:
    """Вернуть коллекцию тасков с их статусами исполнения"""
    tasks = [task.dict() for task in tasks_storage.get_collection()]
    return json_response(tasks)
