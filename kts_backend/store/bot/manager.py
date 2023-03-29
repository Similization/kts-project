import typing
from logging import getLogger
from typing import List

from kts_backend.game.dataclasses import GameFull
from kts_backend.store.game.game import PoleChuDesGame
from kts_backend.store.vk_api.dataclasses import Message, Update

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.game_list: List[PoleChuDesGame] = []
        self.logger = getLogger("handler")

    async def start(self):
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
                self.game_list.append(
                    await PoleChuDesGame(app=self.app).init_from(game=game)
                )

    async def get_game_by_chat_id(self, chat_id: int) -> PoleChuDesGame | None:
        for game in self.game_list:
            if game.game.chat_id == chat_id:
                return game
        return None

    async def handle_updates(
        self, updates: list[Update] | Update | None = None
    ) -> None:
        if updates is None:
            return None
        if isinstance(updates, Update):
            updates = [updates]

        for update in updates:
            game: PoleChuDesGame = await self.get_game_by_chat_id(
                chat_id=int(update.object.peer_id)
            )
            await game.check_guess(
                vk_id=update.object.user_id, guess=update.object.body
            )
            # обновляем данные об игре в базе данных
            # обновляем сообщение с последними результатами
            await self.app.store.vk_api.send_message(
                Message(
                    user_id=update.object.user_id,
                    peer_id=update.object.peer_id,
                    text=update.object.body,
                )
            )
