import pytest

from python_drills.product import Product


@pytest.fixture
def mug():
    return Product("SKU-1", "Mug", 12.50, 10)


@pytest.fixture
def book():
    return Product("SKU-2", "Notebook", 5.0, 20)
