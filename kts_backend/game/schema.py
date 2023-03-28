from marshmallow import Schema, fields


class PlayerByIdSchema(Schema):
    player_id = fields.Int(required=True)


class PlayerByUserIdSchema(Schema):
    user_id = fields.Int(required=True)


class PlayerByIdAndInGameSchema(PlayerByIdSchema):
    in_game = fields.Boolean(required=True)


class PlayerByIdAndIsWinnerSchema(PlayerByIdSchema):
    is_winner = fields.Boolean(required=True)


class PlayerSchema(Schema):
    player_id = fields.Int(required=False)
    user_id = fields.Int(required=False)
    score = fields.Str(required=False)
    in_game = fields.Boolean(required=False)
    is_winner = fields.Boolean(required=False)


class PlayerListSchema(Schema):
    players = fields.Nested(PlayerSchema, many=True)


class GameByIdSchema(Schema):
    game_id = fields.Int(required=True)


class GameByChatIdSchema(Schema):
    chat_id = fields.Int(required=True)


class GameByChatIdAndPlayerListSchema(GameByIdSchema):
    players = fields.Nested(PlayerListSchema, many=True, required=False)


class GameSchema(Schema):
    game_id = fields.Int(required=False)
    chat_id = fields.Int(required=False)
    game_data_id = fields.Int(required=False)
    created_at = fields.DateTime(required=False)
    finished_at = fields.DateTime(required=False)
    required_player_count = fields.Int(required=False)


class GameWithPlayersSchema(GameSchema):
    players = fields.Nested(PlayerListSchema, many=True, required=False)


class GameDataByIdSchema(Schema):
    game_data_id = fields.Int(required=True)


class GameDataSchema(Schema):
    game_data_id = fields.Int(required=False)
    question = fields.Str(required=True)
    answer = fields.Str(required=True)


class GameDataListSchema(Schema):
    game_data_list = fields.Nested(GameDataSchema, many=True, required=False)
