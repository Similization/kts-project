from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        vk_id (int): The user's VKontakte ID.
        name (str): The user's first name.
        last_name (str): The user's last name.
        username (str): The user's username.
    """

    id: int
    vk_id: int
    name: str
    last_name: str
    username: str
