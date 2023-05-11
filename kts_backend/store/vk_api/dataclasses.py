from dataclasses import dataclass


@dataclass(slots=True)
class UpdateObject:
    """Represents an object in an update."""

    id: int
    user_id: int
    message_id: int
    peer_id: str
    body: str


@dataclass(slots=True)
class Update:
    """Represents an update."""

    type: str
    update_object: UpdateObject


@dataclass(slots=True)
class Message:
    """Represents a message."""

    user_id: int
    peer_id: str
    text: str
