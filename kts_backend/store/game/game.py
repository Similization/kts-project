import logging
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
        self.logger = logging.getLogger("game")
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
        if "*" in self.guessed_letters:
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
        return list(filter(lambda player: player.in_game, self.players))

    async def next_player(self) -> None:
        """
        Set next player
        :return: None
        """
        next_player_id = (self.current_player_id + 1) % len(self.players)
        while not self.players[next_player_id].in_game:
            next_player_id = (next_player_id + 1) % len(self.players)
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

    async def check_guess(self, vk_id: int, guess: str) -> str:
        """
        Check player with vk_id guess
        :param vk_id: int
        :param guess: str
        :return: str
        """
        # если vk_id не соответствует vk_id того, кто должен ходить сейчас -> ничего не происходит
        if self.current_player.user.vk_id != vk_id:
            return (
                f"Сейчас не ваш ход или вы выбыли из игры(\n"
                f"Ход принадлежит игроку: {self.current_player.user.username}!\n"
                f"Отгданное слово: {self.guessed_word}\n"
            )

        active_players = await self.get_active_players()
        count_of_active_players = len(active_players)

        if len(guess) > 1 or count_of_active_players == 1:
            return await self.guess_word(
                guess=guess, count_of_active_players=count_of_active_players
            )
        else:
            return await self.guess_letter(guess=guess)

    async def guess_word(self, guess: str, count_of_active_players: int):
        """
        :param guess:
        :param count_of_active_players:
        :return:
        """
        game_result = ""
        if self.check_answer(answer=guess):
            self.logger.debug(
                f"{self.current_player.user.username} guessed a word"
            )
            game_result += await self.add_points()
            self.current_player.is_winner = True
            self.game.finished_at = datetime.utcnow()
            game_result += (
                f"Игрок: {self.current_player.user.username} угадал слово!\n"
            )
            game_result += f"Отгданное слово: {self.guessed_word}\n"
            game_result += "Игра завершена!\n"
            await self.app.store.game.update_one_player_full(
                player=self.current_player
            )
            self.game.previous_player = self.current_player
            await self.app.store.game.update_game(game=self.game)
            return game_result
        else:
            self.logger.debug(
                f"{self.current_player.user.username} didn't guess a word"
            )
            game_result = (
                f"Игрок: {self.current_player.user.username} не угадал слово\n"
            )
            game_result += f"Отгданное слово: {self.guessed_word}\n"
            self.current_player.in_game = False
            await self.app.store.game.update_one_player_full(
                player=self.current_player
            )
            if count_of_active_players == 1:
                self.game.finished_at = datetime.utcnow()
                game_result += "Игра завершена!\n"
            else:
                await self.next_player()
                game_result += (
                    f"Следующий игрок: {self.current_player.user.username}\n"
                )
            self.game.previous_player = self.current_player
            await self.app.store.game.update_game(game=self.game)
            return game_result

    async def guess_letter(self, guess: str) -> str:
        """
        :param guess:
        :return:
        """
        game_result: str = ""
        if await self.guess_letter_result(letter=guess):
            self.logger.debug(
                f"{self.current_player.user.username} guessed letter"
            )
            game_result += await self.add_points()
            game_result += f"Отгаданное слово: {self.guessed_word}\n"
            if self.check_answer(answer=self.guessed_word):
                self.current_player.is_winner = True
                self.game.finished_at = datetime.utcnow()
                game_result += f"Игрок: {self.current_player.user.username} угадал слово!\n"
                game_result += "Игра завершена!\n"
            await self.app.store.game.update_one_player_full(
                player=self.current_player
            )
            self.game.previous_player = self.current_player
            await self.app.store.game.update_game(game=self.game)
            return game_result
        else:
            self.logger.debug(
                f"{self.current_player.user.username} didn't guess letter"
            )
            game_result += (
                f"Игрок: {self.current_player.user.username} не угадал букву(\n"
            )
            game_result += f"Отгданное слово: {self.guessed_word}\n"
            await self.next_player()
            game_result += (
                f"Следующий игрок: {self.current_player.user.username}\n"
            )
            self.game.previous_player = self.current_player
            await self.app.store.game.update_game(game=self.game)
            return game_result

    def check_answer(self, answer: str) -> bool:
        """
        Check answer
        :param answer: str
        :return: bool
        """
        if self.game_data.answer.lower() == answer.lower():
            self.guessed_word = answer.capitalize()
            return True
        return False

    async def finish(self):
        self.game.finished_at = datetime.utcnow()
        self.game.previous_player = self.current_player
        await self.app.store.game.update_game(game=self.game)

    @staticmethod
    def check_letter(letter: str) -> bool:
        """
        Check letter
        :param letter: str
        :return: bool
        """
        return len(letter) == 1 and letter.isalpha()

    async def add_points(self) -> str:
        """
        Add points to player
        :return: str
        """
        generated_points: int = self.generate_points()
        self.current_player.score += generated_points
        return f"Игрок: {self.current_player.user.username} получает {generated_points} очко(ов)\n"

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
        Guesses a letter and updates the game state.

        Args:
            letter (str): The letter to guess.

        Returns:
            bool: True if the guess is correct, False otherwise.
        """
        lower_letter = letter.lower()
        lower_answer = self.game.game_data.answer.lower()

        # If letter has already been guessed or is not in the answer, return False
        if (
            lower_letter in self.guessed_letters
            or lower_letter not in lower_answer
        ):
            return False

        # Add letter to guessed letters and update guessed word
        self.guessed_letters.add(lower_letter)
        for i in range(len(lower_answer)):
            if lower_answer[i] != letter:
                continue
            self.guessed_word = (
                self.guessed_word[:i] + letter + self.guessed_word[i + 1 :]
            )
        return True

    @staticmethod
    def generate_points() -> int:
        """
        Generate a random number of points between 10 and 50 (inclusive) in multiples of 10.
        :return: int
        """
        return randint(1, 5) * 10
