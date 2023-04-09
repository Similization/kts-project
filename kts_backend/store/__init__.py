import typing

from kts_backend.store.database.database import Database

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        """
        Initialize Store object
        :param app: Application
        """
        from kts_backend.store.admin.accessor import AdminAccessor
        from kts_backend.store.bot.manager import BotManager
        from kts_backend.store.game.accessor import GameAccessor
        from kts_backend.store.user.accessor import UserAccessor
        from kts_backend.store.vk_api.accessor import VkApiAccessor

        self.admin = AdminAccessor(app=app)
        self.bots_manager = BotManager(app=app)
        self.game = GameAccessor(app=app)
        self.user = UserAccessor(app=app)
        self.vk_api = VkApiAccessor(app=app)


def setup_store(app: "Application") -> None:
    """
    Setup application store
    :param app: Application
    :return: None
    """
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
