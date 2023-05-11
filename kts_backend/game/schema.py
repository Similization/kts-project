from marshmallow import Schema, fields
from typing import List


class GameDataByIdSchema(Schema):
    """
    A schema representing game data by ID.

    Attributes:
        id (int): The ID of the game data.
    """

    id: int = fields.Int(required=True, description="The ID of the game data.")


class GameDataSchema(Schema):
    """
    A schema representing game data.

    Attributes:
        id (int, optional): The ID of the game data.
        question (str): The question associated with the game data.
        answer (str): The answer associated with the game data.
    """

    id: int = fields.Int(required=False, description="The ID of the game data.")
    question: str = fields.Str(
        required=True, description="The question associated with the game data."
    )
    answer: str = fields.Str(
        required=True, description="The answer associated with the game data."
    )


class GameDataListSchema(Schema):
    """
    A schema representing a list of game data.

    Attributes:
        game_data_list (list of GameDataSchema, optional): A list of game data objects.
    """

    game_data_list: List[GameDataSchema] = fields.Nested(
        GameDataSchema,
        many=True,
        required=False,
        description="A list of game data objects.",
    )
