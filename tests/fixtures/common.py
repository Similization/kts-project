import logging
from hashlib import sha256
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import yaml
from aiohttp.test_utils import loop_context, TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from kts_backend.admin.model import AdminModel, Admin
from kts_backend.store import Database
from kts_backend.store import Store
from kts_backend.web.app import setup_app
from kts_backend.web.config import Config


@pytest.fixture(scope="session")
def event_loop():
    with loop_context() as _loop:
        yield _loop


@pytest.fixture(scope="session")
def server():
    config = yaml.safe_load(Path("config.yaml").read_text())
    app = setup_app(config=config)

    app.on_startup.clear()
    app.on_shutdown.clear()
    app.store.vk_api = AsyncMock()
    app.store.vk_api.send_message = AsyncMock()

    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_shutdown.append(app.database.disconnect)

    return app


@pytest.fixture
def store(server) -> Store:
    return server.store


@pytest.fixture
def db_session(server):
    return server.database.session


@pytest.fixture(autouse=True, scope="function")
async def clear_db(server):
    yield
    try:
        session = AsyncSession(server.database._engine)
        connection = session.connection()
        for table in server.database._db.metadata.tables:
            await session.execute(text(f"TRUNCATE {table} CASCADE"))
            await session.execute(
                text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1")
            )

        await session.commit()
        connection.close()

    except Exception as err:
        logging.warning(err)


@pytest.fixture
def config(server) -> Config:
    return server.config


@pytest.fixture(autouse=True)
def cli(aiohttp_client, event_loop, server) -> TestClient:
    return event_loop.run_until_complete(aiohttp_client(server))


@pytest.fixture
async def authed_cli(cli, config) -> TestClient:
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
    new_admin = AdminModel(
        email=config.admin.email,
        password=sha256(config.admin.password.encode()).hexdigest(),
    )
    async with db_session.begin() as session:
        session.add(new_admin)

    return Admin(admin_id=new_admin.id, email=new_admin.email)
