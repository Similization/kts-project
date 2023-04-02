import asyncio
import typing
from logging import getLogger
from random import choice
from typing import List

from kts_backend.game.dataclasses import GameFull, GameData, Game
from kts_backend.store.bot.util import parse_text
from kts_backend.store.game.game import PoleChuDesGame
from kts_backend.store.vk_api.dataclasses import Message, Update
from kts_backend.store.vk_api.vk_keyboard import KEYBOARD_FINISH

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application

MIN_PLAYER_COUNT: int = 3
MAX_PLAYER_COUNT: int = 5
PARSE_COMMANDS: dict = {
    "start": "Создай игру для: ",
    "finish": "Завершить игру",
}


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
        game_list: List[
            GameFull
        ] = await self.app.store.game.get_unfinished_game_list()
        create_tasks = []
        for game in game_list:
            if len(game.player_list) < game.required_player_count:
                pass
            else:
                new_game: PoleChuDesGame = PoleChuDesGame(app=self.app)
                create_tasks.append(new_game.init_from(game=game))
                self.game_list.append(new_game)
        if create_tasks:
            await asyncio.gather(*create_tasks)

    async def get_game_by_chat_id(self, chat_id: str) -> PoleChuDesGame | None:
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
            chat_id=update.object.peer_id
        )

        if game is None:
            text = (
                "Для того, чтобы создать игру - напишите:\n"
                "Создай игру для: @username, @username ... @username\n"
                "Минимальное число игроков - 3\n"
                "Максимальное число игроков - 5\n"
                "@username пользователей необходимо указывать через запятую с пробелом"
            )
            body = update.object.body
            if body.startswith(PARSE_COMMANDS["start"]):
                username_list = body[len(PARSE_COMMANDS["start"]) :].split(", ")
                count_of_players = len(username_list)
                if count_of_players > MAX_PLAYER_COUNT:
                    await self.app.store.vk_api.send_message(
                        message=Message(
                            user_id=update.object.user_id,
                            peer_id=update.object.peer_id,
                            text=parse_text(
                                text="Игроков слишком много!\n\n" + text
                            ),
                        )
                    )
                    return
                if count_of_players < MIN_PLAYER_COUNT:
                    await self.app.store.vk_api.send_message(
                        message=Message(
                            user_id=update.object.user_id,
                            peer_id=update.object.peer_id,
                            text=parse_text(
                                text="Игроков слишком мало!\n\n" + text
                            ),
                        )
                    )
                    return
                game_data_list: List[
                    GameData
                ] = await self.app.store.game.get_game_data_list()
                random_game_data: GameData = choice(game_data_list)

                # get users from bd if not exist - then create
                profiles: List[
                    dict
                ] = await self.app.store.vk_api.get_chat_users(
                    chat_id=int(update.object.peer_id)
                )
                profile_dicts: List[dict] = [
                    {
                        "vk_id": profile["id"],
                        "name": profile["first_name"],
                        "last_name": profile["last_name"],
                        "username": "@" + profile["screen_name"],
                    }
                    for profile in profiles
                ]
                created_game: Game = await self.app.store.game.create_game(
                    game_data_id=random_game_data.id,
                    answer=random_game_data.answer,
                    chat_id=update.object.peer_id,
                    required_player_count=count_of_players,
                )

                await self.app.store.game.create_player_list_by_user_info(
                    game_id=created_game.id, users_info=profile_dicts
                )

                created_full_game: GameFull = (
                    await self.app.store.game.get_full_game(
                        game_id=created_game.id
                    )
                )
                new_pole_game = PoleChuDesGame(app=self.app)
                await new_pole_game.init_from(game=created_full_game)
                self.game_list.append(new_pole_game)

                player_list = "\n".join(
                    [
                        f"{i + 1}) {player.user.username}: {player.score}"
                        for i, player in enumerate(new_pole_game.players)
                    ]
                )
                result_string = (
                    f"Игра была создана!\n"
                    f"Список игроков:\n{player_list}\n"
                    f"Вопрос:\n{random_game_data.question}\n"
                    f"Cлово: {new_pole_game.guessed_word}\n"
                    f"Первым ходит: {new_pole_game.current_player.user.username}"
                )
                await self.app.store.vk_api.send_message(
                    message=Message(
                        user_id=update.object.user_id,
                        peer_id=update.object.peer_id,
                        text=parse_text(result_string),
                    ),
                    keyboard=KEYBOARD_FINISH,
                )
                new_pole_game.game.chat_message_id = (
                    await self.app.store.vk_api.get_history(
                        chat_id=update.object.peer_id
                    )
                )
                await self.app.store.game.update_game_message_id(
                    game_id=created_game.id,
                    message_id=new_pole_game.game.chat_message_id,
                )
            else:
                await self.app.store.vk_api.send_message(
                    message=Message(
                        user_id=update.object.user_id,
                        peer_id=update.object.peer_id,
                        text=parse_text(text=text),
                    )
                )
        else:
            if update.object.body.find(PARSE_COMMANDS["finish"]) != -1:
                results = [
                    f"{i + 1}) {player.user.username}: {player.score}"
                    for i, player in enumerate(game.players)
                ]
                result_string = "Результаты игры:\n" + "\n".join(results) + "\n"
                await self.app.store.vk_api.send_message(
                    message=Message(
                        user_id=update.object.user_id,
                        peer_id=update.object.peer_id,
                        text=parse_text(result_string),
                    )
                )
                await self.finish_game(game)
                return
            res = await game.check_guess(
                vk_id=update.object.user_id, guess=update.object.body
            )
            keyboard = KEYBOARD_FINISH
            if "Игра завершена" in res:
                await self.finish_game(game)
                keyboard = None
            await self.app.store.vk_api.send_message(
                message=Message(
                    user_id=update.object.user_id,
                    peer_id=update.object.peer_id,
                    text=parse_text(
                        "Результаты игры:\n"
                        + "\n".join(
                            [
                                f"{i + 1}) {player.user.username}: {player.score}"
                                for i, player in enumerate(game.players)
                            ]
                        )
                        + f"\n{res}\n"
                    ),
                ),
                keyboard=keyboard,
            )

    async def finish_game(self, game: PoleChuDesGame):
        await game.finish()
        self.game_list.remove(game)

    async def handle_updates(
        self, updates: list[Update] | Update | None = None
    ) -> None:
        """
        Handle updates.

        :param updates: A list of updates or a single update object. Defaults to None.
        :type updates: list[Update] | Update | None
        :return: None
        """
        # Return if no updates are provided
        if updates is None:
            return None

        # Convert single update to list of updates
        if isinstance(updates, Update):
            updates = [updates]

        # Process each update
        for update in updates:
            # Check the update and handle accordingly
            await self.check_update(update=update)
            # await self.app.store.vk_api.get_history(chat_id=update.object.peer_id)
            # Delete the message from chat after processing
            await self.app.store.vk_api.delete_message_from_chat(
                message_ids=update.object.message_id,
                chat_id=update.object.peer_id,
            )
