import pytest

from sqlalchemy.exc import IntegrityError
from kts_backend.game.model import GameData
from kts_backend.store import Store
from tests.utils import ok_response


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
