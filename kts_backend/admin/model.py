from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from sqlalchemy import Integer, VARCHAR, Column, ForeignKey

from kts_backend.store.database.sqlalchemy_base import db


@dataclass
class Admin:
    admin_id: int
    email: str
    user_id: Optional[int] = None
    password: Optional[str] = None

    def is_password_valid(self, password: str) -> bool:
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(
            admin_id=session["admin"]["id"], email=session["admin"]["email"]
        )


class AdminModel(db):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True
    )
    email = Column(VARCHAR(60), nullable=False, unique=True)
    password = Column(VARCHAR(75), nullable=False)
