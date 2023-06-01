from model_objects import Discount
from receipt import Receipt
from tests.utils import TestCase

class ReceiptPrinterTest(TestCase):
    def setUp(self):
        self.receipt = Receipt()

    def test_one_line_item(self):
        self.receipt.add_product(self.toothbrush, 1, 0.99, 0.99)
        self.compare_with_html(self.receipt)

    def test_quantity_two(self):
        self.receipt.add_product(self.toothbrush, 2, 0.99, 0.99 * 2)
        self.compare_with_html(self.receipt)

    def test_loose_weight(self):
        self.receipt.add_product(self.apples, 2.3, 1.99, 1.99 * 2.3)
        self.compare_with_html(self.receipt)

    def test_total(self):
        self.receipt.add_product(self.toothbrush, 1, 0.99, 0.99 * 2)
        self.receipt.add_product(self.apples, 0.75, 1.99, 1.99 * 0.75)
        self.compare_with_html(self.receipt)

    def test_discounts(self):
        self.receipt.add_discount(Discount(product=self.apples, description="3 for 2", discount_amount=-0.99))
        self.compare_with_html(self.receipt)

    def test_whole_receipt(self):
        self.receipt.add_product(self.toothbrush, 1, 0.99, 0.99)
        self.receipt.add_product(self.toothbrush, 2, 0.99, 0.99*2)
        self.receipt.add_product(self.apples, 0.75, 1.99, 1.99 * 0.75)
        self.receipt.add_discount(Discount(product=self.apples, description="3 for 2", discount_amount=-0.99))
        self.compare_with_html(self.receipt)
