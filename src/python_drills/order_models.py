from pydantic import BaseModel


class LineItem(BaseModel):
    sku: str
    quantity: int
    unit_price: float


class OrderIn(BaseModel):
    order_id: int
    customer_email: str
    currency: str
    items: list[LineItem]

    def total(self) -> float:
        order_total = 0
        for item in self.items:
            item_total = item.quantity * item.unit_price
            order_total += item_total
        return order_total
