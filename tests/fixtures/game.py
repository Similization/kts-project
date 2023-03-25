# import datetime
# from typing import List
#
# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from kts_backend.game.model import (
#     Game,
#     GameModel,
#     Player,
#     PlayerModel,
#     PlayerGameScoreModel,
# )
#
#
# @pytest.fixture
# async def player_1(db_session: AsyncSession) -> Player:
#     vk_id = 239360732
#     name = "Даниил"
#     last_name = "Бахланов"
#     new_player = PlayerModel(vk_id=vk_id, name=name, last_name=last_name)
#     async with db_session.begin() as session:
#         session.add(new_player)
#
#     return Player(vk_id=vk_id, name=name, last_name=last_name)
#
#
# @pytest.fixture
# async def player_2(db_session: AsyncSession) -> Player:
#     vk_id = 239360735
#     name = "Иван"
#     last_name = "Темный"
#     new_player = PlayerModel(vk_id=vk_id, name=name, last_name=last_name)
#     async with db_session.begin() as session:
#         session.add(new_player)
#
#     return Player(vk_id=vk_id, name=name, last_name=last_name)
#
#
# @pytest.fixture
# async def player_3(db_session: AsyncSession) -> Player:
#     vk_id = 239360737
#     name = "Антон"
#     last_name = "Жигуль"
#     new_player = PlayerModel(vk_id=vk_id, name=name, last_name=last_name)
#     async with db_session.begin() as session:
#         session.add(new_player)
#
#     return Player(vk_id=vk_id, name=name, last_name=last_name)
#
#
# @pytest.fixture
# async def game_1(db_session: AsyncSession, players: List[Player]) -> Game:
#     game_id = 1
#     created_at = datetime.datetime.strptime(
#         __date_string="2023-03-19 12:00:00.000000",
#         __format="%Y-%m-%d %H:%M:%S.%f",
#     )
#     chat_id = 1
#     new_game = GameModel(
#         game_id=game_id, created_at=created_at, chat_id=chat_id
#     )
#     async with db_session.begin() as session:
#         i: int = 0
#         for player in players:
#             new_game_score = PlayerGameScoreModel(
#                 id=i, vk_id=player.vk_id, game_id=game_id, score=0
#             )
#             i += 1
#             session.add(new_game_score)
#         session.add(new_game)
#
#     return Game(
#         game_id=game_id, created_at=created_at, chat_id=chat_id, players=players
#     )
#
#
# @pytest.fixture
# async def game_2(db_session: AsyncSession, players: List[Player]) -> Game:
#     game_id = 2
#     created_at = datetime.datetime.strptime(
#         __date_string="2023-05-19 23:45:30.000000",
#         __format="%Y-%m-%d %H:%M:%S.%f",
#     )
#     chat_id = 2
#     new_game = GameModel(
#         game_id=game_id, created_at=created_at, chat_id=chat_id
#     )
#     async with db_session.begin() as session:
#         i: int = 0
#         for player in players:
#             new_game_score = PlayerGameScoreModel(
#                 id=i, vk_id=player.vk_id, game_id=game_id, score=0
#             )
#             i += 1
#             session.add(new_game_score)
#         session.add(new_game)
#
#     return Game(
#         game_id=game_id, created_at=created_at, chat_id=chat_id, players=players
#     )
