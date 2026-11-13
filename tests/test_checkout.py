from python_drills import checkout
from python_drills.cart import Cart


def test_add_to_cart_safely_within_stock(capsys, mug):
    cart = Cart()
    result = checkout.add_to_cart_safely(cart, mug, 3)
    assert result is True
    assert cart.quantity_of("SKU-1") == 3
    captured = capsys.readouterr()
    assert "Checked: SKU-1 * 3" in captured.out


def test_add_to_cart_safely_beyond_stock(capsys, mug):
    cart = Cart()
    result = checkout.add_to_cart_safely(cart, mug, 20)
    assert result is False
    assert len(cart) == 0
    captured = capsys.readouterr()
    assert "Checked: SKU-1 * 20" in captured.out
