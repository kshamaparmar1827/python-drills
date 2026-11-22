import pytest

from python_drills.product import Product


@pytest.fixture
def mug():
    return Product("SKU-1", "Mug", 12.50, 10)


@pytest.fixture
def book():
    return Product("SKU-2", "Notebook", 5.0, 20)


@pytest.fixture
def order_data():
    return {
        "order_id": 5001,
        "customer_email": "test@gmail.com",
        "currency": "CAD",
        "items": [{"sku": "SKU-1", "quantity": 1, "unit_price": 5}],
    }
