"""
Input validation for trading bot CLI arguments.

Validates symbols, sides, order types, quantities, and prices
before any API call is made.
"""

import re
from typing import Optional


# Supported trading symbols (extend as needed)
SUPPORTED_SYMBOLS = {
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT",
    "SOLUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT",
}

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """
    Validate and normalize the trading symbol.

    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT').

    Returns:
        Uppercased, validated symbol string.

    Raises:
        ValueError: If symbol is invalid or unsupported.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol is required and must be a non-empty string.")

    symbol = symbol.strip().upper()

    # Basic format check: letters only, ending in USDT/BUSD/USDC
    if not re.match(r"^[A-Z]{2,10}(USDT|BUSD|USDC)$", symbol):
        raise ValueError(
            f"Invalid symbol format: '{symbol}'. "
            "Symbol must be a valid trading pair (e.g., BTCUSDT)."
        )

    return symbol


def validate_side(side: str) -> str:
    """
    Validate the order side (BUY or SELL).

    Args:
        side: Order side string.

    Returns:
        Uppercased, validated side string.

    Raises:
        ValueError: If side is not BUY or SELL.
    """
    if not side or not isinstance(side, str):
        raise ValueError("Side is required and must be a non-empty string.")

    side = side.strip().upper()

    if side not in VALID_SIDES:
        raise ValueError(
            f"Invalid side: '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}."
        )

    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate the order type (MARKET or LIMIT).

    Args:
        order_type: Order type string.

    Returns:
        Uppercased, validated order type string.

    Raises:
        ValueError: If order type is not MARKET or LIMIT.
    """
    if not order_type or not isinstance(order_type, str):
        raise ValueError("Order type is required and must be a non-empty string.")

    order_type = order_type.strip().upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type: '{order_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )

    return order_type


def validate_quantity(quantity: float) -> float:
    """
    Validate the order quantity.

    Args:
        quantity: The amount to trade.

    Returns:
        Validated quantity as a float.

    Raises:
        ValueError: If quantity is not a positive number.
    """
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Quantity must be a valid number, got: '{quantity}'.")

    if quantity <= 0:
        raise ValueError(f"Quantity must be positive, got: {quantity}.")

    return quantity


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """
    Validate the order price. Required for LIMIT orders.

    Args:
        price: The limit price (can be None for MARKET orders).
        order_type: The validated order type.

    Returns:
        Validated price as a float, or None for MARKET orders.

    Raises:
        ValueError: If price is missing for LIMIT or invalid.
    """
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")

        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError(f"Price must be a valid number, got: '{price}'.")

        if price <= 0:
            raise ValueError(f"Price must be positive, got: {price}.")

        return price

    # MARKET orders don't use price
    return None


def validate_all(symbol: str, side: str, order_type: str,
                 quantity: float, price: Optional[float] = None) -> dict:
    """
    Run all validations and return a cleaned parameter dict.

    Args:
        symbol: Trading pair symbol.
        side: BUY or SELL.
        order_type: MARKET or LIMIT.
        quantity: Amount to trade.
        price: Limit price (required for LIMIT orders).

    Returns:
        Dictionary with validated and normalized parameters.

    Raises:
        ValueError: If any validation fails.
    """
    validated = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
        "price": validate_price(price, validate_order_type(order_type)),
    }
    return validated
