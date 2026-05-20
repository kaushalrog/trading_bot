"""
Order execution module for the trading bot.

Handles placing MARKET and LIMIT orders on Binance Futures Testnet
and formatting the response output.
"""

import logging
from typing import Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException


logger = logging.getLogger("trading_bot")


def place_order(client: Client, symbol: str, side: str,
                order_type: str, quantity: float,
                price: Optional[float] = None) -> dict:
    """
    Place a futures order on Binance Testnet.

    Args:
        client: Authenticated Binance Client.
        symbol: Trading pair (e.g., 'BTCUSDT').
        side: Order side ('BUY' or 'SELL').
        order_type: Order type ('MARKET' or 'LIMIT').
        quantity: Amount to trade.
        price: Limit price (required for LIMIT, ignored for MARKET).

    Returns:
        API response dictionary from Binance.

    Raises:
        BinanceAPIException: If the API returns an error.
        BinanceRequestException: If a network error occurs.
        Exception: For unexpected errors.
    """
    logger.info(f"Sending {order_type} {side} order for {quantity} {symbol}")

    if price is not None:
        logger.info(f"Limit price: {price}")

    try:
        # Build the order parameters
        order_params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        # LIMIT orders require price and timeInForce
        if order_type == "LIMIT":
            order_params["price"] = str(price)
            order_params["timeInForce"] = "GTC"  # Good Till Cancelled

        logger.debug(f"Order parameters: {order_params}")

        # Place the futures order
        response = client.futures_create_order(**order_params)

        logger.info(
            f"Response received: {response.get('status', 'UNKNOWN')} "
            f"(Order ID: {response.get('orderId')})"
        )
        logger.debug(f"Full API response: {response}")

        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e.status_code} - {e.message}")
        raise
    except BinanceRequestException as e:
        logger.error(f"Binance request error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error placing order: {e}")
        raise


def format_response(response: dict) -> str:
    """
    Format the API response into a human-readable string.

    Args:
        response: Raw API response dictionary from Binance.

    Returns:
        Formatted string for terminal display.
    """
    order_id = response.get("orderId", "N/A")
    status = response.get("status", "N/A")
    symbol = response.get("symbol", "N/A")
    side = response.get("side", "N/A")
    order_type = response.get("type", "N/A")
    orig_qty = response.get("origQty", "N/A")
    executed_qty = response.get("executedQty", "N/A")
    avg_price = response.get("avgPrice", "N/A")
    price = response.get("price", "N/A")

    lines = [
        "",
        "=" * 40,
        "           ORDER RESPONSE",
        "=" * 40,
        f"  Order ID      : {order_id}",
        f"  Symbol        : {symbol}",
        f"  Side          : {side}",
        f"  Type          : {order_type}",
        f"  Status        : {status}",
        f"  Orig Qty      : {orig_qty}",
        f"  Executed Qty  : {executed_qty}",
        f"  Price         : {price}",
        f"  Avg Price     : {avg_price}",
        "=" * 40,
    ]

    # Add success/pending message
    if status == "FILLED":
        lines.append("  ✅ Order placed and filled successfully.")
    elif status == "NEW":
        lines.append("  📋 Order placed successfully (pending fill).")
    elif status == "PARTIALLY_FILLED":
        lines.append("  ⏳ Order partially filled.")
    else:
        lines.append(f"  ℹ️  Order status: {status}")

    lines.append("=" * 40)
    lines.append("")

    return "\n".join(lines)
