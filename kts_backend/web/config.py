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
    Setup configuration for the Application based on the provided config dictionary.

    Args:
        app (Application): The Application instance for which the configuration is being set up.
        config (dict): The dictionary containing the configuration settings.

    Returns:
        None
    """
    # Extract configuration settings from the config dictionary
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

    # Create a Config instance with the extracted configuration settings
    app.config = Config(
        admin=admin_config,
        bot=bot_config,
        database=database_config,
        session=session_config,
    )
