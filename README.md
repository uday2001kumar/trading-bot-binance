# Binance Futures Testnet Trading Bot

A lightweight CLI tool for placing **MARKET** and **LIMIT** orders on [Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com). Built with Python 3, using direct REST API calls — no Binance SDK dependency.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance Futures REST API client
│   ├── orders.py         # Order placement logic
│   ├── validators.py     # Input validation
│   └── logging_config.py # Structured logging setup
├── logs/
│   └── bot.log           # Auto-created on first run
├── cli.py                # CLI entry point (argparse)
├── .env.example          # Credentials template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Register for Binance Futures Testnet

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Navigate to **API Key** → generate a new key pair
4. Copy your `API Key` and `Secret Key`

### 2. Clone & install

```bash
git clone https://github.com/uday2001kumar/trading-bot-binance
cd trading-bot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure credentials

```bash
cp .env.example .env
# Open .env and paste your Testnet API key and secret
```

Your `.env` should look like:
```
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_api_secret_here
```

---

## Usage

### Place a MARKET order

```bash
# BUY 0.001 BTC at market price
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# SELL 0.01 ETH at market price
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

### Place a LIMIT order

```bash
# SELL 0.001 BTC when price reaches 97,000
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 97000

# BUY 0.01 ETH at 2,500
python cli.py --symbol ETHUSDT --side BUY --type LIMIT --quantity 0.01 --price 2500
```

### Help

```bash
python cli.py --help
```

---

## Sample Output

```
────────────────────────────────────────────────────────────
  ORDER REQUEST SUMMARY
────────────────────────────────────────────────────────────
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.001
────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────
  ORDER RESPONSE
────────────────────────────────────────────────────────────
  Order ID     : 3280563838
  Status       : FILLED
  Executed Qty : 0.001
  Avg Price    : 96123.40
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
────────────────────────────────────────────────────────────

  ✅  Order placed successfully!
```

---

## Logging

All API requests, responses, and errors are written to `logs/bot.log`:

```
2025-05-01 14:02:11 | INFO     | trading_bot | Placing BUY MARKET order | symbol=BTCUSDT qty=0.001
2025-05-01 14:02:12 | INFO     | trading_bot | Order placed successfully | orderId=3280563838 status=FILLED executedQty=0.001 avgPrice=96123.40
```

Full request/response payloads are logged at `DEBUG` level (file only, not shown on terminal).

---

## Error Handling

| Situation | Behaviour |
|---|---|
| Invalid side/type | Argparse rejects it before execution |
| Negative/zero quantity | Validation error printed, exits with code 1 |
| LIMIT order missing price | Validation error printed, exits with code 1 |
| Network failure | `ConnectionError` caught, message printed + logged |
| Binance API error | HTTP error body surfaced (e.g. insufficient balance) |
| Missing credentials | Clear message to check `.env`, exits with code 1 |

---

## Assumptions

- Testnet base URL is `https://testnet.binancefuture.com` (USDT-M Futures)
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled)
- Credentials are loaded from `.env` in the working directory
- Quantity and price precision must match the symbol's exchange rules (e.g. BTCUSDT min qty = 0.001)
