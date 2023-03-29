import json
from copy import deepcopy
from dataclasses import dataclass
from typing import List

from kts_backend.store.vk_api.vk_button import (
    VkButton,
    CREATE_GAME_BUTTON,
    JOIN_GAME_BUTTON,
    FINISH_GAME_BUTTON,
)


@dataclass(slots=True)
class VkKeyboard:
    def __init__(
        self,
        buttons: List[List[VkButton]],
        one_time: bool = False,
        inline: bool = False,
    ):
        self.one_time: bool = one_time
        self.inline: bool = inline
        self.buttons: List[List[VkButton]] = buttons

    def convert_to_string(self):
        keyboard: dict = deepcopy(self.__dict__)
        keyboard_buttons: List = []
        for button_list in self.buttons[:]:
            new_list = []
            for button in button_list:
                new_list.append(button.convert_to_dict())
            keyboard_buttons.append(new_list)
        keyboard["buttons"] = keyboard_buttons

        keyboard: bytes = json.dumps(obj=keyboard, ensure_ascii=False).encode(
            "utf-8"
        )
        keyboard: str = str(keyboard.decode("utf-8"))

        return keyboard


KEYBOARD_CREATE = VkKeyboard(
    one_time=True, inline=False, buttons=[[CREATE_GAME_BUTTON]]
)
KEYBOARD_JOIN = VkKeyboard(
    one_time=True, inline=False, buttons=[[JOIN_GAME_BUTTON]]
)
KEYBOARD_FINISH = VkKeyboard(
    one_time=True, inline=False, buttons=[[FINISH_GAME_BUTTON]]
)
