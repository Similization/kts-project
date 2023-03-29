from dataclasses import dataclass
from typing import Optional, Literal


@dataclass(slots=True)
class VkButton:
    def __init__(
        self,
        payload: Optional[str] = None,
        type_: Literal["text", "open link", "callback"] = "text",
        color: Literal[
            "primary", "secondary", "negative", "positive"
        ] = "secondary",
        label: Optional[str] = None,
        hash_: Optional[str] = None,
    ):
        self.type: str = type_
        self.color: Optional[str] = color
        self.label: Optional[str] = label
        self.payload: str = payload
        self.hash: Optional[str] = hash_

    def convert_to_dict(self):
        button_to_dict = {"action": {}}
        for k, v in self.__dict__.items():
            if v is None:
                continue
            if k == "color":
                button_to_dict[k] = v
            else:
                button_to_dict["action"][k] = v
        return button_to_dict


CREATE_GAME_BUTTON = VkButton(
    type_="callback", label="Создать игру", color="secondary"
)
JOIN_GAME_BUTTON = VkButton(
    type_="callback", label="Присоединиться", color="positive"
)
FINISH_GAME_BUTTON = VkButton(
    type_="callback", label="Завершить игру", color="negative"
)
