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
    Set up the configuration for the application.

    :param app: The Flask application instance.
    :type app: Application
    :param config: A dictionary containing the configuration options for the application.
    :type config: dict
    :return: None
    """
    admin_config = AdminConfig(
        email=config["admin"]["email"],
        password=config["admin"]["password"],
    )

    bot_config = BotConfig(
        token=config["bot"]["key"],
        group_id=config["bot"]["group_id"],
    )

    database_config = DatabaseConfig(**config["database"])

    session_config = SessionConfig(
        key=config["session"]["key"],
    )

    app.config = Config(
        admin=admin_config,
        bot=bot_config,
        database=database_config,
        session=session_config,
    )
