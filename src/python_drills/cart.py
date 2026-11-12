from python_drills.exceptions import InvalidDiscountError, OutOfStockError
from python_drills.product import Product


class Cart:
    def __init__(self) -> None:
        self.cart_items: dict[str, list[Product | int]] = {}
        self.discount: int = 0

    def __repr__(self):
        total_qty = 0
        for product, qty in self.cart_items.values():
            total_qty += qty

        return (
            f"Cart(items={total_qty}, total={self.total()}, discount={self.discount})"
        )

    def __eq__(self, value: object):
        if not isinstance(value, Cart):
            return NotImplemented
        return self.cart_items == value.cart_items and self.discount == value.discount

    @property
    def item_count(self):
        total_qty = 0
        for product, qty in self.cart_items.values():
            total_qty += qty
        return total_qty

    def add_item(self, product: Product, quantity: int = 1) -> None:

        sku = product.sku
        if self.cart_items.get(sku, None):
            # if sku in self.cart_items:
            if product.qty < self.cart_items.get(sku)[1] + quantity:
                raise OutOfStockError()
            self.cart_items.get(sku)[1] += quantity
        else:
            if product.qty < quantity:
                raise OutOfStockError()
            self.cart_items[sku] = [product, quantity]

    def remove_item(self, sku: str):

        if self.cart_items.get(sku, None):
            del self.cart_items[sku]

    def apply_discount(self, percent: int):
        if percent < 0 or percent > 100:
            raise InvalidDiscountError()
        self.discount = percent

    def total(self) -> float:
        final_price = 0
        for product, qty in self.cart_items.values():
            final_price += product.price * qty

        discount_price = final_price * self.discount / 100
        return round(final_price - discount_price, 2)
