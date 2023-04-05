from kts_backend.store import Store
from tests.utils import ok_response, check_empty_table_exists


class TestAdminStore:
    async def test_table_exists(self, cli):
        """
        Tests if the admin table exists in the database
        :param cli: AsyncioTestClient
        :return: None
        """
        await check_empty_table_exists(cli, "admin")


class TestAdminLoginView:
    async def test_create_on_startup(self, store: Store, config):
        """
        Tests if the admin user is created on startup
        :param store: Store object
        :param config: Config object
        :return: None
        """
        admin = await store.admin.get_by_email(email=config.admin.email)
        assert admin is not None
        assert admin.email == config.admin.email
        assert admin.password != config.admin.password
        assert admin.id == 1

    async def test_successful_login(self, cli, config):
        """
        Tests a successful admin login
        :param cli: AsyncioTestClient
        :param config: Config object
        :return: None
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
        Tests a login with a missing email
        :param cli: AsyncioTestClient
        :return: None
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
        Tests a login with invalid credentials
        :param cli: AsyncioTestClient
        :return: None
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

    async def test_different_http_method(self, cli):
        """
        Tests a login request with an unsupported HTTP method
        :param cli: AsyncioTestClient
        :return: None
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
