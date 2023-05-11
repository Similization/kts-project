from typing import List

from aiohttp.web_response import Response
from aiohttp_apispec import request_schema, response_schema

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
    """
    A view to get a single user's information by their ID.

    Expected request format:
    {
        "user_id": int
    }

    Example response format:
    {
        "id": int,
        "vk_id": int,
        "name": str,
        "last_name": str,
        "username": str
    }
    """

    @request_schema(schema=UserIdSchema)
    @response_schema(schema=UserSchema, code=200)
    async def post(self) -> Response:
        """
        Get a user's information by their ID.

        :return: Response with user information.
        """

        user_id: int = self.data["user_id"]
        user = await self.store.user.get_user(user_id=user_id)
        return json_response(data=UserSchema().dump(obj=user))


class UserGetManyView(View):
    """
    A view to get information for multiple users by their IDs.

    Expected request format:
    {
        "user_id_list": [int]
    }

    Example response format:
    {
        "user_list": [
            {
                "id": int,
                "vk_id": int,
                "name": str,
                "last_name": str,
                "username": str
            },
            ...
        ]
    }
    """

    @request_schema(schema=UserIdListSchema)
    @response_schema(schema=UserManySchema, code=200)
    async def post(self) -> Response:
        """
        Get information for multiple users by their IDs.

        :return: Response with user information.
        """

        user_id_list: List[int] = self.data["user_id_list"]
        user_list = await self.store.user.get_user(user_id=user_id_list)
        raw_users = [UserSchema().dump(obj=user) for user in user_list]
        return json_response(data={"user_list": raw_users})


class UserCreateView(View):
    """
    A view to create a new user.

    Request Body:
    {
        "user": {
            "vk_id": int,
            "name": str,
            "last_name": str,
            "username": str
        }
    }

    Response Body:
    {
        "id": int,
        "vk_id": int,
        "name": str,
        "last_name": str,
        "username": str
    }
    """

    @request_schema(schema=UserFullCreateSchema)
    @response_schema(schema=UserSchema, code=201)
    async def post(self) -> Response:
        """
        Create a new user.

        :return: Response object
        """
        user_dict: dict = self.data["user"]
        created_user = await self.store.user.create_user(user=user_dict)
        return json_response(data=UserSchema().dump(obj=created_user))


class UserCreateManyView(View):
    """
    A view to create multiple users.

    Request Body:
    {
        "user_list": [
            {
                "vk_id": int,
                "name": str,
                "last_name": str,
                "username": str
            },
            ...
        ]
    }

    Response Body:
    {
        "user_list": [
            {
                "id": int,
                "vk_id": int,
                "name": str,
                "last_name": str,
                "username": str
            },
            ...
        ]
    }
    """

    @request_schema(schema=UserFullListCreateSchema)
    @response_schema(schema=UserManySchema, code=201)
    async def post(self) -> Response:
        """
        Create multiple users.

        :return: Response object
        """
        user_list = self.data["user_list"]
        created_user_list = await self.store.user.create_user(user=user_list)
        raw_users = [UserSchema().dump(obj=user) for user in created_user_list]
        return json_response(data={"user_list": raw_users})


class UserUpdateView(View):
    """
    A view to update an existing user.

    Request Body:
    {
        "user": {
            "id": int,
            "vk_id": int,
            "name": str,
            "last_name": str,
            "username": str
        }
    }

    Response Body:
    {
        "id": int,
        "vk_id": int,
        "name": str,
        "last_name": str,
        "username": str
    }
    """

    @request_schema(schema=UserFullUpdateSchema)
    @response_schema(schema=UserSchema, code=200)
    async def post(self) -> Response:
        """
        Update an existing user.

        :return: Response object
        """
        user = self.data["user"]
        updated_user = await self.store.user.update_user(user=user)
        return json_response(data=UserSchema().dump(obj=updated_user))


class UserUpdateManyView(View):
    """
    View for updating multiple user records.

    Request:
    - user_list (list): A list of dictionaries representing the user records to update.

    Response:
    - user_list (list): A list of dictionaries representing the updated user records.

    Example:
    Request:
    {
        "user_list": [
            {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "age": 35
            },
            {
                "username": "janedoe",
                "email": "janedoe@example.com",
                "age": 28
            }
        ]
    }

    Response:
    {
        "user_list": [
            {
                "id": 1,
                "username": "johndoe",
                "email": "johndoe@example.com",
                "age": 35
            },
            {
                "id": 2,
                "username": "janedoe",
                "email": "janedoe@example.com",
                "age": 28
            }
        ]
    }
    """

    @request_schema(schema=UserFullListUpdateSchema)
    @response_schema(schema=UserManySchema, code=200)
    async def post(self) -> Response:
        """
        Update multiple user records.

        Returns:
        Response: The updated user records.
        """
        user_list = self.data["user_list"]
        updated_user_list = await self.store.user.update_user(user=user_list)
        raw_users = [UserSchema().dump(obj=user) for user in updated_user_list]
        return json_response(data={"user_list": raw_users})


class UserDeleteView(View):
    """
    View for deleting a single user record.

    Request:
    - user_id (int): The ID of the user to delete.

    Response:
    - user (dict): A dictionary representing the deleted user record.

    Example:
    Request:
    {
        "user_id": 1
    }

    Response:
    {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "age": 35
    }
    """

    @request_schema(schema=UserIdSchema)
    @response_schema(schema=UserSchema, code=200)
    async def post(self) -> Response:
        """
        Delete a single user record.

        Returns:
        Response: The deleted user record.
        """
        user_id = self.data["user_id"]
        deleted_user = await self.store.user.delete_user(user_id=user_id)
        return json_response(data=UserSchema().dump(obj=deleted_user))


class UserDeleteManyView(View):
    """
    View for deleting multiple users by their IDs.

    The view expects a POST request with a JSON payload containing a list of user IDs:

    Example request body:
    {
        "user_id_list": [1, 2, 3]
    }

    The view returns a JSON response with a list of deleted users in the response body:

    Example response body:
    {
        "user_list": [
            {
                "id": 1,
                "username": "johndoe",
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe"
            },
            {
                "id": 2,
                "username": "janedoe",
                "email": "janedoe@example.com",
                "first_name": "Jane",
                "last_name": "Doe"
            }
        ]
    }
    """

    @request_schema(schema=UserIdListSchema)
    @response_schema(schema=UserManySchema, code=200)
    async def post(self) -> Response:
        """
        Delete multiple users by their IDs.

        Returns a list of deleted users in the response body.
        """
        user_id_list = self.data["user_id_list"]
        deleted_user_list = await self.store.user.delete_user(
            user_id=user_id_list
        )
        raw_users = [UserSchema().dump(obj=user) for user in deleted_user_list]
        return json_response(data={"user_list": raw_users})
