from kts_backend.game.view import (
    GamePlayerListByChatIdView,
    GameCreateView,
    GameLastView,

    PlayerInGameView,

)
from kts_backend.web.app import Application


def setup_routes(app: Application):
    # app.router.add_view(path="/game.players_in_chat", handler=GamePlayerListByChatIdView)
    # app.router.add_view(path="/game.create", handler=GameCreateView)
    # app.router.add_view(path="/game.last", handler=GameLastView)
    #
    # app.router.add_view(path="/player.set_in_game", handler=PlayerInGameView)
    # app.router.add_view(path="/player.set_is_winner", handler=GameLastView)
    # app.router.add_view(path="/player.add_score", handler=GameLastView)
    pass
