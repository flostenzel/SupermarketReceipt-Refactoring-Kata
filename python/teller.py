from catalog import SupermarketCatalog
from model_objects import Offer, Product, SpecialOfferType
from receipt import Receipt
from shopping_cart import ShoppingCart


class Teller:

    def __init__(self, catalog: SupermarketCatalog):
        self.catalog: SupermarketCatalog = catalog
        self.offers: dict[Offer, (Product | list[Product])] = {}

    def add_special_offer(self, offer_type: SpecialOfferType, products: Product | list[Product], argument: float):
        offer = Offer(offer_type, products, argument)
        self.offers[offer] = products

    def checks_out_articles_from(self, the_cart: ShoppingCart):
        receipt = Receipt()
        for product_quantity in the_cart.items:
            receipt.add_cart_item_to_receipt(self.catalog, product_quantity)
        the_cart.handle_all_offers(receipt, self.offers, self.catalog)

        return receipt
