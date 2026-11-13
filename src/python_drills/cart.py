from python_drills.exceptions import InvalidDiscountError, OutOfStockError
from python_drills.product import Product


class Cart:
    def __init__(self) -> None:
        self.cart_items: dict[str, list[Product | int]] = {}
        self.discount: int = 0

    def __repr__(self) -> str:
        return f"Cart(items={self.item_count}, total={self.total()}, discount={self.discount})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Cart):
            return NotImplemented
        return self.cart_items == value.cart_items and self.discount == value.discount

    @property
    def item_count(self) -> int:
        total_qty = 0
        for _, qty in self.cart_items.values():
            total_qty += qty
        return total_qty

    def quantity_of(self, sku: str) -> int:
        if sku in self.cart_items:
            return self.cart_items[sku][1]
        return 0

    def __contains__(self, sku: str) -> bool:
        return sku in self.cart_items

    def __len__(self) -> int:
        return len(self.cart_items)

    def add_item(self, product: Product, quantity: int = 1) -> None:

        sku = product.sku
        already = self.quantity_of(sku)
        if already + quantity > product.qty:
            raise OutOfStockError(
                f"Only {product.qty} of {sku!r} in stock, requested {quantity} ({already} already in cart)"
            )
        if self.cart_items.get(sku, None):
            # if sku in self.cart_items:
            self.cart_items.get(sku)[1] += quantity
        else:
            self.cart_items[sku] = [product, quantity]

    def remove_item(self, sku: str) -> None:

        if self.cart_items.get(sku, None):
            del self.cart_items[sku]

    def apply_discount(self, percent: int) -> None:
        if percent < 0 or percent > 100:
            raise InvalidDiscountError(
                f"Discount must be between 0 and 100, got {percent}"
            )
        self.discount = percent

    def total(self) -> float:
        final_price = 0
        for product, qty in self.cart_items.values():
            final_price += product.price * qty

        discount_price = final_price * self.discount / 100
        return round(final_price - discount_price, 2)
