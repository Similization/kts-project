# from typing import List
#
# from sqlalchemy.future import select
#
# from kts_backend.game.model import Player, PlayerModel
# from kts_backend.store import Store
# from tests.utils import check_empty_table_exists
#
#
# class TestPlayerStore:
#     async def test_table_exists(self, cli):
#         await check_empty_table_exists(cli, "player")
#
#     async def test_create_player(self, cli, store: Store):
#         player = Player(vk_id=239360732, name="Даниил", last_name="Бахланов")
#         created_player = await store.game.create_player(player=player)
#         assert type(created_player) is Player
#
#         async with cli.app.database.session() as session:
#             res = await session.execute(select(PlayerModel))
#             players: List[PlayerModel] = res.scalars().all()
#
#         assert len(players) == 1
#         player_from_db = players[0]
#         assert player_from_db.vk_id == player.vk_id
#         assert player_from_db.name == player.name
#         assert player_from_db.last_name == player.last_name
#
#     async def test_get_player_by_id(self, cli, store: Store, player_1: Player):
#         assert player_1 == await store.game.get_player_by_id(player_1.vk_id)
