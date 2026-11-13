from python_drills.cart import Cart


def test_empty_cart():

    cart = Cart()
    assert cart.total() == 0
    assert cart.item_count == 0


def test_cart_total(mug, book):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.add_item(book, 1)
    assert cart.total() == 30.0


def test_add_same_items(mug):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.add_item(mug, 3)
    assert cart.item_count == 5
    assert len(cart.cart_items) == 1


def test_remove_item(mug, book):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.add_item(book, 1)
    cart.remove_item("SKU-1")
    assert cart.total() == 5.0
    assert "SKU-1" not in cart.cart_items


def test_remove_item_not_in_cart(mug):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.remove_item("SKU-2")
    assert len(cart.cart_items) == 1


def test_apply_discount_to_total(mug, book):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.add_item(book, 1)
    cart.apply_discount(10)
    assert cart.total() == 27.0


def test_item_count(mug, book):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.add_item(book, 1)
    assert cart.item_count == 3


def test_compare_same_carts(mug, book):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.add_item(book, 1)
    cart2 = Cart()
    cart2.add_item(book, 1)
    cart2.add_item(mug, 2)
    assert cart == cart2


def test_compare_same_carts_different_discounts(mug, book):
    cart = Cart()
    cart.add_item(mug, 2)
    cart.add_item(book, 1)
    cart.apply_discount(10)
    cart2 = Cart()
    cart2.add_item(mug, 2)
    cart2.add_item(book, 1)
    cart2.apply_discount(15)
    assert cart != cart2


def test_compare_cart_with_a_noncart():
    assert Cart() != 20


def test_repr_in_cart(mug):
    cart = Cart()
    cart.add_item(mug, 1)
    assert repr(cart) == "Cart(items=1, total=12.5, discount=0)"
