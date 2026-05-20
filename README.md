# Binance Futures Testnet Trading Bot

A Python CLI trading bot for placing **MARKET** and **LIMIT** orders on the Binance Futures Testnet using test funds.

---

## Features

- Binance Futures Testnet integration
- MARKET and LIMIT order support
- BUY and SELL sides
- CLI-based execution via `argparse`
- Comprehensive input validation
- File and console logging
- Graceful error handling
- Clean, modular project structure

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client wrapper
│   ├── logging_config.py  # Logging setup (file + console)
│   ├── orders.py          # Order placement and response formatting
│   └── validators.py      # Input validation logic
│
├── logs/
│   └── trading_bot.log    # Generated at runtime
│
├── cli.py                 # CLI entry point
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd trading_bot
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your Binance Futures Testnet API credentials:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_secret_here
```

Get your testnet keys from: [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

---

## Usage

### Place a MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 115000
```

### View Help

```bash
python cli.py --help
```

---

## Example Output

```
========================================
           ORDER SUMMARY
========================================
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.001
========================================

========================================
           ORDER RESPONSE
========================================
  Order ID      : 12345678
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Status        : FILLED
  Orig Qty      : 0.001
  Executed Qty  : 0.001
  Price         : 0
  Avg Price     : 114532.40
========================================
  ✅ Order placed and filled successfully.
========================================
```

---

## Logging

All activity is logged to:

```
logs/trading_bot.log
```

Log entries include:

- API requests and responses
- Validation results
- Errors and exceptions
- Timestamps for every action

Example log output:

```
2026-05-20 10:00:11 INFO     Sending MARKET BUY order for 0.001 BTCUSDT
2026-05-20 10:00:13 INFO     Response received: FILLED (Order ID: 12345678)
```

---

## Assumptions

- This application uses the **Binance Futures Testnet** only
- All trades use **test/fake funds** — no real money is involved
- API credentials are stored securely using **environment variables** (`.env`)
- The `.env` file is excluded from version control via `.gitignore`

---

## Tech Stack

| Tool           | Purpose                    |
| -------------- | -------------------------- |
| Python 3       | Core language              |
| python-binance | Binance API client library |
| python-dotenv  | Environment variable mgmt  |
| argparse       | CLI argument parsing       |
| logging        | Application logging        |
| rich           | Enhanced terminal output   |

---

## License

This project is for assessment purposes only.
# trading_bot
