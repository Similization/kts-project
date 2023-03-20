from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=True)
    vk_id = fields.Int(required=False)
    name = fields.Str(required=False)
    username = fields.Str(required=False)

