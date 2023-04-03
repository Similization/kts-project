from typing import List

from aiohttp_apispec import request_schema, response_schema
from aiohttp.web_response import Response

from kts_backend.user.schema import (
    UserSchema,
    UserIdSchema,
    UserIdListSchema,
    UserFullCreateSchema,
    UserFullListCreateSchema,
    UserFullUpdateSchema,
    UserFullListUpdateSchema,
    UserManySchema,
)
from kts_backend.web.app import View
from kts_backend.web.util import json_response


class UserGetView(View):
    @request_schema(UserIdSchema)
    @response_schema(UserSchema, 200)
    async def post(self) -> Response:
        """
        :return: Response
        """
        user_id: int = self.data["user_id"]
        user = await self.store.user.get_user(user_id=user_id)
        return json_response(data=UserSchema().dump(obj=user))


class UserGetManyView(View):
    @request_schema(UserIdListSchema)
    @response_schema(UserManySchema, 200)
    async def post(self) -> Response:
        """
        :return: Response
        """
        user_id_list: List[int] = self.data["user_id_list"]
        user_list = await self.store.user.get_user(user_id=user_id_list)
        raw_users = [UserSchema().dump(obj=user) for user in user_list]
        return json_response(data={"user_list": raw_users})


class UserCreateView(View):
    @request_schema(UserFullCreateSchema)
    @response_schema(UserSchema, 200)
    async def post(self) -> Response:
        """
        :return: Response
        """
        user_dict: dict = self.data["user"]
        created_user = await self.store.user.create_user(user=user_dict)
        return json_response(data=UserSchema().dump(obj=created_user))


class UserCreateManyView(View):
    @request_schema(UserFullListCreateSchema)
    @response_schema(UserManySchema, 200)
    async def post(self) -> Response:
        """
        :return: Response
        """
        user_list = self.data["user_list"]
        created_user_list = await self.store.user.create_user(user=user_list)
        raw_users = [UserSchema().dump(obj=user) for user in created_user_list]
        return json_response(data={"user_list": raw_users})


class UserUpdateView(View):
    @request_schema(UserFullUpdateSchema)
    @response_schema(UserSchema, 200)
    async def post(self) -> Response:
        """
        :return:
        """
        user = self.data["user"]
        updated_user = await self.store.user.update_user(user=user)
        return json_response(data=UserSchema().dump(obj=updated_user))


class UserUpdateManyView(View):
    @request_schema(UserFullListUpdateSchema)
    @response_schema(UserManySchema, 200)
    async def post(self) -> Response:
        """
        :return: Response
        """
        user_list = self.data["user_list"]
        updated_user_list = await self.store.user.update_user(user=user_list)
        raw_users = [UserSchema().dump(obj=user) for user in updated_user_list]
        return json_response(data={"user_list": raw_users})


class UserDeleteView(View):
    @request_schema(UserIdSchema)
    @response_schema(UserSchema, 200)
    async def post(self) -> Response:
        """
        :return: Response
        """
        user_id = self.data["user_id"]
        deleted_user = await self.store.user.delete_user(user_id=user_id)
        return json_response(data=UserSchema().dump(obj=deleted_user))


class UserDeleteManyView(View):
    @request_schema(UserIdListSchema)
    @response_schema(UserManySchema, 200)
    async def post(self) -> Response:
        """
        :return: Response
        """
        user_id_list = self.data["user_id_list"]
        deleted_user_list = await self.store.user.delete_user(
            user_id=user_id_list
        )
        raw_users = [UserSchema().dump(obj=user) for user in deleted_user_list]
        return json_response(data={"user_list": raw_users})
