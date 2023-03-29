from typing import Optional, List

from aiohttp_apispec import request_schema, response_schema

from kts_backend.game.dataclasses import (
    GameData,
)
from kts_backend.game.schema import (
    GameDataSchema,
    GameDataListSchema,
)
from kts_backend.web.app import View
from kts_backend.web.util import json_response


class GameDataAddView(View):
    @request_schema(GameDataSchema)
    @response_schema(GameDataSchema)
    async def post(self):
        """
        Create new GameData object in database with question and answer fields
        :return: GameDataSchema
        """
        question = self.data["question"]
        answer = self.data["answer"]
        game_data: GameData = await self.store.game.create_game_data(
            question=question, answer=answer
        )
        return json_response(data=GameDataSchema().dump(game_data))


class GameDataListGetView(View):
    @response_schema(GameDataListSchema)
    async def get(self):
        """
        Get list of GameData object from database
        :return: GameDataListSchema
        """
        game_data_list: Optional[
            List[GameData]
        ] = await self.store.game.get_game_data_list()
        raw_data = [
            GameDataSchema().dump(game_data) for game_data in game_data_list
        ]
        return json_response(data={"game_data_list": raw_data})
