from python_drills.product import Product


def test_product_create(mug):
    assert mug.sku == "SKU-1"
    assert mug.name == "Mug"
    assert mug.price == 12.50
    assert mug.qty == 10


def test_two_products_equal(mug):
    product2 = Product("SKU-1", "Mug", 12.50, 10)
    assert mug == product2


def test_different_products(mug, book):
    assert mug != book


def test_repr_in_product(mug):
    assert repr(mug) == "Product(sku='SKU-1', name='Mug', price=12.5, qty=10)"
