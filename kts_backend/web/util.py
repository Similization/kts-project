from typing import Any, Dict

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


def json_response(data: Dict[str, Any] = None, status: str = "ok") -> Response:
    """
    Return a JSON response with a success status and optional data.

    :param data: Dict[str, Any] or None
    :param status: str
    :return: Response
    """
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: str = "",
    data: Dict[str, Any] = None,
) -> Response:
    """
    Return a JSON response with an error status, message and optional data.

    :param http_status: int
    :param status: str
    :param message: str
    :param data: Dict[str, Any] or None
    :return: Response
    """
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": message,
            "data": data,
        },
    )
