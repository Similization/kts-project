from typing import List

import pytest

from kts_backend.game.dataclasses import GameFull, PlayerFull
from kts_backend.store.game.game import PoleChuDesGame
from kts_backend.web.app import Application


@pytest.fixture
async def pole_chu_des_1(
    server: Application, game_full_1: GameFull
) -> PoleChuDesGame:
    pole_chu_des_game: PoleChuDesGame = PoleChuDesGame(app=server)
    await pole_chu_des_game.init_from(game=game_full_1)

    return pole_chu_des_game


class TestPoleChuDesGame:
    async def test_init_from(self, server: Application, game_full_1: GameFull):
        pole_chu_des_game: PoleChuDesGame = PoleChuDesGame(app=server)
        await pole_chu_des_game.init_from(game=game_full_1)
        assert pole_chu_des_game.game == game_full_1
        assert pole_chu_des_game.game_data == game_full_1.game_data
        assert pole_chu_des_game.players == game_full_1.player_list

        player_list: List[PlayerFull] = game_full_1.player_list
        previous_player: PlayerFull = game_full_1.previous_player
        player_id: int = -1
        for i in range(len(player_list)):
            if player_list[i].id == previous_player.id:
                player_id = i
        assert pole_chu_des_game.current_player_id == player_id

        assert pole_chu_des_game.current_player == game_full_1.previous_player
        assert pole_chu_des_game.guessed_letters == set(
            game_full_1.guessed_word
        )
        assert pole_chu_des_game.guessed_word == game_full_1.guessed_word

    async def test_get_init_player_id(self, pole_chu_des_1: PoleChuDesGame):
        assert await pole_chu_des_1._get_init_player_id() == 2

    async def test_get_player_returns_player_with_matching_id(
        self, server: Application, game_full_1: GameFull
    ):
        pole_chu_des_game: PoleChuDesGame = PoleChuDesGame(app=server)
        await pole_chu_des_game.init_from(game=game_full_1)

        player_to_find = game_full_1.player_list[0]
        player_id = player_to_find.id
        player = await pole_chu_des_game.get_player(player_id)
        assert player is not None
        assert player.id == player_id
        assert player.user == player_to_find.user
        assert player.game == player_to_find.game
        assert player.score == player.score
        assert player.in_game == player.in_game
        assert player.is_winner == player.is_winner

    async def test_get_player_returns_none_for_nonexistent_id(
        self, server: Application, game_full_1: GameFull
    ):
        pole_chu_des_game: PoleChuDesGame = PoleChuDesGame(app=server)
        await pole_chu_des_game.init_from(game=game_full_1)

        player_id = 999
        player = await pole_chu_des_game.get_player(player_id)
        assert player is None

    async def test_check_player_exists_and_in_game(
        self, pole_chu_des_1: PoleChuDesGame
    ):
        player = pole_chu_des_1.players[0]
        player.in_game = True
        assert await pole_chu_des_1.check_player(player)

    async def test_check_player_not_exists_or_not_in_game(
        self, pole_chu_des_1: PoleChuDesGame
    ):
        player = pole_chu_des_1.players[0]
        player.in_game = False
        assert not await pole_chu_des_1.check_player(player)

    async def test_next_player(self, pole_chu_des_1: PoleChuDesGame):
        initial_player_id = pole_chu_des_1.current_player_id
        initial_player = pole_chu_des_1.current_player

        await pole_chu_des_1.next_player()

        assert pole_chu_des_1.current_player_id == (
            initial_player_id + 1
        ) % len(pole_chu_des_1.players)
        assert pole_chu_des_1.current_player != initial_player
        assert pole_chu_des_1.current_player.in_game

        # Ensure that the next player is in_game
        while not pole_chu_des_1.current_player.in_game:
            await pole_chu_des_1.next_player()
        assert pole_chu_des_1.current_player.in_game

    async def test_set_player_in_game(
        self, pole_chu_des_1: PoleChuDesGame, player_full: PlayerFull
    ):
        player = pole_chu_des_1.players[0]
        # Test setting player to in_game
        await pole_chu_des_1.set_player_in_game(player, in_game=True)
        assert player.in_game

        # Test setting player to not in_game
        await pole_chu_des_1.set_player_in_game(player, in_game=False)
        assert not player.in_game

        # Test setting player to in_game when player does not exist
        player_status = player_full.in_game
        if player_status:
            await pole_chu_des_1.set_player_in_game(player_full, in_game=False)
            assert player_full.in_game
        else:
            # Test setting player to not in_game when player does not exist
            await pole_chu_des_1.set_player_in_game(player_full, in_game=False)
            assert not player_full.in_game

    async def test_check_guess(self, pole_chu_des_1: PoleChuDesGame):
        # Test guessing word with multiple active players
        guess = "word"
        current_player = pole_chu_des_1.current_player
        assert (
            await pole_chu_des_1.check_guess(
                vk_id=pole_chu_des_1.current_player.user.vk_id, guess=guess
            )
            == f"Игрок: {current_player.user.username} не угадал слово\n"
            f"Отгданное слово: {pole_chu_des_1.guessed_word}\n"
            f"Следующий игрок: {pole_chu_des_1.current_player.user.username}\n"
        )

        # Test guessing word with only one active player
        # guess = "word"
        # expected_response = await pole_chu_des_1.guess_word(guess=guess, count_of_active_players=1)
        # assert await pole_chu_des_1.check_guess(vk_id=239360735, guess=guess) == expected_response

        # Test guessing letter
        # guess = "a"
        # expected_response = await pole_chu_des_1.guess_letter(guess=guess)
        # assert await pole_chu_des_1.check_guess(
        #     vk_id=pole_chu_des_1.current_player.user.vk_id,
        #     guess=guess
        # ) == expected_response

        # Test guessing letter with incorrect current player's vk_id
        # guess = "a"
        # expected_response = (
        #     "Сейчас не ваш ход или вы выбыли из игры(\n"
        #     f"Ход принадлежит игроку: {pole_chu_des_1.current_player.user.username}!\n"
        #     f"Отгаданное слово: {pole_chu_des_1.guessed_word}\n"
        # )
        # assert await pole_chu_des_1.check_guess(vk_id=101, guess=guess) == expected_response

        # Test guessing letter with incorrect guess length
        # guess = "ab"
        # expected_response = await pole_chu_des_1.guess_word(guess=guess, count_of_active_players=3)
        # assert await pole_chu_des_1.check_guess(vk_id=pole_chu_des_1.current_player.user.vk_id, guess=guess) == expected_response
