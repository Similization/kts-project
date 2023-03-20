from typing import Optional, List

from aiohttp_apispec import request_schema

from kts_backend.game.model import PlayerDC, GameDC
from kts_backend.game.schema import (
    PlayerResponseSchema,
    GameSchema,
    GamePlayersSchema,
)
from kts_backend.web.app import View
from kts_backend.web.utils import json_response


class GamePlayerListView(View):
    @request_schema(GameSchema)
    # @request_schema(PlayerListSchema)
    async def post(self):
        chat_id = self.data["chat_id"]
        players: Optional[
            List[PlayerDC]
        ] = await self.store.game.get_players_by_chat_id(chat_id=chat_id)
        raw_players = [
            PlayerResponseSchema().dump(player) for player in players
        ]
        return json_response(data={"players": raw_players})


class GameCreateView(View):
    @request_schema(GamePlayersSchema)
    # @request_schema(GamePlayersSchema)
    async def post(self):
        players = [
            PlayerDC(
                vk_id=player["vk_id"],
                name=player["name"],
                last_name=player["last_name"],
            )
            for player in self.data["players"]
        ]
        chat_id = self.data["chat_id"]
        game: Optional[GameDC] = await self.store.game.create_new_game(
            players=players, chat_id=chat_id
        )
        return json_response(data={"game": GamePlayersSchema().dump(game)})


class GameLastView(View):
    # @request_schema(GamePlayersSchema)
    async def get(self):
        game: Optional[GameDC] = await self.store.game.get_last_game()
        return json_response(data={"last_game": GamePlayersSchema().dump(game)})
