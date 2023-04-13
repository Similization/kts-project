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
from kts_backend.web.config import setup_config
from kts_backend.web.dataclasses import Config
from kts_backend.web.logger import setup_logging
from kts_backend.web.middlewares import setup_middlewares
from kts_backend.web.route import setup_routes


class Application(AiohttpApplication):
    """
    Custom application class that extends aiohttp.web.Application.

    Attributes:
        config (Config | None): Optional configuration object for the application.
        store (Store | None): Optional store object for the application.
        database (Database | None): Optional database object for the application.
    """

    config: Config | None = None
    store: Store | None = None
    database: Database | None = None


class Request(AiohttpRequest):
    """
    Custom request class that extends aiohttp.web.Request.

    Attributes:
        admin (Admin | None): Admin object associated with the request, or None if not available.
    """

    admin: Admin | None = None

    @property
    def app(self) -> Application:
        """
        Return the application associated with the request.

        Returns:
            Application: The application associated with the request.
        """
        return super().app()


class View(AiohttpView):
    """
    Custom view class that extends aiohttp.web.View.

    Attributes:
        request (Request | None): The request associated with the view, or None if not available.
    """

    @property
    def request(self) -> Request | None:
        """
        Return the request associated with the view.

        Returns:
            Request | None: The request associated with the view, or None if not available.
        """
        return super().request

    @property
    def database(self) -> Database | None:
        """
        Return the database associated with the view.

        Returns:
            Database | None: The database associated with the view, or None if not available.
        """
        return self.request.app.database

    @property
    def store(self) -> Store | None:
        """
        Return the store associated with the view.

        Returns:
            Store | None: The store associated with the view, or None if not available.
        """
        return self.request.app.store

    @property
    def data(self) -> dict:
        """
        Return the request data associated with the view.

        Returns:
            dict: The request data associated with the view.
        """
        return self.request.get("data", {})


app = Application()
cors = aiohttp_cors.setup(app)


def setup_app(config: dict) -> Application:
    """
    Setup the Application using the provided configuration.

    Args:
        config (dict): Configuration settings for the Application.

    Returns:
        Application: The configured Application instance.
    """
    # Setup logging
    setup_logging(app)

    # Setup configuration
    setup_config(app=app, config=config)

    # Setup session with encrypted cookie storage
    session_setup(app, EncryptedCookieStorage(app.config.session.key))

    # Setup aiohttp-apispec for API documentation
    setup_aiohttp_apispec(
        app, title="Vk Bot", url="/docs/json", swagger_path="/docs"
    )

    # Setup routes
    setup_routes(app=app)

    # Setup middlewares
    setup_middlewares(app=app)

    # Setup store
    setup_store(app=app)

    return app
