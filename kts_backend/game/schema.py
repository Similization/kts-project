from marshmallow import Schema, fields


class PlayerRequestSchema(Schema):
    vk_id = fields.Int(required=True)


class PlayerResponseSchema(PlayerRequestSchema):
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)


class PlayerListSchema(Schema):
    players = fields.Nested(PlayerRequestSchema, many=True)


class GameScoreSchema(Schema):
    id = fields.Int(required=True)
    player = fields.Nested(PlayerResponseSchema, many=False, required=True)
    game = fields.Nested("GameSchema", many=False, required=True)
    score = fields.Int(required=False)


class GameSchema(Schema):
    game_id = fields.Int(required=False)
    created_at = fields.DateTime(required=False)
    chat_id = fields.Int(required=True)


class GamePlayersSchema(GameSchema):
    players = fields.Nested(PlayerResponseSchema, many=True, required=True)
