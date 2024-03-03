from typing import Type

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.sellers import Seller
from src.schemas.sellers import IncomingSeller

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_seller(self, seller_data: IncomingSeller) -> Seller:
        hashed_password = self.hash_password(seller_data.password)
        new_seller = Seller(
            first_name=seller_data.first_name,
            last_name=seller_data.last_name,
            email=seller_data.email,
            password=hashed_password
        )
        self.db_session.add(new_seller)
        await self.db_session.commit()
        await self.db_session.refresh(new_seller)
        return new_seller

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
