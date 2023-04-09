from sqlalchemy import Integer, VARCHAR, Column, ForeignKey

from kts_backend.store.database.sqlalchemy_base import db


class AdminModel(db):
    """
    A SQLAlchemy model representing an admin in the database.

    Attributes:
        id (int): The primary key ID of the admin.
        user_id (int): The ID of the associated user, if any.
        email (str): The email address of the admin.
        password (str): The hashed password of the admin.
    """

    __tablename__ = "admin"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="The unique ID of the admin.",
    )
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        doc="The ID of the user associated with the admin.",
    )
    email = Column(
        VARCHAR(60),
        nullable=False,
        unique=True,
        doc="The email address of the admin.",
    )
    password = Column(
        VARCHAR(75),
        nullable=False,
        doc="The password of the admin, hashed for security.",
    )
