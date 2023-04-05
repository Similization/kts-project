from dataclasses import dataclass
from hashlib import sha256
from typing import Optional


@dataclass(slots=True)
class Admin:
    """A class representing an admin user"""

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
