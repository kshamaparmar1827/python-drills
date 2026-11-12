class CartError(Exception):
    """Base class for all cart errors."""


class OutOfStockError(CartError):
    """Raised when a product is out of stock"""


class InvalidDiscountError(CartError):
    """Raised when discount is invalid"""
