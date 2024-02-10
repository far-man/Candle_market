from sqlalchemy import Computed, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base
from app.candles.models import Candles
from app.users.models import Users


class Baskets(Base):
    __tablename__ = "baskets"

    id: Mapped[int] = mapped_column(primary_key=True)
    candle_id: Mapped[int] = mapped_column(ForeignKey("candles.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quantity: Mapped[int]
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed("quantity * price"))

    user: Mapped["Users"] = relationship(back_populates="baskets")
    candle: Mapped["Candles"] = relationship(back_populates="baskets")

    def __str__(self):
        return f"Basket #{self.id}"

