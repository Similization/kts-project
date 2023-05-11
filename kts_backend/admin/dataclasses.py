from dataclasses import dataclass
from hashlib import sha256
from typing import Optional


@dataclass(slots=True)
class Admin:
    """
    A class representing an admin user.

    Attributes:
        id (int): The unique identifier for the admin.
        email (str): The email address associated with the admin.
        user_id (int | None): The ID of the User associated with the admin, or None if not applicable.
        password (str | None): The hashed password for the admin, or None if not applicable.

    Methods:
        is_password_valid(password: str) -> bool:
            Checks if the given password is correct for the admin.
        from_session(session: dict | None) -> Optional[Admin]:
            Returns an Admin object from a given session.
    """

    id: int
    email: str
    user_id: int | None = None
    password: str | None = None

    def is_password_valid(self, password: str) -> bool:
        """
        Checks if the password is correct.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: dict | None) -> Optional["Admin"]:
        """
        Get Admin object from session.

        Args:
            session (dict | None): The session to get the Admin object from.

        Returns:
            Optional["Admin"]: The Admin object, or None if the session is None.
        """
        if session is None:
            return None

        admin_data = session["admin"]
        return cls(id=admin_data["id"], email=admin_data["email"])
