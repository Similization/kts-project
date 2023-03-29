from typing import Optional

from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session
from aiohttp.web_response import Response

from kts_backend.admin.dataclasses import Admin
from kts_backend.admin.schema import AdminSchema
from kts_backend.web.app import View
from kts_backend.web.util import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self) -> Response:
        """
        Get new admin email and password and return created Admin object schema
        :return: Response
        """
        data: dict = self.request["data"]
        admin: Optional[Admin] = await self.store.admin.get_admin_by_email(
            email=data["email"]
        )
        if admin is None or not admin.is_password_valid(data["password"]):
            raise HTTPForbidden

        session = await new_session(request=self.request)
        session["admin"] = {"id": admin.id, "email": admin.email}

        return json_response(data=AdminSchema().dump(admin))


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self) -> Response:
        """
        Get Admin object from database and return Admin object schema,
        otherwise raise HTTPUnauthorized
        :return: Response
        :raises: HTTPUnauthorized
        """
        admin = self.request.admin
        if admin is None:
            raise HTTPUnauthorized
        return json_response(data=AdminSchema().dump(admin))
