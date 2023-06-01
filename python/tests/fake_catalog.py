from catalog import SupermarketCatalog
from model_objects import Product


class FakeCatalog(SupermarketCatalog):
    prices: dict[Product, float] = {}

    def add_product(self, product: Product, price: float):
        self.prices[product] = price

    def unit_price(self, product: Product) -> float:
        return self.prices[product]
