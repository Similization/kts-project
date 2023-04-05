from sqlalchemy import inspect
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncEngine


def ok_response(data: dict) -> dict:
    """
    Returns a response dictionary with 'status' set to 'ok' and 'data' set to the given data dictionary.

    :param data: dict
    :return: dict
    """
    return {
        "status": "ok",
        "data": data,
    }


def error_response(status: str, message: str, data: dict) -> dict:
    """
    Returns a response dictionary with 'status', 'message', and 'data' set to the given arguments.

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
    Returns a list of table names in the given database connection.

    :param conn: SQLAlchemy database connection
    :return: list of str
    """
    inspector = inspect(conn)
    return inspector.get_table_names()


async def check_empty_table_exists(cli, table_name: str):
    """
    Asserts that the given table name exists in the database connected to the given CLI, and that it is empty.

    :param cli: KTS CLI object
    :param table_name: str
    :raises AssertionError: if the table does not exist or if it is not empty
    """
    engine: AsyncEngine = cli.app.database._engine
    async with engine.begin() as conn:
        tables = await conn.run_sync(use_inspector)

    assert table_name in tables
    statement = text(f'SELECT COUNT(*) FROM "{table_name}"')
    async with cli.app.database.session() as session:
        result = await session.execute(statement)
        count = result.scalar()
    if table_name == "admin":
        assert count == 1
    else:
        assert count == 0
