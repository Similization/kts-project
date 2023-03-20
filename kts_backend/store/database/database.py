from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import URL

from kts_backend.store.database.sqlalchemy_base import db

if TYPE_CHECKING:
    from kts_backend.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app: Application = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        database = self.app.config.database
        url = URL.create(
            drivername="postgresql+asyncpg",
            username=database.user,
            password=database.password,
            host=database.host,
            port=database.port,
            database=database.database
        )
        self._engine = create_async_engine(
            url=url,
            echo=True,
            future=True
        )
        self.session = async_sessionmaker(
            bind=self._engine, expire_on_commit=False, class_=AsyncSession
        )

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine is not None:
            await self._engine.dispose()
