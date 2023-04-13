from kts_backend.web.app import Application


def setup_routes(app: Application) -> None:
    """
    Set up the routes for the application.

    Args:
        app (Application): The application instance to set up the routes for.

    Returns:
        None
    """
    from kts_backend.game.view import GameDataAddView
    from kts_backend.game.view import GameDataListGetView

    app.router.add_view(path="/game_data.post", handler=GameDataAddView)
    app.router.add_view(path="/game_data.get", handler=GameDataListGetView)
