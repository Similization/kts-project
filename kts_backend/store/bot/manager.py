import typing
from typing import List, Optional
from logging import getLogger
from random import choice

from kts_backend.game.model import Game, GameData
from kts_backend.store.game.game import PoleChudesGame
from kts_backend.store.vk_api.dataclasses import Message, Update

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")

    async def start(self):
        # user_list = get_users()
        # for user in user_list:
        #     if self.app.store.user.get_user(user_id=user.user_id) is None:
        #         self.app.store.user.create_user(user=user)
        chat_id_list: List[int] = await self.app.store.vk_api.get_active_chats()
        for chat_id in chat_id_list:
            game: Optional[Game] = await self.app.store.game.get_last_game(
                chat_id=chat_id
            )
            if game is None:
                game_data_list: List[
                    GameData
                ] = await self.app.store.game.get_game_data_list()
                created_game = await self.app.store.game.create_game(
                    game_data_id=choice(game_data_list).game_data_id,
                    chat_id=chat_id,
                )
                new_pole_chudes_game = PoleChudesGame()
                # add game to game_list(async Queue?)
            else:
                players = await self.app.store.game.get_players_from_game(
                    game_id=game.game_id
                )
                if len(players) < game.required_number_of_players:
                    # restart timing if lobby isn't full
                    # wait for all players
                    # when player join ->
                    # check if user is in db, otherwise add him before create player
                    pass
                else:
                    # listen for player with id == game.next_player_id
                    pass

    async def check_answer(self, answer: str):
        if PoleChudesGame().check_answer(answer=answer):
            pass
            # player can guess again
        # else turn goes to next player

    async def handle_updates(
        self, updates: Optional[list[Update]] = None
    ) -> None:
        if updates is None:
            return None

        for update in updates:
            # if update.object.user_id == id_of_the_user_who_is_guessing_now:
            #     await self.check_answer(answer=update.object.body)
            await self.app.store.vk_api.send_message(
                Message(
                    user_id=update.object.user_id,
                    peer_id=update.object.peer_id,
                    text=update.object.body,
                )
            )
