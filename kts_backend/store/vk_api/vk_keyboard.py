import json
from typing import List, Dict
from dataclasses import dataclass

from kts_backend.store.vk_api.vk_button import (
    VkButton,
    CREATE_GAME_BUTTON,
    JOIN_GAME_BUTTON,
    FINISH_GAME_BUTTON,
)


@dataclass
class VkKeyboard:
    def __init__(
        self,
        buttons: List[List[VkButton]],
        one_time: bool = False,
        inline: bool = False,
    ) -> None:
        """
        Initialize VkKeyboard object.

        :param buttons: A list of button rows, where each row is a list of VkButton objects.
        :param one_time: A flag to indicate whether the keyboard should be hidden after use.
        :param inline: A flag to indicate whether the keyboard should be displayed inline with the message.
        """
        self.one_time: bool = one_time
        self.inline: bool = inline
        self.buttons: List[List[VkButton]] = buttons

    def convert_to_string(self) -> str:
        """
        Convert VkKeyboard object to a JSON string.

        :return: A JSON string representing the VkKeyboard object.
        """
        buttons = [
            [button.convert_to_dict() for button in row] for row in self.buttons
        ]
        keyboard = {
            "buttons": buttons,
            "one_time": self.one_time,
            "inline": self.inline,
        }
        return json.dumps(keyboard, ensure_ascii=False)


VK_KEYBOARDS: Dict[str, str] = {
    "KEYBOARD_CREATE": VkKeyboard(
        one_time=True, inline=False, buttons=[[CREATE_GAME_BUTTON]]
    ).convert_to_string(),
    "KEYBOARD_JOIN": VkKeyboard(
        one_time=True, inline=False, buttons=[[JOIN_GAME_BUTTON]]
    ).convert_to_string(),
    "KEYBOARD_FINISH": VkKeyboard(
        one_time=True, inline=False, buttons=[[FINISH_GAME_BUTTON]]
    ).convert_to_string(),
}
