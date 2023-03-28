from sqlalchemy.exc import IntegrityError
from typing import List

from sqlalchemy.future import select

import pytest
from kts_backend.game.model import Player, PlayerModel
from kts_backend.store import Store
from kts_backend.user.model import User
from tests.utils import check_empty_table_exists


class TestPlayerStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "player")

    async def test_create_player(self, cli, store: Store, user_1: User):
        player_id = 1
        score = 200
        is_winner = True
        in_game = False
        player = Player(
            player_id=player_id,
            user_id=user_1.user_id,
            score=score,
            is_winner=is_winner,
            in_game=in_game,
        )
        created_player = await store.game.create_player(player=player)
        assert type(created_player) is Player

        async with cli.app.database.session() as session:
            res = await session.execute(select(PlayerModel))
            player_list: List[PlayerModel] = res.scalars().all()

        assert len(player_list) == 1
        player_from_db: PlayerModel = player_list[0]
        assert player_from_db.player_id == player.player_id
        assert player_from_db.user_id == player.user_id
        assert player_from_db.score == player.score
        assert player_from_db.in_game == player.in_game
        assert player_from_db.is_winner == player.is_winner

    async def test_create_player_with_no_user(self, cli, store: Store):
        player_id = 1
        user_id = 1
        score = 200
        is_winner = True
        in_game = False
        player = Player(
            player_id=player_id,
            user_id=user_id,
            score=score,
            is_winner=is_winner,
            in_game=in_game,
        )
        with pytest.raises(IntegrityError) as exc_info:
            await store.game.create_player(player=player)
            print()
        assert exc_info.value.orig.pgcode == "23503"

    async def test_create_existed_player(
        self, cli, store: Store, user_1: User, player_1: Player
    ):
        score = 150
        is_winner = True
        in_game = False
        player = Player(
            player_id=player_1.player_id,
            user_id=user_1.user_id,
            score=score,
            is_winner=is_winner,
            in_game=in_game,
        )
        with pytest.raises(IntegrityError) as exc_info:
            await store.game.create_player(player=player)
        assert exc_info.value.orig.pgcode == "23505"

    async def test_get_player_by_id(
        self, cli, store: Store, user_1: User, player_1: Player
    ):
        assert player_1 == await store.game.get_player(
            player_id=player_1.player_id
        )
