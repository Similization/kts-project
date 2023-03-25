from marshmallow import Schema, fields


class UserIdSchema(Schema):
    user_id = fields.Int(required=True)


class UserCreateSchema(Schema):
    vk_id = fields.Int(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)


class UserUpdateSchema(Schema):
    user_id = fields.Int(required=True)
    vk_id = fields.Int(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)


class UserSchema(UserIdSchema):
    vk_id = fields.Int(required=False)
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    username = fields.Str(required=False)


class UserManySchema(UserIdSchema):
    users = fields.Nested(UserSchema, many=True, required=False)
