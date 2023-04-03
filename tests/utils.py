from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine


def ok_response(data: dict) -> dict:
    """
    Response if no error occurs
    :param data: dict
    :return: dict
    """
    return {
        "status": "ok",
        "data": data,
    }


def error_response(status: str, message: str, data: dict) -> dict:
    """
    Response in case of errors
    :param status: str
    :param message: str
    :param data: dict
    :return: dict
    """
    return {
        "status": status,
        "message": message,
        "data": data,
    }


def use_inspector(conn):
    """
    Get table names
    :param conn:
    :return:
    """
    inspector = inspect(conn)
    return inspector.get_table_names()


async def check_empty_table_exists(cli, table_name: str):
    """
    Check if empty table is exist
    :param cli:
    :param table_name: str
    :return:
    """
    engine: AsyncEngine = cli.app.database._engine
    async with engine.begin() as conn:
        tables = await conn.run_sync(use_inspector)

    assert table_name in tables
