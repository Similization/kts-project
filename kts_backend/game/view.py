from typing import Optional, List

from aiohttp_apispec import request_schema, response_schema

from kts_backend.game.model import Player, Game
from kts_backend.game.schema import (
    PlayerSchema,
    PlayerByIdSchema,
    PlayerByIdAndInGameSchema,
    PlayerListSchema,
    GameByChatIdAndPlayerListSchema,
    GameWithPlayersSchema,
)
from kts_backend.web.app import View
from kts_backend.web.util import json_response


class GamePlayerListByChatIdView(View):
    @request_schema(PlayerByIdSchema)
    @response_schema(PlayerListSchema)
    async def post(self):
        chat_id = self.data["chat_id"]
        players: Optional[
            List[Player]
        ] = await self.store.game.get_players_by_chat_id(chat_id=chat_id)
        raw_players = [PlayerSchema().dump(player) for player in players]
        return json_response(data={"players": raw_players})


class GameCreateView(View):
    @request_schema(GameByChatIdAndPlayerListSchema)
    @response_schema(GameWithPlayersSchema)
    async def post(self):
        players = [
            Player(
                user_id=player.user_id,
                player_id=player.player_id,
                score=player.score,
                is_winner=player.is_winner,
                in_game=player.in_game,
            )
            for player in self.data["players"]
        ]
        chat_id = self.data["chat_id"]
        game: Optional[Game] = await self.store.game.create_new_game(
            players=players, chat_id=chat_id
        )
        return json_response(data=GameWithPlayersSchema().dump(game))


class GameLastView(View):
    @response_schema(GameWithPlayersSchema)
    async def get(self):
        game: Optional[Game] = await self.store.game.get_last_game()
        return json_response(data=GameWithPlayersSchema().dump(game))


class PlayerInGameView(View):
    @request_schema(PlayerByIdAndInGameSchema)
    @response_schema(PlayerSchema)
    async def post(self):
        player_id = self.data["player_id"]
        in_game = self.data["in_game"]

        player: Optional[Player] = await self.store.game.set_player_in_game(
            player_id=player_id, in_game=in_game
        )
        return json_response(data=PlayerSchema().dump(player))


class PlayerIsWinnerView(View):
    @request_schema(PlayerByIdAndInGameSchema)
    @response_schema(PlayerSchema)
    async def post(self):
        player_id = self.data["player_id"]
        in_game = self.data["in_game"]

        player: Optional[Player] = await self.store.game.set_player_in_game(
            player_id=player_id, in_game=in_game
        )
        return json_response(data=PlayerSchema().dump(player))
