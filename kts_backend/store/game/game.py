import random
from random import choice
from typing import List, Set

from kts_backend.game.model import Player, GameData
from kts_backend.web.app import app

# create game for N (from 3 to 5) players
#
# wait for N players to connect
#
# create game
# create queue
#
# if player guess letter -> he gets random points and can guess again
# else another player guess
#
# if player guess word -> he wins
# else -> he loses

# import asyncio
#
# get players id from message
# create players if they are not exists
# players_id = [1, 2, 3, 4, 5]
# queue = asyncio.Queue(maxsize=len(players_id))
#
# while not queue.empty():


class PoleChudesGame:
    def __init__(self, players: List[Player]):
        self.players: List[Player] = players
        self.game: GameData = self.generate_game_data()
        self.guessed_word = "*" * len(self.game.answer)
        self.guessed_letters: Set[str] = set()

    @staticmethod
    def generate_game_data() -> GameData:
        game_datas = await app.store.game.get_game_data_list()
        return choice(seq=game_datas)

    def check_answer(self, answer: str) -> bool:
        return self.game.answer == answer

    @staticmethod
    def check_letter(letter: str) -> bool:
        return len(letter) == 1 and (
            "a" <= letter <= "z" or "A" <= letter <= "Z"
        )

    def guess_letter_result(self, letter: str) -> bool:
        if letter in self.guessed_letters or letter not in self.game.answer:
            return False
        self.guessed_letters.add(letter)
        for i in range(len(self.game.answer)):
            if self.game.answer[i] != letter:
                continue
            self.guessed_word = (
                self.guessed_word[:i] + letter + self.guessed_word[i + 1 :]
            )
        return True

    @staticmethod
    def generate_points() -> int:
        return random.randint(1, 5) * 10
