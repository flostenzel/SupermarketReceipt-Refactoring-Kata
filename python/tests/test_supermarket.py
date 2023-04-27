import unittest
import pytest

from approvaltests.approvals import verify
from approvaltests.core.options import Options

from model_objects import Product, SpecialOfferType, ProductUnit
from receipt import Receipt
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class SupermarketTest(unittest.TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()
        self.teller = Teller(self.catalog)
        self.the_cart = ShoppingCart()

        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.catalog.add_product(self.toothbrush, 0.99)
        self.toothpaste = Product("toothpaste", ProductUnit.EACH)
        self.catalog.add_product(self.toothpaste, 1.79)
        self.rice = Product("rice", ProductUnit.EACH)
        self.catalog.add_product(self.rice, 2.99)
        self.apples = Product("apples", ProductUnit.KILO)
        self.catalog.add_product(self.apples, 1.99)
        self.cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
        self.catalog.add_product(self.cherry_tomatoes, 0.69)

    def compare_with_html(self, receipt: Receipt):
        verify(ReceiptPrinter().print_receipt(receipt), options=Options({'extension_with_dot':'.html'}))

    def test_an_empty_shopping_cart_should_cost_nothing(self):
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 0
        assert receipt.total_discount_amount() == 0
        assert receipt.total_price() == 0
        self.compare_with_html(receipt)

    def test_one_normal_item(self):
        self.the_cart.add_item(self.toothbrush)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 0.99
        assert receipt.total_discount_amount() == 0
        assert receipt.total_price() == 0.99
        self.compare_with_html(receipt)

    def test_two_normal_items(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.rice)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 0.99 + 2.99
        assert receipt.total_discount_amount() == 0
        assert receipt.total_price() == pytest.approx(0.99 + 2.99, 0.01)
        self.compare_with_html(receipt)

    def test_buy_two_get_one_free(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.toothbrush, self.catalog.unit_price(self.toothbrush))
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 3 * 0.99
        assert receipt.total_discount_amount() == pytest.approx(-0.99, 0.01)
        assert receipt.total_price() == pytest.approx(2 * 0.99, 0.01)
        self.compare_with_html(receipt)

    def test_buy_five_get_one_free(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.toothbrush, self.catalog.unit_price(self.toothbrush))
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == pytest.approx(5 * 0.99, 0.01)
        assert receipt.total_discount_amount() == pytest.approx(-0.99, 0.01)
        assert receipt.total_price() == pytest.approx(4 * 0.99, 0.01)
        self.compare_with_html(receipt)

    def test_loose_weight_product(self):
        self.the_cart.add_item_quantity(self.apples, 0.5)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == .5 * 1.99
        assert receipt.total_discount_amount() == 0
        assert receipt.total_price() == 0.99
        self.compare_with_html(receipt)

    def test_percent_discount(self):
        self.the_cart.add_item(self.rice)
        self.teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.rice, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 2.99
        assert receipt.total_discount_amount() == pytest.approx(-2.99 / 10, 0.01)
        assert receipt.total_price() == pytest.approx(2.99 - 2.99 / 10, 0.01)
        self.compare_with_html(receipt)

    def test_x_for_y_discount(self):
        self.the_cart.add_item(self.cherry_tomatoes)
        self.the_cart.add_item(self.cherry_tomatoes)
        self.teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, self.cherry_tomatoes, 0.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 0.69 * 2
        assert receipt.total_discount_amount() == pytest.approx(0.99 - (0.69 * 2), 0.01)
        assert receipt.total_price() == pytest.approx(0.99, 0.01)
        self.compare_with_html(receipt)

    def test_five_for_y_discount(self):
        self.the_cart.add_item_quantity(self.apples, 5)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 5.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 5 * 1.99
        assert receipt.total_discount_amount() == pytest.approx(5.99 - 5 * 1.99, 0.01)
        assert receipt.total_price() == pytest.approx(5.99, 0.01)
        self.compare_with_html(receipt)

    def test_five_for_y_discount_with_six(self):
        self.the_cart.add_item_quantity(self.apples, 6)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 5.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 6 * 1.99
        assert receipt.total_discount_amount() == pytest.approx(5.99 - 5 * 1.99,  0.01)
        assert receipt.total_price() == pytest.approx(5.99 + 1.99,  0.01)
        self.compare_with_html(receipt)

    def test_five_for_y_discount_with_sixteen(self):
        self.the_cart.add_item_quantity(self.apples, 16)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 7.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 16 * 1.99
        assert receipt.total_discount_amount() == pytest.approx(-5.88, 0.01)
        assert receipt.total_price() == pytest.approx(25.96,  0.01)
        self.compare_with_html(receipt)

    def test_five_for_y_discount_with_four(self):
        self.the_cart.add_item_quantity(self.apples, 4)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 6.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 4 * 1.99
        assert receipt.total_discount_amount() == 0
        assert receipt.total_price() == 4 * 1.99
        self.compare_with_html(receipt)

    def test_one_complete_bundle(self):
        self.the_cart.add_item_quantity(self.toothbrush, 1)
        self.the_cart.add_item_quantity(self.toothpaste, 2)
        self.teller.add_special_offer(SpecialOfferType.BUNDLE, [self.toothbrush, self.toothpaste], 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 0.99 + 2 * 1.79
        assert receipt.total_discount_amount() == -(0.99 + 1.79) / 10
        assert receipt.total_price() == 4.29
        self.compare_with_html(receipt)

    def test_incomplete_bundle(self):
        self.the_cart.add_item_quantity(self.toothpaste, 2)
        self.teller.add_special_offer(SpecialOfferType.BUNDLE, [self.toothbrush, self.toothpaste], 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 2 * 1.79
        assert receipt.total_discount_amount() == 0
        assert receipt.total_price() == 2 * 1.79
        self.compare_with_html(receipt)

    def test_two_bundles(self):
        self.the_cart.add_item_quantity(self.toothbrush, 2)
        self.the_cart.add_item_quantity(self.toothpaste, 2)
        self.teller.add_special_offer(SpecialOfferType.BUNDLE, [self.toothbrush, self.toothpaste], 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert receipt.total_item_price_amount() == 2 * 0.99 + 2 * 1.79
        assert receipt.total_discount_amount() == -(0.99 + 1.79) / 5
        assert receipt.total_price() == 5.0
        self.compare_with_html(receipt)
