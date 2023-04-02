from dataclasses import asdict
from hashlib import sha256

from sqlalchemy import insert, select

from kts_backend.admin.dataclasses import Admin
from kts_backend.admin.model import AdminModel
from kts_backend.base.base_accessor import BaseAccessor


class AdminAccessor(BaseAccessor):
    @staticmethod
    def admin_model2admin(admin_model: AdminModel) -> Admin:
        """
        Convert AdminModel object to Admin object
        :param admin_model: AdminModel
        :return: Admin
        """
        return Admin(
            id=admin_model.id,
            email=admin_model.email,
            password=admin_model.password,
        )

    @staticmethod
    def admin2dict(admin: Admin) -> dict:
        """
        Convert AdminModel object to dict object
        :param admin: Admin
        :return: dict
        """
        return asdict(admin)

    async def get_by_email(self, email: str) -> Admin | None:
        """
        Get Admin object from database, otherwise return None
        :param email: str
        :return: Admin | None
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
        Create Admin object in database and return it if it does not exist,
        otherwise return existed one
        :param email: str
        :param password: str
        :return: Admin
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

    async def update_admin(self):
        raise NotImplementedError

    async def delete_admin(self):
        raise NotImplementedError
