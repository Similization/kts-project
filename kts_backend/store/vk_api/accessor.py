import logging
import random
import typing
from typing import List

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from kts_backend.base.base_accessor import BaseAccessor
from kts_backend.store.vk_api.dataclasses import Message, Update, UpdateObject
from kts_backend.store.vk_api.poller import Poller
from kts_backend.store.vk_api.worker import Worker

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application

API_PATH = "https://api.vk.com/method/"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        """
        :param app:
        :param args:
        :param kwargs:
        """
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.poller: Poller | None = None
        self.worker: Worker | None = None
        self.ts: int | None = None
        self.logger = logging.getLogger(__name__)

    async def connect(self, app: "Application"):
        """
        :param app:
        :return:
        """
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        try:
            await self._get_long_poll_service()
        except Exception as e:
            self.logger.error("Exception", exc_info=e)
        self.poller = Poller(store=app.store)
        self.worker = Worker(store=app.store, concurrent_workers=4)

        self.logger.warning(msg="start polling")
        await self.poller.start()
        self.logger.warning(msg="start workers")
        await self.worker.start()

    async def disconnect(self, app: "Application") -> None:
        """
        :param app:Application
        :return: None
        """
        if self.worker:
            await self.worker.stop()
        if self.poller:
            await self.poller.stop()
        if self.session:
            await self.session.close()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        """
        :param host:
        :param method:
        :param params:
        :return:
        """
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        param_list: List[str] = []
        for k, v in params.items():
            param_list.append(f"{k}={v}")
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        """
        :return:
        """
        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="groups.getLongPollServer",
                params={
                    "group_id": self.app.config.bot.group_id,
                    "access_token": self.app.config.bot.token,
                },
            )
        ) as resp:
            try:
                data = (await resp.json())["response"]
                self.logger.info(data)
                self.key = data["key"]
                self.server = data["server"]
                self.ts = data["ts"]
                self.logger.info(msg=self.server)
            except KeyError as e:
                self.logger.error(e)

    async def poll(self) -> List[Update]:
        """
        :return:
        """
        async with self.session.get(
            self._build_query(
                host=self.server,
                method="",
                params={
                    "act": "a_check",
                    "key": self.key,
                    "ts": self.ts,
                    "wait": 30,
                },
            )
        ) as resp:
            try:
                data = await resp.json()
                self.logger.info(data)
                self.ts = data["ts"]
                raw_updates = data.get("updates", [])
                return [
                    Update(
                        type=update["type"],
                        update_object=UpdateObject(
                            id=update["object"]["message"]["id"],
                            user_id=update["object"]["message"]["from_id"],
                            message_id=update["object"]["message"][
                                "conversation_message_id"
                            ],
                            peer_id=str(update["object"]["message"]["peer_id"]),
                            body=update["object"]["message"]["text"],
                        ),
                    )
                    for update in raw_updates
                ]
            except KeyError as e:
                self.logger.error(e)

    async def get_chat_users(self, chat_id: str):
        """
        :param chat_id:
        :return:
        """
        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="messages.getConversationMembers",
                params={
                    "access_token": self.app.config.bot.token,
                    "peer_id": chat_id,
                    "group_id": self.app.config.bot.group_id,
                },
            )
        ) as resp:
            try:
                data = await resp.json()
                self.logger.warning(msg=data)
                profiles = data["response"]["profiles"]
                return profiles
            except KeyError as e:
                self.logger.error(e)

    async def get_history(self, chat_id: str, count: int = 10):
        """
        :param count:
        :param chat_id:
        :return:
        """
        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="messages.getHistory",
                params={
                    "access_token": self.app.config.bot.token,
                    "count": count,
                    "peer_id": chat_id,
                    "group_id": self.app.config.bot.group_id,
                },
            )
        ) as resp:
            try:
                data = (await resp.json())["response"]
                self.logger.info(msg=data)
                items = data["items"]
                for item in items:
                    if item["from_id"] == -self.app.config.bot.group_id:
                        return int(item["conversation_message_id"])
            except KeyError as e:
                self.logger.error(e)
            return None

    async def delete_message_from_chat(
        self, message_ids: str, chat_id: str, delete_for_all: bool = True
    ):
        """
        :param delete_for_all:
        :param message_ids:
        :param chat_id:
        :return:
        """
        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="messages.delete",
                params={
                    "cmids": message_ids,
                    "access_token": self.app.config.bot.token,
                    "delete_for_all": int(delete_for_all),
                    "peer_id": int(chat_id),
                    "group_id": self.app.config.bot.group_id,
                },
            )
        ) as resp:
            try:
                data = await resp.json()
                self.logger.warning(msg=data)
            except KeyError as e:
                self.logger.error(e)

    async def get_active_chat_id_list(self) -> List[dict]:
        """
        :return:
        """
        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="messages.getConversations",
                params={
                    "group_id": self.app.config.bot.group_id,
                    "access_token": self.app.config.bot.token,
                },
            )
        ) as resp:
            try:
                data = (await resp.json())["response"]
                chat_list: List[dict] = data["items"]
                self.logger.info(msg=data)
                return [
                    chat["conversation"]["peer"]["id"]
                    for chat in chat_list
                    if chat["conversation"]["peer"]["type"] == "chat"
                    and chat["conversation"]["can_write"]["allowed"]
                ]
            except KeyError as e:
                self.logger.error(e)

    async def send_message(
        self, message: Message, keyboard: dict | None = None
    ) -> None:
        """
        :param message:
        :param keyboard:
        :return:
        """
        params = {
            "random_id": random.randint(1, 2**32),
            "message": message.text,
            "access_token": self.app.config.bot.token,
        }
        if keyboard:
            params["keyboard"] = keyboard

        if int(message.peer_id) > 2000000000:
            params["chat_id"] = int(message.peer_id) - 2000000000
        else:
            params["user_id"] = message.peer_id
        async with self.session.get(
            self._build_query(
                API_PATH,
                "messages.send",
                params=params,
            )
        ) as resp:
            try:
                data = (await resp.json())["response"]
                self.logger.info(msg=data)
            except KeyError as e:
                self.logger.error(e)

    async def edit_message(
        self, message_id: int, message: Message, keyboard: str | None = None
    ) -> None:
        """
        Edit message data
        :param keyboard:
        :param message_id: int
        :param message: str
        :return: None
        """
        params = {
            "group_id": self.app.config.bot.group_id,
            "access_token": self.app.config.bot.token,
            "peer_id": int(message.peer_id),
            "conversation_message_id": str(message_id),
            "message": message.text,
        }
        if keyboard:
            params["keyboard"] = keyboard

        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="messages.edit",
                params=params,
            )
        ) as resp:
            try:
                data = await resp.json()
                self.logger.warning(msg=data)
            except KeyError as e:
                self.logger.error(e)

    async def pin_message(
        self, message_id: int, peer_id: int, keyboard: str | None = None
    ) -> None:
        params = {
            "group_id": self.app.config.bot.group_id,
            "access_token": self.app.config.bot.token,
            "peer_id": peer_id,
            "conversation_message_id": message_id,
        }
        if keyboard:
            params["keyboard"] = keyboard

        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="messages.pin",
                params=params,
            )
        ) as resp:
            try:
                data = await resp.json()
                self.logger.info(msg=data)
            except KeyError as e:
                self.logger.error(e)
