import random
import typing
from typing import Optional, List

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
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.poller: Poller | None = None
        self.worker: Worker | None = None
        self.ts: int | None = None

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        try:
            await self._get_long_poll_service()
        except Exception as e:
            self.logger.error("Exception", exc_info=e)
        self.poller = Poller(store=app.store)
        self.worker = Worker(store=app.store, concurrent_workers=4)

        self.logger.info("start polling")
        await self.poller.start()
        self.logger.info("start workers")
        await self.worker.start()

    async def disconnect(self, app: "Application"):
        if self.poller:
            await self.poller.stop()
        if self.session:
            await self.session.close()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
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
            data = (await resp.json())["response"]
            self.logger.info(data)
            self.key = data["key"]
            self.server = data["server"]
            self.ts = data["ts"]
            self.logger.info(self.server)

    async def poll(self) -> List[Update]:
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
            data = await resp.json()
            self.logger.info(data)
            self.ts = data["ts"]
            raw_updates = data.get("updates", [])
            updates = []
            for update in raw_updates:
                updates.append(
                    Update(
                        type=update["type"],
                        object=UpdateObject(
                            id=update["object"]["message"]["id"],
                            user_id=update["object"]["message"]["from_id"],
                            peer_id=str(update["object"]["message"]["peer_id"]),
                            body=update["object"]["message"]["text"],
                        ),
                    )
                )
            return updates

    # get user from chat
    async def get_chat_users(self, chat_id: str):
        async with self.session.get(
            self._build_query(
                host=API_PATH,
                method="messages.getConversationMembers",
                params={
                    "peer_id": chat_id,
                    "access_token": self.app.config.bot.token,
                },
            )
        ) as resp:
            data = (await resp.json())["response"]
            profiles = data["profiles"]
            return profiles

    async def get_active_chat_id_list(self) -> List[dict]:
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
            data = (await resp.json())["response"]
            chat_list: List[dict] = data["items"]
            return [
                chat["conversation"]["peer"]["id"]
                for chat in chat_list
                if chat["conversation"]["peer"]["type"] == "chat"
                and chat["conversation"]["can_write"]["allowed"]
            ]

    # send message to chat or to user
    async def send_message(
        self, message: Message, keyboard: Optional[dict] = None
    ) -> None:
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
            data = await resp.json()
            self.logger.info(data)
