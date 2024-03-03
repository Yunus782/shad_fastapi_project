from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.schemas.sellers import ReturnedSeller, IncomingSeller
from src.services.sellers import SellerService

seller_router = APIRouter(tags=["seller"], prefix="/seller")

DBSession = Depends(get_async_session)


@seller_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(
        seller: IncomingSeller, session: AsyncSession = DBSession
):
    seller_service = SellerService(session)
    new_seller = await seller_service.create_seller(seller)
    return new_seller
