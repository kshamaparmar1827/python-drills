import csv
import random
from pathlib import Path

random.seed(42)
Path("data").mkdir(exist_ok=True)
sku_list = [f"SKU-{x}" for x in range(200)]

with open("data/orders.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "sku", "quantity", "unit_price", "currency"])
    for n in range(10_000):
        sku = random.choice(sku_list)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(5, 100), 2)
        currency = random.choice(["CAD", "USD", "INR"])
        writer.writerow([n, sku, quantity, unit_price, currency])
