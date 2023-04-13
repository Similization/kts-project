from kts_backend.web.app import Application


def setup_routes(app: Application) -> None:
    """
    Set up routes for user-related views in the web application.

    This function adds views for various user-related operations such as getting, creating, updating, and deleting
    users to the application's router. The views are defined in the `kts_backend.user.view` module and are added to the
    router with their corresponding URL paths.

    Parameters:
        app (Application): The web application instance to which the routes will be added.

    Returns:
        None
    """

    from kts_backend.user.view import (
        UserGetView,
        UserGetManyView,
        UserCreateView,
        UserCreateManyView,
        UserUpdateView,
        UserUpdateManyView,
        UserDeleteView,
        UserDeleteManyView,
    )

    app.router.add_view(path="/user.get", handler=UserGetView)
    app.router.add_view(path="/user.create", handler=UserCreateView)
    app.router.add_view(path="/user.update", handler=UserUpdateView)
    app.router.add_view(path="/user.delete", handler=UserDeleteView)

    app.router.add_view(path="/user.get_many", handler=UserGetManyView)
    app.router.add_view(path="/user.create_many", handler=UserCreateManyView)
    app.router.add_view(path="/user.update_many", handler=UserUpdateManyView)
    app.router.add_view(path="/user.delete_many", handler=UserDeleteManyView)
