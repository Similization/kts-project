from kts_backend.admin.dataclasses import Admin
from kts_backend.store import Store
from kts_backend.web.dataclasses import Config
from tests.utils import ok_response


class TestAdminLoginView:
    """
    A collection of test cases for the Admin Login View.

    This class contains several test cases that exercise different aspects of the Admin Login View endpoint,
    including positive and negative scenarios. These test cases are designed to ensure that the endpoint is
    working as expected and that it correctly handles a variety of inputs and conditions.

    """
    async def test_admin_created_on_startup(self, store: Store, config: Config):
        """
        Test that the admin user is created on application startup.

        Args:
            store (Store): An instance of the application store.
            config (Config): An instance of the application configuration.

        Returns:
            None
        """
        admin = await store.admin.get_by_email(email=config.admin.email)
        assert admin is not None
        assert admin.email == config.admin.email
        assert admin.password != config.admin.password
        assert admin.id == 1

    async def test_admin_login_successful(self, cli, config: Config):
        """
        Test that an admin user can successfully log in.

        Args:
            cli (TestClient): A client object for making HTTP requests.
            config (Config): An instance of the application configuration.

        Returns:
            None
        """
        resp = await cli.post(
            "/admin.login",
            json={
                "email": config.admin.email,
                "password": config.admin.password,
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            {"id": 1, "email": config.admin.email, "user_id": None}
        )

    async def test_missing_email(self, cli):
        """
        Test that an error is returned when email is missing in the login request.

        Args:
            cli (TestClient): A client object for making HTTP requests.

        Returns:
            None
        """
        resp = await cli.post(
            "/admin.login",
            json={
                "password": "qwerty",
            },
        )
        assert resp.status == 400
        data = await resp.json()
        assert data["status"] == "bad_request"
        assert data["data"]["email"][0] == "Missing data for required field."

    async def test_invalid_credentials(self, cli):
        """
          Test that an error is returned when invalid credentials are used for login.

          Args:
              cli (TestClient): A client object for making HTTP requests.

          Returns:
              None
          """
        resp = await cli.post(
            "/admin.login",
            json={
                "email": "qwerty@gmail.com",
                "password": "qwerty",
            },
        )
        assert resp.status == 403
        data = await resp.json()
        assert data["status"] == "forbidden"

    async def test_admin_login_method_not_allowed(self, cli):
        """
        Test that an error is returned when an unsupported HTTP method is used for login.

        Args:
            cli (TestClient): A client object for making HTTP requests.

        Returns:
            None
        """
        resp = await cli.get(
            "/admin.login",
            json={
                "email": "qwerty",
                "password": "qwerty",
            },
        )
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"


class TestAdminCurrentView:
    """Unit tests for the AdminCurrentView class"""

    async def test_admin_current_view_success(self, authed_cli, admin: Admin, config: Config):
        """Test the successful behavior of the AdminCurrentView endpoint

        Args:
            authed_cli (TestClient): A client object authenticated with an admin user
            admin (Admin): An admin object for the authenticated user
            config (Config): A configuration object containing application configuration

        Returns:
            None
        """
        resp = await authed_cli.get(
            "/admin.current",
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            {"id": 1, "email": config.admin.email, "user_id": None}
        )

    async def test_admin_current_view_failure(self, cli, config: Config):
        """Test the failure behavior of the AdminCurrentView endpoint

        Args:
            cli (TestClient): A client object
            config (Config): A configuration object containing application configuration

        Returns:
            None
        """
        resp = await cli.get(
            "/admin.current",
        )
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_different_http_method(self, cli):
        """Test that an unsupported HTTP method returns a 405 error

        Args:
            cli (TestClient): A client object

        Returns:
            None
        """
        resp = await cli.post(
            "/admin.current",
        )
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"
