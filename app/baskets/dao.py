from sqlalchemy import select, func, insert

from app.baskets.models import Baskets
from app.candles.models import Candles
from app.dao.base import BaseDAO


from app.database import async_session_maker


class BasketDAO(BaseDAO):
    model = Baskets

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            get_baskets = (
                select(
                    Baskets.__table__.columns,
                    Candles.name.label("name"),
                    Candles.description.label("description"),
                    Candles.image_id.label("image_id")
                )
                .where(Candles.id == Baskets.candle_id)
                .filter_by(**filter_by)
            )
            baskets = await session.execute(get_baskets)
            return baskets.mappings().all()

    @classmethod
    async def add(cls, user_id: int, candle_id: int, quantity: int):
        """
               WITH basket_candles AS(
               SELECT * FROM baskets
               WHERE candle_id = 1
               )
               SELECT candles.quantity - sum(basket_candles.quantity) FROM candles
               LEFT JOIN basket_candles ON basket_candles.candle_id = candles.id
               WHERE candles.id = 1
               GROUP BY candles.quantity, basket_candles.candle_id
               """

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

                # print(candles_left.compile(engine, compile_kwargs={"literal_binds": True}))
                get_candles_left = await session.execute(get_candles_left)
                get_candles_left = get_candles_left.scalar()
                print(get_candles_left)

            else:
                get_candles_left = select(Candles.quantity).where(Candles.id == candle_id)
                get_candles_left = await session.execute(get_candles_left)
                get_candles_left = get_candles_left.scalar()
                print(get_candles_left)

            if get_candles_left > quantity:
                get_price = select(Candles.price).filter_by(id=candle_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = insert(Baskets).values(
                    candle_id=candle_id,
                    user_id=user_id,
                    quantity=quantity,
                    price=price
                ).returning(
                    Baskets.id,
                    Baskets.user_id,
                    Baskets.candle_id,
                    Baskets.quantity,
                    Baskets.price,
                    Baskets.total_cost
                )

                new_basket = await session.execute(add_booking)
                await session.commit()
                return new_basket.mappings().one()
            else:
                pass



