import typing
from typing import List
from random import choice
from logging import getLogger

from kts_backend.game.dataclasses import GameFull, GameData, Player, Game
from kts_backend.store.game.game import PoleChuDesGame
from kts_backend.store.vk_api.dataclasses import Message, Update

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        """
        Initialize BotManager object, using app
        :param app: Application
        """
        self.app = app
        self.bot = None
        self.game_list: List[PoleChuDesGame] = []
        self.logger = getLogger("handler")

    async def start(self) -> None:
        """
        Get all unfinished games and create PoleChuDes objects for each entity
        :return: None
        """
        # получаем все активные игры
        game_list: List[
            GameFull
        ] = await self.app.store.game.get_unfinished_game_list()
        # и смотрим их состояние
        for game in game_list:
            # недостаточно игроков - ждем
            if len(game.player_list) < game.required_player_count:
                # запускаем таймер и ждем оставшихся игроков
                pass
            else:
                # создаем класс PoleChuDesGame
                new_game: PoleChuDesGame = PoleChuDesGame(app=self.app)
                await new_game.init_from(game=game)
                self.game_list.append(new_game)

    async def get_game_by_chat_id(self, chat_id: int) -> PoleChuDesGame | None:
        """
        Get game from self.game_list by chat_id
        :param chat_id: int
        :return: PoleChuDesGame | None
        """
        for game in self.game_list:
            if game.game.chat_id == chat_id:
                return game
        return None

    async def check_update(self, update: Update):
        game: PoleChuDesGame | None = await self.get_game_by_chat_id(
            chat_id=int(update.object.peer_id)
        )
        if game is None:
            body = update.object.body
            if body.startswith("Создай игру для: "):
                username_list = body[17:].strip(', ')
                if len(username_list) < 3 or len(username_list) > 5:
                    await self.app.store.vk_api.send_message(
                        Message(
                            user_id=update.object.user_id,
                            peer_id=update.object.peer_id,
                            text="Для того, чтобы создать игру - напишите:\n"
                                 "Создай игру для: @username, @username ... @username\n"
                                 "Минимальное число игроков - 3\n"
                                 "Максимальное число игроков - 5\n"
                                 "@username пользователей необходимо указывать через запятую с пробелом",
                        )
                    )
                game_data_list: List[GameData] = await self.app.store.game.get_game_data_list()
                random_game_data: GameData = choice(game_data_list)

                # get users from bd if not exist - then create
                player_list: List[Player] = await self.app.store.game.create_player_list_by_username_list(
                    username_list=username_list
                )

                created_game: Game = await self.app.store.game.create_game_with_players(
                    game_data_id=random_game_data.id,
                    chat_id=update.object.peer_id,
                    player_list=player_list
                )
                created_full_game: GameFull = await self.app.store.game.get_full_game(game_id=created_game.id)
                new_pole_game = PoleChuDesGame(app=self.app)
                await new_pole_game.init_from(game=created_full_game)
                self.game_list.append(new_pole_game)

                await self.app.store.vk_api.send_message(
                    Message(
                        user_id=update.object.user_id,
                        peer_id=update.object.peer_id,
                        text="Игра была создана!\n"
                             "Список игроков:\n" +
                             "".join([
                                 str(i + 1) + ") " +
                                 new_pole_game.players[i].user.username + ": " +
                                 str(new_pole_game.players[i].score)
                                 for i in range(len(new_pole_game.players))
                             ]) + "\n" + f"Первым ходит: {new_pole_game.current_player.user.username}",
                    )
                )
            else:
                await self.app.store.vk_api.send_message(
                    Message(
                        user_id=update.object.user_id,
                        peer_id=update.object.peer_id,
                        text="Для того, чтобы создать игру - напишите:\n"
                             "Создай игру для: @username, @username ... @username\n"
                             "Минимальное число игроков - 3\n"
                             "Максимальное число игроков - 5\n"
                             "@username пользователей необходимо указывать через запятую с пробелом",
                    )
                )
        else:
            res = await game.check_guess(vk_id=update.object.user_id, guess=update.object.body)
            await self.app.store.vk_api.send_message(
                Message(
                    user_id=update.object.user_id,
                    peer_id=update.object.peer_id,
                    text="Результаты игры:\n"
                         "\n".join([
                            str(i + 1) + ") " +
                            game.players[i].user.username + ": " +
                            str(game.players[i].score)
                            for i in range(len(game.players))
                         ]) + "\n" + res,
                )
            )

    async def handle_updates(
            self, updates: list[Update] | Update | None = None
    ) -> None:
        """
        Handle updates
        :param updates: list[Update] | Update | None
        :return: None
        """
        if updates is None:
            return None

        if isinstance(updates, Update):
            updates = [updates]

        for update in updates:
            await self.check_update(update=update)
