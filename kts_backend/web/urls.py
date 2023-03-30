from aiohttp.web_app import Application
from aiohttp_cors import CorsConfig

__all__ = ("register_urls",)


def register_urls(app: Application, cors: CorsConfig) -> None:
    """
    Register urls for application
    :param app: Application
    :param cors: CorsConfig
    :return: None
    """
    import kts_backend.user.urls
    import kts_backend.game.urls

    kts_backend.user.urls.register_urls(app, cors)
    kts_backend.game.urls.register_urls(app, cors)
