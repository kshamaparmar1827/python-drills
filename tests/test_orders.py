from collections.abc import Iterator

import pytest

from python_drills.orders import large_orders, read_orders

HEADER = "order_id,sku,quantity,unit_price,currency\n"


@pytest.fixture
def orders_csv(tmp_path):
    path = tmp_path / "orders.csv"
    path.write_text(
        HEADER
        + "100001,SKU-1,2,12.5,CAD\n"
        + "100002,SKU-2,5,100.0,USD\n"
        + "100003,SKU-3,1,7.25,INR\n"
    )
    return str(path)


def test_read_orders_yields_every_row(orders_csv):
    rows = list(read_orders(orders_csv))
    assert len(rows) == 3


def test_rows_are_dicts_of_strings(orders_csv):
    first = next(read_orders(orders_csv))
    assert first == {
        "order_id": "100001",
        "sku": "SKU-1",
        "quantity": "2",
        "unit_price": "12.5",
        "currency": "CAD",
    }


def test_read_orders_returns_an_iterator_not_a_list(orders_csv):
    rows = read_orders(orders_csv)
    assert isinstance(rows, Iterator)


def test_read_orders_is_lazy():
    rows = read_orders("does-not-exist.csv")
    with pytest.raises(FileNotFoundError):
        next(rows)


def test_generator_is_used_up_after_one_pass(orders_csv):
    rows = read_orders(orders_csv)
    assert len(list(rows)) == 3
    assert list(rows) == []


def test_header_only_file_yields_nothing(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text(HEADER)
    assert list(read_orders(str(path))) == []


def test_large_orders_keeps_only_big_totals(orders_csv):
    big = large_orders(read_orders(orders_csv), 400)
    assert [row["order_id"] for row in big] == ["100002"]


def test_large_orders_with_no_matches_yields_nothing(orders_csv):
    assert list(large_orders(read_orders(orders_csv), 10_000)) == []
