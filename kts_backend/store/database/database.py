from typing import TYPE_CHECKING, Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from kts_backend.store.database.sqlalchemy_base import db

if TYPE_CHECKING:
    from kts_backend.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        """
        Initialize new Database object, using app
        :param app: Application
        """
        self.app: Application = app
        self._engine: AsyncEngine | None = None
        self._db: Any = None
        self.session: async_sessionmaker | None = None

    async def connect(self, *_: list, **__: dict) -> None:
        """
        Create new connection to database, from self.app.config.database
        :param _: list
        :param __: dict
        :return: None
        """
        self._db = db
        database = self.app.config.database
        url = URL.create(
            drivername="postgresql+asyncpg",
            username=database.user,
            password=database.password,
            host=database.host,
            port=database.port,
            database=database.database,
        )
        self._engine = create_async_engine(url=url, echo=True, future=True)
        self.session = async_sessionmaker(
            bind=self._engine, expire_on_commit=False, class_=AsyncSession
        )
        # TODO: disabled for tests/enabled for run
        if self.app.config.database.type != "test":
            await self.app.store.admin.get_or_create(
                email=self.app.config.admin.email,
                password=self.app.config.admin.password,
            )

    async def disconnect(self, *_: list, **__: dict) -> None:
        """
        Close connection with database
        :param _: list
        :param __: dict
        :return: None
        """
        if self._engine is not None:
            await self._engine.dispose()
