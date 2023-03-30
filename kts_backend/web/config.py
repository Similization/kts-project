import typing

from kts_backend.web.dataclasses import (
    Config,
    AdminConfig,
    BotConfig,
    DatabaseConfig,
    SessionConfig,
)

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


def setup_config(app: "Application", config: dict) -> None:
    """
    Setup application configuration
    :param app: Application
    :param config: dict
    :return: None
    """
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
