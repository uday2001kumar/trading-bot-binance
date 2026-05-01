#!/usr/bin/env python3
# cli.py  —  Binance Futures Testnet Trading Bot CLI

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import OrderService
from bot.validators import ValidationError, validate_order

load_dotenv()
logger = setup_logger()

SEPARATOR = "─" * 60


def print_summary(validated: dict) -> None:
    print(SEPARATOR)
    print("  ORDER REQUEST SUMMARY")
    print(SEPARATOR)
    print(f"  Symbol   : {validated['symbol']}")
    print(f"  Side     : {validated['side']}")
    print(f"  Type     : {validated['type']}")
    print(f"  Quantity : {validated['quantity']}")
    if validated.get("price"):
        print(f"  Price    : {validated['price']}")
    print(SEPARATOR)


def print_response(response: dict) -> None:
    print()
    print(SEPARATOR)
    print("  ORDER RESPONSE")
    print(SEPARATOR)
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price    : {response.get('avgPrice', 'N/A')}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Side         : {response.get('side', 'N/A')}")
    print(f"  Type         : {response.get('type', 'N/A')}")
    print(SEPARATOR)
    print()
    print("  ✅  Order placed successfully!")
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500
        """,
    )
    parser.add_argument(
        "--symbol", required=True,
        help="Trading pair symbol, e.g. BTCUSDT"
    )
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type", required=True, dest="order_type", choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT"
    )
    parser.add_argument(
        "--quantity", required=True,
        help="Order quantity (e.g. 0.001 for BTC)"
    )
    parser.add_argument(
        "--price",
        help="Limit price — required for LIMIT orders"
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # --- Load credentials ---
    
    api_key = os.getenv("API_KEY", "").strip()
    api_secret = os.getenv("API_SECRET", "").strip()
    client = BinanceClient(api_key, api_secret)
    current_price = client.get_price(args.symbol)
    print(f"\n  📊 Current Market Price: {current_price}")

    if not api_key or not api_secret:
        print(
            "\n  ❌  Error: API_KEY and API_SECRET must be set in the .env file.\n",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- Validate inputs ---
    try:
        validated = validate_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            current_price=current_price,
        )
    except ValidationError as exc:
        print(f"\n  ❌  {exc}\n", file=sys.stderr)
        logger.error("Validation error: %s", exc)
        sys.exit(1)

    print_summary(validated)

    # --- Place order ---
    try:
        client = BinanceClient(api_key, api_secret)
        service = OrderService(client)
        response = service.place_order(validated)
    except (ConnectionError, TimeoutError) as exc:
        print(f"\n  ❌  Network error: {exc}\n", file=sys.stderr)
        logger.error("Network error: %s", exc)
        sys.exit(1)
    except RuntimeError as exc:
        print(f"\n  ❌  API error: {exc}\n", file=sys.stderr)
        logger.error("API error: %s", exc)
        sys.exit(1)
    except Exception as exc:
        print(f"\n  ❌  Unexpected error: {exc}\n", file=sys.stderr)
        logger.exception("Unexpected error")
        sys.exit(1)

    print_response(response)


if __name__ == "__main__":
    main()
