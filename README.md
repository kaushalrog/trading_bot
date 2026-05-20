# Binance Futures Testnet Trading Bot

A Python CLI trading bot for placing **MARKET**, **LIMIT**, and **STOP_MARKET** orders on the Binance Futures Testnet using test funds.

---

## Features

### Core
- Binance Futures Testnet integration
- **MARKET**, **LIMIT**, and **STOP_MARKET** order support
- BUY and SELL sides
- CLI-based execution via `argparse`
- Comprehensive input validation
- File and console logging
- Graceful error handling
- Clean, modular project structure

### Bonus
- 🎯 **STOP_MARKET order type** — A third order type with trigger/stop price
- 🎨 **Enhanced CLI UX** — Powered by `rich`:
  - Colored, styled terminal output
  - Interactive guided mode (`--interactive`)
  - Numbered menus for side and order type selection
  - Loading spinners during API calls
  - Confirmation prompt before placing orders
  - Color-coded BUY (green) / SELL (red) indicators

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package init
│   ├── client.py            # Binance API client wrapper
│   ├── logging_config.py    # File + console logging setup
│   ├── orders.py            # Order placement & response formatting
│   └── validators.py        # Input validation logic
│
├── logs/
│   └── trading_bot.log      # Generated at runtime
│
├── cli.py                   # Main CLI entry point (argparse + rich)
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

### 2. Create a Virtual Environment (recommended)

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

### Direct Mode (flags)

#### MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 115000
```

#### STOP_MARKET Order (Bonus)

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 100000
```

### Interactive Mode (Bonus)

```bash
python cli.py --interactive
```

This launches a guided experience with prompts, menus, and confirmation:

```
╔══════════════════════════════════════════════╗
║  ⚡ Binance Futures Testnet Trading Bot      ║
╚══════════════════════════════════════════════╝

Interactive Order Builder
Answer the prompts below to build your order.

Trading Symbol [BTCUSDT]:
  1. BUY   — Go long
  2. SELL  — Go short
Side [BUY]:

  1. MARKET      — Execute at current market price
  2. LIMIT       — Execute at a specific price
  3. STOP_MARKET — Trigger market order at stop price
Order Type [MARKET]:

Quantity [0.001]:

Place this order? [Y/n]:
```

### View Help

```bash
python cli.py --help
```

---

## Example Output

```
    📋 Order Summary
 ━━━━━━━━━━━━━━━━━━━━━━━
  Symbol          BTCUSDT
  Side            BUY
  Type            MARKET
  Quantity        0.001

✓ Connected to Binance Futures Testnet

    📊 Order Response
╭────────────────────────────╮
│  Order ID      12345678   │
│  Symbol        BTCUSDT    │
│  Side          BUY        │
│  Type          MARKET     │
│  Status        FILLED     │
│  Orig Qty      0.001      │
│  Executed Qty  0.001      │
│  Price         0          │
│  Avg Price     114532.40  │
╰────────────────────────────╯

  ✅ Order filled successfully!
```

---

## Logging

All activity is logged to:

```
logs/trading_bot.log
```

Log entries include timestamps, levels, API requests/responses, and errors:

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

| Tool           | Purpose                          |
| -------------- | -------------------------------- |
| Python 3       | Core language                    |
| python-binance | Binance API client library       |
| python-dotenv  | Environment variable management  |
| argparse       | CLI argument parsing             |
| logging        | Application logging              |
| rich           | Enhanced CLI UX, colors, prompts |

---

## License

This project is for assessment purposes only.
