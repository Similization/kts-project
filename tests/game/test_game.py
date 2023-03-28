from typing import List

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from kts_backend.game.model import Game, GameData, GameModel
from kts_backend.store import Store
from tests.utils import check_empty_table_exists


class TestPlayerStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "game")

    async def test_create_game(self, cli, store: Store, game_data_1: GameData):
        chat_id: int = 1
        created_game = await store.game.create_game(
            game_data_id=game_data_1.game_data_id,
            chat_id=chat_id
        )
        assert type(created_game) is Game

        async with cli.app.database.session() as session:
            res = await session.execute(select(GameModel))
            game_model_list: List[GameModel] = res.scalars().all()

        assert len(game_model_list) == 1
        game_from_db: GameModel = game_model_list[0]
        assert game_from_db.game_id == 1
        assert game_from_db.game_data_id == game_data_1.game_data_id
        assert game_from_db.finished_at is None
        assert game_from_db.chat_id == chat_id

    async def test_create_game_with_no_game_data(self, cli, store: Store):
        chat_id: int = 1
        game_data_id: int = 1

        with pytest.raises(IntegrityError) as exc_info:
            await store.game.create_game(
                game_data_id=game_data_id,
                chat_id=chat_id
            )
        assert exc_info.value.orig.pgcode == "23503"

    async def test_get_game_by_id(
            self, cli, store: Store, game_1: Game
    ):
        assert game_1 == await store.game.get_game(
            game_id=game_1.game_id
        )
