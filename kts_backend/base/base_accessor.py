import typing
from logging import getLogger

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class BaseAccessor:
    """
    A base class for creating database accessors.

    Attributes:
        app (Application): The application object.
        logger (Logger): The logger object for logging messages.

    Methods:
        __init__(self, app: Application, *args: tuple, **kwargs: dict) -> None:
            Initializes the BaseAccessor object and registers connect and disconnect methods
            to be called on application start-up and shutdown, respectively.

        async connect(self, app: Application) -> None:
            This method is called on application start-up and should be overridden by child classes
            to establish a connection to the database.

        async disconnect(self, app: Application) -> None:
            This method is called on application shutdown and should be overridden by child classes
            to disconnect from the database.

    """

    def __init__(self, app: "Application", *args: tuple, **kwargs: dict):
        """
        Initializes the BaseAccessor object and registers connect and disconnect methods
        to be called on application start-up and shutdown, respectively.

        Args:
            app (Application): The application object.
            *args: Any extra arguments to be passed to child classes.
            **kwargs: Any extra keyword arguments to be passed to child classes.

        Returns:
            None
        """
        self.app = app
        self.logger = getLogger("accessor")

        # Register to connect and disconnect methods to be called on application start-up and shutdown, respectively.
        app.on_startup.append(self.connect)
        app.on_cleanup.append(self.disconnect)

    async def connect(self, app: "Application") -> None:
        """
        This method is called on application start-up and should be overridden by child classes
        to establish a connection to the database.

        Args:
            app (Application): The application object.

        Returns:
            None
        """
        return

    async def disconnect(self, app: "Application") -> None:
        """
        This method is called on application shutdown and should be overridden by child classes
        to disconnect from the database.

        Args:
            app (Application): The application object.

        Returns:
            None
        """
        return
