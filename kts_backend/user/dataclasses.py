from dataclasses import dataclass


@dataclass
class User:
    id: int
    vk_id: int
    name: str
    last_name: str
    username: str
