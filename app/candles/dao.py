from sqlalchemy import select, func

from app.dao.base import BaseDAO
from app.candles.models import Candles
from app.database import async_session_maker, engine
from app.baskets.models import Baskets


class CandleDAO(BaseDAO):
    model = Candles

    @classmethod
    async def find_all_self(cls, candle_id: int, quantity: int,  **filter_by):
        async with async_session_maker() as session:
            basket_have_or_none = select(Baskets.quantity).where(Baskets.candle_id == candle_id)
            basket_have_or_none = await session.execute(basket_have_or_none)
            result = basket_have_or_none.scalar()

            if result is not None:
                basket_candles = select(Baskets).where(Baskets.candle_id == candle_id).cte("basket_candles")

                get_candles_left = select(
                    (Candles.quantity - func.sum(basket_candles.c.quantity)).label("candles_left")
                ).select_from(Candles).join(
                    basket_candles, basket_candles.c.candle_id == Candles.id
                ).where(Candles.id == candle_id).group_by(Candles.quantity, basket_candles.c.candle_id)

                get_candles_left = await session.execute(get_candles_left)

                get_candles_left = get_candles_left.scalar()
                print(get_candles_left)

            else:
                get_candles_left = select(Candles.quantity).where(Candles.id == candle_id)
                get_candles_left = await session.execute(get_candles_left)
                get_candles_left = get_candles_left.scalar()
                print(get_candles_left)

            if get_candles_left >= quantity:
                get_candles = (
                    select(
                        Candles.__table__.columns,
                        (Candles.price * quantity).label("total_coast"),
                        (Candles.quantity - Candles.quantity + get_candles_left).label("candles_left")
                    )
                    .filter_by(**filter_by)
                )
                candles = await session.execute(get_candles)
                return candles.mappings().all()









            




