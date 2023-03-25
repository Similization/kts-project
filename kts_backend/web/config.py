import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class BotConfig:
    token: str
    group_id: int


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class Config:
    admin: AdminConfig = None
    bot: BotConfig = None
    database: DatabaseConfig = None
    session: SessionConfig = None


def setup_config(app: "Application", config: dict):
    app.config = Config(
        admin=AdminConfig(
            email=config["admin"]["email"],
            password=config["admin"]["password"],
        ),
        bot=BotConfig(
            token=config["bot"]["key"],
            group_id=config["bot"]["group_id"],
        ),
        database=DatabaseConfig(**config["database"]),
        session=SessionConfig(
            key=config["session"]["key"],
        ),
    )
