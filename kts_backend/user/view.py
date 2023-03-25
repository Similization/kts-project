from typing import List

from aiohttp_apispec import request_schema, response_schema

from kts_backend.user.schema import (
    UserSchema,
    UserIdSchema, UserCreateSchema, UserUpdateSchema, UserManySchema,

)
from kts_backend.web.app import View
from kts_backend.web.util import json_response


class UserGetView(View):
    @request_schema(UserIdSchema)
    @response_schema(UserSchema)
    async def get(self):
        user_id: int = self.data["user_id"]
        user = await self.store.user.get_user(user_id=user_id)
        return json_response(data=UserSchema().dump(obj=user))


class UserGetManyView(View):
    @request_schema(UserIdSchema)
    @response_schema(UserManySchema)
    async def get(self):
        user_id_list: List[int] = self.data["user_ids"]
        user_list = await self.store.user.get_user(user_id=user_id_list)
        return json_response(data=UserManySchema().dump(obj=user_list))


class UserCreateView(View):
    @request_schema(UserCreateSchema)
    @response_schema(UserSchema)
    async def get(self):
        user = self.data["user"]
        created_user = await self.store.user.create_user(user=user)
        return json_response(data=UserSchema().dump(obj=created_user))


class UserCreateManyView(View):
    @request_schema(UserCreateSchema)
    @response_schema(UserManySchema)
    async def get(self):
        user_list = await self.data["users"]
        created_user_list = self.store.user.create_user(user=user_list)
        return json_response(data=UserManySchema().dump(obj=created_user_list))


class UserUpdateView(View):
    @request_schema(UserUpdateSchema)
    @response_schema(UserSchema)
    async def get(self):
        user = self.data["user"]
        updated_user = await self.store.user.update_user(user=user)
        return json_response(data=UserSchema().dump(obj=updated_user))


class UserUpdateManyView(View):
    @request_schema(UserUpdateSchema)
    @response_schema(UserManySchema)
    async def get(self):
        user_list = self.data["users"]
        updated_user_list = await self.store.user.update_user(user=user_list)
        return json_response(data=UserManySchema().dump(obj=updated_user_list))


class UserDeleteView(View):
    @request_schema(UserIdSchema)
    @response_schema(UserSchema)
    async def get(self):
        user_id = self.data["user_id"]
        deleted_user = await self.store.user.delete_user(user_id=user_id)
        return json_response(data=UserSchema().dump(obj=deleted_user))


class UserDeleteManyView(View):
    @request_schema(UserIdSchema)
    @response_schema(UserManySchema)
    async def get(self):
        user_id_list = self.data["user_ids"]
        deleted_user_list = await self.store.user.delete_user(user_id=user_id_list)
        return json_response(data=UserManySchema().dump(obj=deleted_user_list))
