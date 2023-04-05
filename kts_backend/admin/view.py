from aiohttp.web import HTTPForbidden, HTTPUnauthorized, Response
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from kts_backend.admin.dataclasses import Admin
from kts_backend.admin.schema import AdminSchema
from kts_backend.web.app import View
from kts_backend.web.util import json_response


class AdminLoginView(View):
    """
    A view for logging in an admin and creating a new session.
    """

    @request_schema(schema=AdminSchema)
    @response_schema(schema=AdminSchema, code=200)
    async def post(self) -> Response:
        """
        Authenticate an admin with the provided email and password, create a new session and return the admin object.

        Raises:
            HTTPForbidden: If the provided email and password do not match an existing admin object in the database.

        Returns:
            Response: A JSON response with the serialized admin object.
        """
        data: dict = self.request["data"]
        if not (
            admin := await self.store.admin.get_by_email(email=data["email"])
        ) or not admin.is_password_valid(data["password"]):
            raise HTTPForbidden

        session = await new_session(request=self.request)
        session["admin"] = {"id": admin.id, "email": admin.email}

        return json_response(data=AdminSchema().dump(obj=admin))


class AdminCurrentView(View):
    """
    A view for getting the current admin object.
    """

    @response_schema(schema=AdminSchema, code=200)
    async def get(self) -> Response:
        """
        Get the current admin object from the session and return the serialized admin object.

        Raises:
            HTTPUnauthorized: If there is no current admin object in the session.

        Returns:
            Response: A JSON response with the serialized admin object.
        """
        admin: Admin | None = await self.get_admin()
        if admin is None:
            raise HTTPUnauthorized
        return json_response(data=AdminSchema().dump(obj=admin))

    async def get_admin(self) -> Admin | None:
        """
        Get the current admin object from the session.

        Returns:
            Optional[Admin]: The current admin object if it exists in the session, otherwise None.
        """
        return self.request.admin
