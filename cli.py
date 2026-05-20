#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot — CLI Entry Point.

Usage:
    MARKET order:
        python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

    LIMIT order:
        python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 115000
"""

import sys
import argparse

from bot.logging_config import setup_logging
from bot.validators import validate_all
from bot.client import get_client, test_connection
from bot.orders import place_order, format_response


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot — Place MARKET and LIMIT orders.",
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.001\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type LIMIT  --quantity 0.001 --price 115000\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity (e.g., 0.001)",
    )
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Limit price (required for LIMIT orders)",
    )

    return parser


def print_order_summary(params: dict) -> None:
    """Print a formatted order summary before execution."""
    print()
    print("=" * 40)
    print("           ORDER SUMMARY")
    print("=" * 40)
    print(f"  Symbol   : {params['symbol']}")
    print(f"  Side     : {params['side']}")
    print(f"  Type     : {params['order_type']}")
    print(f"  Quantity : {params['quantity']}")
    if params["price"] is not None:
        print(f"  Price    : {params['price']}")
    print("=" * 40)


def main() -> None:
    """Main entry point for the trading bot CLI."""
    # Initialize logging first
    logger = setup_logging()

    # Parse CLI arguments
    parser = build_parser()
    args = parser.parse_args()

    logger.info("=" * 50)
    logger.info("Trading Bot CLI started")
    logger.info("=" * 50)

    # ── Step 1: Validate inputs ──────────────────────────
    try:
        params = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        logger.info("Input validation passed.")
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n❌ Validation Error: {e}")
        sys.exit(1)

    # Print order summary
    print_order_summary(params)

    # ── Step 2: Initialize Binance client ────────────────
    try:
        client = get_client()
        test_connection(client)
    except EnvironmentError as e:
        logger.error(f"Environment error: {e}")
        print(f"\n❌ Configuration Error: {e}")
        sys.exit(1)
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        print(f"\n❌ Connection Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Client initialization failed: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    # ── Step 3: Place the order ──────────────────────────
    try:
        response = place_order(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        )

        # Display formatted response
        formatted = format_response(response)
        print(formatted)

        logger.info("Order workflow completed successfully.")

    except Exception as e:
        logger.error(f"Order failed: {e}")
        print(f"\n❌ Order Failed: {e}")
        sys.exit(1)

    logger.info("Trading Bot CLI finished.")


if __name__ == "__main__":
    main()
