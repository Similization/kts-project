import json
import typing

from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPUnprocessableEntity,
    HTTPUnauthorized,
    HTTPForbidden,
    HTTPNotFound,
    HTTPNotImplemented,
    HTTPMethodNotAllowed,
    HTTPConflict,
)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from kts_backend.admin.model import Admin
from kts_backend.web.util import error_json_response

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    if session:
        request.admin = Admin.from_session(session)
    return await handler(request)


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except (HTTPBadRequest, HTTPUnprocessableEntity) as e:
        try:
            data = json.loads(e.text)
        except Exception:
            data = e.text

        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=data,
        )
    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401],
            message=e.reason,
            data=e.text,
        )
    except HTTPForbidden as e:
        return error_json_response(
            http_status=403,
            status=HTTP_ERROR_CODES[403],
            message=e.reason,
            data=e.text,
        )
    except HTTPNotFound as e:
        return error_json_response(
            http_status=404,
            status=HTTP_ERROR_CODES[404],
            message=e.reason,
            data=e.text,
        )
    except (HTTPNotImplemented, HTTPMethodNotAllowed) as e:
        return error_json_response(
            http_status=405,
            status=HTTP_ERROR_CODES[405],
            message=e.reason,
            data=e.text,
        )
    except HTTPConflict as e:
        return error_json_response(
            http_status=409,
            status=HTTP_ERROR_CODES[409],
            message=e.reason,
            data=e.text,
        )
    except Exception as e:
        print(e)
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
        )


def setup_middlewares(app: "Application"):
    # app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
