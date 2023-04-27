from catalog import SupermarketCatalog

from model_objects import Offer, ProductQuantity, SpecialOfferType, Discount, Product
from receipt import Receipt


class ShoppingCart:

    def __init__(self) -> None:
        self._items: list[ProductQuantity] = []
        self._product_quantities: dict[Product, float] = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product: Product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: float):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_all_offers(self, receipt: Receipt, offers: dict[Offer, Product | list[Product]], catalog: SupermarketCatalog):
        # go through all offers to see which are applicable to the cart
        for offer, products in offers.items():
            # First check if there is any bundle offer with a list of products associated
            if offer.offer_type == SpecialOfferType.BUNDLE and not isinstance(products, Product):
                self.handle_bundle_offers(receipt, products, catalog)
            # else if one of the same product offers is valid
            elif isinstance(products, Product):
                self.handle_same_product_offers(receipt, products, offer, catalog)

    def handle_bundle_offers(self, receipt: Receipt, products: list[Product], catalog: SupermarketCatalog):
        complete_bundles = self.count_complete_bundles(products)
        if not complete_bundles:
            return
        discount_amount = self.calculate_bundle_discount(complete_bundles, products, catalog)
        description = f"{complete_bundles} Bundle"
        receipt.add_discount(Discount(products, description, discount_amount))

    def count_complete_bundles(self, products: list[Product]):
        product_quantities = [self._product_quantities.get(product, 0) for product in products]
        return int(min(product_quantities))

    def calculate_bundle_discount(self, complete_bundles: int, products: list[Product], catalog: SupermarketCatalog) -> float:
        full_bundle_price = sum(catalog.unit_price(prod) for prod in products)
        # 10% discount for every complete bundle
        return -complete_bundles * full_bundle_price * 10 / 100.0

    def handle_same_product_offers(self, receipt: Receipt, product: Product, offer: Offer, catalog: SupermarketCatalog):
        quantity = self._product_quantities[product]
        unit_price = catalog.unit_price(product)
        discount = self.calculate_same_product_discount(product, quantity, offer, unit_price)
        receipt.add_discount(discount)

    def calculate_same_product_discount(self, product: Product, quantity: float, offer: Offer, unit_price: float) -> Discount | None:
        discount_amount, description = None, None
        # check which offer type is associated and return discount if conditions are true
        if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
            discount_amount = self._calculate_bulk_purchase_discount(quantity, unit_price, 3, 2 * unit_price)
            description = "3 for 2"

        if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
            discount_amount = self._calculate_bulk_purchase_discount(quantity, unit_price, 2, offer.argument)
            description = f"2 for {offer.argument}"

        if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
            discount_amount = self._calculate_bulk_purchase_discount(quantity, unit_price, 5, offer.argument)
            description = f"5 for {offer.argument}"

        if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            discount_amount = self._calculate_discount_x_percent(quantity, unit_price, 10.0)
            description = "10.0% off"

        if discount_amount and description:
            return Discount(product, description, discount_amount)

        return None

    @staticmethod
    def _calculate_bulk_purchase_discount(quantity: float, unit_price: float, bulk: int, amount: float):
        total = amount * (quantity // bulk) + quantity % bulk * unit_price
        discount_amount = total - unit_price * quantity
        return discount_amount

    @staticmethod
    def _calculate_discount_x_percent(quantity: float, unit_price: float, offer_argument: float):
        discount_amount = -quantity * unit_price * offer_argument / 100.0
        return discount_amount
