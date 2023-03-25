from kts_backend.user.view import (
    UserGetView,
    UserGetManyView,
    UserCreateView,
    UserCreateManyView,
    UserUpdateView,
    UserUpdateManyView,
    UserDeleteView,
    UserDeleteManyView
)
from kts_backend.web.app import Application


def setup_routes(app: Application):
    app.router.add_view(path="/user.get", handler=UserGetView)
    app.router.add_view(path="/user.create", handler=UserCreateView)
    app.router.add_view(path="/user.update", handler=UserUpdateView)
    app.router.add_view(path="/user.delete", handler=UserDeleteView)

    app.router.add_view(path="/user.get_many", handler=UserGetManyView)
    app.router.add_view(path="/user.create_many", handler=UserCreateManyView)
    app.router.add_view(path="/user.update_many", handler=UserUpdateManyView)
    app.router.add_view(path="/user.delete_many", handler=UserDeleteManyView)
