import tracemalloc

from python_drills.orders import large_orders, read_orders
from python_drills.timer import Timer

PATH = "data/orders.csv"


# ---------- 1. Speed: how long does reading take? ----------

with Timer("import"):
    count = sum(1 for _ in read_orders(PATH))
print(count)

with Timer("import big orders"):
    count = sum(1 for _ in large_orders(read_orders(PATH), 400))
print(count)


# ---------- 2. Memory: list vs generator ----------


def measure_peak_kb(func):
    """Run func and return (its result, the peak memory it used in KB)."""
    tracemalloc.start()
    result = func()
    _, peak = tracemalloc.get_traced_memory()  # (current, peak) in bytes
    tracemalloc.stop()
    return result, peak / 1024


def count_with_list() -> int:
    rows = list(read_orders(PATH))  # loads ALL 10,000 rows into memory at once
    return len(rows)


def count_with_generator() -> int:
    return sum(1 for _ in read_orders(PATH))  # only one row in memory at a time


list_count, list_peak = measure_peak_kb(count_with_list)
gen_count, gen_peak = measure_peak_kb(count_with_generator)

print(f"list:      {list_count} rows, peak {list_peak:,.0f} KB")
print(f"generator: {gen_count} rows, peak {gen_peak:,.0f} KB")
print(f"the list version used {list_peak / gen_peak:.0f}x more memory")
