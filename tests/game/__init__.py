from kts_backend.game.dataclasses import Game
from kts_backend.user.dataclasses import User


def user2dict(user: User):
    return {
        "id": int(user.id),
        "vk_id": int(user.vk_id),
        "name": str(user.name),
        "last_name": str(user.last_name),
        "username": str(user.last_name),
    }


# def game2dict(game: Game):
#     return {
#         "game_id": int(game.id),
#         "created_at": str(game.created_at),
#         "chat_id": int(game.chat_id),
#         "players": [player2dict(player) for player in game.player_list],
#     }
