from typing import Any, Dict

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


def json_response(data: Dict[str, Any] = None, status: str = "ok") -> Response:
    """
    Create a JSON response.

    This function creates a JSON response with the provided data and status. The `data` parameter is an optional
    dictionary that contains the data to be included in the response. The `status` parameter is an optional string
    that indicates the status of the response, which defaults to "ok" if not provided.

    Args:
        data (Dict[str, Any], optional): The data to be included in the response. Defaults to None.
        status (str, optional): The status of the response. Defaults to "ok".

    Returns:
        Response: A JSON response with the provided data and status.
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
    Create an error JSON response.

    This function creates an error JSON response with the provided HTTP status code, status, message, and data.
    The `http_status` parameter is the HTTP status code to be included in the response. The `status` parameter
    is an optional string that indicates the status of the error, which defaults to "error" if not provided.
    The `message` parameter is an optional string that provides a description of the error, which defaults to
    an empty string if not provided. The `data` parameter is an optional dictionary that contains additional
    data related to the error, which defaults to None.

    Args:
        http_status (int): The HTTP status code of the error response.
        status (str, optional): The status of the error response. Defaults to "error".
        message (str, optional): The error message. Defaults to "".
        data (Dict[str, Any], optional): Additional data related to the error. Defaults to None.

    Returns:
        Response: An error JSON response with the provided HTTP status code, status, message, and data.
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
