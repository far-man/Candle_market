import asyncio

from pydantic import TypeAdapter

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.candles.dao import CandleDAO
from app.candles.schemas import SCandleInfo, SCandle
from app.exceptions import CandleFullyBooked


router = APIRouter(
    prefix="/candles",
    tags=["Свечи"],
)


@router.get("/{candle_id}")
@cache(expire=40)
async def get_candles(candle_id: int, quantity: int) -> list[SCandleInfo]:
    await asyncio.sleep(3)
    candles = await CandleDAO.find_all_self(candle_id, quantity, id=candle_id)
    if not candles:
        raise CandleFullyBooked
    return candles


@router.get("")
async def get_all_candles():
    candles = await CandleDAO.find_all()
    return candles








