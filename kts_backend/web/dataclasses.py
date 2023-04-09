from dataclasses import dataclass


@dataclass(slots=True)
class SessionConfig:
    """Class that holds the configuration for session."""

    key: str


@dataclass(slots=True)
class AdminConfig:
    """Class that holds the configuration for admin."""

    email: str
    password: str


@dataclass(slots=True)
class BotConfig:
    """Class that holds the configuration for bot."""

    token: str
    group_id: int


@dataclass(slots=True)
class DatabaseConfig:
    """Class that holds the configuration for database."""

    type: str
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(slots=True)
class Config:
    """Class that holds the configuration for the application."""

    admin: AdminConfig = None
    bot: BotConfig = None
    database: DatabaseConfig = None
    session: SessionConfig = None
