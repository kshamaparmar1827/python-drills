import pytest

from python_drills.cart import Cart
from python_drills.exceptions import InvalidDiscountError, OutOfStockError


def test_add_item_raises(mug):
    my_cart = Cart()
    with pytest.raises(OutOfStockError):
        my_cart.add_item(mug, 11)


def test_add_item_raises_at_second_add(mug):
    my_cart = Cart()
    my_cart.add_item(mug, 8)
    with pytest.raises(OutOfStockError):
        my_cart.add_item(mug, 3)
    assert my_cart.item_count == 8


def test_add_item(mug):
    my_cart = Cart()
    my_cart.add_item(mug, 10)
    assert my_cart.item_count == 10


def test_apply_discount_raises():
    my_cart = Cart()
    with pytest.raises(InvalidDiscountError):
        my_cart.apply_discount(-5)


def test_apply_discount_raises_two():
    my_cart = Cart()
    with pytest.raises(InvalidDiscountError):
        my_cart.apply_discount(150)


def test_apply_discount():
    my_cart = Cart()
    my_cart.apply_discount(0)
    assert my_cart.discount == 0


def test_apply_discount_100():
    my_cart = Cart()
    my_cart.apply_discount(100)
    assert my_cart.discount == 100
