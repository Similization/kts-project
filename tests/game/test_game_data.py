from typing import List

import pytest

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from kts_backend.game.model import GameData, GameDataModel
from kts_backend.store import Store
from tests.utils import ok_response, check_empty_table_exists


class TestGameDataStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "game_data")

    async def test_create_game_data(self, cli, store: Store):
        question = "Who wants to be a billionaire?"
        answer = "Everyone"

        created_game_data = await store.game.create_game_data(question=question, answer=answer)
        assert type(created_game_data) is GameData

        async with cli.app.database.session() as session:
            res = await session.execute(select(GameDataModel))
            game_datas: List[GameDataModel] = res.scalars().all()

        assert len(game_datas) == 1
        game_data_from_db: GameDataModel = game_datas[0]
        assert game_data_from_db.game_data_id == 1
        assert game_data_from_db.question == question
        assert game_data_from_db.answer == answer

    async def test_create_existed_game_data(
        self, cli, store: Store, game_data_1: GameData
    ):
        with pytest.raises(IntegrityError) as exc_info:
            await store.game.create_game_data(
                question=game_data_1.question,
                answer=game_data_1.answer
            )
        assert exc_info.value.orig.pgcode == "23505"

    async def test_get_game_data_by_id(
            self, cli, store: Store, game_data_1: GameData
    ):
        assert game_data_1 == await store.game.get_game_data(game_data_id=game_data_1.game_data_id)

    async def test_get_game_data_list_one(
            self, cli, store: Store, game_data_1: GameData
    ):
        game_data_list = await store.game.get_game_data_list()
        assert len(game_data_list) == 1
        assert game_data_1 == game_data_list[0]

    async def test_get_game_data_list_many(
            self, cli, store: Store, game_data_1: GameData, game_data_2: GameData
    ):
        game_data_list = await store.game.get_game_data_list()
        assert len(game_data_list) == 2
        created_game_data_1, created_game_data_2 = game_data_list
        assert game_data_1 == created_game_data_1
        assert game_data_2 == created_game_data_2


class TestGameDataAddView:
    async def test_success(self, cli):
        resp = await cli.post(
            "/game_data.add",
            json={
                "question": "Who wants to be a billionaire?",
                "answer": "Everyone",
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            {
                "game_data_id": 1,
                "question": "Who wants to be a billionaire?",
                "answer": "Everyone",
            }
        )

    async def test_missed_answer(self, cli):
        resp = await cli.post(
            "/game_data.add",
            json={
                "question": "???",
            },
        )
        assert resp.status == 400
        data = await resp.json()
        assert data["status"] == "bad_request"
        assert data["data"]["answer"][0] == "Missing data for required field."

    async def test_existed_question(
            self, cli, store: Store, game_data_1: GameData
    ):
        with pytest.raises(IntegrityError) as exc_info:
            await store.game.create_game_data(
                question=game_data_1.question, answer=game_data_1.answer
            )
        assert exc_info.value.orig.pgcode == "23505"

    async def test_different_method(self, cli):
        resp = await cli.get(
            "/game_data.add",
            json={
                "question": "Who wants to be a billionaire?",
                "answer": "Everyone",
            },
        )
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"


class TestGameDataGetView:
    async def test_success(self, cli, game_data_3):
        resp = await cli.get("/game_data.get")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            {
                "game_data_list": [
                    {
                        "game_data_id": 1,
                        "question": "Who wants to be a billionaire?",
                        "answer": "Everyone",
                    }
                ]
            }
        )

    async def test_different_method(self, cli):
        resp = await cli.post("/game_data.get")
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"
