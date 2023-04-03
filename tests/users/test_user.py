from sqlalchemy.exc import IntegrityError
from typing import List

from sqlalchemy.future import select

import pytest
from kts_backend.store import Store
from kts_backend.user.dataclasses import User
from kts_backend.user.model import UserModel
from tests.utils import check_empty_table_exists


class TestPlayerStore:
    async def test_table_exists(self, cli):
        """
        :param cli:
        :return:
        """
        await check_empty_table_exists(cli, "user")

    async def test_create_user(self, cli, store: Store):
        """
        :param cli:
        :param store:
        :return:
        """
        user_id = 1
        vk_id = 100001
        name = "Dan"
        last_name = "Ban"
        username = "@db"
        user = User(
            id=user_id,
            vk_id=vk_id,
            name=name,
            last_name=last_name,
            username=username,
        )
        created_user = await store.user.create_user(user=user.__dict__)
        assert type(created_user) is User

        async with cli.app.database.session() as session:
            res = await session.execute(select(UserModel))
            user_model_list: List[UserModel] = res.scalars().all()

        assert len(user_model_list) == 1
        user_from_db: UserModel = user_model_list[0]
        assert user_from_db.id == user.id
        assert user_from_db.vk_id == user.vk_id
        assert user_from_db.name == user.name
        assert user_from_db.last_name == user.last_name
        assert user_from_db.username == user.username

    async def test_create_existed_user(self, cli, store: Store, user_1: User):
        """
        :param cli:
        :param store:
        :param user_1:
        :return:
        """
        user_id = 1
        vk_id = 100001
        name = "Dan"
        last_name = "Ban"
        username = "@db"
        user = User(
            id=user_id,
            vk_id=vk_id,
            name=name,
            last_name=last_name,
            username=username,
        )
        with pytest.raises(IntegrityError) as exc_info:
            await store.user.create_user(user=user.__dict__)
        assert exc_info.value.orig.pgcode == "23505"

    async def test_get_user_by_id(self, cli, store: Store, user_1: User):
        """
        :param cli:
        :param store:
        :param user_1:
        :return:
        """
        assert user_1 == await store.user.get_user(user_id=user_1.id)
