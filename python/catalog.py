
from model_objects import Product


class SupermarketCatalog:

    def add_product(self, product: Product, price: float) -> None:
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product: Product):
        raise Exception("cannot be called from a unit test - it accesses the database")
        return float
