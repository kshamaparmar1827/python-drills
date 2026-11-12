from src.python_drills.product import Product


class Cart:
    def __init__(self):
        self.cart_items: dict[str, list[Product | int]] = {}
        self.discount: int = 0

    def add_item(self, product: Product, quantity: int = 1) -> None:

        sku = product.sku
        if self.cart_items.get(sku, None):
            # if sku in self.cart_items:
            self.cart_items.get(sku)[1] += quantity
        else:
            self.cart_items[sku] = [product, quantity]

    def remove_item(self, sku: str):

        if self.cart_items.get(sku, None):
            del self.cart_items[sku]

    def apply_discount(self, percent: int):
        self.discount = percent

    def total(self) -> float:
        final_price = 0
        for product, qty in self.cart_items.values():
            final_price += product.price * qty

        discount_price = final_price * self.discount / 100
        return round(final_price - discount_price, 2)
