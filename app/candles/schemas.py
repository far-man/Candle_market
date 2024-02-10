from pydantic import BaseModel, ConfigDict


class SCandle(BaseModel):

    id: int
    name: str
    description: str
    price: int
    quantity: int
    image_id: int


class SCandleInfo(SCandle):
    total_coast: int
    candles_left: int

    model_config = ConfigDict(from_attributes=True)



