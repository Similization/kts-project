import typing

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


def setup_routes(app: "Application"):
    """
    Setup routes /admin route.<method> for application
    :param app: Application
    :return: None
    """
    from kts_backend.admin.view import AdminLoginView
    from kts_backend.admin.view import AdminCurrentView

    app.router.add_view("/admin.login", AdminLoginView)
    app.router.add_view("/admin.current", AdminCurrentView)
