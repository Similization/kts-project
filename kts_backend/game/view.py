from typing import List

from aiohttp_apispec import request_schema, response_schema

from kts_backend.game.dataclasses import GameData
from kts_backend.game.schema import GameDataSchema, GameDataListSchema
from kts_backend.web.app import View
from kts_backend.web.util import json_response


class GameDataAddView(View):
    @request_schema(schema=GameDataSchema)
    @response_schema(schema=GameDataSchema, code=200)
    async def post(self):
        """
        Creates a new GameData object in the database with question and answer fields.

        Request Body:
        {
            "question": str,
            "answer": str
        }

        Response Body:
        {
            "id": int,
            "question": str,
            "answer": str
        }

        Returns:
        A JSON response with the newly created GameData object.
        """

        question = self.data["question"]
        answer = self.data["answer"]
        game_data: GameData = await self.store.game.create_game_data(
            question=question, answer=answer
        )
        return json_response(data=GameDataSchema().dump(game_data))


class GameDataListGetView(View):
    @response_schema(schema=GameDataListSchema, code=200)
    async def get(self):
        """
        Gets a list of GameData objects from the database.

        Response Body:
        {
            "game_data_list": [
                {
                    "id": int,
                    "question": str,
                    "answer": str
                },
                ...
            ]
        }

        Returns:
        A JSON response with the list of GameData objects.
        """

        game_data_list: List[
            GameData
        ] | None = await self.store.game.get_game_data_list()
        raw_data = [
            GameDataSchema().dump(game_data) for game_data in game_data_list
        ]
        return json_response(data={"game_data_list": raw_data})
