import pytest
from pydantic import ValidationError

from python_drills.order_models import OrderIn


def item(**overrides):
    """A valid line item, with any fields overridden."""
    return {"sku": "SKU-1", "quantity": 1, "unit_price": 5} | overrides


@pytest.mark.parametrize(
    ("field", "value"),
    [
        # order_id
        pytest.param("order_id", 5001, id="order_id-int"),
        pytest.param("order_id", "5001", id="order_id-numeric-str"),
        pytest.param("order_id", 20.0, id="order_id-whole-float"),
        pytest.param("order_id", 0, id="order_id-zero"),
        # customer_email
        pytest.param(
            "customer_email", "first.last+tag@example.co.uk", id="email-complex"
        ),
        # currency
        pytest.param("currency", "USD", id="currency-usd"),
        pytest.param("currency", "INR", id="currency-inr"),
        pytest.param("currency", "cad", id="currency-lowercase"),
        pytest.param("currency", "  usd  ", id="currency-whitespace"),
        # items
        pytest.param(
            "items", [item(), item(sku="SKU-2", quantity=3)], id="items-multiple"
        ),
        pytest.param("items", [item(quantity="2")], id="quantity-numeric-str"),
        pytest.param("items", [item(unit_price=0)], id="unit_price-zero"),
        pytest.param("items", [item(unit_price="12.50")], id="unit_price-numeric-str"),
        pytest.param("items", [item(unit_price=12.5)], id="unit_price-float"),
        pytest.param("items", [item(note="gift")], id="item-extra-field-ignored"),
    ],
)
def test_OrderIn_valid(order_data, field, value):
    assert OrderIn(**(order_data | {field: value}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        # order_id
        pytest.param("order_id", 23.6, id="order_id-fractional-float"),
        pytest.param("order_id", "abc", id="order_id-non-numeric-str"),
        pytest.param("order_id", "", id="order_id-empty-str"),
        pytest.param("order_id", None, id="order_id-none"),
        pytest.param("order_id", [5001], id="order_id-list"),
        # customer_email
        pytest.param("customer_email", "ABC", id="email-no-at"),
        pytest.param("customer_email", "test@", id="email-no-domain"),
        pytest.param("customer_email", "@gmail.com", id="email-no-local-part"),
        pytest.param("customer_email", "", id="email-empty"),
        pytest.param("customer_email", None, id="email-none"),
        # currency
        pytest.param("currency", "EUR", id="currency-unsupported"),
        pytest.param("currency", "", id="currency-empty"),
        pytest.param("currency", "CA D", id="currency-inner-space"),
        pytest.param("currency", 123, id="currency-int"),
        pytest.param("currency", None, id="currency-none"),
        # items (list-level)
        pytest.param("items", [], id="items-empty"),
        pytest.param("items", None, id="items-none"),
        pytest.param("items", item(), id="items-dict-not-list"),
        pytest.param("items", ["SKU-1"], id="items-str-entry"),
        # line item: sku
        pytest.param("items", [item(sku=None)], id="sku-none"),
        pytest.param("items", [item(sku=123)], id="sku-int"),
        # line item: quantity
        pytest.param("items", [item(quantity=0)], id="quantity-zero"),
        pytest.param("items", [item(quantity=-1)], id="quantity-negative"),
        pytest.param("items", [item(quantity=1.5)], id="quantity-fractional"),
        pytest.param("items", [item(quantity="two")], id="quantity-non-numeric-str"),
        # line item: unit_price
        pytest.param("items", [item(unit_price=-0.01)], id="unit_price-negative"),
        pytest.param(
            "items", [item(unit_price="free")], id="unit_price-non-numeric-str"
        ),
        pytest.param("items", [item(unit_price=None)], id="unit_price-none"),
        # one bad item among good ones
        pytest.param("items", [item(), item(quantity=0)], id="items-second-invalid"),
    ],
)
def test_OrderIn_invalid_data(order_data, field, value):
    with pytest.raises(ValidationError):
        OrderIn(**(order_data | {field: value}))


@pytest.mark.parametrize("field", ["order_id", "customer_email", "currency", "items"])
def test_OrderIn_missing_field(order_data, field):
    del order_data[field]
    with pytest.raises(ValidationError):
        OrderIn(**order_data)


@pytest.mark.parametrize("field", ["sku", "quantity", "unit_price"])
def test_LineItem_missing_field(order_data, field):
    line = item()
    del line[field]
    with pytest.raises(ValidationError):
        OrderIn(**(order_data | {"items": [line]}))


def test_OrderIn_converts_order_id_str_to_int(order_data):
    order = OrderIn(**(order_data | {"order_id": "5001"}))
    assert order.order_id == 5001
    assert isinstance(order.order_id, int)


def test_OrderIn_normalizes_currency(order_data):
    order = OrderIn(**(order_data | {"currency": " usd "}))
    assert order.currency == "USD"


def test_LineItem_converts_unit_price_str_to_float(order_data):
    order = OrderIn(**(order_data | {"items": [item(unit_price="12.50")]}))
    assert order.items[0].unit_price == 12.5


def test_LineItem_ignores_extra_field(order_data):
    order = OrderIn(**(order_data | {"items": [item(note="gift")]}))
    assert "note" not in order.items[0].model_dump()
