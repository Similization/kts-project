from dataclasses import dataclass
from datetime import datetime
from typing import List

from kts_backend.user.dataclasses import User


@dataclass(slots=True)
class Player:
    user_id: int
    game_id: int
    id: int | None = None
    score: int | None = None
    is_winner: bool | None = None
    in_game: bool | None = None


@dataclass(slots=True)
class GameData:
    id: int
    question: str
    answer: str


@dataclass(slots=True)
class Game:
    id: int
    game_data_id: int

    created_at: datetime
    finished_at: datetime

    chat_id: str
    chat_message_id: int | None

    guessed_word: str
    required_player_count: int
    previous_player_id: int | None

    player_list: List[Player]


@dataclass
class PlayerFull:
    id: int
    user: User
    game: Game | None
    score: int
    is_winner: bool | None
    in_game: bool


@dataclass(slots=True)
class GameFull:
    id: int
    game_data: GameData

    created_at: datetime
    finished_at: datetime

    chat_id: str
    chat_message_id: int | None

    guessed_word: str
    required_player_count: int
    previous_player: Player | None

    player_list: List[PlayerFull]
