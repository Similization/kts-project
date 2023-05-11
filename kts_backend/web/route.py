from aiohttp.web_app import Application


def setup_routes(app: Application) -> None:
    """
    Set up routes for the application.

    This function sets up routes for different modules or components of the application by calling the
    `setup_routes` function from respective modules. The routes are registered with the provided `app` object,
    which is an instance of the `Application` class from aiohttp web framework.

    Args:
        app (Application): The aiohttp web application object.

    Returns:
        None
    """

    from kts_backend.user.route import setup_routes as user_setup_routes
    from kts_backend.game.route import setup_routes as game_setup_routes
    from kts_backend.admin.route import setup_routes as admin_setup_routes

    # Call the setup_routes functions from respective modules to register routes with the app
    user_setup_routes(app=app)
    game_setup_routes(app=app)
    admin_setup_routes(app=app)
