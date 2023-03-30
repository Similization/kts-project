from datetime import datetime
from random import randint, choice
from typing import List, Set

from kts_backend.game.dataclasses import GameData, GameFull, PlayerFull
from kts_backend.web.app import Application


class PoleChuDesException(Exception):
    pass


class PoleChuDesGame:
    def __init__(self, app: Application):
        """
        Initialize PoleChuDes object, using app
        :param app: Application
        """
        self.app = app
        self.game: GameFull | None = None
        self.players: List[PlayerFull] = list()
        self.current_player: PlayerFull | None = None
        self.current_player_id: int = 0
        self.game_data: GameData | None = None
        self.guessed_word: str = ""
        self.guessed_letters: Set[str] = set()

    async def init_from(self, game: GameFull) -> None:
        """
        Fill PoleChuDes object fields, using game
        :param game: GameFull
        :return: None
        """
        self.game: GameFull = game
        self.players = game.player_list
        self.current_player = choice(self.players)
        self.current_player_id = self.players.index(self.current_player)
        self.game_data = self.game.game_data
        self.guessed_word = game.guessed_word
        self.guessed_letters = set(self.guessed_word)
        self.guessed_letters.remove("*")

    async def get_player(self, player_id: int) -> PlayerFull | None:
        """
        Get player from PoleChuDes object players,
        otherwise return None
        :param player_id: int
        :return: PlayerFull | None
        """
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    async def check_player(self, player: PlayerFull) -> bool:
        """
        Check if player exist and his status is in_game
        :param player: PlayerFull
        :return: bool
        """
        player = await self.get_player(player_id=player.id)
        if not player or not player.in_game:
            return False
        return True

    async def get_active_players(self) -> List[PlayerFull]:
        """
        Get game players, which status is in_game
        :return: List[PlayerFull]
        """
        return [player for player in self.players if player.in_game]

    async def next_player(self) -> None:
        """
        Set next player
        :return: None
        """
        # подразумевается, что после того как останется один игрок - игра завершится,
        # поэтому переходить к следующему игроку смысла нет
        next_player_id = self.current_player_id + 1 % len(self.players)
        while not self.players[next_player_id].in_game:
            next_player_id = next_player_id + 1 % len(self.players)
        self.current_player_id = next_player_id
        self.current_player = self.players[self.current_player_id]

    async def set_player_in_game(
        self, player: PlayerFull, in_game: bool = False
    ) -> None:
        """
        Set player in_game status
        :param player: PlayerFull
        :param in_game: bool
        :return: None
        """
        if not await self.check_player(player=player):
            return
        player.in_game = in_game

    async def check_guess(self, vk_id: int, guess: str) -> None:
        """
        Check player with vk_id guess
        :param vk_id: int
        :param guess: str
        :return: None
        """
        # если vk_id не соответствует vk_id того, кто должен ходить сейчас -> ничего не происходит
        if self.current_player.user.vk_id != vk_id:
            return

        active_players = await self.get_active_players()
        count_of_active_players = len(active_players)

        if len(guess) > 1 or count_of_active_players == 1:
            # угадал слово
            if self.check_answer(answer=guess):
                self.current_player.score += self.generate_points()
                self.current_player.is_winner = True
                self.game.finished_at = datetime.utcnow()
            # не угадал слово
            else:
                self.current_player.in_game = False
                if count_of_active_players == 1:
                    self.game.finished_at = datetime.utcnow()
                else:
                    await self.next_player()
        else:
            if self.guess_letter_result(letter=guess):
                self.current_player.score += self.generate_points()
                if self.check_answer(answer=self.guessed_word):
                    self.current_player.is_winner = True
                    self.game.finished_at = datetime.utcnow()
            else:
                await self.next_player()

    def check_answer(self, answer: str) -> bool:
        """
        Check answer
        :param answer: str
        :return: bool
        """
        return self.game_data.answer == answer

    @staticmethod
    def check_letter(letter: str) -> bool:
        """
        Check letter
        :param letter: str
        :return: bool
        """
        return len(letter) == 1 and (
            "a" <= letter <= "z" or "A" <= letter <= "Z"
        )

    async def add_points(self, player_id: int) -> None:
        """
        Add points to player
        :param player_id: int
        :return: None
        """
        player = await self.get_player(player_id=player_id)
        if await self.check_player(player=player):
            player.score += self.generate_points()

    async def set_winner(self, player_id: int) -> None:
        """
        Set game winner
        :param player_id: int
        :return: None
        """
        player = await self.get_player(player_id=player_id)
        if await self.check_player(player=player):
            player.is_winner = True

    async def guess_letter_result(self, letter: str) -> bool:
        """
        Guess letter result
        :param letter: str
        :return: bool
        """
        if (
            letter in self.guessed_letters
            or letter not in self.game_data.answer
        ):
            return False
        self.guessed_letters.add(letter)
        for i in range(len(self.game_data.answer)):
            if self.game_data.answer[i] != letter:
                continue
            self.guessed_word = (
                self.guessed_word[:i] + letter + self.guessed_word[i + 1 :]
            )
        return True

    @staticmethod
    def generate_points() -> int:
        """
        Generate random points
        :return: int
        """
        return randint(1, 5) * 10
