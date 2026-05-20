"""
Binance Futures Testnet client wrapper.

Handles authentication, connection, and raw API communication
with the Binance Futures Testnet.
"""

import os
import logging

from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException


logger = logging.getLogger("trading_bot")

# Binance Futures Testnet endpoints
FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"
FUTURES_TESTNET_DATA_URL = "https://testnet.binancefuture.com/futures/data"


def get_client() -> Client:
    """
    Create and return an authenticated Binance Futures Testnet client.

    Loads API credentials from environment variables (.env file)
    and configures the client for the futures testnet endpoint.

    Returns:
        Authenticated Binance Client instance.

    Raises:
        EnvironmentError: If API keys are missing from environment.
        BinanceAPIException: If authentication fails.
    """
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise EnvironmentError(
            "Missing API credentials. "
            "Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file."
        )

    logger.info("Initializing Binance Futures Testnet client...")

    # Note: testnet=True only configures the SPOT testnet in python-binance.
    # For futures testnet, we create a standard client and manually override
    # the futures URLs to point to the testnet endpoint.
    client = Client(api_key, api_secret)

    # Override futures endpoints to use the testnet
    client.FUTURES_URL = FUTURES_TESTNET_URL
    client.FUTURES_DATA_URL = FUTURES_TESTNET_DATA_URL

    logger.info("Binance Futures Testnet client initialized successfully.")
    return client


def test_connection(client: Client) -> bool:
    """
    Test the API connection by pinging the server.

    Args:
        client: Authenticated Binance Client.

    Returns:
        True if the connection is successful.

    Raises:
        ConnectionError: If the ping fails.
    """
    try:
        client.futures_ping()
        logger.info("Connection to Binance Futures Testnet verified.")
        return True
    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Connection test failed: {e}")
        raise ConnectionError(f"Cannot reach Binance Futures Testnet: {e}")
