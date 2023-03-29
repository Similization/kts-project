from kts_backend.web.app import Application


def setup_routes(app: Application) -> None:
    """
    Setup routes /game_data route.<method> for application
    :param app: Application
    :return: None
    """
    from kts_backend.game.view import GameDataAddView
    from kts_backend.game.view import GameDataListGetView

    app.router.add_view(path="/game_data.add", handler=GameDataAddView)
    app.router.add_view(path="/game_data.get", handler=GameDataListGetView)
