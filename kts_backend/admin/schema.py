from marshmallow import Schema, fields, validate


class AdminSchema(Schema):
    """
    Schema for validating and serializing Admin data.

    Attributes:
        id (int): The ID of the Admin.
        user_id (int): The ID of the user associated with the Admin.
        email (str): The email associated with the Admin (required, maximum length 60 characters).
        password (str): The password associated with the Admin (required, load only).
    """

    id: int = fields.Int(required=False, description="The ID of the Admin.")
    user_id: int = fields.Int(
        required=False,
        description="The ID of the user associated with the Admin.",
    )
    email: str = fields.Email(
        required=True,
        validate=validate.Length(max=60),
        description="The email associated with the Admin (required, maximum length 60 characters).",
    )
    password: str = fields.Str(
        required=True,
        load_only=True,
        description="The password associated with the Admin (required, load only).",
    )
