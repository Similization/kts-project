from dataclasses import dataclass
from hashlib import sha256
from typing import Optional


@dataclass(slots=True)
class Admin:
    id: int
    email: str
    user_id: int | None = None
    password: str | None = None

    def is_password_valid(self, password: str) -> bool:
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: dict | None) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])
