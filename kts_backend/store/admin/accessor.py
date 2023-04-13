from dataclasses import asdict
from hashlib import sha256

from sqlalchemy import insert, select, update, delete

from kts_backend.admin.dataclasses import Admin
from kts_backend.admin.model import AdminModel
from kts_backend.base.base_accessor import BaseAccessor


class AdminAccessor(BaseAccessor):
    """
    A class providing methods for accessing and manipulating admin data in the database.

    Methods:
        admin_model2admin: Convert an AdminModel instance to an Admin instance.
        admin2dict: Convert an Admin instance to a dictionary.
        get_by_email: Get an admin user by email.
        get_or_create: Get an admin user by email or create a new one.
        update_admin: Update an admin user's email and password by ID.
        delete_admin: Delete an admin user by ID.
        delete_admin_by_email: Delete an admin user by email.
    """

    @staticmethod
    def admin_model2admin(admin_model: AdminModel) -> Admin:
        """
        Convert an `AdminModel` instance to an `Admin` instance.

        Args:
            admin_model (AdminModel): The `AdminModel` instance to convert.

        Returns:
            Admin: The `Admin` instance.
        """
        return Admin(
            id=admin_model.id,
            email=admin_model.email,
            password=admin_model.password,
        )

    @staticmethod
    def admin2dict(admin: Admin) -> dict:
        """
        Convert an `Admin` instance to a dictionary.

        Args:
            admin (Admin): The `Admin` instance to convert.

        Returns:
            dict: The dictionary representation of the `Admin` instance.
        """
        return asdict(admin)

    async def get_by_email(self, email: str) -> Admin | None:
        """
        Get an admin user by email.

        Args:
            email (str): The email of the admin user.

        Returns:
            Admin | None: The `Admin` instance if found, else `None`.
        """
        statement = select(AdminModel).filter_by(email=email)
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
        admin_model: AdminModel | None = res.scalar()

        if admin_model:
            return self.admin_model2admin(admin_model=admin_model)
        return None

    async def get_or_create(self, email: str, password: str) -> Admin:
        """
        Get an admin user by email or create a new one.

        Args:
            email (str): The email of the admin user.
            password (str): The password of the admin user.

        Returns:
            Admin: The `Admin` instance.
        """
        admin: Admin | None = await self.get_by_email(email=email)
        if admin is not None:
            return admin

        new_password = sha256(password.encode()).hexdigest()
        statement = (
            insert(AdminModel)
            .values(email=email, password=new_password)
            .returning(AdminModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
        admin_model: AdminModel | None = res.scalar()
        return self.admin_model2admin(admin_model=admin_model)

    async def update_admin(
        self, admin_id: int, email: str, password: str
    ) -> Admin:
        """
        Update an admin user's email and password by ID.

        Args:
            admin_id (int): The ID of the admin user.
            email (str): The new email of the admin user.
            password (str): The new password of the admin user.

        Returns:
            Admin: The updated `Admin` instance.
        """
        new_password = sha256(password.encode()).hexdigest()
        statement = (
            update(AdminModel)
            .filter_by(id=admin_id)
            .values(email=email, password=new_password)
            .returning(AdminModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
        admin_model: AdminModel | None = res.scalar()
        return self.admin_model2admin(admin_model=admin_model)

    async def delete_admin(self, admin_id: int) -> Admin | None:
        """
        Deletes an Admin instance with the specified ID.

        Args:
            admin_id (int): The ID of the Admin instance to be deleted.

        Returns:
            Admin | None: The deleted Admin instance if it exists, otherwise None.
        """
        statement = (
            delete(AdminModel).filter_by(id=admin_id).returning(AdminModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
        admin_model: AdminModel | None = res.scalar()

        if admin_model:
            return self.admin_model2admin(admin_model=admin_model)
        return None

    async def delete_admin_by_email(self, email: str) -> Admin | None:
        """
        Deletes an Admin instance with the specified email.

        Args:
            email (str): The email of the Admin instance to be deleted.

        Returns:
            Admin | None: The deleted Admin instance if it exists, otherwise None.
        """
        statement = (
            delete(AdminModel).filter_by(email=email).returning(AdminModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
        admin_model: AdminModel | None = res.scalar()

        if admin_model:
            return self.admin_model2admin(admin_model=admin_model)
        return None
