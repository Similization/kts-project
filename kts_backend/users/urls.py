from aiohttp.web_app import Application
from aiohttp_cors import CorsConfig

__all__ = ("register_urls",)


def register_urls(app: Application, cors: CorsConfig):
    # hello_resource = cors.add(app.router.add_resource("/hello"))
    # cors.add(hello_resource.add_route("POST", handler_post))
    # cors.add(hello_resource.add_route("PUT", handler_put))
    pass
