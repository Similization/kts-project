from marshmallow import Schema, fields


class GameDataByIdSchema(Schema):
    id = fields.Int(required=True)


class GameDataSchema(Schema):
    id = fields.Int(required=False)
    question = fields.Str(required=True)
    answer = fields.Str(required=True)


class GameDataListSchema(Schema):
    game_data_list = fields.Nested(GameDataSchema, many=True, required=False)
