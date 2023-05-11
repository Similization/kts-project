from datetime import datetime
from typing import List

from sqlalchemy import (
    Integer,
    VARCHAR,
    Column,
    TIMESTAMP,
    ForeignKey,
    BOOLEAN,
    SmallInteger,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from kts_backend.store.database.sqlalchemy_base import db
from kts_backend.user.model import UserModel


class PlayerModel(db):
    """
    A SQLAlchemy model representing a player in a game.

    Attributes:
        id (int): The ID of the player (primary key, auto-incremented).
        user_id (int): The ID of the user associated with the player (foreign key to `UserModel`).
        user (`UserModel`): The user associated with the player.
        game_id (int): The ID of the game associated with the player (foreign key to `GameModel`).
        game (`GameModel`): The game associated with the player.
        score (int): The score of the player (default 0, nullable=False).
        is_winner (bool): A boolean flag indicating whether the player is a winner (default False, nullable=False).
        in_game (bool): A boolean flag indicating whether the player is still in the game (default True, nullable=False).
    """

    __tablename__ = "player"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="The primary key ID of the player.",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", use_alter=False, ondelete="CASCADE"),
        nullable=False,
        doc="The ID of the user associated with the player (foreign key to `UserModel`).",
    )
    user: Mapped["UserModel"] = relationship(
        foreign_keys=[user_id],
        backref="player",
        lazy="subquery",
        doc="The user associated with the player.",
    )

    game_id: Mapped[int] = mapped_column(
        ForeignKey("game.id", use_alter=False, ondelete="CASCADE"),
        nullable=False,
        doc="The ID of the game associated with the player (foreign key to `GameModel`).",
    )
    game: Mapped["GameModel"] = relationship(
        back_populates="player_list",
        foreign_keys=[game_id],
        lazy="subquery",
        doc="The game associated with the player.",
    )

    score = Column(
        Integer,
        nullable=False,
        default=0,
        doc="The score of the player (default 0, nullable=False).",
    )
    is_winner = Column(
        BOOLEAN,
        default=False,
        nullable=False,
        doc="A boolean flag indicating whether the player is a winner (default False, nullable=False).",
    )
    in_game = Column(
        BOOLEAN,
        default=True,
        nullable=False,
        doc="A boolean flag indicating whether the player is still in the game (default True, nullable=False).",
    )


class GameDataModel(db):
    """
    A SQLAlchemy model representing a game data in a game.

    Attributes:
        id (int): The primary key ID of the game data.
        question (str): The question associated with the game data (required, maximum length 300 characters, unique).
        answer (str): The answer associated with the game data (required, maximum length 30 characters, non-unique).
    """

    __tablename__ = "game_data"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="The primary key ID of the game data.",
    )
    question = Column(
        VARCHAR(300),
        nullable=False,
        unique=True,
        doc="The question associated with the game data (required, maximum length 300 characters, unique).",
    )
    answer = Column(
        VARCHAR(30),
        nullable=False,
        unique=False,
        doc="The answer associated with the game data (required, maximum length 30 characters, non-unique).",
    )


class GameModel(db):
    """
    A SQLAlchemy model representing a game instance.

    Attributes:
        id (int): The primary key of the game instance.
        game_data_id (int): The foreign key of the associated game data.
        game_data (GameDataModel): The game data object associated with the game.
        created_at (datetime): The timestamp of when the game was created.
        finished_at (datetime, optional): The timestamp of when the game was finished, default is None.
        chat_id (str): The ID of the chat where the game is taking place.
        chat_message_id (int, optional): The ID of the message in the chat associated with the game, default is None.
        guessed_word (str): The word that players must guess in the game.
        required_player_count (int): The number of players required to start the game.
        previous_player_id (int, optional): The ID of the previous player in the game, default is None.
        previous_player (PlayerModel, optional): The player object representing the previous player in the game, default is None.
        player_list (List[PlayerModel]): The list of player objects associated with the game.
    """

    __tablename__ = "game"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="The unique ID of the game.",
    )
    game_data_id: Mapped[int] = mapped_column(
        ForeignKey("game_data.id", use_alter=False, ondelete="SET NULL"),
        nullable=False,
        doc="The ID of the game data associated with this game.",
    )
    game_data: Mapped["GameDataModel"] = relationship(
        cascade="all,delete",
        foreign_keys=[game_data_id],
        backref="data_game",
        lazy="subquery",
        doc="The game data associated with this game instance.",
    )

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow,
        doc="The time when the game instance was created.",
    )
    finished_at = Column(
        TIMESTAMP,
        nullable=True,
        default=None,
        doc="The time when the game instance was finished.",
    )

    chat_id = Column(
        VARCHAR(15),
        nullable=False,
        doc="The chat ID where the game instance takes place.",
    )
    chat_message_id = Column(
        Integer,
        nullable=True,
        default=None,
        doc="The message ID of the game instance in the chat.",
    )
    guessed_word = Column(
        VARCHAR(30),
        nullable=False,
        default="",
        doc="The word that is being guessed in the game instance.",
    )
    required_player_count = Column(
        SmallInteger,
        nullable=False,
        default=3,
        doc="The minimum number of players required to start the game.",
    )
    previous_player_id: Mapped[int] = mapped_column(
        ForeignKey("player.id", use_alter=True, ondelete="SET NULL"),
        nullable=True,
        default=None,
        doc="The ID of the previous player who played in the game instance.",
    )
    previous_player: Mapped["PlayerModel"] = relationship(
        foreign_keys=[previous_player_id],
        lazy="subquery",
        doc="The previous player who played in the game instance.",
    )
    player_list: Mapped[List["PlayerModel"]] = relationship(
        back_populates="game",
        cascade="all,delete",
        primaryjoin="(GameModel.id==PlayerModel.game_id)",
        lazy="subquery",
        doc="The list of players who are playing in the game instance.",
    )
