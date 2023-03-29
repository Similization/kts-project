from typing import Optional

import aiohttp_cors
from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest,
)

from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_apispec import setup_aiohttp_apispec

from kts_backend.admin.dataclasses import Admin
from kts_backend.store import setup_store, Store
from kts_backend.store.database.database import Database
from kts_backend.web.config import setup_config, Config
from kts_backend.web.logger import setup_logging
from kts_backend.web.middlewares import setup_middlewares
from kts_backend.web.route import setup_routes
from kts_backend.web.urls import register_urls


class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database: Optional[Database] = None


class Request(AiohttpRequest):
    admin: Optional[Admin] = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def database(self):
        return self.request.app.database

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


app = Application()
cors = aiohttp_cors.setup(app)


def setup_app(config: dict) -> Application:
    setup_logging(app)
    setup_config(app=app, config=config)
    session_setup(app, EncryptedCookieStorage(app.config.session.key))
    setup_aiohttp_apispec(
        app, title="Vk Bot", url="/docs/json", swagger_path="/docs"
    )
    setup_routes(app=app)
    register_urls(app=app, cors=cors)
    setup_middlewares(app=app)
    setup_store(app=app)
    return app
