from dataclasses import asdict
from typing import List, Sequence

from sqlalchemy import select, update, insert, delete

from kts_backend.base.base_accessor import BaseAccessor
from kts_backend.user.dataclasses import User
from kts_backend.user.model import UserModel


class UserError(Exception):
    pass


class UserAccessor(BaseAccessor):
    @staticmethod
    def user_model2user(user_model: UserModel) -> User:
        """
        Convert UserModel object to User object
        :param user_model: UserModel
        :return: User
        """
        return User(
            id=user_model.id,
            vk_id=user_model.vk_id,
            name=user_model.name,
            last_name=user_model.last_name,
            username=user_model.username,
        )

    @staticmethod
    def user_model_list2user_list(
        user_model_list: List[UserModel],
    ) -> List[User]:
        """
        Convert list of UserModel objects to list of User objects
        :param user_model_list: List[UserModel]
        :return: List[User]
        """
        print(user_model_list)
        return [
            UserAccessor.user_model2user(user_model=user_model)
            for user_model in user_model_list
        ]

    @staticmethod
    def user2dict(user: User) -> dict:
        """
        Convert user to dictionary
        :param user: List[UserModel]
        :return: dict
        """
        return asdict(user)

    @staticmethod
    def user_list2dict_list(user_list: List[User]) -> List[dict]:
        """
        Convert list of UserModel objects to list of User objects
        :param user_list: List[User]
        :return: List[dict]
        """
        return [asdict(user) for user in user_list]

    async def get_user(
        self, user_id: List[int] | int
    ) -> List[User] | User | None:
        """
        Get users from database by their ids
        :param user_id: List[int] | int
        :return: List[User] | User | None
        """
        if isinstance(user_id, int):
            return await self.get_one_user(user_id=user_id)
        if isinstance(user_id, list):
            return await self.get_user_list(user_id_list=user_id)

    async def get_one_user(self, user_id: int) -> User | None:
        """
        Get one user from database by his id
        :param user_id: int
        :return: User | None
        """
        async with self.app.database.session.begin() as session:
            user_model: UserModel | None = await session.get(UserModel, user_id)
            if user_model:
                return self.user_model2user(user_model=user_model)
            return None

    async def get_user_list(self, user_id_list: List[int]) -> List[User] | None:
        """
        Get list of users from database by their ids
        :param user_id_list:  List[int]
        :return: List[User] | None
        """
        # TODO: var 1
        # result_list = []
        # for user_id in user_id_list:
        #     result_list.append(await self.get_one_user(user_id=user_id))
        # return result_list
        # TODO: var 2
        statement = select(UserModel).where(UserModel.id.in_(user_id_list))
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement)
            user_model_seq: Sequence[UserModel] | None = res.scalars().all()
            user_model_list: List[UserModel] | None = list(user_model_seq)
            if user_model_list:
                return self.user_model_list2user_list(
                    user_model_list=user_model_list
                )
            return None

    async def get_one_user_by_vk_id(self, vk_id: int) -> User | None:
        """
        Get one user from database by his vk id
        :param vk_id: int
        :return: User | None
        """
        statement = select(UserModel).filter_by(vk_id=vk_id)
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            user_model: UserModel | None = res.scalar()
            if user_model:
                return self.user_model2user(user_model=user_model)
            return None

    async def get_user_list_by_vk_id_list(
        self, vk_id_list: List[str]
    ) -> List[User]:
        """
        Get User object list from database by vk_id list
        :param vk_id_list: List[str]
        :return: List[User]
        """
        statement = select(UserModel).where(UserModel.vk_id.in_(vk_id_list))
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            user_model_list: List[UserModel] | None = res.scalars()
            print(user_model_list)
            if user_model_list:
                return self.user_model_list2user_list(
                    user_model_list=user_model_list
                )
            return []

    async def create_user(self, user: List[dict] | dict) -> List[User] | User:
        """
        Create users in database if they do not exist
        otherwise throws an exception
        :param user: List[dict] | dict
        :return: List[User] | User
        """
        if isinstance(user, dict):
            return await self.create_one_user(user=user)
        if isinstance(user, list):
            return await self.create_user_list(user_list=user)

    async def create_one_user(self, user: dict) -> User:
        """
        Create one user if he does not exist
        otherwise throws an exception
        :param user: dict
        :return: User
        """
        if await self.get_one_user_by_vk_id(vk_id=user.get("vk_id")):
            raise UserError("User is already exists")

        async with self.app.database.session.begin() as session:
            res = await session.execute(
                insert(UserModel).returning(UserModel), user
            )
            user_model: UserModel | None = res.scalar()
            await session.commit()

            return self.user_model2user(user_model=user_model)

    async def create_user_list(self, user_list: List[dict]) -> List[User]:
        """
        Create user list if such users does not exist
        otherwise throws an exception
        :param user_list: List[dict]
        :return: List[User]
        """
        # TODO: var 1
        # result_list = []
        # for user in user_list:
        #     result_list.append(await self.create_one_user(user=user))
        # return result_list
        # TODO: var 2
        async with self.app.database.session.begin() as session:
            res = await session.execute(
                insert(UserModel).returning(UserModel), user_list
            )
            user_model_seq: Sequence[UserModel] | None = res.scalars().all()
            user_model_list: List[UserModel] | None = list(user_model_seq)
            await session.commit()

            return self.user_model_list2user_list(
                user_model_list=user_model_list
            )

    async def update_user(self, user: List[dict] | dict) -> List[User] | User:
        """
        Update users if such users does not exist
        otherwise throws an exception
        :param user: List[dict] | dict
        :return: List[User] | User
        """
        if isinstance(user, dict):
            return await self.update_one_user(user=user)
        if isinstance(user, list):
            return await self.update_user_list(user_list=user)

    async def update_one_user(self, user: dict) -> User:
        """
        Update one user if he does not exist
        otherwise throws an exception
        :param user: User
        :return: User
        """
        user_id: int = user.get("user_id")
        if not self.get_one_user(user_id=user_id):
            raise UserError("User does not exist")
        user.pop("user_id")

        async with self.app.database.session.begin() as session:
            res = await session.execute(
                update(UserModel).filter_by(id=user_id).returning(UserModel),
                user,
            )
            user_model: UserModel | None = res.scalar()
            await session.commit()

            return self.user_model2user(user_model=user_model)

    async def update_user_list(self, user_list: List[dict]) -> List[User]:
        """
        Update user list if such users does not exist
        otherwise throws an exception
        :param user_list:
        :return:
        """
        # TODO: var 1
        result_list = []
        for user in user_list:
            result_list.append(await self.update_one_user(user=user))
        return result_list
        # TODO: var 2
        # user_id_list = []
        # for user in user_list:
        #     user_id_list.append(user.pop("user_id"))
        #
        # async with self.app.database.session.begin() as session:
        #     res = await session.execute(
        #         update(UserModel).where(UserModel.user_id.in_(user_id_list)).returning(UserModel),
        #         user_list
        #     )
        #     user_model_list: Optional[List[UserModel]] = res.scalars()
        #     await session.commit()
        #
        #     return self.user_model_list2user_list(
        #         user_model_list=user_model_list
        #     )

    async def create_or_update_user(
        self, user: List[dict] | dict
    ) -> List[User] | User:
        """
        Create users or update information about them in database
        otherwise trows an exception
        :param user: List[dict] | dict
        :return: List[User] | User
        """
        # TODO: var 1
        # try:
        #     return await self.create_user(user=user)
        # except UserError:
        #     return await self.update_user(user=user)
        # TODO: var 2
        if isinstance(user, dict):
            try:
                return await self.create_one_user(user=user)
            except UserError:
                return await self.update_one_user(user=user)
        if isinstance(user, list):
            for user_one in user:
                try:
                    return await self.create_one_user(user=user_one)
                except UserError:
                    return await self.update_one_user(user=user_one)

    async def delete_user(self, user_id: List[int] | int):
        """
        Delete information about users
        :param user_id:
        :return:
        """
        if isinstance(user_id, int):
            return await self.delete_one_user(user_id=user_id)
        if isinstance(user_id, list):
            return await self.delete_user_list(user_id_list=user_id)

    async def delete_one_user(self, user_id: int) -> User:
        """
        Delete one user from database
        :param user_id: int
        :return: User
        """
        async with self.app.database.session.begin() as session:
            user_model: UserModel | None = await session.get(UserModel, user_id)
            if user_model:
                await session.delete(user_model)
            await session.commit()

            return self.user_model2user(user_model=user_model)

    async def delete_user_list(self, user_id_list: List[int]) -> List[User]:
        """
        Delete list of users from database
        :param user_id_list: List[int]
        :return: List[User]
        """
        # TODO: var 1
        # result_list: List[User] = []
        # for user_id in user_id_list:
        #     result_list.append(await self.delete_one_user(user_id=user_id))
        # return result_list
        # TODO: var 2
        statement = (
            delete(UserModel)
            .where(UserModel.id.in_(user_id_list))
            .returning(UserModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            user_model_seq: Sequence[UserModel] | None = res.scalars().all()
            user_model_list: List[UserModel] | None = list(user_model_seq)
            await session.commit()

            return self.user_model_list2user_list(
                user_model_list=user_model_list
            )
