import datetime
from typing import List

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from kts_backend.game.model import (
    GameModel,
    PlayerModel,
    GameDataModel,
)
from kts_backend.game.dataclasses import (
    Game,
    GameData,
    Player,
)
from kts_backend.store import Store
from kts_backend.user.dataclasses import User
from kts_backend.user.model import UserModel


@pytest.fixture
def users(store: Store) -> list[User]:
    """
    :param store:
    :return:
    """
    return [
        User(id=1, vk_id=100, name="Dan", last_name="Ban", username="@db"),
        User(
            id=2,
            vk_id=101,
            name="Yana",
            last_name="Ayan",
            username="@yanayan",
        ),
        User(
            id=3,
            vk_id=102,
            name="Daria",
            last_name="Torch",
            username="@Tor4D",
        ),
    ]


@pytest.fixture
def players_1(store: Store, user_1: User, user_2: User) -> list[PlayerModel]:
    """
    :param user_2:
    :param user_1:
    :param store:
    :return:
    """
    return [
        PlayerModel(
            id=1,
            user_id=user_1.id,
            score=25,
            game_id=2,
            in_game=True,
            is_winner=False,
        ),
        PlayerModel(
            id=2,
            user_id=user_2.id,
            score=75,
            game_id=2,
            in_game=True,
            is_winner=False,
        ),
    ]


@pytest.fixture
def players_2(
    store: Store, user_1: User, user_2: User, user_3: User
) -> list[PlayerModel]:
    """
    :param user_3:
    :param user_2:
    :param user_1:
    :param store:
    :return:
    """
    return [
        PlayerModel(
            id=1,
            user_id=user_1.id,
            score=35,
            game_id=3,
            in_game=True,
            is_winner=False,
        ),
        PlayerModel(
            id=2,
            user_id=user_2.id,
            score=70,
            game_id=3,
            in_game=True,
            is_winner=False,
        ),
        PlayerModel(
            id=3,
            user_id=user_3.id,
            score=45,
            game_id=3,
            in_game=True,
            is_winner=False,
        ),
    ]


@pytest.fixture
async def user_1(db_session: AsyncSession) -> User:
    """
    :param db_session:
    :return:
    """
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
        id=new_user.id,
        vk_id=vk_id,
        name=name,
        last_name=last_name,
        username=username,
    )


@pytest.fixture
async def user_2(db_session: AsyncSession) -> User:
    """
    :param db_session:
    :return:
    """
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
        id=new_user.id,
        vk_id=vk_id,
        name=name,
        last_name=last_name,
        username=username,
    )


@pytest.fixture
async def user_3(db_session: AsyncSession) -> User:
    """
    :param db_session:
    :return:
    """
    vk_id = 239360737
    name = "Анна"
    last_name = "Панн"
    username = "@pannanna"
    new_user = UserModel(
        vk_id=vk_id, name=name, last_name=last_name, username=username
    )
    async with db_session.begin() as session:
        session.add(new_user)
    return User(
        id=new_user.id,
        vk_id=vk_id,
        name=name,
        last_name=last_name,
        username=username,
    )


@pytest.fixture
async def game_data_1(db_session: AsyncSession) -> GameData:
    """
    :param db_session:
    :return:
    """
    question = "Who is the president of Uganda?"
    answer = "Sonic"
    new_game_data = GameDataModel(question=question, answer=answer)

    async with db_session.begin() as session:
        session.add(new_game_data)

    return GameData(
        id=new_game_data.id,
        question=question,
        answer=answer,
    )


@pytest.fixture
async def game_data_2(db_session: AsyncSession) -> GameData:
    """
    :param db_session:
    :return:
    """
    question = "Somebody once told who?"
    answer = "Me"
    new_game_data = GameDataModel(question=question, answer=answer)

    async with db_session.begin() as session:
        session.add(new_game_data)

    return GameData(
        id=new_game_data.id,
        question=question,
        answer=answer,
    )


@pytest.fixture
async def game_data_3(db_session: AsyncSession) -> GameData:
    """
    :param db_session:
    :return:
    """
    question = "Who wants to be a billionaire?"
    answer = "Everyone"
    new_game_data = GameDataModel(question=question, answer=answer)

    async with db_session.begin() as session:
        session.add(new_game_data)

    return GameData(
        id=new_game_data.id,
        question=question,
        answer=answer,
    )


@pytest.fixture
async def game_1(db_session: AsyncSession, game_data_1: GameData) -> Game:
    """
    :param db_session:
    :param game_data_1:
    :return:
    """
    game_data_id = game_data_1.id
    chat_id: str = "1"
    chat_message_id = 200

    new_game = GameModel(
        game_data_id=game_data_id,
        chat_id=chat_id,
        chat_message_id=chat_message_id,
    )

    async with db_session.begin() as session:
        session.add(new_game)

    return Game(
        id=new_game.id,
        game_data_id=game_data_id,
        created_at=new_game.created_at,
        finished_at=new_game.finished_at,
        chat_id=chat_id,
        chat_message_id=new_game.chat_message_id,
        guessed_word=new_game.guessed_word,
        required_player_count=new_game.required_player_count,
        previous_player_id=new_game.previous_player_id,
        player_list=[],
    )


@pytest.fixture
async def game_2(
    db_session: AsyncSession, players_1: List[Player], game_data_2: GameData
) -> Game:
    """
    :param db_session:
    :param players_1:
    :param game_data_2:
    :return:
    """
    game_data_id = game_data_2.id
    created_at = datetime.datetime.strptime(
        "2023-02-22 12:45:00.000000",
        "%Y-%m-%d %H:%M:%S.%f",
    )
    chat_id: str = "1"
    chat_message_id = 200

    new_game = GameModel(
        game_data_id=game_data_id,
        created_at=created_at,
        chat_id=chat_id,
        chat_message_id=chat_message_id,
    )

    async with db_session.begin() as session:
        session.add(new_game)

    async with db_session.begin() as session:
        for player in players_1:
            player.game_id = new_game.id
            session.add(player)

    return Game(
        id=new_game.id,
        game_data_id=game_data_id,
        created_at=created_at,
        finished_at=new_game.finished_at,
        chat_id=chat_id,
        chat_message_id=new_game.chat_message_id,
        guessed_word=new_game.guessed_word,
        required_player_count=new_game.required_player_count,
        previous_player_id=new_game.previous_player_id,
        player_list=players_1,
    )


@pytest.fixture
async def game_3(
    db_session: AsyncSession, players_2: List[Player], game_data_3: GameData
) -> Game:
    """
    :param db_session:
    :param players_2:
    :param game_data_3:
    :return:
    """
    game_data_id = game_data_3.id
    chat_id: str = "2"
    # finished_at = datetime.datetime.strptime(
    #     "2023-02-24 20:02:22.000000",
    #     "%Y-%m-%d %H:%M:%S.%f",
    # )

    new_game = GameModel(game_data_id=game_data_id, chat_id=chat_id)

    async with db_session.begin() as session:
        session.add(new_game)

    async with db_session.begin() as session:
        for player in players_2:
            player.game_id = new_game.id
            session.add(player)

    return Game(
        id=new_game.id,
        game_data_id=game_data_id,
        created_at=new_game.created_at,
        finished_at=new_game.finished_at,
        chat_id=chat_id,
        chat_message_id=new_game.chat_message_id,
        guessed_word=new_game.guessed_word,
        required_player_count=new_game.required_player_count,
        previous_player_id=players_2[0].id,
        player_list=players_2,
    )


@pytest.fixture
async def game_4(
    db_session: AsyncSession, players_2: List[Player], game_data_3: GameData
) -> Game:
    """
    :param db_session:
    :param players_2:
    :param game_data_3:
    :return:
    """
    game_data_id = game_data_3.id
    chat_id: str = "2"
    finished_at = datetime.datetime.strptime(
        "2023-02-24 20:02:22.000000",
        "%Y-%m-%d %H:%M:%S.%f",
    )

    new_game = GameModel(
        game_data_id=game_data_id, chat_id=chat_id, finished_at=finished_at
    )

    async with db_session.begin() as session:
        session.add(new_game)

    async with db_session.begin() as session:
        for player in players_2:
            player.game_id = new_game.id
            session.add(player)

    return Game(
        id=new_game.id,
        game_data_id=game_data_id,
        created_at=new_game.created_at,
        finished_at=new_game.finished_at,
        chat_id=chat_id,
        chat_message_id=new_game.chat_message_id,
        guessed_word=new_game.guessed_word,
        required_player_count=new_game.required_player_count,
        previous_player_id=players_2[0].id,
        player_list=players_2,
    )


@pytest.fixture
async def player_1(
    db_session: AsyncSession, user_1: User, game_1: Game
) -> Player:
    """
    :param db_session:
    :param user_1:
    :param game_1:
    :return:
    """
    user_id = user_1.id
    game_id = game_1.id
    new_player = PlayerModel(user_id=user_id, game_id=game_id)
    async with db_session.begin() as session:
        session.add(new_player)

    return Player(
        id=new_player.id,
        user_id=user_id,
        game_id=game_1.id,
        score=new_player.score,
        is_winner=new_player.is_winner,
        in_game=new_player.in_game,
    )


@pytest.fixture
async def player_2(
    db_session: AsyncSession, user_2: User, game_2: Game
) -> Player:
    """
    :param user_2:
    :param db_session:
    :param game_2:
    :return:
    """
    user_id = 2
    new_player = PlayerModel(user_id=user_id)
    async with db_session.begin() as session:
        session.add(new_player)

    return Player(
        id=new_player.id,
        user_id=user_id,
        game_id=game_2.id,
        score=new_player.score,
        is_winner=new_player.is_winner,
        in_game=new_player.in_game,
    )


@pytest.fixture
async def player_3(
    db_session: AsyncSession, user_3: User, game_1: Game
) -> Player:
    """
    :param user_3:
    :param db_session:
    :param game_1:
    :return:
    """
    user_id = 3
    new_player = PlayerModel(user_id=user_id)
    async with db_session.begin() as session:
        session.add(new_player)

    return Player(
        id=new_player.id,
        user_id=user_id,
        game_id=game_1.id,
        score=new_player.score,
        is_winner=new_player.is_winner,
        in_game=new_player.in_game,
    )
