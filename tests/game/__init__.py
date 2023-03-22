from kts_backend.game.model import GameDC, PlayerDC


def player2dict(player: PlayerDC):
    return {
        "vk_id": int(player.vk_id),
        "name": str(player.name),
        "last_name": str(player.last_name)
    }


def game2dict(game: GameDC):
    return {
        "game_id": int(game.game_id),
        "created_at": str(game.created_at),
        "chat_id": int(game.chat_id),
        "players": [player2dict(player) for player in game.players],
    }
