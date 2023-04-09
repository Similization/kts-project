from sqlalchemy import Integer, VARCHAR, Column

from kts_backend.store.database.sqlalchemy_base import db


class UserModel(db):
    """
    SQLAlchemy model representing a user in the database.

    Attributes:
        id (int): Primary key ID for the user.
        vk_id (int): The VK ID of the user.
        name (str): The first name of the user.
        last_name (str): The last name of the user.
        username (str): The username of the user.
    """

    __tablename__ = "user"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="The unique identifier for the user.",
    )
    vk_id = Column(
        Integer,
        unique=True,
        nullable=False,
        doc="The ID of the user's VK account.",
    )
    name = Column(VARCHAR(45), nullable=False, doc="The user's first name.")
    last_name = Column(VARCHAR(45), nullable=False, doc="The user's last name.")
    username = Column(VARCHAR(45), nullable=False, doc="The user's username.")
