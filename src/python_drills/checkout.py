from python_drills.cart import Cart
from python_drills.exceptions import OutOfStockError
from python_drills.product import Product


def add_to_cart_safely(cart: Cart, product: Product, quantity: int) -> bool:
    # try block: add_item can raise error when product stock is less than quantity requested
    try:
        cart.add_item(product, quantity)
    # except: handles OutOfStockError raised by try block and returns False
    except OutOfStockError as e:
        print(f"Could not add {product.name}: {e}")
        # → Could not add Coffee Mug: Only 10 of 'SKU-1' in stock, requested 20
        return False
    # else: executed when try block doesn't throw any error
    else:
        print(f"Added: {quantity} * {product.name}")
        return True
    # finally: executed whether any error is thrown or not
    finally:
        print(f"Checked: {product.sku} * {quantity}")
