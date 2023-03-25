from typing import Optional
from hashlib import sha256

from sqlalchemy import insert

from kts_backend.admin.model import Admin, AdminModel
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
            admin_id=admin_model.admin_id,
            email=admin_model.email,
            password=admin_model.password,
        )

    async def get_admin_by_email(self, email: str) -> Admin | None:
        """
        Get Admin object from database, otherwise return None
        :param email: str
        :return: Admin | None
        """
        async with self.app.database.session.begin() as session:
            res = await session.query(AdminModel).filter(
                AdminModel.email == email
            )
            admin_model: Optional[AdminModel] = res.scalar()

            if admin_model:
                return self.admin_model2admin(admin_model=admin_model)
            return None

    async def create_admin(self, email: str, password: str) -> Admin:
        """
        Create Admin object in database and return it if it does not exist,
        otherwise return existed one
        :param email: str
        :param password: str
        :return: Admin
        """
        admin: Optional[Admin] = await self.get_admin_by_email(email=email)
        if admin is not None:
            return admin

        new_password = sha256(password.encode()).hexdigest()
        statement = insert(AdminModel).values(
            email=email, password=new_password
        )
        async with self.app.database.session.begin() as session:
            await session.execute(statement=statement)
            await session.commit()
        return await self.get_admin_by_email(email=email)

    async def update_admin(self, admin: Admin) -> Admin:
        pass

    async def delete_admin(self, admin_id: int) -> Admin:
        pass
