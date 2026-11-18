from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class LineItem(BaseModel):
    sku: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)


class OrderIn(BaseModel):
    order_id: int
    customer_email: EmailStr
    currency: Literal["CAD", "USD", "INR"]
    items: list[LineItem] = Field(min_length=1)

    def total(self) -> float:
        order_total = 0
        for item in self.items:
            item_total = item.quantity * item.unit_price
            order_total += item_total
        return order_total

    @field_validator("currency", mode="before")
    @classmethod
    def validate_currency_before(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        return value.strip().upper()
