import asyncio

import litestar
from litestar.di import Provide
import uvicorn
from litestar import Litestar
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server

from quiz_examples.code_snippet.background.courses import CoursesWorker
from quiz_examples.code_snippet.controllers.auth import AuthController
from quiz_examples.code_snippet.controllers.courses import CoursesController
from quiz_examples.code_snippet.controllers.user import UserController
from quiz_examples.code_snippet.core.publisher import MockedPublisher
from quiz_examples.code_snippet.core.repository import MockedRepository
from quiz_examples.code_snippet.exceptions.handler import EXCEPTION_HANDLERS
from quiz_examples.code_snippet.exceptions.handler import handle_all_errors


async def _startup(app: Litestar):
    repository = await app.dependencies["db_repository"]()
    publisher = await app.dependencies["publisher"]()

    worker = await app.dependencies["courses_worker"](
        db_repository=repository,
        publisher=publisher,
    )

    app.state.worker_task = asyncio.create_task(worker.run())

async def _shutdown():
    pass

def app():
    _middlewares = [

    ]
    logging_config = LoggingConfig(
        exception_logging_handler=handle_all_errors, configure_root_logger=False
    )
    _litestar_app = Litestar(
        debug=True,
        openapi_config=OpenAPIConfig(
            title="API",
            description="API",
            version="1.0.0",
            servers=[
                Server(url="/", description="Local based server"),
            ],
            path="/docs",
            create_examples=False,
        ),
        route_handlers=[
            litestar.Router(
                path="/",
                route_handlers=[
                    # AuthController,
                    UserController,
                    CoursesController
                ],
            ),
        ],
        logging_config=logging_config,
        middleware=_middlewares,
        on_startup=[_startup],
        on_shutdown=[_shutdown],
        exception_handlers=EXCEPTION_HANDLERS,
        dependencies={
                    "db_repository": Provide(MockedRepository, use_cache=True),
                    "publisher": Provide(MockedPublisher, use_cache=True),
                    "courses_worker": Provide(
                        CoursesWorker,
                        use_cache=True
                    )
                }
    )
    return _litestar_app
if __name__ == '__main__':
    uvicorn.run(
        "quiz_examples.code_snippet.run:app",
        host="0.0.0.0",
        port=9090,
        reload=True,
    )
