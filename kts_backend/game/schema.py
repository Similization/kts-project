from marshmallow import Schema, fields
from typing import List


class GameDataByIdSchema(Schema):
    """Schema for retrieving a single game data object by ID."""

    id: int = fields.Int(required=True, description="The ID of the game data.")


class GameDataSchema(Schema):
    """Schema for representing game data."""

    id: int = fields.Int(required=False, description="The ID of the game data.")
    question: str = fields.Str(
        required=True, description="The question associated with the game data."
    )
    answer: str = fields.Str(
        required=True, description="The answer associated with the game data."
    )


class GameDataListSchema(Schema):
    """Schema for representing a list of game data objects."""

    game_data_list: List[GameDataSchema] = fields.Nested(
        GameDataSchema,
        many=True,
        required=False,
        description="A list of game data objects.",
    )
