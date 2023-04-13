from marshmallow import Schema, fields


class UserIdSchema(Schema):
    """
    Schema for representing a user ID.

    Attributes:
        id (int): User ID.
    """

    id = fields.Int(required=True, description="User ID")


class UserIdListSchema(Schema):
    """
    Schema for representing a list of user IDs.

    Attributes:
        user_id_list (List[int]): List of user IDs.
    """

    user_id_list = fields.List(
        cls_or_instance=fields.Int,
        required=True,
        description="List of User IDs",
    )


class UserCreateSchema(Schema):
    """
    Schema for creating a new user.

    Attributes:
        vk_id (int): VK ID of the user.
        name (str): First name of the user.
        last_name (str): Last name of the user.
        username (str): Username of the user.
    """

    vk_id = fields.Int(required=True, description="VK ID of user")
    name = fields.Str(required=True, description="First name of user")
    last_name = fields.Str(required=True, description="Last name of user")
    username = fields.Str(required=True, description="Username of user")


class UserFullCreateSchema(Schema):
    """
    Schema representing the full details of a user to be created.

    Attributes:
        user (UserCreateSchema): Nested schema representing the details of the user to be created.
    """

    user = fields.Nested(
        UserCreateSchema,
        many=False,
        required=True,
        description="Details of user to be created",
    )


class UserFullListCreateSchema(Schema):
    """
    Schema representing a list of full details of users to be created.

    Attributes:
        user_list (List[UserCreateSchema]): Nested schema representing a list of details of users to be created.
    """

    user_list = fields.Nested(
        UserCreateSchema,
        many=True,
        required=True,
        description="List of details of users to be created",
    )


class UserUpdateSchema(Schema):
    """
    Schema representing the details of a user to be updated.

    Attributes:
        id (int): ID of the user to be updated.
        vk_id (int): New VK ID of the user.
        name (str): New first name of the user.
        last_name (str): New last name of the user.
        username (str): New username of the user.
    """

    id = fields.Int(required=True, description="ID of user to be updated")
    vk_id = fields.Int(required=True, description="New VK ID of user")
    name = fields.Str(required=True, description="New first name of user")
    last_name = fields.Str(required=True, description="New last name of user")
    username = fields.Str(required=True, description="New username of user")


class UserFullUpdateSchema(Schema):
    """
    Schema representing the full details of a user to be updated.

    Attributes:
        user (UserUpdateSchema): Nested schema representing the details of the user to be updated.
    """

    user = fields.Nested(
        UserUpdateSchema,
        many=False,
        required=True,
        description="Details of user to be updated",
    )


class UserFullListUpdateSchema(Schema):
    """
    Schema representing a list of full details of users to be updated.

    Attributes:
        user_list (List[UserUpdateSchema]): Nested schema representing a list of details of users to be updated.
    """

    user_list = fields.Nested(
        UserUpdateSchema,
        many=True,
        required=True,
        description="List of details of users to be updated",
    )


class UserSchema(UserIdSchema):
    """
    Schema representing the details of a user.

    Inherits from:
        - UserIdSchema: Schema representing the user ID.

    Attributes:
        vk_id (int): VK ID of the user.
        name (str): First name of the user.
        last_name (str): Last name of the user.
        username (str): Username of the user.
    """

    vk_id = fields.Int(required=False, description="VK ID of user")
    name = fields.Str(required=False, description="First name of user")
    last_name = fields.Str(required=False, description="Last name of user")
    username = fields.Str(required=False, description="Username of user")


class UserManySchema(UserIdSchema):
    """
    Schema representing a list of users' details.

    Inherits from:
        - UserIdSchema: Schema representing the user ID.

    Attributes:
        user_list (List[UserSchema]): List of users' details.
    """

    user_list = fields.Nested(
        UserSchema,
        many=True,
        required=False,
        description="List of users' details",
    )
