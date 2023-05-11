from dataclasses import dataclass


@dataclass(slots=True)
class SessionConfig:
    """
    Configuration for session management.

    Attributes:
        key (str): The key used for session management.
    """

    key: str


@dataclass(slots=True)
class AdminConfig:
    """
    Configuration for admin settings.

    Attributes:
        email (str): The email of the admin user.
        password (str): The password of the admin user.
    """

    email: str
    password: str


@dataclass(slots=True)
class BotConfig:
    """
    Configuration for bot settings.

    Attributes:
        token (str): The token used for authentication with the bot API.
        group_id (int): The ID of the group associated with the bot.
    """

    token: str
    group_id: int


@dataclass(slots=True)
class DatabaseConfig:
    """
    Configuration for database settings.

    Attributes:
        type (str): The type of database being used.
        host (str): The hostname or IP address of the database server.
        port (int): The port number of the database server.
        user (str): The username used for authentication with the database server.
        password (str): The password used for authentication with the database server.
        database (str): The name of the database.
    """

    type: str
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(slots=True)
class Config:
    """
    Configuration class for storing various settings.

    Attributes:
        admin (AdminConfig): The configuration for admin settings.
        bot (BotConfig): The configuration for bot settings.
        database (DatabaseConfig): The configuration for database settings.
        session (SessionConfig): The configuration for session management.
    """

    admin: AdminConfig = None
    bot: BotConfig = None
    database: DatabaseConfig = None
    session: SessionConfig = None
