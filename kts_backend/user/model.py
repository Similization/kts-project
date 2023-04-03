from sqlalchemy import Integer, VARCHAR, Column

from kts_backend.store.database.sqlalchemy_base import db


class UserModel(db):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    name = Column(VARCHAR(45), nullable=False)
    last_name = Column(VARCHAR(45), nullable=False)
    username = Column(VARCHAR(45), nullable=False)
