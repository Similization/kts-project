import typing
from hashlib import sha256

from sqlalchemy import select, insert
from sqlalchemy.engine.result import ChunkedIteratorResult

from kts_backend.admin.model import Admin, AdminModel
from kts_backend.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    pass


class AdminAccessor(BaseAccessor):

    async def get_by_email(self, email: str) -> Admin | None:
        query = select(AdminModel).where(AdminModel.email == email)

        async with self.app.database.session.begin() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            admin: AdminModel = res.scalar()

            if admin:
                return Admin(admin_id=admin.admin_id, email=admin.email, password=admin.password)
            return None

    async def create_admin(self, email: str, password: str) -> Admin:
        # hash password
        new_password = sha256(password.encode()).hexdigest()

        # create admin in db
        admin: typing.Optional[Admin] = await self.get_by_email(email=email)
        if admin is not None:
            return admin

        query = insert(AdminModel).values(email=email, password=new_password)
        async with self.app.database.session.begin() as session:
            # res: ChunkedIteratorResult = await session.execute(query)
            await session.execute(query)
            # commit
            await session.commit()
        # get admin from db
        return await self.get_by_email(email=email)