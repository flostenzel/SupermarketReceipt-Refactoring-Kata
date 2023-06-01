import unittest

from approvaltests.approvals import verify  # type: ignore
from approvaltests.core.options import Options  # type: ignore

from model_objects import Product, ProductUnit
from receipt import Receipt
from receipt_printer import ReceiptPrinter

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.toothbrush = Product(name="toothbrush", unit=ProductUnit.EACH)
        cls.apples = Product(name="apples", unit=ProductUnit.KILO)
        cls.toothpaste = Product(name="toothpaste", unit=ProductUnit.EACH)
        cls.cherry_tomatoes = Product(name="cherry tomatoes", unit=ProductUnit.EACH)
        cls.rice = Product(name="rice", unit=ProductUnit.EACH)

    def compare_with_html(self, receipt: Receipt):
        verify(ReceiptPrinter().print_receipt(receipt), options=Options({'extension_with_dot': '.html'}))
