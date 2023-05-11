from kts_backend.admin.dataclasses import Admin
from kts_backend.web.dataclasses import Config


class TestAdminDataclass:
    def test_admin_is_password_valid(self, admin: Admin, config: Config):
        """
        Test the `is_password_valid` method of the Admin class with a valid password.

        Args:
            admin (Admin): An instance of the Admin class.

        Returns:
            None
        """
        assert admin.is_password_valid(config.admin.password)

    def test_admin_is_password_invalid(self, admin: Admin):
        """
        Test the `is_password_valid` method of the Admin class with an invalid password.

        Args:
            admin (Admin): An instance of the Admin class.

        Returns:
            None
        """
        assert not admin.is_password_valid("invalidpassword")

    def test_admin_from_session_with_valid_session(self):
        """
        Test the `from_session` method of the Admin class with a valid session.

        Returns:
            None
        """
        session = {"admin": {"id": 1, "email": "admin@example.com"}}
        admin = Admin.from_session(session)
        assert isinstance(admin, Admin)
        assert admin.id == 1
        assert admin.email == "admin@example.com"

    def test_admin_from_session_with_invalid_session(self):
        """
        Test the `from_session` method of the Admin class with an invalid session.

        Returns:
            None
        """
        assert Admin.from_session(None) is None
