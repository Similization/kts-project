from marshmallow import Schema, fields


class UserIdSchema(Schema):
    """
    Schema for User ID
    """

    id = fields.Int(required=True, description="User ID")


class UserIdListSchema(Schema):
    """
    Schema for list of User IDs
    """

    user_id_list = fields.List(
        cls_or_instance=fields.Int,
        required=True,
        description="List of User IDs",
    )


class UserCreateSchema(Schema):
    """
    Schema for creating a new user
    """

    vk_id = fields.Int(required=True, description="VK ID of user")
    name = fields.Str(required=True, description="First name of user")
    last_name = fields.Str(required=True, description="Last name of user")
    username = fields.Str(required=True, description="Username of user")


class UserFullCreateSchema(Schema):
    """
    Schema for creating a new user (full)
    """

    user = fields.Nested(
        UserCreateSchema,
        many=False,
        required=True,
        description="Details of user to be created",
    )


class UserFullListCreateSchema(Schema):
    """
    Schema for creating a list of new users (full)
    """

    user_list = fields.Nested(
        UserCreateSchema,
        many=True,
        required=True,
        description="List of details of users to be created",
    )


class UserUpdateSchema(Schema):
    """
    Schema for updating an existing user
    """

    id = fields.Int(required=True, description="ID of user to be updated")
    vk_id = fields.Int(required=True, description="New VK ID of user")
    name = fields.Str(required=True, description="New first name of user")
    last_name = fields.Str(required=True, description="New last name of user")
    username = fields.Str(required=True, description="New username of user")


class UserFullUpdateSchema(Schema):
    """
    Schema for updating an existing user (full)
    """

    user = fields.Nested(
        UserUpdateSchema,
        many=False,
        required=True,
        description="Details of user to be updated",
    )


class UserFullListUpdateSchema(Schema):
    """
    Schema for updating a list of existing users (full)
    """

    user_list = fields.Nested(
        UserUpdateSchema,
        many=True,
        required=True,
        description="List of details of users to be updated",
    )


class UserSchema(UserIdSchema):
    """
    Schema for retrieving user details
    """

    vk_id = fields.Int(required=False, description="VK ID of user")
    name = fields.Str(required=False, description="First name of user")
    last_name = fields.Str(required=False, description="Last name of user")
    username = fields.Str(required=False, description="Username of user")


class UserManySchema(UserIdSchema):
    """
    Schema for retrieving details of multiple users
    """

    user_list = fields.Nested(
        UserSchema,
        many=True,
        required=False,
        description="List of users' details",
    )
