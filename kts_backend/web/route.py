from aiohttp.web_app import Application


def setup_routes(app: Application):
    from kts_backend.user.route import setup_routes as user_setup_routes
    from kts_backend.game.route import setup_routes as game_setup_routes
    from kts_backend.admin.route import setup_routes as admin_setup_routes

    user_setup_routes(app=app)
    game_setup_routes(app=app)
    admin_setup_routes(app=app)
