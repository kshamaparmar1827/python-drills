import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from python_drills.order_models import OrderIn
from python_drills.order_parser import format_errors, parse_order

EXAMPLES = Path(__file__).parent.parent / "examples"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("order_id", 5001, id="order_id-int"),
        pytest.param("order_id", "5001", id="order_id-numeric-str"),
        pytest.param("currency", "usd", id="currency-lowercase"),
        pytest.param(
            "items",
            [{"sku": "SKU-1", "quantity": "2", "unit_price": "12.50"}],
            id="item-numeric-strs",
        ),
    ],
)
def test_parse_order_valid(order_data, field, value):
    raw_json = json.dumps(order_data | {field: value})
    assert isinstance(parse_order(raw_json), OrderIn)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("order_id", "abc", id="order_id-non-numeric-str"),
        pytest.param("customer_email", "ABC", id="email-no-at"),
        pytest.param("currency", "EUR", id="currency-unsupported"),
        pytest.param("items", [], id="items-empty"),
        pytest.param(
            "items",
            [{"sku": "SKU-1", "quantity": 0, "unit_price": 5}],
            id="quantity-zero",
        ),
    ],
)
def test_parse_order_invalid(order_data, field, value):
    raw_json = json.dumps(order_data | {field: value})
    assert parse_order(raw_json) is None


@pytest.mark.parametrize(
    "raw_json",
    [
        pytest.param("{bad", id="malformed-json"),
        pytest.param("", id="empty-string"),
        pytest.param("{}", id="empty-object"),
    ],
)
def test_parse_order_bad_json(raw_json):
    assert parse_order(raw_json) is None


def test_parse_order_prints_errors(order_data, capsys):
    raw_json = json.dumps(order_data | {"currency": "EUR"})
    parse_order(raw_json)
    output = capsys.readouterr().out
    assert "Order rejected (1 problems):" in output
    assert "currency" in output


def test_format_errors_invalid_value(order_data):
    with pytest.raises(ValidationError) as exc_info:
        OrderIn(**(order_data | {"currency": "EUR"}))
    assert format_errors(exc_info.value) == [
        "currency: Input should be 'CAD', 'USD' or 'INR' (you sent 'EUR')"
    ]


def test_format_errors_missing_field(order_data):
    del order_data["currency"]
    with pytest.raises(ValidationError) as exc_info:
        OrderIn(**order_data)
    assert format_errors(exc_info.value) == ["currency: Field required"]


def test_format_errors_nested_location(order_data):
    items = [{"sku": "SKU-1", "quantity": 0, "unit_price": 5}]
    with pytest.raises(ValidationError) as exc_info:
        OrderIn(**(order_data | {"items": items}))
    assert format_errors(exc_info.value) == [
        "items.0.quantity: Input should be greater than 0 (you sent 0)"
    ]


def test_format_errors_broken_json():
    with pytest.raises(ValidationError) as exc_info:
        OrderIn.model_validate_json("{bad")
    [line] = format_errors(exc_info.value)
    assert line.startswith("json: Invalid JSON")


def test_parse_order_reports_all_problems(capsys):
    raw_json = (EXAMPLES / "order_bad.json").read_text()
    assert parse_order(raw_json) is None
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Order rejected (3 problems):"
    assert lines[1].startswith("order_id: ")
    assert lines[2].startswith("customer_email: ")
    assert lines[3].startswith("items.0.quantity: ")
