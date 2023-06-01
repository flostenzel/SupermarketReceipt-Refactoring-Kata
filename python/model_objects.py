from enum import Enum
from pydantic import BaseModel


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class Product(BaseModel):
    name: str
    unit: ProductUnit

    class Config:
        frozen = True


class ProductQuantity(BaseModel):
    product: Product
    quantity: float


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4
    BUNDLE = 5


class Offer(BaseModel):
    offer_type: SpecialOfferType
    product: Product | list[Product]
    argument: float

    class Config:
        frozen = True


class Discount(BaseModel):
    product: Product | list[Product]
    description: str
    discount_amount: float
