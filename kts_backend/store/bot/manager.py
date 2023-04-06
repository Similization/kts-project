import asyncio
import typing
from logging import getLogger
from random import choice
from typing import List

from kts_backend.game.dataclasses import GameFull, GameData, Game
from kts_backend.store.bot.util import parse_text
from kts_backend.store.game.game import PoleChuDesGame
from kts_backend.store.vk_api.dataclasses import Message, Update
from kts_backend.store.vk_api.vk_keyboard import VK_KEYBOARDS

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application

MIN_PLAYER_COUNT: int = 3
MAX_PLAYER_COUNT: int = 5
PARSE_COMMANDS: dict = {
    "start": "Создай игру для: ",
    "finish": "Завершить игру",
}


class BotManager:
    """
    A class representing a bot manager for a PoleChudes game.

    Args:
        app (Application): An instance of the Application class.

    Attributes:
        app (Application): An instance of the Application class.
        bot (None): An instance of the VK Bot API.
        game_list (List[PoleChuDesGame]): A list of all PoleChuDesGame instances associated with the bot.
        logger (Logger): An instance of the Python logger.

    """

    def __init__(self, app: "Application"):
        """
        Initialize a BotManager object with the given application instance.

        Args:
            app (Application): An instance of the Application class.

        Returns:
            None
        """
        self.app = app
        self.bot = None
        self.game_list: List[PoleChuDesGame] = []
        self.logger = getLogger("handler")

    async def start(self) -> None:
        """
        Asynchronously retrieve all unfinished games from the database and create new PoleChuDesGame objects
        from them. Add each new game object to the game_list attribute.

        Returns:
            None
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
        Asynchronously search for a PoleChuDesGame instance in the game_list attribute using the provided chat_id.

        Args:
            chat_id (str): The chat ID to search for.

        Returns:
            PoleChuDesGame: A PoleChuDesGame instance if found.
            None: If no PoleChuDesGame instance was found.
        """
        for game in self.game_list:
            if game.game.chat_id == chat_id:
                return game
        return None

    async def send_message(self, update, message_text, keyboard=None):
        """
        Asynchronously send a message to a VK user.

        Args:
            update (Update): An instance of the Update class.
            message_text (str): The message text to send.
            keyboard (Optional[List[List[str]]]): A keyboard to attach to the message.

        Returns:
            None
        """
        message = Message(
            user_id=update.update_object.user_id,
            peer_id=update.update_object.peer_id,
            text=parse_text(text=message_text),
        )
        await self.app.store.vk_api.send_message(
            message=message, keyboard=keyboard
        )

    async def check_update(self, update: Update):
        """
        Asynchronously check for a new update to a VK chat.

        Args:
            update (Update): An instance of the Update class.

        Returns:
            None
        """

        # Try to retrieve the game associated with the chat id from the database
        game: PoleChuDesGame | None = await self.get_game_by_chat_id(
            chat_id=update.update_object.peer_id
        )

        # If the game is not found, display instructions for starting a new game
        if game is None:
            text = (
                "Для того, чтобы создать игру - напишите:\n"
                "Создай игру для: @username, @username ... @username\n"
                "Минимальное число игроков - 3\n"
                "Максимальное число игроков - 5\n"
                "@username пользователей необходимо указывать через запятую с пробелом"
            )
            # If the user is trying to start a game, extract the usernames from the message
            body = update.update_object.body
            if body.startswith(PARSE_COMMANDS["start"]):
                username_list = body[len(PARSE_COMMANDS["start"]) :].split(", ")
                count_of_players = len(username_list)

                # If there are too many players, send a message to the user and return
                if count_of_players > MAX_PLAYER_COUNT:
                    await self.send_message(
                        update=update,
                        message_text="Игроков слишком много!\n\n" + text,
                    )
                    return

                # If there are too few players, send a message to the user and return
                if count_of_players < MIN_PLAYER_COUNT:
                    await self.send_message(
                        update=update,
                        message_text="Игроков слишком мало!\n\n" + text,
                    )
                    return

                # Select a random game data from the database
                game_data_list: List[
                    GameData
                ] = await self.app.store.game.get_game_data_list()
                random_game_data: GameData = choice(game_data_list)

                # Get the profile information for each user in the chat
                profiles: List[
                    dict
                ] = await self.app.store.vk_api.get_chat_users(
                    chat_id=int(update.update_object.peer_id)
                )
                username_list = [
                    username[username.find("@") : -1]
                    for username in username_list
                ]
                profile_dicts: List[dict] = [
                    {
                        "vk_id": profile["id"],
                        "name": profile["first_name"],
                        "last_name": profile["last_name"],
                        "username": "@" + profile["screen_name"],
                    }
                    for profile in profiles
                    if "@" + profile["screen_name"] in username_list
                ]

                # Check if all the usernames in the message were found
                actual_usernames = [
                    profile_dict["username"] for profile_dict in profile_dicts
                ]
                if len(actual_usernames) < len(username_list):
                    await self.send_message(
                        update=update,
                        message_text="Проверьте указанные username, вероятно вы допустили ошибку в них, перепроверье:\n"
                        f"{set(username_list) - set(actual_usernames)}\n\n{text}",
                    )
                    return
                created_game: Game = await self.app.store.game.create_game(
                    game_data_id=random_game_data.id,
                    answer=random_game_data.answer,
                    chat_id=update.update_object.peer_id,
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
                await self.send_message(
                    update=update,
                    message_text=result_string,
                    keyboard=VK_KEYBOARDS["KEYBOARD_FINISH"],
                )
                new_pole_game.game.chat_message_id = (
                    await self.app.store.vk_api.get_history(
                        chat_id=update.update_object.peer_id
                    )
                )
                await self.app.store.game.update_game_message_id(
                    game_id=created_game.id,
                    message_id=new_pole_game.game.chat_message_id,
                )
                await self.app.store.vk_api.pin_message(
                    message_id=new_pole_game.game.chat_message_id,
                    peer_id=update.update_object.peer_id,
                )
            else:
                await self.send_message(
                    update=update,
                    message_text=text,
                )
        else:
            results = [
                f"{i + 1}) {player.user.username}: {player.score}"
                for i, player in enumerate(game.game.player_list)
            ]
            if update.update_object.body.find(PARSE_COMMANDS["finish"]) != -1:
                result_string = "Результаты игры:\n" + "\n".join(results) + "\n"
                await self.send_message(
                    update=update,
                    message_text=result_string,
                )
                await self.finish_game(game)
                return

            res = await game.check_guess(
                vk_id=update.update_object.user_id,
                guess=update.update_object.body,
            )
            result_string = (
                "Результаты игры:\n" + "\n".join(results) + f"\n{res}\n"
            )
            keyboard = VK_KEYBOARDS["KEYBOARD_FINISH"]

            if "Игра завершена" in res:
                await self.finish_game(game)
                keyboard = None
            await self.send_message(
                update=update, message_text=result_string, keyboard=keyboard
            )

    async def finish_game(self, game: PoleChuDesGame):
        """
        Ends the current game session and updates the game leaderboard.

        This method is called when the game is finished and a winner is declared.
        It updates the leaderboard with the results of the game and resets the
        game board and players for the next round.

        Returns:
            None
        """
        await game.finish()
        self.game_list.remove(game)

    async def handle_updates(
        self, updates: list[Update] | Update | None = None
    ) -> None:
        """
        Process the provided updates and delete the corresponding messages from the chat.

        Args:
            updates (list[Update] | Update | None): A list of `Update` objects, a single `Update` object,
                or None if there are no updates to process. If a single `Update` object is provided,
                it will be converted to a list with a single element.

        Returns:
            None
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
                message_ids=update.update_object.message_id,
                chat_id=update.update_object.peer_id,
            )
