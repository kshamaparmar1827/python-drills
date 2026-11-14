import csv
from collections.abc import Iterator


def read_orders(path: str) -> Iterator[dict[str, str]]:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        yield from reader


def large_orders(
    rows: Iterator[dict[str, str]], min_total: float
) -> Iterator[dict[str, str]]:
    for row in rows:
        if int(row["quantity"]) * float(row["unit_price"]) > min_total:
            yield row
