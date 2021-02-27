from aiohttp import web
from loguru import logger

from magnit_test import middlewares
from magnit_test import urls


def get_web_app() -> web.Application:
    app = web.Application(middlewares=[
        middlewares.log_requests,
    ])
    app.add_routes(urls.routes)
    return app


if __name__ == "__main__":
    logger.info('Run app')
    web_app = get_web_app()
    web.run_app(web_app)
