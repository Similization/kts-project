from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy import Integer, VARCHAR, Column, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from kts_backend.store.database.sqlalchemy_base import db


# class GameScoreDC:
#     points: int


@dataclass
class PlayerDC:
    vk_id: int
    name: str
    last_name: str


@dataclass
class GameDC:
    game_id: int
    created_at: datetime
    chat_id: int

    players: list[PlayerDC]


# class GameScoreModel(db):
#     __tablename__ = "game_score"
#
#     points = Column(Integer, nullable=False)


class PlayerModel(db):
    __tablename__ = "player"

    vk_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    last_name = Column(VARCHAR(45), nullable=False)


class PlayerGameScoreModel(db):
    __tablename__ = "player_game_score"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(
        Integer, ForeignKey("player.vk_id", ondelete="CASCADE"), nullable=False
    )
    game_id = Column(
        Integer, ForeignKey("game.game_id", ondelete="CASCADE"), nullable=False
    )
    score = Column(Integer, nullable=False, default=0)


class GameModel(db):
    __tablename__ = "game"

    game_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    chat_id = Column(Integer, nullable=False)

    # players: List["PlayerModel"] = relationship("PlayerModel", cascade="all,delete", backref="game")
