from pydantic import BaseModel
from model_objects import Product


class SupermarketCatalog(BaseModel):

    def add_product(self, product: Product, price: float) -> None:
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product: Product) -> float:
        raise Exception("cannot be called from a unit test - it accesses the database")
