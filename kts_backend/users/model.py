from dataclasses import dataclass

from sqlalchemy import Integer, VARCHAR, Column

from kts_backend.store.database.sqlalchemy_base import db


@dataclass
class User:
    vk_id: int
    name: str
    last_name: str


class UserModel(db):
    __tablename__ = "user"

    vk_id = Column(Integer, primary_key=True, autoincrement=True)
    # username = Column(VARCHAR(45), nullable=False)
    name = Column(VARCHAR(45), nullable=False)
    last_name = Column(VARCHAR(45), nullable=False)
