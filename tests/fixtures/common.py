import logging
from hashlib import sha256
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import yaml
from aiohttp.test_utils import loop_context, TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.util._collections import FacadeDict

from kts_backend.admin.dataclasses import Admin
from kts_backend.admin.model import AdminModel
from kts_backend.store import Database
from kts_backend.store import Store
from kts_backend.store.bot.manager import BotManager
from kts_backend.web.app import setup_app, Application
from kts_backend.web.config import Config


@pytest.fixture(scope="session")
def event_loop():
    """
    :return:
    """
    with loop_context() as _loop:
        yield _loop


@pytest.fixture(scope="session")
def server() -> Application:
    """
    :return: Application
    """
    config = yaml.safe_load(Path("config.yaml").read_text())
    app = setup_app(config=config)

    app.on_startup.clear()
    app.on_shutdown.clear()
    app.store.vk_api = AsyncMock()
    app.store.vk_api.send_message = AsyncMock()
    app.store.vk_api.get_chat_users.return_value = [
        {
            "id": 123,
            "first_name": "Dan",
            "last_name": "Ban",
            "screen_name": "reducter",
        },
        {
            "id": 456,
            "first_name": "Art",
            "last_name": "Shi",
            "screen_name": "stop_27",
        },
        {
            "id": 789,
            "first_name": "Olg",
            "last_name": "Max",
            "screen_name": "cheatcrap",
        },
    ]

    # app.store.bots_manager = BotManager(app=app)
    app.database = Database(app=app)
    app.on_startup.append(app.database.connect)
    app.on_shutdown.append(app.database.disconnect)

    return app


@pytest.fixture
def store(server) -> Store:
    """
    :param server:
    :return: Store
    """
    return server.store


@pytest.fixture
def bot_manager(store) -> BotManager:
    """
    :param store:
    :return: BotManager
    """
    return store.bots_manager


@pytest.fixture
def db_session(server) -> async_sessionmaker | None:
    """
    :param server:
    :return:  async_sessionmaker | None
    """
    return server.database.session


@pytest.fixture(autouse=True, scope="function")
async def clear_db(server):
    """
    :param server:
    :return:
    """
    yield
    try:
        session = AsyncSession(server.database._engine)
        connection = session.connection()
        table_list: FacadeDict = server.database._db.metadata.tables
        for table in table_list.values():
            await session.execute(text(f'TRUNCATE "{table}" CASCADE'))
            await session.execute(
                text(
                    f"ALTER SEQUENCE "
                    f"{table}_{table.primary_key.columns_autoinc_first[0].description}_seq "
                    f"RESTART WITH 1"
                )
            )

        await session.commit()
        connection.close()

    except Exception as err:
        logging.warning(err)


@pytest.fixture
def config(server) -> Config:
    """
    :param server:
    :return: Config
    """
    return server.config


@pytest.fixture(autouse=True)
def cli(aiohttp_client, event_loop, server) -> TestClient:
    """
    :param aiohttp_client:
    :param event_loop:
    :param server:
    :return: TestClient
    """
    return event_loop.run_until_complete(aiohttp_client(server))


@pytest.fixture
async def authed_cli(cli, config) -> TestClient:
    """
    :param cli:
    :param config:
    :return: TestClient
    """
    await cli.post(
        "/admin.login",
        data={
            "email": config.admin.email,
            "password": config.admin.password,
        },
    )
    yield cli


@pytest.fixture(autouse=True)
async def admin(cli, db_session, config: Config) -> Admin:
    """
    :param cli:
    :param db_session:
    :param config:
    :return: Admin
    """
    new_admin = AdminModel(
        email=config.admin.email,
        password=sha256(config.admin.password.encode()).hexdigest(),
    )
    async with db_session.begin() as session:
        session.add(new_admin)

    return Admin(id=new_admin.id, email=new_admin.email, password=new_admin.password)
