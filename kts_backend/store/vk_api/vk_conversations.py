from dataclasses import dataclass
from typing import Literal


@dataclass(slots=True)
class VkConversation:
    def __init__(
        self,
        group_id: int,
        offset: int = 0,
        count: int = 30,
        filter_: Literal["all", "important", "unanswered", "unread"] = "all",
        fields: str = "",
    ):
        self.offset: int = offset
        self.count: int = count
        self.filter: str = filter_
        # self.extended: bool
        # self.start_message_id: int
        self.fields: str = fields
        self.group_id: int = group_id
