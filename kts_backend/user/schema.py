from marshmallow import Schema, fields


class UserIdSchema(Schema):
    user_id = fields.Int(required=True)


class UserIdListSchema(Schema):
    user_id_list = fields.List(cls_or_instance=fields.Int, required=True)


class UserCreateSchema(Schema):
    vk_id = fields.Int(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)


class UserFullCreateSchema(Schema):
    user = fields.Nested(UserCreateSchema, many=False, required=True)


class UserFullListCreateSchema(Schema):
    user_list = fields.Nested(UserCreateSchema, many=True, required=True)


class UserUpdateSchema(Schema):
    user_id = fields.Int(required=True)
    vk_id = fields.Int(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)


class UserFullUpdateSchema(Schema):
    user = fields.Nested(UserUpdateSchema, many=False, required=True)


class UserFullListUpdateSchema(Schema):
    user_list = fields.Nested(UserUpdateSchema, many=True, required=True)


class UserSchema(UserIdSchema):
    vk_id = fields.Int(required=False)
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    username = fields.Str(required=False)


class UserManySchema(UserIdSchema):
    user_list = fields.Nested(UserSchema, many=True, required=False)
