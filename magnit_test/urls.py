from aiohttp import web

from . import views

routes = [
    web.post("/tasks", views.create_task),
    web.get(r"/tasks/{id}/result", views.get_task_result),
    web.get("/tasks", views.get_tasks),
]
