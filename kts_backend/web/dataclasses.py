from dataclasses import dataclass


@dataclass(slots=True)
class SessionConfig:
    key: str


@dataclass(slots=True)
class AdminConfig:
    email: str
    password: str


@dataclass(slots=True)
class BotConfig:
    token: str
    group_id: int


@dataclass(slots=True)
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(slots=True)
class Config:
    admin: AdminConfig = None
    bot: BotConfig = None
    database: DatabaseConfig = None
    session: SessionConfig = None
