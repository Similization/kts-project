from typing import List

import pytest

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from kts_backend.game.dataclasses import GameData
from kts_backend.game.model import GameDataModel
from kts_backend.store import Store
from tests.utils import ok_response, check_empty_table_exists


class TestGameDataStore:
    """
    A collection of tests for the GameDataStore class.
    """
    async def test_table_exists(self, cli):
        """
        Test if the 'game_data' table exists in the database.

        Parameters:
            cli (TestClient): An instance of TestClient used to make requests to the API.

        Raises:
            AssertionError: If the table doesn't exist in the database.
        """
        await check_empty_table_exists(cli, "game_data")

    async def test_create_game_data(self, cli, store: Store):
        """
        Test creating a new GameData object in the database.

        Parameters:
            cli (TestClient): An instance of TestClient used to make requests to the API.
            store (Store): An instance of the Store class.

        Raises:
            AssertionError: If the created game data object is not of type GameData.
            AssertionError: If the values in the database for the created game data object
                don't match the values passed to create_game_data() function.
        """
        question = "Who wants to be a billionaire?"
        answer = "Everyone"

        created_game_data = await store.game.create_game_data(
            question=question, answer=answer
        )
        assert type(created_game_data) is GameData

        async with cli.app.database.session() as session:
            res = await session.execute(select(GameDataModel))
            game_datas: List[GameDataModel] = res.scalars().all()

        assert len(game_datas) == 1
        game_data_from_db: GameDataModel = game_datas[0]
        assert game_data_from_db.id == 1
        assert game_data_from_db.question == question
        assert game_data_from_db.answer == answer

    async def test_create_existed_game_data(
            self, cli, store: Store, game_data_1: GameData
    ):
        """
        Test creating a game data object that already exists in the database.

        Parameters:
            cli (TestClient): An instance of TestClient used to make requests to the API.
            store (Store): An instance of the Store class.
            game_data_1 (GameData): An instance of the GameData class.

        Raises:
            IntegrityError: If the game data object already exists in the database.
            AssertionError: If the error code for the raised exception is not '23505'.
        """
        with pytest.raises(IntegrityError) as exc_info:
            await store.game.create_game_data(
                question=game_data_1.question, answer=game_data_1.answer
            )
        assert exc_info.value.orig.pgcode == "23505"

    async def test_get_game_data_by_id(
            self, cli, store: Store, game_data_1: GameData
    ):
        """
        Test creating a game data object that already exists in the database.

        Parameters:
            cli (TestClient): An instance of TestClient used to make requests to the API.
            store (Store): An instance of the Store class.
            game_data_1 (GameData): An instance of the GameData class.

        Raises:
            IntegrityError: If the game data object already exists in the database.
            AssertionError: If the error code for the raised exception is not '23505'.
        """
        assert game_data_1 == await store.game.get_game_data(
            game_data_id=game_data_1.id
        )

    async def test_get_game_data_list_one(
            self, cli, store: Store, game_data_1: GameData
    ):
        """
        Test retrieving a list of game data objects when only one object is in the database.

        Parameters:
            cli (TestClient): An instance of TestClient used to make requests to the API.
            store (Store): An instance of the Store class.
            game_data_1 (GameData): An instance of the GameData class.

        Raises:
            AssertionError: If the length of the retrieved list is not 1.
            AssertionError: If the retrieved game data object doesn't match the expected object.
        """
        game_data_list = await store.game.get_game_data_list()
        assert len(game_data_list) == 1
        assert game_data_1 == game_data_list[0]

    async def test_get_game_data_list_many(
            self, cli, store: Store, game_data_1: GameData, game_data_2: GameData
    ):
        """
          Test retrieving a list of game data objects when more than one object is in the database.

          Parameters:
              cli (TestClient): An instance of TestClient used to make requests to the API.
              store (Store): An instance of the Store class.
              game_data_1 (GameData): An instance of the GameData class.
              game_data_2 (GameData): An instance of the GameData class.

          Raises:
              AssertionError: If the length of the retrieved list is not 2.
              AssertionError: If the retrieved game data objects don't match the expected objects.
          """
        game_data_list = await store.game.get_game_data_list()
        assert len(game_data_list) == 2
        created_game_data_1, created_game_data_2 = game_data_list
        assert game_data_1 == created_game_data_1
        assert game_data_2 == created_game_data_2


class TestGameDataPostView:
    """
    A class that contains test methods for the game_data.post API endpoint.
    """
    async def test_success(self, cli):
        """
        A test method that verifies the success scenario when creating a new game data entry.

        :param cli: An instance of the TestClient for the FastAPI app.
        """
        resp = await cli.post(
            "/game_data.post",
            json={
                "question": "Who wants to be a billionaire?",
                "answer": "Everyone",
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            {
                "id": 1,
                "question": "Who wants to be a billionaire?",
                "answer": "Everyone",
            }
        )

    async def test_missed_answer(self, cli):
        """
        A test method that verifies the scenario when a request to create a game data entry is missing the answer field.

        :param cli: An instance of the TestClient for the FastAPI app.
        """
        resp = await cli.post(
            "/game_data.post",
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
        """
        A test method that verifies the scenario when a request to create a game data entry contains a question that already exists in the database.

        :param cli: An instance of the TestClient for the FastAPI app.
        :param store: An instance of the Store for the application.
        :param game_data_1: An instance of the GameData model representing an existing game data entry.
        """
        with pytest.raises(IntegrityError) as exc_info:
            await store.game.create_game_data(
                question=game_data_1.question, answer=game_data_1.answer
            )
        assert exc_info.value.orig.pgcode == "23505"

    async def test_different_method(self, cli):
        """
          A test method that verifies the scenario when an HTTP GET request is made to the game_data.post API endpoint.

          :param cli: An instance of the TestClient for the FastAPI app.
          """
        resp = await cli.get(
            "/game_data.post",
            json={
                "question": "Who wants to be a billionaire?",
                "answer": "Everyone",
            },
        )
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"


class TestGameDataGetView:
    async def test_get_game_data_success(self, cli, game_data_3):
        """
        Test retrieving a list of game data objects when only one object is in the database.

        Parameters:
            cli (TestClient): An instance of TestClient used to make requests to the API.
            game_data_3 (GameData): An instance of the GameData class.

        Raises:
            AssertionError: If the length of the retrieved list is not 1.
            AssertionError: If the retrieved game data object doesn't match the expected object.
        """
        resp = await cli.get("/game_data.get")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            {
                "game_data_list": [
                    {
                        "id": 1,
                        "question": "Who wants to be a billionaire?",
                        "answer": "Everyone",
                    }
                ]
            }
        )

    async def test_different_method(self, cli):
        """
        Test that a POST request is not allowed for the /game_data.get endpoint.

        Parameters:
            cli (TestClient): An instance of TestClient used to make requests to the API.

        Raises:
            AssertionError: If the response status code is not 405.
            AssertionError: If the response status message is not 'not_implemented'.
        """
        resp = await cli.post("/game_data.get")
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"
