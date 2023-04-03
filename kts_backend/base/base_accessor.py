import typing
from logging import getLogger

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class BaseAccessor:
    def __init__(self, app: "Application", *args: tuple, **kwargs: dict):
        """
        Initialize BaseAccessor object, using app
        :param app: Application
        :param args: tuple
        :param kwargs: dict
        """
        self.app = app
        self.logger = getLogger("accessor")
        app.on_startup.append(self.connect)
        app.on_cleanup.append(self.disconnect)

    async def connect(self, app: "Application"):
        """
        Connection method for overwriting
        :param app: Application
        :return: None
        """
        return

    async def disconnect(self, app: "Application"):
        """
        Disable connection method for overwriting
        :param app: Application
        :return: None
        """
        return
