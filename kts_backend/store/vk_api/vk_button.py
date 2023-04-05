from dataclasses import dataclass
from typing import Literal


@dataclass
class VkButton:
    """
    A class representing a button used in VK messages.

    :param payload: Additional data to be passed with the button. Defaults to None.
    :type payload: dict, optional
    :param type_: The type of the button. Must be one of "text", "open link", or "callback". Defaults to "text".
    :type type_: Literal["text", "open link", "callback"], optional
    :param color: The color of the button. Must be one of "primary", "secondary", "negative", or "positive". Defaults to "secondary".
    :type color: Literal["primary", "secondary", "negative", "positive"], optional
    :param label: The text displayed on the button. Defaults to None.
    :type label: str, optional
    :param hash_: A unique identifier for the button. Defaults to None.
    :type hash_: str, optional
    """
    def __init__(
        self,
        payload: dict | None = None,
        type_: Literal["text", "open link", "callback"] = "text",
        color: Literal[
            "primary", "secondary", "negative", "positive"
        ] = "secondary",
        label: str | None = None,
        hash_: str | None = None,
    ):
        """
        Initialize VkButton object, using:
        :param payload: str | None
        :param type_: Literal["text", "open link", "callback"]
        :param color: Literal["primary", "secondary", "negative", "positive"]
        :param label: str | None
        :param hash_: str | None
        """
        self.type: Literal["text", "open link", "callback"] = type_
        self.color: Literal[
            "primary", "secondary", "negative", "positive"
        ] = color
        self.label: str | None = label
        self.payload: dict = payload
        self.hash: str | None = hash_

    def convert_to_dict(self) -> dict:
        """
        Convert the button to a dictionary that can be used in a VK message.

        :return: A dictionary representing the button.
        :rtype: dict
        """
        button_to_dict = {"action": {}}
        for k, v in self.__dict__.items():
            if v is None:
                continue
            if k == "color":
                button_to_dict[k] = v
            else:
                button_to_dict["action"][k] = v
        return button_to_dict


CALLBACK_PAYLOAD = ("{finish}",)

CREATE_GAME_BUTTON = VkButton(
    type_="callback",
    label="Создать игру",
    color="secondary",
)
JOIN_GAME_BUTTON = VkButton(
    type_="callback",
    label="Присоединиться",
    color="positive",
)
FINISH_GAME_BUTTON = VkButton(
    label="Завершить игру",
    color="negative"
)
