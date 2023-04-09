import typing
from logging import getLogger

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class BaseAccessor:
    """
    Base class for implementing database accessors.

    Subclasses must implement the `connect` and `disconnect` methods to establish and close connections to the database,
    respectively.

    :param app: The aiohttp web application instance.
    :type app: Application
    """

    def __init__(self, app: "Application", *args: tuple, **kwargs: dict):
        """
        Initialize a new instance of the BaseAccessor class.

        :param app: The aiohttp web application instance.
        :type app: Application
        :param args: Additional positional arguments to be passed to the `connect` and `disconnect` methods.
        :type args: tuple
        :param kwargs: Additional keyword arguments to be passed to the `connect` and `disconnect` methods.
        :type kwargs: dict
        """
        self.app = app
        self.logger = getLogger("accessor")

        # Register to connect and disconnect methods to be called on application start-up and shutdown, respectively.
        app.on_startup.append(self.connect)
        app.on_cleanup.append(self.disconnect)

    async def connect(self, app: "Application") -> None:
        """
        Method to establish a connection to the database.

        This method should be implemented by subclasses.

        :param app: The aiohttp web application instance.
        :type app: Application
        """
        return

    async def disconnect(self, app: "Application") -> None:
        """
        Method to close the connection to the database.

        This method should be implemented by subclasses.

        :param app: The aiohttp web application instance.
        :type app: Application
        """
        return
