from dataclasses import dataclass


@dataclass(slots=True)
class UpdateObject:
    id: int
    user_id: int
    peer_id: str
    body: str


@dataclass(slots=True)
class Update:
    type: str
    object: UpdateObject


@dataclass(slots=True)
class Message:
    user_id: int
    peer_id: str
    text: str
