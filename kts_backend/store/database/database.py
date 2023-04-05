import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

from kts_backend.store.database.sqlalchemy_base import db

if TYPE_CHECKING:
    from kts_backend.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        """
        Initializes a new Database object.

        :param app: The Application object used to configure the database.
        """
        self.app: Application = app
        self._engine: AsyncEngine | None = None
        self._db: Any = None
        self.session: async_sessionmaker | None = None
        self.logger = logging.getLogger(__name__)

    async def connect(self, *_: list, **__: dict) -> None:
        """
        Creates a new connection to the database using the configuration settings specified in the Application object.

        :param _: Unused positional argument.
        :param __: Unused keyword argument.
        """
        self.logger.debug("Connecting to database")

        # Initialize the database object.
        self._db = db

        # Create the connection URL.
        database = self.app.config.database
        url = URL.create(
            drivername="postgresql+asyncpg",
            username=database.user,
            password=database.password,
            host=database.host,
            port=database.port,
            database=database.database,
        )

        # Create the engine and session objects.
        self._engine = create_async_engine(url=url, echo=True, future=True)
        self.session = async_sessionmaker(
            bind=self._engine, expire_on_commit=False, class_=AsyncSession
        )

        # Set up the admin user, but only if this is not a test database.
        if self.app.config.database.type != "test":
            await self._setup_admin()

    async def disconnect(self, *_: list, **__: dict) -> None:
        """
        Closes the connection to the database.

        :param _: Unused positional argument.
        :param __: Unused keyword argument.
        """
        self.logger.debug("Disconnecting from database")

        # Dispose of the engine to close the connection.
        if self._engine is not None:
            await self._engine.dispose()

    async def _setup_admin(self):
        """
        Sets up the admin user account, if it does not already exist in the database.
        """
        await self.app.store.admin.get_or_create(
            email=self.app.config.admin.email,
            password=self.app.config.admin.password,
        )
