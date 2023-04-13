import json
import typing
from typing import Dict
from json import JSONDecodeError

from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPUnprocessableEntity,
    HTTPUnauthorized,
    HTTPForbidden,
    HTTPNotFound,
    HTTPNotImplemented,
    HTTPMethodNotAllowed,
    HTTPConflict,
    HTTPException,
)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from kts_backend.admin.dataclasses import Admin
from kts_backend.web.util import error_json_response

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    """
    Authentication middleware for web application.

    This middleware function is used for authentication in a web application. It takes in a `request` object and a
    `handler` callable as parameters. The `request` parameter represents the incoming HTTP request, and the `handler`
    parameter represents the next handler in the middleware chain.

    The middleware checks for the presence of a session in the incoming request using the `get_session` function. If
    a session is found, it is used to create an `Admin` object using the `from_session` method. The `Admin` object
    is then attached to the `request` object as an attribute named `admin`.

    After the authentication process, the `handler` is called with the modified `request` object to continue processing
    subsequent middleware or request handlers.

    Args:
        request (Request): The incoming HTTP request.
        handler (callable): The next handler in the middleware chain.

    Returns:
        Response: The response returned by the `handler` after processing the request.
    """
    session = await get_session(request)
    if session:
        request.admin = Admin.from_session(session)
    return await handler(request)


HTTP_ERROR_CODES: Dict[int, str] = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler: callable):
    """
    Error handling middleware for web application.

    This middleware function is used for handling errors in a web application. It takes in a `request` object and a
    `handler` callable as parameters. The `request` parameter represents the incoming HTTP request, and the `handler`
    parameter represents the next handler in the middleware chain.

    The middleware wraps the execution of the `handler` with error handling logic. If an exception is raised during
    the execution of the `handler`, the middleware catches specific HTTP exceptions, such as `HTTPBadRequest`,
    `HTTPUnauthorized`, etc., and generates an error response using the `error_json_response` function with the
    appropriate HTTP status code, status, message, and data.

    If a caught exception does not have a specific error response defined, a default error response with a status
    code of 500 and status "Internal Server Error" is generated using the `error_json_response` function.

    Args:
        request (Request): The incoming HTTP request.
        handler (callable): The next handler in the middleware chain.

    Returns:
        Response: The response returned by the `handler` after processing the request, or an error response generated
        by the middleware.
    """
    try:
        response = await handler(request)
        return response
    except (HTTPBadRequest, HTTPUnprocessableEntity) as e:
        try:
            data = json.loads(e.text)
        except JSONDecodeError | TypeError:
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
    except HTTPException:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
        )


def setup_middlewares(app: "Application") -> None:
    """
    Setup middlewares for a web application.

    This function is used to set up middlewares for a web application using the `app` parameter, which represents the
    application instance. The middlewares are appended to the `middlewares` list of the application instance.

    The middlewares are functions or coroutines that can process incoming HTTP requests and responses before they
    reach the route handlers. They can be used for various purposes, such as authentication, error handling, request
    validation, etc.

    Args:
        app (Application): The web application instance.

    Returns:
        None
    """
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
