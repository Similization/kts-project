import datetime
from typing import List

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from kts_backend.game.model import (
    Game,
    GameModel,
    Player,
    PlayerModel,
    PlayerGameModel,
    GameData,
    GameDataModel,
)
from kts_backend.user.model import UserModel, User


@pytest.fixture
async def user_1(db_session: AsyncSession) -> User:
    vk_id = 239360732
    name = "Даниил"
    last_name = "Бахланов"
    username = "@reductor"
    new_user = UserModel(
        vk_id=vk_id, name=name, last_name=last_name, username=username
    )
    async with db_session.begin() as session:
        session.add(new_user)
    return User(
        user_id=new_user.user_id,
        vk_id=vk_id,
        name=name,
        last_name=last_name,
        username=username,
    )


@pytest.fixture
async def user_2(db_session: AsyncSession) -> User:
    vk_id = 239360735
    name = "Петр"
    last_name = "Движев"
    username = "@dvizhevv"
    new_user = UserModel(
        vk_id=vk_id, name=name, last_name=last_name, username=username
    )
    async with db_session.begin() as session:
        session.add(new_user)
    return User(
        user_id=new_user.user_id,
        vk_id=vk_id,
        name=name,
        last_name=last_name,
        username=username,
    )


@pytest.fixture
async def user_3(db_session: AsyncSession) -> User:
    vk_id = 239360735
    name = "Анна"
    last_name = "Панн"
    username = "@pannanna"
    new_user = UserModel(
        vk_id=vk_id, name=name, last_name=last_name, username=username
    )
    async with db_session.begin() as session:
        session.add(new_user)
    return User(
        user_id=new_user.user_id,
        vk_id=vk_id,
        name=name,
        last_name=last_name,
        username=username,
    )


@pytest.fixture
async def player_1(db_session: AsyncSession) -> Player:
    user_id = 1
    new_player = PlayerModel(user_id=user_id)
    async with db_session.begin() as session:
        session.add(new_player)

    return Player(
        player_id=new_player.player_id,
        user_id=user_id,
        score=new_player.score,
        is_winner=new_player.is_winner,
        in_game=new_player.in_game,
    )


@pytest.fixture
async def player_2(db_session: AsyncSession) -> Player:
    user_id = 2
    new_player = PlayerModel(user_id=user_id)
    async with db_session.begin() as session:
        session.add(new_player)

    return Player(
        player_id=new_player.player_id,
        user_id=user_id,
        score=new_player.score,
        is_winner=new_player.is_winner,
        in_game=new_player.in_game,
    )


@pytest.fixture
async def player_3(db_session: AsyncSession) -> Player:
    user_id = 3
    new_player = PlayerModel(user_id=user_id)
    async with db_session.begin() as session:
        session.add(new_player)

    return Player(
        player_id=new_player.player_id,
        user_id=user_id,
        score=new_player.score,
        is_winner=new_player.is_winner,
        in_game=new_player.in_game,
    )


@pytest.fixture
async def game_data_1(db_session: AsyncSession) -> GameData:
    question = "Who is the president of Uganda?"
    answer = "Who cares"
    new_game_data = GameDataModel(question=question, answer=answer)

    async with db_session.begin() as session:
        session.add(new_game_data)

    return GameData(
        game_data_id=new_game_data.game_data_id,
        question=question,
        answer=answer,
    )


@pytest.fixture
async def game_data_2(db_session: AsyncSession) -> GameData:
    question = "Somebody once told who?"
    answer = "Me"
    new_game_data = GameDataModel(question=question, answer=answer)

    async with db_session.begin() as session:
        session.add(new_game_data)

    return GameData(
        game_data_id=new_game_data.game_data_id,
        question=question,
        answer=answer,
    )


@pytest.fixture
async def game_data_3(db_session: AsyncSession) -> GameData:
    question = "Who wants to be a billionaire?"
    answer = "Everyone"
    new_game_data = GameDataModel(question=question, answer=answer)

    async with db_session.begin() as session:
        session.add(new_game_data)

    return GameData(
        game_data_id=new_game_data.game_data_id,
        question=question,
        answer=answer,
    )


@pytest.fixture
async def game_1(db_session: AsyncSession, players: List[Player]) -> Game:
    game_data_id = 1
    created_at = datetime.datetime.strptime(
        __date_string="2023-03-19 12:00:00.000000",
        __format="%Y-%m-%d %H:%M:%S.%f",
    )
    chat_id = 1
    new_game = GameModel(created_at=created_at, chat_id=chat_id)

    async with db_session.begin() as session:
        session.add(new_game)

        player_game_list = [
            PlayerGameModel(
                game_id=new_game.game_id, player_id=player.player_id
            )
            for player in players
        ]

        for player_game in player_game_list:
            session.add(player_game)

    return Game(
        game_id=new_game.game_id,
        game_data_id=game_data_id,
        created_at=created_at,
        chat_id=chat_id,
        finished_at=new_game.finished_at,
        player_list=players,
    )


@pytest.fixture
async def game_2(db_session: AsyncSession, players: List[Player]) -> Game:
    game_data_id = 2
    created_at = datetime.datetime.strptime(
        __date_string="2023-02-22 12:45:00.000000",
        __format="%Y-%m-%d %H:%M:%S.%f",
    )
    chat_id = 1
    new_game = GameModel(created_at=created_at, chat_id=chat_id)

    async with db_session.begin() as session:
        session.add(new_game)

        player_game_list = [
            PlayerGameModel(
                game_id=new_game.game_id, player_id=player.player_id
            )
            for player in players
        ]

        for player_game in player_game_list:
            session.add(player_game)

    return Game(
        game_id=new_game.game_id,
        game_data_id=game_data_id,
        created_at=created_at,
        chat_id=chat_id,
        finished_at=new_game.finished_at,
        player_list=players,
    )


@pytest.fixture
async def game_3(db_session: AsyncSession, players: List[Player]) -> Game:
    game_data_id = 3
    created_at = datetime.datetime.strptime(
        __date_string="2023-02-25 02:15:50.000000",
        __format="%Y-%m-%d %H:%M:%S.%f",
    )
    chat_id = 2
    new_game = GameModel(created_at=created_at, chat_id=chat_id)

    async with db_session.begin() as session:
        session.add(new_game)

        player_game_list = [
            PlayerGameModel(
                game_id=new_game.game_id, player_id=player.player_id
            )
            for player in players
        ]

        for player_game in player_game_list:
            session.add(player_game)

    return Game(
        game_id=new_game.game_id,
        game_data_id=game_data_id,
        created_at=created_at,
        chat_id=chat_id,
        finished_at=new_game.finished_at,
        player_list=players,
    )
