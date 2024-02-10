from typing import Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class Candles(Base):
    __tablename__ = "candles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    quantity: Mapped[int]
    image_id: Mapped[int]

    baskets: Mapped[list["Baskets"]] = relationship(back_populates="candle")

    def __str__(self):
        return f"{self.name}"
