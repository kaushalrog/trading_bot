#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot — CLI Entry Point.

Supports two modes:
  1. Direct mode (via flags):
       python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  2. Interactive mode (guided prompts):
       python cli.py --interactive
"""

import sys
import argparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, Confirm
from rich.text import Text
from rich import box

from bot.logging_config import setup_logging
from bot.validators import validate_all, VALID_SIDES, VALID_ORDER_TYPES
from bot.client import get_client, test_connection
from bot.orders import place_order, format_response

# Rich console for all output
console = Console()


# ── CLI Argument Parser ──────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot — Place MARKET, LIMIT, and STOP_MARKET orders.",
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY  --type MARKET      --quantity 0.001\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type LIMIT       --quantity 0.001 --price 115000\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 100000\n"
            "  python cli.py --interactive\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Launch interactive guided mode with prompts",
    )
    parser.add_argument(
        "--symbol",
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)",
    )
    parser.add_argument(
        "--side",
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        dest="order_type",
        help="Order type: MARKET, LIMIT, or STOP_MARKET",
    )
    parser.add_argument(
        "--quantity",
        type=float,
        help="Order quantity (e.g., 0.001)",
    )
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Limit price (required for LIMIT orders)",
    )
    parser.add_argument(
        "--stop-price",
        type=float,
        default=None,
        dest="stop_price",
        help="Stop/trigger price (required for STOP_MARKET orders)",
    )

    return parser


# ── Rich-Enhanced Output ─────────────────────────────────────

def print_banner() -> None:
    """Print a styled welcome banner."""
    banner = Text()
    banner.append("╔══════════════════════════════════════════════╗\n", style="bold cyan")
    banner.append("║  ", style="bold cyan")
    banner.append("⚡ Binance Futures Testnet Trading Bot", style="bold white")
    banner.append("  ║\n", style="bold cyan")
    banner.append("╚══════════════════════════════════════════════╝", style="bold cyan")
    console.print(banner)
    console.print()


def print_order_summary(params: dict) -> None:
    """Print a rich-formatted order summary panel."""
    table = Table(
        show_header=False,
        box=box.SIMPLE_HEAVY,
        padding=(0, 2),
        title="📋 Order Summary",
        title_style="bold yellow",
    )
    table.add_column("Field", style="bold cyan", width=14)
    table.add_column("Value", style="bold white")

    side_color = "green" if params["side"] == "BUY" else "red"

    table.add_row("Symbol", params["symbol"])
    table.add_row("Side", f"[bold {side_color}]{params['side']}[/]")
    table.add_row("Type", params["order_type"])
    table.add_row("Quantity", str(params["quantity"]))

    if params.get("price") is not None:
        table.add_row("Price", str(params["price"]))
    if params.get("stop_price") is not None:
        table.add_row("Stop Price", str(params["stop_price"]))

    console.print()
    console.print(table)
    console.print()


def print_rich_response(response: dict) -> None:
    """Print the API response in a rich-styled panel."""
    status = response.get("status", "N/A")
    side = response.get("side", "N/A")

    # Pick status color
    if status == "FILLED":
        status_style = "bold green"
        status_icon = "✅"
        status_msg = "Order filled successfully!"
    elif status == "NEW":
        status_style = "bold yellow"
        status_icon = "📋"
        status_msg = "Order placed (pending fill)"
    elif status == "PARTIALLY_FILLED":
        status_style = "bold yellow"
        status_icon = "⏳"
        status_msg = "Order partially filled"
    else:
        status_style = "bold dim"
        status_icon = "ℹ️ "
        status_msg = f"Status: {status}"

    side_color = "green" if side == "BUY" else "red"

    table = Table(
        show_header=False,
        box=box.ROUNDED,
        padding=(0, 2),
        title="📊 Order Response",
        title_style="bold cyan",
    )
    table.add_column("Field", style="cyan", width=14)
    table.add_column("Value", style="white")

    table.add_row("Order ID", str(response.get("orderId", "N/A")))
    table.add_row("Symbol", response.get("symbol", "N/A"))
    table.add_row("Side", f"[bold {side_color}]{side}[/]")
    table.add_row("Type", response.get("type", "N/A"))
    table.add_row("Status", f"[{status_style}]{status}[/]")
    table.add_row("Orig Qty", response.get("origQty", "N/A"))
    table.add_row("Executed Qty", response.get("executedQty", "N/A"))
    table.add_row("Price", response.get("price", "N/A"))
    table.add_row("Avg Price", response.get("avgPrice", "N/A"))

    stop_price = response.get("stopPrice")
    if stop_price and stop_price != "0":
        table.add_row("Stop Price", stop_price)

    console.print()
    console.print(table)
    console.print(f"\n  {status_icon} [{status_style}]{status_msg}[/]\n")


# ── Interactive Mode ─────────────────────────────────────────

def run_interactive() -> dict:
    """
    Launch an interactive guided mode that prompts the user
    for each order parameter with validation.

    Returns:
        Validated parameter dictionary.
    """
    print_banner()
    console.print("[bold cyan]Interactive Order Builder[/bold cyan]")
    console.print("[dim]Answer the prompts below to build your order.[/dim]\n")

    # ── Symbol ──
    symbol = Prompt.ask(
        "[bold yellow]Trading Symbol[/bold yellow]",
        default="BTCUSDT",
    )

    # ── Side ──
    console.print("\n[dim]Choose order side:[/dim]")
    console.print("  [green]1.[/green] BUY   — Go long")
    console.print("  [red]2.[/red] SELL  — Go short")
    side_choice = Prompt.ask(
        "[bold yellow]Side[/bold yellow]",
        choices=["1", "2", "BUY", "SELL", "buy", "sell"],
        default="BUY",
    )
    side = "BUY" if side_choice in ("1", "BUY", "buy") else "SELL"

    # ── Order Type ──
    console.print("\n[dim]Choose order type:[/dim]")
    console.print("  [white]1.[/white] MARKET      — Execute at current market price")
    console.print("  [white]2.[/white] LIMIT       — Execute at a specific price")
    console.print("  [white]3.[/white] STOP_MARKET — Trigger market order at stop price")
    type_choice = Prompt.ask(
        "[bold yellow]Order Type[/bold yellow]",
        choices=["1", "2", "3", "MARKET", "LIMIT", "STOP_MARKET",
                 "market", "limit", "stop_market"],
        default="MARKET",
    )
    type_map = {
        "1": "MARKET", "2": "LIMIT", "3": "STOP_MARKET",
        "MARKET": "MARKET", "LIMIT": "LIMIT", "STOP_MARKET": "STOP_MARKET",
        "market": "MARKET", "limit": "LIMIT", "stop_market": "STOP_MARKET",
    }
    order_type = type_map[type_choice]

    # ── Quantity ──
    console.print()
    quantity = FloatPrompt.ask(
        "[bold yellow]Quantity[/bold yellow]",
        default=0.001,
    )

    # ── Price (LIMIT only) ──
    price = None
    if order_type == "LIMIT":
        console.print()
        price = FloatPrompt.ask(
            "[bold yellow]Limit Price[/bold yellow]",
        )

    # ── Stop Price (STOP_MARKET only) ──
    stop_price = None
    if order_type == "STOP_MARKET":
        console.print()
        stop_price = FloatPrompt.ask(
            "[bold yellow]Stop (Trigger) Price[/bold yellow]",
        )

    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
        "stop_price": stop_price,
    }


# ── Main Execution ───────────────────────────────────────────

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

    # ── Step 1: Get order parameters ─────────────────────
    if args.interactive:
        # Interactive guided mode
        logger.info("Running in interactive mode.")
        raw_params = run_interactive()
    else:
        # Direct flag mode — require mandatory fields
        if not all([args.symbol, args.side, args.order_type, args.quantity]):
            print_banner()
            console.print(
                "[bold red]Error:[/bold red] Missing required arguments. "
                "Use [bold]--interactive[/bold] for guided mode, "
                "or provide [bold]--symbol --side --type --quantity[/bold].\n"
            )
            parser.print_help()
            sys.exit(1)

        raw_params = {
            "symbol": args.symbol,
            "side": args.side,
            "order_type": args.order_type,
            "quantity": args.quantity,
            "price": args.price,
            "stop_price": args.stop_price,
        }

    # ── Step 2: Validate inputs ──────────────────────────
    try:
        params = validate_all(
            symbol=raw_params["symbol"],
            side=raw_params["side"],
            order_type=raw_params["order_type"],
            quantity=raw_params["quantity"],
            price=raw_params.get("price"),
            stop_price=raw_params.get("stop_price"),
        )
        logger.info("Input validation passed.")
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        console.print(f"\n[bold red]❌ Validation Error:[/bold red] {e}\n")
        sys.exit(1)

    # Print order summary
    print_order_summary(params)

    # ── Step 3: Confirm (interactive mode) ───────────────
    if args.interactive:
        if not Confirm.ask("[bold yellow]Place this order?[/bold yellow]", default=True):
            console.print("\n[dim]Order cancelled.[/dim]\n")
            logger.info("Order cancelled by user.")
            sys.exit(0)

    # ── Step 4: Initialize Binance client ────────────────
    try:
        with console.status("[bold cyan]Connecting to Binance Futures Testnet...[/bold cyan]"):
            client = get_client()
            test_connection(client)
        console.print("[green]✓[/green] Connected to Binance Futures Testnet\n")
    except EnvironmentError as e:
        logger.error(f"Environment error: {e}")
        console.print(f"\n[bold red]❌ Configuration Error:[/bold red] {e}\n")
        sys.exit(1)
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        console.print(f"\n[bold red]❌ Connection Error:[/bold red] {e}\n")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Client initialization failed: {e}")
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")
        sys.exit(1)

    # ── Step 5: Place the order ──────────────────────────
    try:
        with console.status("[bold cyan]Placing order...[/bold cyan]"):
            response = place_order(
                client=client,
                symbol=params["symbol"],
                side=params["side"],
                order_type=params["order_type"],
                quantity=params["quantity"],
                price=params.get("price"),
                stop_price=params.get("stop_price"),
            )

        # Display rich-formatted response
        print_rich_response(response)

        logger.info("Order workflow completed successfully.")

    except Exception as e:
        logger.error(f"Order failed: {e}")
        console.print(f"\n[bold red]❌ Order Failed:[/bold red] {e}\n")
        sys.exit(1)

    logger.info("Trading Bot CLI finished.")


if __name__ == "__main__":
    main()
