from kts_backend.admin.dataclasses import Admin
from kts_backend.store import Store
from utils import check_empty_table_exists


class TestAdminStore:
    async def test_table_exists(self, cli):
        """
        Tests if the admin table exists in the database
        :param cli: AsyncioTestClient
        :return: None
        """
        await check_empty_table_exists(cli, "admin")

    async def test_admin_get_existed(self, store: Store, admin: Admin):
        email = admin.email
        password = admin.password
        fetched_admin = await store.admin.get_or_create(email=email, password=password)
        assert isinstance(fetched_admin, Admin)
        assert fetched_admin.email == email

    async def test_admin_create(self, store: Store):
        email = "test@test.com"
        password = "password"
        admin1 = await store.admin.get_or_create(email=email, password=password)
        admin2 = await store.admin.get_or_create(email=email, password=password)
        assert admin1.id == admin2.id

    async def test_admin_update_admin(self, store: Store):
        email = "test@test.com"
        password = "password"
        admin = await store.admin.get_or_create(email=email, password=password)
        updated_email = "updated@test.com"
        updated_password = "updated_password"
        updated_admin = await store.admin.update_admin(
            admin_id=admin.id,
            email=updated_email,
            password=updated_password
        )
        assert isinstance(updated_admin, Admin)
        assert updated_admin.id == admin.id
        assert updated_admin.email == updated_email

    async def test_admin_delete_admin(self, store: Store):
        email = "test@test.com"
        password = "password"
        admin = await store.admin.get_or_create(email=email, password=password)
        deleted_admin = await store.admin.delete_admin(admin_id=admin.id)
        assert isinstance(deleted_admin, Admin)
        assert deleted_admin.id == admin.id
        assert await store.admin.get_by_email(email=email) is None

    async def test_admin_delete_admin_by_email(self, store: Store):
        email = "test@test.com"
        password = "password"
        admin = await store.admin.get_or_create(email=email, password=password)
        deleted_admin = await store.admin.delete_admin_by_email(email=email)
        assert isinstance(deleted_admin, Admin)
        assert deleted_admin.id == admin.id
        assert await store.admin.get_by_email(email=email) is None
