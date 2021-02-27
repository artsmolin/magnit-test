import asyncio

import pytest


async def test_create_task_without_body(client):
    resp = await client.post('/tasks')
    assert resp.status == 400

    body = await resp.text()
    assert body == 'Body is required'


@pytest.mark.parametrize(
    'data',
    [
        {},
        {'x': 1},
        {'x': 1, 'y': 1, 'o': '++'},
        {'x': 1.2, 'y': 1, 'o': '+'},
    ]
)
async def test_create_task_with_invalid_body(client, data: dict):
    resp = await client.post('/tasks', json=data)
    body = await resp.text()
    assert resp.status == 400
    assert 'validation error' in body


async def test_create_task(client, tasks_storage):
    resp = await client.post('/tasks', json={'x': 1, 'y': 2, 'operator': '+'})
    task_id: str = await resp.text()
    assert resp.status == 200
    assert task_id

    task = tasks_storage.get(task_id)
    assert task.x == 1
    assert task.y == 2
    assert task.operator == '+'
    assert task.id == task_id


async def test_get_tasks(client):
    await client.post('/tasks', json={'x': 1, 'y': 2, 'operator': '+'})
    await client.post('/tasks', json={'x': 2, 'y': 2, 'operator': '*'})

    await asyncio.sleep(.5)

    resp = await client.get('/tasks')
    body = await resp.json()
    assert resp.status == 200
    assert len(body) == 2

    assert body[0]['x'] == 1
    assert body[0]['y'] == 2
    assert body[0]['operator'] == '+'
    assert body[0]['result'] == 3
    assert body[0]['status'] == 'done'

    assert body[1]['x'] == 2
    assert body[1]['y'] == 2
    assert body[1]['operator'] == '*'
    assert body[1]['result'] == 4
    assert body[1]['status'] == 'done'


async def test_get_task_result(client):
    resp = await client.post('/tasks', json={'x': 1, 'y': 2, 'operator': '+'})
    task_id: str = await resp.text()

    await asyncio.sleep(.5)

    resp = await client.get(f'/tasks/{task_id}/result')
    assert resp.status == 200

    body = await resp.text()
    assert body == '3'


async def test_get_not_exists_task_result(client):
    resp = await client.get(f'/tasks/1234567890/result')
    assert resp.status == 404
