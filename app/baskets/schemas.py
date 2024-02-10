from pydantic import BaseModel, ConfigDict


class SBasket(BaseModel):
    id: int
    candle_id: int
    user_id: int
    quantity: int
    price: int
    total_cost: int

    class Config:
        from_attributes = True


class SBasketInfo(SBasket):
    name: str
    description: str
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class SNewBasket(BaseModel):
    candle_id: int
    quantity: int
    total_cost: int



