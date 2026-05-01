from typing import Optional


class ValidationError(Exception):
    pass


VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT"}


def validate_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    current_price: Optional[float] = None,   # ✅ FIX
) -> dict:

    errors = []

    symbol = symbol.strip().upper()
    side = side.strip().upper()
    order_type = order_type.strip().upper()

    if side not in VALID_SIDES:
        errors.append("Invalid side")

    if order_type not in VALID_TYPES:
        errors.append("Invalid order type")

    try:
        qty = float(quantity)
        if qty <= 0:
            errors.append("Quantity must be positive")
    except:
        errors.append("Invalid quantity")

    clean_price = None

    if order_type == "LIMIT":
        if not price:
            errors.append("Price required for LIMIT")
        else:
            try:
                clean_price = float(price)
                if clean_price <= 0:
                    errors.append("Price must be positive")
            except:
                errors.append("Invalid price")

        # ✅ NEW VALIDATION
        if clean_price and current_price:
            if side == "BUY" and clean_price > current_price:
                errors.append(
                    f"BUY price must be <= current price ({current_price})"
                )
            if side == "SELL" and clean_price < current_price:
                errors.append(
                    f"SELL price must be >= current price ({current_price})"
                )

    if errors:
        raise ValidationError("\n  ".join(errors))

    result = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": qty,
    }

    if clean_price:
        result["price"] = clean_price

    return result