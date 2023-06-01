from model_objects import Discount, Product
from receipt import Receipt, ReceiptItem
from jinja2 import Environment, FileSystemLoader

class ReceiptPrinter:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates/'))
        self.template = self.env.get_template('receipt_template.html')

    def print_receipt(self, receipt: Receipt):
        receipt_items = [self._format_receipt_item(item) for item in receipt.items]
        discounts = [self._format_discount(discount) for discount in receipt.discounts]
        total = receipt.total_price()
        return self.template.render(receipt_items=receipt_items, discounts=discounts, total=total)

    def _format_receipt_item(self, item: ReceiptItem):
        name = item.product.name
        quantity = item.quantity if item.quantity % 1 != 0 else int(item.quantity)
        price = item.price
        total_price = item.total_price

        return {
            'name': name,
            'quantity': quantity,
            'price': self._format_price(price),
            'total_price': self._format_price(total_price),
        }

    def _format_discount(self, discount: Discount):
        product = discount.product
        description = discount.description
        discount_amount = discount.discount_amount

        if isinstance(product, Product):
            name = product.name
        else:
            name = ', '.join(p.name for p in product)

        return {
            'name': name,
            "description": description,
            "discount_amount": self._format_price(discount_amount),
        }

    def _format_price(self, price: float):
        return f'${price:.2f}'
