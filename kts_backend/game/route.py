from kts_backend.game.view import (
    GamePlayerListView,
    GameCreateView,
    GameLastView
)
from kts_backend.web.app import Application


def setup_routes(app: Application):
    app.router.add_view("/game.players_in_chat", GamePlayerListView)
    app.router.add_view("/game.create", GameCreateView)
    app.router.add_view("/game.last", GameLastView)

