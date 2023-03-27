from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Integer,
    VARCHAR,
    Column,
    TIMESTAMP,
    ForeignKey,
    BOOLEAN,
    Null,
)

from kts_backend.store.database.sqlalchemy_base import db
from kts_backend.user.model import User


@dataclass
class Player:
    player_id: int
    user_id: int
    score: int
    is_winner: Optional[bool]
    in_game: bool


@dataclass
class GameData:
    game_data_id: int
    question: str
    answer: str


@dataclass
class Game:
    game_id: int
    game_data_id: int
    created_at: datetime
    finished_at: datetime
    chat_id: int

    player_list: List[Player]


@dataclass
class PlayerGame:
    player_game_id: int
    player_id: int
    game_id: int


@dataclass
class PlayerFull:
    user: User
    player_id: int
    score: int
    is_winner: bool


@dataclass
class GameFull:
    game_id: int
    game_data: GameData
    created_at: datetime
    finished_at: datetime
    chat_id: int

    player_list: List[PlayerFull]


@dataclass
class PlayerGameFull:
    player_game_id: int
    player: Player
    game: Game


class PlayerModel(db):
    __tablename__ = "player"

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )
    score = Column(Integer, nullable=False, default=0)
    is_winner = Column(BOOLEAN)
    in_game = Column(BOOLEAN, default=True)


class GameDataModel(db):
    __tablename__ = "game_data"

    game_data_id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(VARCHAR(90), nullable=False, unique=True)
    answer = Column(VARCHAR(30), nullable=False, unique=True)


class GameModel(db):
    __tablename__ = "game"

    game_id = Column(Integer, primary_key=True, autoincrement=True)
    game_data_id = Column(
        Integer,
        ForeignKey("game_data.game_data_id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    finished_at = Column(TIMESTAMP, nullable=True, default=Null)
    chat_id = Column(Integer, nullable=False)
    # required_player_count = Column(Integer, nullable=False, default=3)


class PlayerGameModel(db):
    __tablename__ = "player_game_data"

    player_game_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(
        Integer,
        ForeignKey("player.player_id", ondelete="CASCADE"),
        nullable=False,
    )
    game_id = Column(
        Integer, ForeignKey("game.game_id", ondelete="CASCADE"), nullable=False
    )
