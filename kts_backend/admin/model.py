from sqlalchemy import Integer, VARCHAR, Column, ForeignKey

from kts_backend.store.database.sqlalchemy_base import db


class AdminModel(db):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    email = Column(VARCHAR(60), nullable=False, unique=True)
    password = Column(VARCHAR(75), nullable=False)
