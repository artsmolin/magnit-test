import uuid

from aiohttp.web import Response


def handle_exceptions(*exceptions):
    """
    Декоратор на view-функцию. В случае вызова пересичленных исключений
    возвращает ответ (aiohttp.web_response.Response) с текстом исключения
    и кодом 400.
    """

    def fn_wrapper(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as exc:
                return Response(status=400, text=(str(exc)))

        return wrapper

    return fn_wrapper


def uuid4_str() -> str:
    return str(uuid.uuid4())
