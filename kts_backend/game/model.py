from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, relationship, mapped_column

from sqlalchemy import (
    Integer,
    VARCHAR,
    Column,
    TIMESTAMP,
    ForeignKey,
    BOOLEAN,
    SmallInteger,
)

from kts_backend.store.database.sqlalchemy_base import db
from kts_backend.user.model import UserModel


class PlayerModel(db):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", use_alter=False, ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["UserModel"] = relationship(
        foreign_keys=[user_id], backref="player", lazy="subquery"
    )

    game_id: Mapped[int] = mapped_column(
        ForeignKey("game.id", use_alter=False, ondelete="CASCADE"),
        nullable=False,
    )
    game: Mapped["GameModel"] = relationship(
        back_populates="player_list", foreign_keys=[game_id], lazy="subquery"
    )

    score = Column(Integer, nullable=False, default=0)
    is_winner = Column(BOOLEAN, default=False, nullable=False)
    in_game = Column(BOOLEAN, default=True)


class GameDataModel(db):
    __tablename__ = "game_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(VARCHAR(300), nullable=False, unique=True)
    answer = Column(VARCHAR(30), nullable=False, unique=False)


class GameModel(db):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)

    game_data_id: Mapped[int] = mapped_column(
        ForeignKey("game_data.id", use_alter=False, ondelete="SET NULL"),
        nullable=False,
    )
    game_data: Mapped["GameDataModel"] = relationship(
        cascade="all,delete",
        foreign_keys=[game_data_id],
        backref="data_game",
        lazy="subquery",
    )

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    finished_at = Column(TIMESTAMP, nullable=True, default=None)

    chat_id = Column(VARCHAR(15), nullable=False)
    chat_message_id = Column(Integer, nullable=True, default=None)

    guessed_word = Column(VARCHAR(30), nullable=False, default="")
    required_player_count = Column(SmallInteger, nullable=False, default=3)

    previous_player_id: Mapped[int] = mapped_column(
        ForeignKey("player.id", use_alter=True, ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    previous_player: Mapped["PlayerModel"] = relationship(
        backref="player_game",
        foreign_keys=[previous_player_id],
        lazy="subquery",
    )

    player_list: Mapped[List["PlayerModel"]] = relationship(
        back_populates="game",
        cascade="all,delete",
        primaryjoin="(GameModel.id==PlayerModel.game_id)",
        lazy="subquery",
    )
