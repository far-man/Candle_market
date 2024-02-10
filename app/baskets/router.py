from fastapi import APIRouter, Depends
from fastapi_versioning import version

from app.baskets.dao import BasketDAO
from app.users.models import Users
from app.baskets.schemas import SBasketInfo, SNewBasket
from app.users.dependencies import get_current_user
from app.exceptions import CandleFullyBooked, BasketGetException
from pydantic import TypeAdapter

from app.tasks.tasks import send_basket_confirmation_email


router = APIRouter(
    prefix="/baskets",
    tags=["Корзина"],
)


@router.delete("/{basket_id}")
@version(1)
async def del_baskets(basket_id: int, user: Users = Depends(get_current_user)):
    basket = await BasketDAO.find_one_or_none(id=basket_id, user_id=user.id)
    if not basket:
        raise BasketGetException
    else:
        await BasketDAO.delete(id=basket_id, user_id=user.id)


@router.get("")
@version(1)
async def get_baskets(user: Users = Depends(get_current_user)) -> list[SBasketInfo]:
    baskets = await BasketDAO.find_all(user_id=user.id)
    return baskets


@router.post("")
@version(2)
async def add_basket(candle_id: int, quantity: int, user: Users = Depends(get_current_user)):
    basket = await BasketDAO.add(user.id, candle_id, quantity)
    if not basket:
        raise CandleFullyBooked
    basket = TypeAdapter(SNewBasket).validate_python(basket).model_dump()
    send_basket_confirmation_email.delay(basket, user.email)
    return basket









