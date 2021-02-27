from aiohttp.web import middleware
from aiohttp.web import Request
from loguru import logger


@middleware
async def log_requests(request: Request, handler: callable):
    raw_body = await request.text()
    logger.info(f'{request.method} {request.path} {request.query_string} {raw_body}')
    return await handler(request)
