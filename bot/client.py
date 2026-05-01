from binance.client import Client
import time


class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        # Fix timestamp drift
        server_time = self.client.futures_time()
        local_time = int(time.time() * 1000)
        self.client.FUTURES_TIME_OFFSET = server_time["serverTime"] - local_time

    def new_order(self, **params):
        return self.client.futures_create_order(**params)

    def get_order(self, symbol, order_id):
        return self.client.futures_get_order(
            symbol=symbol,
            orderId=order_id
        )

    def get_price(self, symbol):
        ticker = self.client.futures_symbol_ticker(symbol=symbol)
        return float(ticker["price"])