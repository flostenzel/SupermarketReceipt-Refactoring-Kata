
from pydantic import BaseModel
from catalog import SupermarketCatalog
from model_objects import Discount, Product, ProductQuantity


class ReceiptItem(BaseModel):
    product: Product
    quantity: float
    price: float
    total_price: float

class Receipt(BaseModel):
    items: list[ReceiptItem] = []
    discounts: list[Discount] = []

    def add_cart_item_to_receipt(self, catalog: SupermarketCatalog, product_quantity: ProductQuantity):
        product = product_quantity.product
        quantity = product_quantity.quantity
        unit_price = catalog.unit_price(product)
        price = quantity * unit_price
        self.add_product(product, quantity, unit_price, price)

    def total_price(self) -> float:
        return round(self.total_item_price_amount() + self.total_discount_amount(), 2)

    def total_item_price_amount(self) -> float:
        return sum(item.total_price for item in self.items)

    def total_discount_amount(self) -> float:
        return sum(discount.discount_amount for discount in self.discounts)

    def add_product(self, product: Product, quantity: float, price: float, total_price: float):
        self.items.append(ReceiptItem(product=product, quantity=quantity, price=price, total_price=total_price))

    def add_discount(self, discount: Discount):
        self.discounts.append(discount)
