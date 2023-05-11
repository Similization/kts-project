from dataclasses import dataclass
from datetime import datetime
from typing import List

from kts_backend.user.dataclasses import User


@dataclass(slots=True)
class Player:
    """
    Represents a player in a game.

    Attributes:
        user_id (int): The ID of the user associated with the player.
        game_id (int): The ID of the game the player is in.
        id (int, optional): The ID of the player (default None).
        score (int, optional): The player's score (default None).
        is_winner (bool, optional): True if the player is the winner, False otherwise (default None).
        in_game (bool, optional): True if the player is still in the game, False otherwise (default None).
    """

    user_id: int
    game_id: int
    id: int | None = None
    score: int | None = None
    is_winner: bool | None = None
    in_game: bool | None = None


@dataclass(slots=True)
class GameData:
    """
    Class for representing game data.

    Attributes:
        id (int): The ID of the game.
        question (str): The question for the game.
        answer (str): The answer to the question.
    """

    id: int
    question: str
    answer: str


@dataclass(slots=True)
class Game:
    """
    A class representing a game instance.

    Attributes:
        id (int): The ID of the game.
        game_data_id (int): The ID of the game data associated with the game.
        created_at (datetime): The datetime when the game was created.
        finished_at (datetime): The datetime when the game was finished.
        chat_id (str): The ID of the chat associated with the game.
        chat_message_id (int): The ID of the message associated with the game.
        guessed_word (str): The word to be guessed in the game.
        required_player_count (int): The number of players required to start the game.
        previous_player_id (int): The ID of the previous player who made a guess.
        player_list (List[Player]): A list of player instances who are part of the game.
    """

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
    """
    Data class representing a player in a game.

    Attributes:
        id (int): The ID of the player.
        user (User): The user associated with the player.
        game (Game): The game associated with the player, if any.
        score (int): The score of the player.
        is_winner (bool): True if the player is a winner, False otherwise.
        in_game (bool): True if the player is currently in a game, False otherwise.
    """

    id: int
    user: User
    game: Game | None
    score: int
    is_winner: bool | None
    in_game: bool


@dataclass(slots=True)
class GameFull:
    """
    A dataclass representing a full game.

    Attributes:
        id (int): The ID of the game.
        game_data (GameData): The data for the game.
        created_at (datetime): The datetime when the game was created.
        finished_at (datetime): The datetime when the game was finished.
        chat_id (str): The ID of the chat associated with the game.
        chat_message_id (int | None): The ID of the message associated with the game.
        guessed_word (str): The word that players must guess.
        required_player_count (int): The required number of players for the game.
        previous_player (PlayerFull | None): The previous player who guessed the word, if any.
        player_list (List[PlayerFull]): A list of players in the game.
    """

    id: int
    game_data: GameData
    created_at: datetime
    finished_at: datetime
    chat_id: str
    chat_message_id: int | None
    guessed_word: str
    required_player_count: int
    previous_player: PlayerFull | None
    player_list: List[PlayerFull]
